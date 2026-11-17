import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createEvent,validateEvent,assertEvent} from '../src/index.js';
const make = (payloadJson: string, sourcePath='a.jsonl', sourceLine=1, occurrence=0) => createEvent({payloadJson,sourcePath,sourceLine,occurrence,namespace:'fixture'});
test('opaque exact JSON preserves large numbers, whitespace, unknown types and null', () => {
 const raw=' {"type":"future","x":9007199254740993123,"n":null,"f":4.500} ';
 const {record}=make(raw); assert.equal(record.payloadJson,raw); assert.equal(record.nativeType,'future'); assert.ok(validateEvent(record).success);
 for (const value of ['null','42','"string"','[1,2]']) assert.equal(make(value).record.payloadJson,value);
});
test('native UUID correction stable, streams distinct, synthetic content identities deterministic', () => {
 assert.equal(make('{"uuid":"u","x":1}').rkey,make('{"uuid":"u","x":2}').rkey);
 assert.notEqual(make('{"uuid":"u"}').rkey,make('{"uuid":"u"}','sub/a.jsonl').rkey);
 assert.equal(make('{"x":1}').rkey,make('{"x":1}','a.jsonl',9).rkey);
 assert.notEqual(make('{"x":1}').rkey,make('{"x":2}').rkey);
 assert.notEqual(make('{"x":1}').rkey,make('{"x":1}','a.jsonl',2,1).rkey);
});
test('runtime Lexicon and payload checks reject invalid records, digest and overflow', () => {
 const {record}=make('{}'); assert.equal(validateEvent({...record,sourceLine:0}).success,false);
 assert.equal(validateEvent({...record,payloadEncoding:'other'}).success,false);
 assert.throws(()=>assertEvent({...record,payloadJson:'null'}),/digest/);
 assert.throws(()=>make(JSON.stringify({text:'é'.repeat(8388609)})),/16777216|too long|length/i);
});
test('malformed optional native metadata stays in payload without blocking publication',()=>{
 const raw='{"timestamp":"yesterday","version":{"future":1},"type":null}';
 const {record}=make(raw); assert.equal(record.occurredAt,undefined); assert.equal(record.harnessVersion,undefined); assert.equal(record.payloadJson,raw);
});
test('wire variants have concrete Lexicons and strict runtime validation',async()=>{
 const {validateLexiconRecord,EVENT_COLLECTION}=await import('../src/index.js');
 const manifest={$type:EVENT_COLLECTION,transportType:'com.ensembleworks.session.chunkManifest',encoding:'base64-json',digest:'a'.repeat(64),bytes:1000000,count:3};
 assert.ok(validateLexiconRecord(EVENT_COLLECTION,manifest).success);
 assert.equal(validateEvent(manifest).success,false);
 assert.equal(validateLexiconRecord(EVENT_COLLECTION,{...manifest,count:undefined}).success,false);
 assert.ok(validateLexiconRecord('com.ensembleworks.session.chunk',{$type:'com.ensembleworks.session.chunk',digest:'a'.repeat(64),index:0,data:'e30='}).success);
});
