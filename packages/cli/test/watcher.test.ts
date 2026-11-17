import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp, mkdir, writeFile, readFile, appendFile, rename, rm, symlink} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {runOnce,watchDirectory, type WatchOptions} from '../src/watcher.js';
import type {EventRecord} from '@ensemble/protocol';
async function setup(t: {after: (fn:()=>Promise<void>)=>void}) {
 const base=await mkdtemp(join(tmpdir(),'ensemble-fixture-')); t.after(()=>rm(base,{recursive:true,force:true}));
 const dir=join(base,'logs'); await mkdir(dir);
 const records=new Map<string,EventRecord>(); let calls=0;
 const options:WatchOptions={dir,stateFile:join(base,'state.json'),namespace:'fixture',destination:'test-space',transport:{async putEvent(key,record) {calls++; records.set(key,structuredClone(record)); return {uri:`at://did:plc:fixture/com.ensembleworks.session.event/${key}`,cid:'fake-test-cid'};}}};
 return {base,dir,records,options,calls:()=>calls};
}
test('backfill all fixtures, nested/subagent separation, durable restart dedupe',async t=>{
 const s=await setup(t); const fixture=await readFile(new URL('./fixtures/session.jsonl',import.meta.url),'utf8');
 await writeFile(join(s.dir,'session.jsonl'),fixture); await mkdir(join(s.dir,'subagents'));
 await writeFile(join(s.dir,'subagents/agent.jsonl'),'{"uuid":"u1","sessionId":"synthetic-session","isSidechain":true}\n');
 const first=await runOnce(s.options); assert.equal(first.published,11); assert.equal(first.issues.length,0);
 assert.equal((await runOnce(s.options)).published,0); assert.equal(s.calls(),11);
 const raw=[...s.records.values()].find(r=>r.nativeType==='future-new-event')!.payloadJson;
 assert.match(raw,/900719925474099312345/); assert.match(raw,/4.500/);
 assert.ok([...s.records.values()].every(r=>!r.sourcePath.startsWith('/')));
});
test('partial UTF8 final line waits, malformed completed lines report and recovery imports',async t=>{
 const s=await setup(t), path=join(s.dir,'a.jsonl');
 await writeFile(path,'{"uuid":"first"}\ninvalid\n{"uuid":"partial","text":"');
 let result=await runOnce(s.options); assert.equal(result.published,1); assert.equal(result.partialFiles,1); assert.equal(result.issues[0].kind,'malformed');
 const utf8=Buffer.from('é'); await appendFile(path,utf8.subarray(0,1)); assert.equal((await runOnce(s.options)).published,0);
 await appendFile(path,Buffer.concat([utf8.subarray(1),Buffer.from('"}\n')])); assert.equal((await runOnce(s.options)).published,1);
 await writeFile(path,'{"uuid":"first"}\n{"uuid":"fixed"}\n{"uuid":"partial","text":"é"}\n');
 assert.equal((await runOnce(s.options)).published,1);
});
test('rewrites update UUID, keep removed archive; duplicate UUID takes last observed value',async t=>{
 const s=await setup(t), path=join(s.dir,'a.jsonl');
 await writeFile(path,'{"uuid":"u","text":"old"}\n{"meta":1}\n'); await runOnce(s.options);
 const key=[...s.records].find(([,r])=>r.nativeId==='u')![0];
 await writeFile(path,'{"uuid":"u","text":"old"}\n{"uuid":"u","text":"new"}\n{"meta":2}\n');
 assert.equal((await runOnce(s.options)).published,2); assert.match(s.records.get(key)!.payloadJson,/new/);
 assert.equal(s.records.size,3); assert.equal((await runOnce(s.options)).published,0);
});
test('outage and ambiguous commit retry identical record after source removal',async t=>{
 const s=await setup(t); await writeFile(join(s.dir,'a.jsonl'),'{"uuid":"u"}\n');
 const real=s.options.transport; let observed:EventRecord|undefined;
 s.options.transport={async putEvent(key,record){ observed=structuredClone(record); await real.putEvent(key,record); throw new Error('secret password must not leak'); }};
 const result=await runOnce(s.options); assert.equal(result.issues[0].kind,'publish'); assert.doesNotMatch(JSON.stringify(result),/secret/);
 await rm(join(s.dir,'a.jsonl')); s.options.transport=real;
 assert.equal((await runOnce(s.options)).published,1); assert.equal(s.records.size,1); assert.deepEqual([...s.records.values()][0],observed);
 assert.equal((await runOnce(s.options)).published,0);
});
test('numbered rotation retains logical stream identity; no symlink traversal',async t=>{
 const s=await setup(t); await writeFile(join(s.dir,'a.jsonl'),'{"uuid":"old"}\n'); await runOnce(s.options);
 await rename(join(s.dir,'a.jsonl'),join(s.dir,'a.jsonl.1')); await writeFile(join(s.dir,'a.jsonl'),'{"uuid":"new"}\n');
 await writeFile(join(s.base,'outside.jsonl'),'{"secret":true}\n'); await symlink(join(s.base,'outside.jsonl'),join(s.dir,'link.jsonl'));
 assert.equal((await runOnce(s.options)).published,2); assert.equal(s.records.size,2);
 assert.equal((await runOnce(s.options)).published,0);
});
test('oversize visible and retryable on correction; bad UTF8 never replaced silently',async t=>{
 const s=await setup(t), path=join(s.dir,'a.jsonl');
 await writeFile(path,JSON.stringify({uuid:'large',text:'x'.repeat(16777217)})+'\n'); assert.equal((await runOnce(s.options)).issues[0].kind,'invalid'); assert.equal(s.records.size,0);
 await writeFile(path,'{"uuid":"large","text":"fixed"}\n'); assert.equal((await runOnce(s.options)).published,1);
 await appendFile(path,Buffer.from([0xff,0x0a])); assert.equal((await runOnce(s.options)).issues[0].kind,'malformed');
});
test('checkpoint mismatch, corrupt state and simultaneous writer fail explicitly',async t=>{
 const s=await setup(t); await runOnce(s.options);
 await assert.rejects(runOnce({...s.options,destination:'another-account'}),/mismatch/);
 await writeFile(s.options.stateFile,'bad json'); await assert.rejects(runOnce(s.options));
 await rm(s.options.stateFile);
 let release!:()=>void; let started!:()=>void; const ready=new Promise<void>(r=>started=r);
 await writeFile(join(s.dir,'a.jsonl'),'{\"uuid\":\"lock\"}\n');
 const running=runOnce({...s.options,transport:{async putEvent(){started(); await new Promise<void>(r=>release=r); return {uri:'uri',cid:'cid'};}}});
 await ready; await assert.rejects(runOnce(s.options),/locked/); release(); await running;
});
test('watch imports new appends and exits through abort',async t=>{
 const s=await setup(t),controller=new AbortController(); let scans=0;
 const path=join(s.dir,'a.jsonl'); await writeFile(path,'{"uuid":"first"}\n');
 await watchDirectory({...s.options,intervalMs:10,signal:controller.signal,onScan:result=>{
   scans++; if (scans===1) void appendFile(path,'{"uuid":"second"}\n');
   if (s.records.size===2) controller.abort(); if(scans>30) {controller.abort(); assert.fail('append not observed');}
 }});
 assert.equal(s.records.size,2);
});
test('SIGKILL releases OS lock and pending ledger restarts unattended',async t=>{
 const {spawn}=await import('node:child_process');
 const s=await setup(t); await writeFile(join(s.dir,'a.jsonl'),'{"uuid":"crash"}\n');
 const worker=join(s.base,'crash.mjs'), marker=join(s.base,'entered');
 await writeFile(worker,`import {runOnce} from ${JSON.stringify(new URL('../src/watcher.ts',import.meta.url).href)}; import {writeFile} from 'node:fs/promises'; await runOnce({...${JSON.stringify({...s.options,transport:undefined})},transport:{async putEvent(){await writeFile(${JSON.stringify(marker)},'ready'); await new Promise(()=>{});}}});`);
 const child=spawn(process.execPath,['--import','tsx',worker],{stdio:'ignore'});
 t.after(async()=>{child.kill('SIGKILL');});
 const exited=new Promise<void>(r=>child.once('exit',()=>r()));
 for(let i=0;i<200;i++){try {await readFile(marker);break;} catch {await new Promise(r=>setTimeout(r,10));}}
 assert.equal(await readFile(marker,'utf8'),'ready'); child.kill('SIGKILL'); await exited;
 // The OS helper notices EOF asynchronously after the owner dies.
 let result;
 for(let i=0;i<100;i++){try{result=await runOnce(s.options);break;}catch(e){if(!String(e).includes('locked'))throw e; await new Promise(r=>setTimeout(r,10));}}
 assert.equal(result?.published,1); assert.equal((await runOnce(s.options)).published,0);
});
test('missing source directory reports and retries pending writes; watch resumes when it returns',async t=>{
 const s=await setup(t),path=join(s.dir,'a.jsonl');
 await writeFile(path,'{"uuid":"pending"}\n');
 await runOnce({...s.options,transport:{async putEvent(){throw new Error('outage');}}});
 await rename(s.dir,join(s.base,'temporarily-away'));
 const missing=await runOnce(s.options);
 assert.equal(missing.published,1); assert.equal(missing.issues[0].kind,'source');
 assert.equal(missing.issues[0].sourcePath,'.'); assert.match(missing.issues[0].message,/ENOENT/);
 const controller=new AbortController(); let scans=0; let restore:Promise<void>|undefined;
 await watchDirectory({...s.options,intervalMs:10,maxRetryMs:20,signal:controller.signal,onScan:result=>{
   scans++;
   if(scans===1){
     assert.equal(result.issues[0].kind,'source');
     restore=(async()=>{await rename(join(s.base,'temporarily-away'),s.dir); await appendFile(path,'{"uuid":"after-return"}\n');})();
   }
   if(s.records.size===2) controller.abort();
   if(scans>30){controller.abort(); assert.fail('source restoration not observed');}
 }});
 await restore;
 assert.equal(s.records.size,2); assert.equal((await runOnce(s.options)).published,0);
});
