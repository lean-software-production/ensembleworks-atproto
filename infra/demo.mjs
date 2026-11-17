import {mkdir,readFile,writeFile,copyFile,appendFile} from 'node:fs/promises';
import {constants} from 'node:fs';
import {randomUUID} from 'node:crypto';
import {spawn} from 'node:child_process';
import {resolve} from 'node:path';
const mode=process.argv[2];
const inDocker=process.argv.includes('--docker');
if(!['seed','once','watch','append'].includes(mode))throw new Error('Use seed, once, watch, or append');
await mkdir('.local/demo-fixtures',{recursive:true,mode:0o700});
const accounts=JSON.parse(await readFile('.local/accounts.json','utf8'));
const alice=accounts.accounts.find(a=>a.name==='alice');
await writeFile('.local/demo-writer.json',JSON.stringify({service:accounts.service,space:accounts.space,identifier:alice.handle,password:alice.password,namespace:'repository-synthetic-demo'},null,2)+'\n',{mode:0o600});
try{await copyFile('packages/cli/test/fixtures/session.jsonl','.local/demo-fixtures/session.jsonl',constants.COPYFILE_EXCL);}catch(e){if(e.code!=='EEXIST')throw e;}
if(mode==='seed')console.log('Synthetic fixture ready in .local/demo-fixtures; writer config .local/demo-writer.json; existing demo preserved.');
else if(mode==='append'){
 const uuid=randomUUID();await appendFile('.local/demo-fixtures/session.jsonl',JSON.stringify({uuid,type:'user',sessionId:'synthetic-session',timestamp:new Date().toISOString(),message:{role:'user',content:'Synthetic append: confirm this event arrives without reloading the feed.'}})+'\n');
 console.log(JSON.stringify({appended:true,uuid,path:'.local/demo-fixtures/session.jsonl'}));
}else{
 const cliArgs=['--import','tsx','packages/cli/src/main.ts',mode,'--dir','.local/demo-fixtures','--config','.local/demo-writer.json','--state',inDocker?'.local/demo-docker-state.json':'.local/demo-state.json','--interval','2000'];
 const child=inDocker
   ? spawn('docker',['compose','run','--rm','-T','--no-deps','-v',`${resolve('.local')}:/app/.local`,'-e','PDS_SERVICE=http://pds:2583','feed','node',...cliArgs],{stdio:'inherit'})
   : spawn(process.execPath,cliArgs,{stdio:'inherit'});
 child.on('error',error=>{console.error(`Could not start watcher: ${error.message}`);process.exitCode=1;});
 for(const signal of ['SIGINT','SIGTERM'])process.on(signal,()=>child.kill(signal));
 child.on('exit',(code)=>{process.exitCode=code??1;});
}
