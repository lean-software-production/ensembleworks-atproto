// Run: node tests/acceptance/browser.mjs SESSION HOST [URL]
import assert from 'node:assert/strict';
import {readFile,mkdtemp,writeFile,rm} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
const [session,host,url='http://localhost:3100']=process.argv.slice(2);
const password=(await readFile('.local/feed.env','utf8')).match(/^FEED_LOGIN_PASSWORD=(.*)$/m)[1];
const tmp=await mkdtemp(join(tmpdir(),'acceptance-browser-'));
async function run(script){const file=join(tmp,'check.js');await writeFile(file,script,{mode:0o600});const out=JSON.parse(execFileSync('bb',['browser-automation','run',session,'--script-file',file,'--script-host',host,'--json'],{encoding:'utf8'}));if(out.exitCode)throw Error(out.text);return out.text;}
try{
 await run(`const p=await browser.getPage('main');await p.goto(${JSON.stringify(url+'/login')});await p.evaluate(()=>{document.querySelector('input[name=password]').value=${JSON.stringify(password)};document.querySelector('form').requestSubmit();});`);
 await new Promise(r=>setTimeout(r,1500));
 console.log(await run(`const p=await browser.getPage('main');await p.evaluate(async()=>{const data=await fetch('/api/sessions').then(r=>r.json());const sessions=data.sessions.filter(s=>s.id.startsWith('acceptance-'));if(!sessions.length)throw Error('No acceptance data');let inspected=0;for(const s of sessions){const card=[...document.querySelectorAll('.card')][data.sessions.indexOf(s)];if(!card)throw Error('Missing acceptance card');card.click();const texts=[...document.querySelectorAll('#detail .event details:first-of-type pre')].map(e=>e.textContent);for(const e of s.events){if(!texts.includes(e.envelope.payloadJson))throw Error('Native payload mismatch in browser');inspected++;}if(document.querySelector('#detail img,#detail svg,#detail script')||globalThis.__acceptanceXss)throw Error('XSS');}globalThis.__acceptanceDocument=Date.now();return {passed:true,inspected,check:'exact native browser payloads and literal XSS text'};});`));
 const state=JSON.parse(await readFile('.local/accounts.json','utf8')),a=state.accounts.find(a=>a.name==='alice');
 const id=`browser-refresh-${Date.now()}`;const raw=JSON.stringify({uuid:id,sessionId:id,type:'user',message:{content:id}});await writeFile(join(tmp,'refresh.jsonl'),raw+'\n');
 execFileSync(process.execPath,['--import','tsx','packages/cli/src/main.ts','once','--dir',tmp,'--state',join(tmp,'state.json'),'--namespace',id],{env:{...process.env,PDS_SERVICE:state.service,PDS_SPACE:state.space,PDS_IDENTIFIER:a.handle,PDS_PASSWORD:a.password},stdio:'pipe'});
 await new Promise(r=>setTimeout(r,6500));
 console.log(await run(`const p=await browser.getPage('main');await p.evaluate(()=>{if(!globalThis.__acceptanceDocument)throw Error('Page navigated');const card=[...document.querySelectorAll('.card')].find(c=>c.textContent.includes(${JSON.stringify(id)}));if(!card)throw Error('Append not refreshed');card.click();if(!document.querySelector('#detail').textContent.includes(${JSON.stringify(raw)}))throw Error('Missing exact refreshed event');return {passed:true,check:'actual CLI append appears without browser navigation'};});`));
}finally{await rm(tmp,{recursive:true,force:true});}
