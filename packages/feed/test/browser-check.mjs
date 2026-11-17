// Run with: node --env-file=.local/feed.env packages/feed/test/browser-check.mjs SESSION HOST [URL]
// SESSION is an explicit bb browser-automation local/headless session on HOST.
import {mkdtemp,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
const [session,host,url='http://localhost:3100']=process.argv.slice(2);
if(!session||!host||!process.env.FEED_LOGIN_PASSWORD)throw Error('SESSION HOST and FEED_LOGIN_PASSWORD required');
const dir=await mkdtemp(join(tmpdir(),'feed-browser-'));
const run=async(script)=>{const path=join(dir,'check.js');await writeFile(path,script,{mode:0o600});const output=execFileSync('bb',['browser-automation','run',session,'--script-file',path,'--script-host',host,'--json'],{encoding:'utf8'});const result=JSON.parse(output);if(result.exitCode)throw Error(result.text);return result;};
try {
 await run(`const p=await browser.getPage('main');await p.goto(${JSON.stringify(url+'/login')});await p.evaluate(()=>{document.querySelector('input[name=password]').value=${JSON.stringify(process.env.FEED_LOGIN_PASSWORD)};document.querySelector('form').requestSubmit();});`);
 let result;
 for(let attempt=0;attempt<20;attempt++){
   result=await run(`const p=await browser.getPage('main');await p.evaluate(()=>({url:location.pathname,cards:document.querySelectorAll('.card').length,status:document.querySelector('#status')?.textContent,error:document.querySelector('#error')?.hidden===false}));`);
   if(result.text.includes('"cards":')&&!result.text.includes('"cards": 0'))break;
   await new Promise(resolve=>setTimeout(resolve,500));
 }
 const verified=await run(`const p=await browser.getPage('main'); await p.evaluate(()=>{if(location.pathname!=='/')throw Error('Login failed');const cards=document.querySelectorAll('.card');if(!cards.length)throw Error('Missing synthetic session cards');cards[0].click();const details=document.querySelector('#detail details');if(!details)throw Error('Missing complete native event inspector');details.open=true;if(!details.querySelector('pre').textContent)throw Error('Empty native payload');if(document.querySelector('#detail script,#detail iframe,#detail img'))throw Error('Unsafe native markup');return {cards:cards.length,events:document.querySelectorAll('.event').length,status:document.querySelector('#status').textContent,inspectorOpened:details.open};});`);
 console.log(verified.text);
} finally {await rm(dir,{recursive:true,force:true});}
