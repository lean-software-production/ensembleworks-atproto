import {createHash} from 'node:crypto';
export const CHUNK_COLLECTION='com.ensembleworks.session.chunk';
export const MANIFEST_TYPE='com.ensembleworks.session.chunkManifest';
export const MAX_RECORD_BYTES=900_000;
export const MAX_EVENT_BYTES=20*1024*1024;
const CHUNK_BYTES=350_000;
export const sha256=(b:Uint8Array)=>createHash('sha256').update(b).digest('hex');
export interface Manifest {$type:string;transportType:typeof MANIFEST_TYPE;encoding:'base64-json';digest:string;bytes:number;count:number}
export function encodeRecord(record:Record<string,unknown>){
 const bytes=Buffer.from(JSON.stringify(record));
 if(bytes.length>MAX_EVENT_BYTES)throw new Error(`Record exceeds ${MAX_EVENT_BYTES} byte reconstructed limit`);
 if(bytes.length<=MAX_RECORD_BYTES)return {record,chunks:[]};
 const digest=sha256(bytes);const chunks=[];
 for(let i=0;i<bytes.length;i+=CHUNK_BYTES){const index:number=chunks.length;chunks.push({rkey:`${digest}-${String(index).padStart(6,'0')}`,value:{$type:CHUNK_COLLECTION,digest,index,data:bytes.subarray(i,i+CHUNK_BYTES).toString('base64')}});}
 return {record:{$type:record.$type,transportType:MANIFEST_TYPE,encoding:'base64-json',digest,bytes:bytes.length,count:chunks.length},chunks};
}
export function assertManifest(m:any):asserts m is Manifest{
 if(m.transportType!==MANIFEST_TYPE||m.encoding!=='base64-json'||!/^[a-f0-9]{64}$/.test(m.digest)||!Number.isInteger(m.bytes)||m.bytes<=MAX_RECORD_BYTES||m.bytes>MAX_EVENT_BYTES||m.count!==Math.ceil(m.bytes/CHUNK_BYTES))throw new Error('Invalid chunk manifest');
}
export function decodeRecord(m:any,records:any[]):Record<string,unknown>{
 assertManifest(m);
 if(records.length!==m.count)throw new Error('Missing event chunks');
 const chunks=records.map(r=>r.value).sort((a,b)=>a.index-b.index);
 const bytes=Buffer.concat(chunks.map((c,i)=>{
  if(c.$type!==CHUNK_COLLECTION||c.digest!==m.digest||c.index!==i||typeof c.data!=='string'||c.data.length>Math.ceil(CHUNK_BYTES/3)*4||!/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(c.data))throw new Error('Invalid event chunk');
  return Buffer.from(c.data,'base64');
 }));
 if(bytes.length!==m.bytes||sha256(bytes)!==m.digest)throw new Error('Event chunk digest mismatch');
 const value=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));
 if(!value||typeof value!=='object'||Array.isArray(value)||value.transportType===MANIFEST_TYPE)throw new Error('Invalid reconstructed event');
 return value;
}
