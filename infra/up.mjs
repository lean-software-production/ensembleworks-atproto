import {spawnSync} from 'node:child_process';
await import('./init.mjs');
function run(args){const r=spawnSync('docker',['compose',...args],{stdio:'inherit',env:process.env});if(r.status!==0)throw new Error(`docker compose ${args.join(' ')} failed`);}
run(['up','-d','--build','pds']);
let ready=false;for(let i=0;i<60;i++){try{const r=await fetch('http://localhost:2583/xrpc/_health',{signal:AbortSignal.timeout(1000)});if(r.ok){ready=true;break;}}catch{}await new Promise(r=>setTimeout(r,1000));}
if(!ready)throw new Error('PDS did not become healthy in 60 seconds');
await import('./bootstrap.mjs');
run(['up','-d','--build','--no-deps','feed']);
console.log('Feed: http://localhost:3100; PDS: http://localhost:2583. Login credentials are in .local/feed.env');
