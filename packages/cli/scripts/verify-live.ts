// Explicit opt-in integration check using local synthetic pilot accounts only.
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createTransport } from '@ensemble/transport';
import { assertEvent } from '@ensemble/protocol';
const path = process.argv[2];
if (!path) throw new Error('Pass the local pilot accounts JSON explicitly');
const settings = JSON.parse(await readFile(path,'utf8'));
const bob = settings.accounts.find((account: {name:string})=>account.name==='bob');
const transport = createTransport({service:settings.service,space:settings.space,identifier:bob.handle,password:bob.password});
let cursor: string | undefined; const fixture=[];
do {
  const page=await transport.listEvents({cursor});
  for(const entry of page.records) {
    if(entry.value.sessionId!=='synthetic-session') continue;
    assertEvent(entry.value); fixture.push(entry);
  }
  cursor=page.cursor;
} while(cursor);
assert.ok(fixture.length>=8,'Expected synthetic fixture events visible to Bob');
const unknown=fixture.find(entry=>entry.value.nativeType==='future-new-event');
assert.ok(unknown); assert.match(unknown.value.payloadJson,/900719925474099312345/);
assert.match(unknown.value.payloadJson,/4.500/);
console.log(JSON.stringify({verifiedAs:'bob',syntheticSessionRecords:fixture.length,exactLargeIntegerAndDecimal:true}));
