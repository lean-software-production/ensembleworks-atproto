import {test} from 'node:test';
import assert from 'node:assert/strict';
// Opt-in: this test only reads a running feed backed by the real PDS.
// Set FEED_TEST_URL and FEED_LOGIN_PASSWORD in the environment.
test('real PDS feed exposes complete synthetic events behind login', {skip:!process.env.FEED_TEST_URL}, async()=>{
 const base=process.env.FEED_TEST_URL!;
 assert.ok(process.env.FEED_LOGIN_PASSWORD,'FEED_LOGIN_PASSWORD required');
 assert.equal((await fetch(base+'/api/sessions')).status,401);
 const login=await fetch(base+'/login',{method:'POST',headers:{origin:base},body:new URLSearchParams({password:process.env.FEED_LOGIN_PASSWORD!}),redirect:'manual'});
 assert.equal(login.status,303);const cookie=login.headers.get('set-cookie')!;
 const response=await fetch(base+'/api/sessions',{headers:{cookie}});assert.equal(response.status,200);
 const data=await response.json();assert.ok(data.recordCount>0,'Publish synthetic watcher fixtures before running');
 const events=data.sessions.flatMap((s:any)=>s.events);
 assert.equal(events.length,data.recordCount);
 for(const event of events.filter((e:any)=>e.envelope.payloadEncoding==='json')){assert.match(event.uri,/^at:\/\/did:/);assert.equal(typeof event.envelope.payloadJson,'string');assert.deepEqual(event.native,JSON.parse(event.envelope.payloadJson));}
 const expected=(process.env.FEED_EXPECT_TYPES||'user,assistant').split(',');
 for(const type of expected)assert.ok(events.some((e:any)=>e.type===type),`Missing ${type}`);
});
