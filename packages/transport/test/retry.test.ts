import {test} from 'node:test';import assert from 'node:assert/strict';
import {createTransport} from '../src/index.ts';
import {CHUNK_COLLECTION,decodeRecord} from '../src/chunks.ts';
test('interrupted chunk publication leaves no manifest and retry uses identical keys',async()=>{
 const original=globalThis.fetch;const stored=new Map<string,string>();let fail=true,writes=0;
 globalThis.fetch=async(input,init)=>{
  const method=new URL(String(input)).pathname.split('/').at(-1);
  if(method==='com.atproto.server.createSession')return Response.json({did:'did:plc:testauthor',handle:'pilot.test',accessJwt:'test-token'});
  if(method==='com.atproto.space.getDelegationToken')return Response.json({token:'test-delegation'});
  if(method==='com.atproto.space.authorizeSpaceSync')return Response.json({credential:'test-credential'});
  assert.equal(method,'com.atproto.space.putRecord');const body=JSON.parse(String(init?.body));writes++;
  if(fail&&writes===2)throw new Error('simulated connection loss');
  assert.equal(body.space,'at://did:plc:company/space/com.ensembleworks.company/company');
  assert.equal(body.repo,'did:plc:testauthor');
  const key=`${body.collection}/${body.rkey}`;stored.set(key,JSON.stringify(body.record));return Response.json({uri:`at://test/${key}`,cid:'test-cid'});
 };
 try{
  const t=createTransport({service:'http://localhost:12345',identifier:'test',password:'synthetic',space:'at://did:plc:company/space/com.ensembleworks.company/company'});
  const record={$type:'com.ensembleworks.session.event',payloadJson:'x'.repeat(1_000_000)};
  await assert.rejects(()=>t.putEvent('stable-event',record),/connection loss/);
  assert.equal(stored.size,1);assert.ok([...stored.keys()].every(k=>k.startsWith(CHUNK_COLLECTION)));
  const first=[...stored.entries()][0];fail=false;await t.putEvent('stable-event',record);
  assert.equal(stored.size,4);assert.equal(stored.get(first[0]),first[1]);assert.equal([...stored.keys()].at(-1),'com.ensembleworks.session.event/stable-event');
  await t.putEvent('stable-event',record);assert.equal(stored.size,4);
  const manifestKey='com.ensembleworks.session.event/stable-event';
  const priorManifest=JSON.parse(stored.get(manifestKey)!);
  const priorChunks=[...stored.entries()].filter(([key])=>key.startsWith(CHUNK_COLLECTION)).map(([,value])=>({value:JSON.parse(value)}));
  const correction={...record,payloadJson:'🦋'.repeat(300000)};
  // A failed correction must leave the prior complete event visible.
  writes=0;fail=true;await assert.rejects(()=>t.putEvent('stable-event',correction),/connection loss/);
  assert.deepEqual(JSON.parse(stored.get(manifestKey)!),priorManifest);
  assert.deepEqual(decodeRecord(priorManifest,priorChunks),record);
  fail=false;await t.putEvent('stable-event',correction);
  const nextManifest=JSON.parse(stored.get(manifestKey)!);
  assert.notEqual(nextManifest.digest,priorManifest.digest);
  const nextChunks=[...stored.entries()].filter(([key])=>key.startsWith(`${CHUNK_COLLECTION}/${nextManifest.digest}-`)).map(([,value])=>({value:JSON.parse(value)}));
  assert.deepEqual(decodeRecord(nextManifest,nextChunks),correction);
  for(const c of priorChunks){
   const key=`${CHUNK_COLLECTION}/${c.value.digest}-${String(c.value.index).padStart(6,'0')}`;
   assert.deepEqual(JSON.parse(stored.get(key)!),c.value);
  }
  assert.deepEqual(decodeRecord(priorManifest,priorChunks),record);

 }finally{globalThis.fetch=original;}
});
