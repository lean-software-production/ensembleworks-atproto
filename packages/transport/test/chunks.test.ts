import {test} from 'node:test';import assert from 'node:assert/strict';
import {encodeRecord,decodeRecord,MAX_EVENT_BYTES} from '../src/chunks.ts';
test('oversized Unicode record roundtrips exactly with stable chunk keys',()=>{
 const value={$type:'com.ensembleworks.session.event',payloadJson:JSON.stringify({text:'🦋'.repeat(300000)})};
 const a=encodeRecord(value),b=encodeRecord(value);assert.deepEqual(a,b);assert.ok(a.chunks.length>1);
 assert.deepEqual(decodeRecord(a.record,a.chunks.map(c=>({value:c.value}))),value);
 assert.throws(()=>decodeRecord(a.record,a.chunks.slice(1).map(c=>({value:c.value}))),/Missing/);
 const damaged=structuredClone(a.chunks);damaged[0].value.data='AAAA';assert.throws(()=>decodeRecord(a.record,damaged.map(c=>({value:c.value}))),/digest/);
});
test('inline remains inline, above maximum rejects visibly',()=>{
 assert.equal(encodeRecord({$type:'example.event',text:'small'}).chunks.length,0);
 assert.throws(()=>encodeRecord({data:'x'.repeat(MAX_EVENT_BYTES)}),/exceeds/);
});
