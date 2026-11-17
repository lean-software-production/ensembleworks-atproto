import {readFile,writeFile} from 'node:fs/promises';
import {randomBytes} from 'node:crypto';
await import('./init.mjs');
const service=process.env.PDS_URL??'http://localhost:2583';
async function rpc(method,body,token){
 const r=await fetch(`${service}/xrpc/${method}`,{method:'POST',headers:{'content-type':'application/json',...(token?{authorization:`Bearer ${token}`}:{})},body:JSON.stringify(body)});
 const raw=await r.text();const data=raw?JSON.parse(raw):{};if(!r.ok)throw Object.assign(new Error(`${method}: ${JSON.stringify(data)}`),{code:data.error});return data;
}
let state;
try{state=JSON.parse(await readFile('.local/accounts.json','utf8'));}catch(e){if(e.code!=='ENOENT')throw e;state={service,accounts:[]};}
for(const name of ['company','alice','bob','outsider']){
 let a=state.accounts.find(a=>a.name===name);
 if(!a){a={name,handle:`pilot-${name}.test`,password:randomBytes(24).toString('base64url')};state.accounts.push(a);await save();}
 let session;
 try{session=await rpc('com.atproto.server.createSession',{identifier:a.handle,password:a.password});}
 catch(e){if(a.did)throw e;session=await rpc('com.atproto.server.createAccount',{handle:a.handle,email:`${name}@example.test`,password:a.password});}
 a.did=session.did;await save();
 if(name==='company'){
  state.space=`at://${a.did}/space/com.ensembleworks.company/company`;
  try{await rpc('com.atproto.space.createSpace',{spaceType:'com.ensembleworks.company',skey:'company',policy:{$type:'com.atproto.memberspace.policy',publicRead:false,publicWrite:false}},session.accessJwt);}catch(e){if(e.code!=='SpaceAlreadyExists')throw e;}
 }
}
const owner=state.accounts[0];const auth=await rpc('com.atproto.server.createSession',{identifier:owner.handle,password:owner.password});
await rpc('com.atproto.memberspace.putMembers',{space:state.space,members:state.accounts.filter(a=>a.name!=='outsider').map(a=>({did:a.did,read:true,write:true}))},auth.accessJwt);
await save();console.log(JSON.stringify({service,space:state.space,accounts:state.accounts.map(({name,handle,did})=>({name,handle,did})),credentialsFile:'.local/accounts.json'},null,2));
async function save(){await writeFile('.local/accounts.json',JSON.stringify(state,null,2)+'\n',{mode:0o600});}
