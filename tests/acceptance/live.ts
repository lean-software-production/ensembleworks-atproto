// Synthetic-only real-stack acceptance. Never prints credentials or native payloads.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,appendFile,rename} from 'node:fs/promises';
import {spawn,execFileSync} from 'node:child_process';
import {once} from 'node:events';
import {createHash} from 'node:crypto';
import {createTransport} from '../../packages/transport/src/index.ts';
const state=JSON.parse(await readFile('.local/accounts.json','utf8'));
const base=process.env.FEED_TEST_URL||'http://localhost:3100';
const envText=await readFile('.local/feed.env','utf8');
const password=envText.match(/^FEED_LOGIN_PASSWORD=(.*)$/m)![1];
const run=`acceptance-${Date.now()}`,dir=`.local/${run}`,source=`${dir}/logs`,checkpoint=`${dir}/state.json`;
await mkdir(source,{recursive:true});
const account=(name:string)=>state.accounts.find((a:any)=>a.name===name);
const config=(name:string)=>({service:state.service,space:state.space,identifier:account(name).handle,password:account(name).password});
const reader=createTransport(config('bob'));
const sleep=(ms:number)=>new Promise(r=>setTimeout(r,ms));
async function until(fn:()=>Promise<boolean>,label:string,timeout=90000){const start=Date.now();while(Date.now()-start<timeout){try{if(await fn())return;}catch{}await sleep(500);}throw Error(`Timed out: ${label}`);}
const expected=new Map<string,string>();
const event=(id:string,extra:any={})=>JSON.stringify({uuid:`${run}-${id}`,sessionId:run,type:'unknown-native',...extra});
async function append(id:string,extra:any={},file=`${source}/session.jsonl`){const raw=event(id,extra);expected.set(`${run}-${id}`,raw);await appendFile(file,raw+'\n');return raw;}
let child:ReturnType<typeof spawn>|undefined,logs='';
function start(name='alice',mode='watch',path=source,cp=checkpoint){const c=spawn(process.execPath,['--import','tsx','packages/cli/src/main.ts',mode,'--dir',path,'--state',cp,'--namespace',run,'--interval','200'],{env:{...process.env,PDS_SERVICE:state.service,PDS_SPACE:state.space,PDS_IDENTIFIER:account(name).handle,PDS_PASSWORD:account(name).password},stdio:['ignore','pipe','pipe']});c.stdout!.on('data',b=>logs+=b);c.stderr!.on('data',b=>logs+=b);return c;}
async function stop(signal:NodeJS.Signals='SIGTERM'){if(child&&child.exitCode===null&&child.signalCode===null){const exited=once(child,'exit');child.kill(signal);await exited;}child=undefined;}
async function rows(){let all:any[]=[],cursor;do{const p=await reader.listEvents({limit:100,cursor});all.push(...p.records);cursor=p.cursor;}while(cursor);return all.filter(r=>r.value.sessionId===run);}
async function caughtUp(){await until(async()=>{const all=await rows();return [...expected].every(([id,raw])=>all.some(r=>r.value.nativeId===id&&r.value.payloadJson===raw));},'exact PDS readback');}
const pass=(name:string)=>console.log(`PASS ${name}`);
let cookie='';
async function login(){const r=await fetch(base+'/login',{method:'POST',headers:{origin:base},body:new URLSearchParams({password}),redirect:'manual'});assert.equal(r.status,303);cookie=r.headers.get('set-cookie')!.split(';')[0];}
async function feed(){const r=await fetch(base+'/api/sessions',{headers:{cookie}});assert.equal(r.status,200);return r.json();}
function compose(...args:string[]){execFileSync('docker',['compose',...args],{env:{...process.env,DOCKER_CONFIG:'/tmp/ew-docker'},stdio:'pipe'});}
try{
 await append('initial',{type:'system',content:'Existing synthetic event'});
 child=start();await caughtUp();pass('actual CLI watch imports existing log');
 await append('prompt',{type:'user',message:{role:'user',content:'Synthetic prompt <img src=x onerror="globalThis.__acceptanceXss=1">'}});
 await append('call',{type:'assistant',message:{role:'assistant',content:[{type:'tool_use',id:'tool-1',name:'Bash',input:{command:'echo synthetic'}}]}});
 await append('result',{type:'user',message:{role:'user',content:[{type:'tool_result',tool_use_id:'tool-1',content:'synthetic tool output'}]}});
 await append('title',{type:'custom-title',customTitle:`${run} <svg onload="globalThis.__acceptanceXss=1">`});
 await append('unknown',{type:'future-native-type',timestamp:'not-a-date',version:42,data:{arbitrary:[null,true,42,'雪']}});
 await caughtUp();pass('prompt, tool_use, tool_result, title, unknown type and arbitrary timestamp roundtrip');
 const partial=event('partial',{content:'split line'});await appendFile(`${source}/session.jsonl`,partial.slice(0,35));await sleep(1200);assert.ok(!(await rows()).some(r=>r.value.nativeId===`${run}-partial`));await appendFile(`${source}/session.jsonl`,partial.slice(35)+'\n');expected.set(`${run}-partial`,partial);await caughtUp();pass('partial line held until newline');
 await appendFile(`${source}/session.jsonl`,'{malformed\n');await append('recovery');await caughtUp();assert.match(logs,/malformed/);pass('malformed line visible; later valid line publishes');
 await mkdir(`${source}/subagents`,{recursive:true});await append('subagent',{type:'progress',isSidechain:true},`${source}/subagents/agent.jsonl`);await caughtUp();pass('nested subagent log');
 const before=await rows();await sleep(1500);assert.deepEqual(await rows(),before);await stop();child=start();await caughtUp();await sleep(1000);assert.deepEqual(await rows(),before);await append('during-crash');let held=false;for(let i=0;i<1000&&!held;i++){try{execFileSync('flock',['--nonblock',checkpoint+'.lock','true'],{stdio:'pipe'});}catch(e){if((e as any).status!==1)throw e;held=true;}if(!held)await sleep(10);}assert.ok(held,'checkpoint lock held before SIGKILL');await stop('SIGKILL');child=start();await append('after-crash');await caughtUp();pass('repeat scans and clean restart preserve records/CID/capturedAt; SIGKILL during held lock recovers');
 await rename(`${source}/session.jsonl`,`${source}/session.jsonl.1`);await append('rotated');await caughtUp();assert.equal((await rows()).length,expected.size);pass('numbered rotation adds only new event');
 await append('rotated',{content:'rewritten UUID current value'});await caughtUp();assert.equal((await rows()).length,expected.size);pass('same UUID updates in place');
 if(process.env.ACCEPTANCE_LARGE==='1'){await append('large',{type:'user',message:{content:[{type:'tool_result',content:'雪"\\'.repeat(220000)}]}});await caughtUp();const row=(await rows()).find(r=>r.value.nativeId===`${run}-large`);assert.equal(row.value.payloadDigest,createHash('sha256').update(expected.get(`${run}-large`)!).digest('hex'));pass('oversized Unicode/escaped tool output exact digest and payload');}
 await mkdir(`${dir}/bob`,{recursive:true});await append('bob',{type:'user',message:{content:'Bob synthetic prompt'}},`${dir}/bob/bob.jsonl`);const bob=start('bob','once',`${dir}/bob`,`${dir}/bob-state.json`);assert.equal((await once(bob,'exit'))[0],0);await caughtUp();assert.equal((await rows()).find(r=>r.value.nativeId===`${run}-bob`).authorDid,account('bob').did);pass('second writer authentic attribution');
 assert.equal((await fetch(base+'/api/sessions')).status,401);assert.equal((await fetch(base+'/',{redirect:'manual'})).status,303);assert.equal((await fetch(base+'/login',{method:'POST',headers:{origin:'http://evil.invalid'},body:new URLSearchParams({password}),redirect:'manual'})).status,403);await login();
 const data=await feed();for(const [id,raw]of expected){const session=data.sessions.find((s:any)=>s.events.some((e:any)=>e.envelope.nativeId===id));assert.ok(session);assert.equal(session.authorDid,account(id.endsWith('-bob')?'bob':'alice').did);const e=session.events.find((e:any)=>e.envelope.nativeId===id);assert.equal(e.envelope.payloadJson,raw);assert.deepEqual(e.native,JSON.parse(raw));}pass('feed auth gate, exact payloads and two-person authorship');
 await assert.rejects(()=>createTransport(config('outsider')).listEvents());await assert.rejects(()=>createTransport(config('outsider')).putEvent('acceptance-denied',{$type:'com.ensembleworks.session.event'}));
 for(const name of ['alice','bob'])for(const collection of ['com.ensembleworks.session.event','com.ensembleworks.session.chunk']){const query=new URLSearchParams({repo:account(name).did,collection});const r=await fetch(`${state.service}/xrpc/com.atproto.repo.listRecords?${query}`);assert.equal(r.status,200);assert.deepEqual((await r.json()).records,[]);}pass('outsider read/write denied and both public event/chunk collections empty');
 if(process.env.ACCEPTANCE_DISRUPT==='1'){
  compose('stop','pds');try{await append('outage');await until(async()=>logs.includes('Publication failed'),'visible outage');assert.equal((await fetch(base+'/api/sessions',{headers:{cookie}})).status,502);await writeFile(`${source}/session.jsonl`,'');pass('PDS outage retains pending event after source truncation; feed fails visibly');}finally{compose('start','pds');}
  await caughtUp();await feed();pass('watcher and feed recover after PDS outage');await stop();const durable=await rows();compose('restart','postgres','plc','pds','feed');await until(async()=>{await login();return (await rows()).length===durable.length;},'Compose restart recovery');assert.deepEqual(await rows(),durable);await feed();pass('Compose restart preserves exact records and feed access');
 }
 await writeFile(`${dir}/summary.json`,JSON.stringify({run,events:expected.size,large:process.env.ACCEPTANCE_LARGE==='1',disruptive:process.env.ACCEPTANCE_DISRUPT==='1'}));console.log(`ACCEPTED_RUN ${run} events=${expected.size}`);
}finally{await stop();}
