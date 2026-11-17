import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createFeedServer} from '../src/server.ts';
import {sessionsFromRecords,readAllRecords} from '../src/model.ts';
const row=(native:unknown,extra:Record<string,unknown>={})=>({uri:'at://did:plc:alice/com.ensembleworks.session.event/a',cid:'cid',value:{sessionId:'s',streamId:'one',sourceLine:1,sourceOrder:0,payloadJson:JSON.stringify(native),...extra}});
test('all native events survive grouping, author identity and deterministic ordering',()=>{
 const rows=[row({type:'future',strange:['<script>alert(1)</script>']},{occurredAt:'2026-01-02'}),{...row({type:'user',cwd:'/synthetic/repo',message:{content:[{type:'text',text:'First\nsecond'}]}},{occurredAt:'2026-01-01',parentId:'parent'}),uri:'at://did:plc:alice/com.ensembleworks.session.event/b'}, {...row(false),uri:'at://did:plc:bob/com.ensembleworks.session.event/c'}];
 const result=sessionsFromRecords(rows,{'did:plc:alice':'Alice'});
 const alice=result.find(s=>s.author==='Alice');assert.equal(alice.events.length,2);assert.equal(alice.prompt,'First\nsecond');assert.equal(alice.project,'/synthetic/repo');assert.equal(alice.events[0].envelope.parentId,'parent');assert.equal(alice.events[1].native.strange[0],'<script>alert(1)</script>');assert.equal(result.length,2);assert.equal(result.find(s=>s.authorDid==='did:plc:bob').events[0].native,false);
});
test('pagination fetches every page and rejects a repeated cursor',async()=>{
 let calls=0;const rows=await readAllRecords({async listEvents({cursor}){calls++;return cursor?{records:[{...row(null),uri:'second'}]}:{records:[row(null)],cursor:'next'};}});assert.equal(calls,2);assert.equal(rows.length,2);
 await assert.rejects(readAllRecords({async listEvents(){return {records:[],cursor:'stuck'};}}),/repeated/);
});
test('feed protects HTML/API, verifies login origin and cookie, and reports PDS errors without secrets',async(t)=>{
 let fail=false;let reads=0;
 const server=createFeedServer({password:'test-company-only',secret:'x'.repeat(32),transport:{async listEvents(){reads++;if(fail)throw new Error('password=secret-reader');return {records:[row({type:'assistant',message:{content:'hello'}})]};}}});
 await new Promise<void>(resolve=>server.listen(0,'127.0.0.1',resolve));t.after(()=>server.close());
 const address=server.address() as {port:number};const base=`http://127.0.0.1:${address.port}`;
 assert.equal((await fetch(base,{redirect:'manual'})).status,303);assert.equal((await fetch(base+'/api/sessions')).status,401);assert.equal(reads,0);
 assert.equal((await fetch(base+'/login',{method:'POST',body:'password=test-company-only'})).status,403);
 const bad=await fetch(base+'/login',{method:'POST',headers:{origin:base},body:'password=wrong'});assert.equal(bad.status,401);
 const login=await fetch(base+'/login',{method:'POST',headers:{origin:base},body:'password=test-company-only',redirect:'manual'});assert.equal(login.status,303);const cookie=login.headers.get('set-cookie')!;assert.match(cookie,/HttpOnly/);assert.match(cookie,/SameSite=Strict/);
 assert.equal((await fetch(base+'/api/sessions',{headers:{cookie:cookie.replace(/ensemble_session=./,'ensemble_session=0')}})).status,401);
 const feed=await fetch(base+'/api/sessions',{headers:{cookie}});assert.equal(feed.status,200);assert.equal((await feed.json()).recordCount,1);
 fail=true;const error=await fetch(base+'/api/sessions',{headers:{cookie}});assert.equal(error.status,502);assert.doesNotMatch(await error.text(),/secret-reader/);
 assert.match((await fetch(base+'/app.js',{headers:{cookie}})).headers.get('content-security-policy')!,/object-src 'none'/);
});
test('Space record URI identifies writer DID, not company authority',()=>{
 const rows=[{...row({type:'user'}),uri:'at://did:plc:company/space/team/abc/did:plc:alice/com.ensembleworks.session.event/a'}];
 assert.equal(sessionsFromRecords(rows)[0].authorDid,'did:plc:alice');
});
test('two Space writers with same session ID stay separate and custom title wins over summary',()=>{
 const uri=(author:string,key:string)=>`at://did:plc:company/space/team/abc/did:plc:${author}/com.ensembleworks.session.event/${key}`;
 const result=sessionsFromRecords([{...row({customTitle:'Human title'},{sourceOrder:0}),uri:uri('alice','a')},{...row({summary:'Compacted summary'},{sourceOrder:1}),uri:uri('alice','b')},{...row({aiTitle:'Generated title'}),uri:uri('bob','c')}]);
 assert.equal(result.length,2);assert.equal(result.find(s=>s.authorDid==='did:plc:alice').title,'Human title');assert.equal(result.find(s=>s.authorDid==='did:plc:bob').title,'Generated title');
});
test('unknown events without sessionId join the unique session in their stream',()=>{
 const unknown=row(null,{sessionId:undefined});unknown.uri+='-unknown';
 const result=sessionsFromRecords([row({type:'user'}),unknown]);assert.equal(result.length,1);assert.equal(result[0].events.length,2);
});
