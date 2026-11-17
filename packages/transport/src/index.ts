import { P256Keypair } from '@atproto/crypto';
import { createSpaceSigHeaders } from '@atproto/space';
import {encodeRecord,decodeRecord,assertManifest,CHUNK_COLLECTION,MANIFEST_TYPE} from './chunks.ts';
export {MAX_RECORD_BYTES,MAX_EVENT_BYTES} from './chunks.ts';
export interface TransportConfig {service:string; identifier:string; password:string; space:string; collection?:string}
export interface EventResult {uri:string;cid:string;value:any;authorDid:string}
export class TransportError extends Error {
  status:number; code:string;
  constructor(message:string, status:number, code:string) {super(message);this.name='TransportError';this.status=status;this.code=code}
}
export function createTransport(config:TransportConfig) {
 const service=config.service.replace(/\/$/,'');
 const collection=config.collection??'com.ensembleworks.session.event';
 if (!/^at:\/\/did:[^/]+\/space\/[^/]+\/[^/]+$/.test(config.space)) throw new Error('A company Space URI is required');
 const authority=config.space.split('/')[2];
 let session:any; let sessionUntil=0; const signingKeyPromise=P256Keypair.create(); let signingKey:Awaited<ReturnType<typeof P256Keypair.create>>;
 async function request(method:string, params:any, post=false, headers:Record<string,string>={}) {
  const url=new URL(`${service}/xrpc/${method}`);
  if(!post) for(const [k,v] of Object.entries(params)) if(v!==undefined)url.searchParams.set(k,String(v));
  const response=await fetch(url,{method:post?'POST':'GET',headers:{...(post?{'content-type':'application/json'}:{}),...headers},body:post?JSON.stringify(params):undefined,signal:AbortSignal.timeout(15000)});
  const body=await response.json().catch(()=>({}));
  if(!response.ok)throw new TransportError(`${method}: ${body.message??response.statusText}`,response.status,body.error??'RequestFailed');
  return body;
 }
 async function authenticate(){
  if(!session||Date.now()>sessionUntil){session=await request('com.atproto.server.createSession',{identifier:config.identifier,password:config.password},true);sessionUntil=Date.now()+60*60*1000;}
  return {did:session.did as string,handle:session.handle as string};
 }
 async function own(method:string,params:any,post=false){await authenticate();return request(method,params,post,{authorization:`Bearer ${session.accessJwt}`});}
 // Reauthorize each listing/write so member removal is checked on the next operation.
 async function credential(){
  signingKey=await signingKeyPromise;
  const {token}=await own('com.atproto.space.getDelegationToken',{space:config.space});
  const {credential}=await request('com.atproto.space.authorizeSpaceSync',{space:config.space,credentialKey:signingKey.did(),delegationToken:token},true);
  return credential as string;
 }
 async function read(method:string,params:any,cred:string){
  const {headers}=await createSpaceSigHeaders({authorization:`Atproto-Space-Credential ${cred}`,audience:(params.repo??authority) as `did:${string}:${string}`,keypair:signingKey});
  return request(method,params,false,headers);
 }
 return {authenticate,
  async putEvent(rkey:string,record:Record<string,unknown>):Promise<{uri:string;cid:string}>{
   let encoded;try{encoded=encodeRecord(record);}catch(e){throw new TransportError((e as Error).message,413,'RecordTooLarge');}
   await credential();
   const {did}=await authenticate();
   for(const chunk of encoded.chunks)await own('com.atproto.space.putRecord',{space:config.space,repo:did,collection:CHUNK_COLLECTION,rkey:chunk.rkey,record:chunk.value,validate:false},true);
   return own('com.atproto.space.putRecord',{space:config.space,repo:did,collection,rkey,record:encoded.record,validate:false},true);
  },
  async listEvents({cursor,limit=100}:{cursor?:string;limit?:number}={}):Promise<{records:EventResult[];cursor?:string}>{
   if(!Number.isInteger(limit)||limit<1||limit>1000)throw new Error('limit must be 1..1000');
   const cred=await credential();
   let state:{repos:string[];index:number;after?:string};
   if(cursor){try{state=JSON.parse(Buffer.from(cursor,'base64url').toString());if(!Array.isArray(state.repos)||!state.repos.every(x=>typeof x==='string'&&x.startsWith('did:'))||!Number.isInteger(state.index)||state.index<0)throw Error();}catch{throw new Error('Invalid transport cursor');}}
   else{
    const repos:string[]=[];let after:string|undefined;
    do{const page=await read('com.atproto.space.listWriters',{space:config.space,limit:1000,cursor:after},cred);for(const r of page.repos)if(r.$type==='com.atproto.space.defs#repoWrite')repos.push(r.repo);after=page.cursor;}while(after);
    state={repos:[...new Set(repos)].sort(),index:0};
   }
   const records:EventResult[]=[];
   while(state.index<state.repos.length&&records.length<limit){
    const repo=state.repos[state.index];
    const page=await read('com.atproto.space.listRecords',{space:config.space,repo,collection,limit:limit-records.length,cursor:state.after},cred);
    for(const r of page.records){
     if(r.value?.transportType===MANIFEST_TYPE){
      assertManifest(r.value);
      // Pinned PDS lists descending URI; this cursor starts immediately above this digest's numeric suffixes.
      const chunks=await read('com.atproto.space.listRecords',{space:config.space,repo,collection:CHUNK_COLLECTION,limit:r.value.count,cursor:`${config.space}/${repo}/${CHUNK_COLLECTION}/${r.value.digest}-999999`},cred);
      r.value=decodeRecord(r.value,chunks.records);
     }
    }
    records.push(...page.records.map((r:any)=>({uri:`${config.space}/${repo}/${r.collection}/${r.rkey}`,cid:r.cid,value:r.value,authorDid:repo})));
    if(page.cursor)state.after=page.cursor;else{state.index++;delete state.after;}
   }
   return {records,...(state.index<state.repos.length?{cursor:Buffer.from(JSON.stringify(state)).toString('base64url')}:{})};
  }
 };
}
