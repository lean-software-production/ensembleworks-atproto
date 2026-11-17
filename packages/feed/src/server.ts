import {createServer, type IncomingMessage} from 'node:http';
import {createHmac, timingSafeEqual, randomBytes} from 'node:crypto';
import {readFile} from 'node:fs/promises';
import {sessionsFromRecords,readAllRecords} from './model.ts';
const equal = (a:string,b:string) => {const x=Buffer.from(a),y=Buffer.from(b); return x.length===y.length && timingSafeEqual(x,y);};
export function createFeedServer(config:{password:string;secret:string;secureCookie?:boolean;names?:Record<string,string>;transport:Parameters<typeof readAllRecords>[0]}) {
  if (!config.password || config.secret.length<32) throw new Error('FEED_LOGIN_PASSWORD and FEED_SESSION_SECRET (32+ characters) required');
  const sign = (v:string)=>createHmac('sha256',config.secret).update(v).digest('hex');
  const authenticated = (req:IncomingMessage) => {
    const token = req.headers.cookie?.split(';').map(x=>x.trim()).find(x=>x.startsWith('ensemble_session='))?.slice(17) || '';
    const [expires,nonce,signature] = token.split('.');
    return !!signature && Number(expires)>Date.now() && equal(signature,sign(`${expires}.${nonce}`));
  };
  let inFlight:Promise<any>|undefined;
  return createServer(async(req,res)=>{
    res.setHeader('Cache-Control','no-store'); res.setHeader('X-Content-Type-Options','nosniff');
    res.setHeader('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'");
    res.setHeader('Referrer-Policy','same-origin');
    const send = (status:number,body:string,type='text/plain; charset=utf-8')=>{res.writeHead(status,{'Content-Type':type});res.end(body);};
    try {
      const path = req.url?.split('?')[0];
      if(req.method==='POST') {
        // Browser submissions must originate from this host, including logout.
        if (!req.headers.origin || !/^https?:\/\//.test(req.headers.origin) || new URL(req.headers.origin).host !== req.headers.host) return send(403,'Origin rejected');
        if(path==='/login') {
          let body=''; for await (const chunk of req) {body+=chunk; if(body.length>4096) return send(413,'Request too large');}
          if(!equal(new URLSearchParams(body).get('password')||'',config.password)) return send(401,'Incorrect company password. Return to login and try again.');
          const token = `${Date.now()+8*60*60*1000}.${randomBytes(16).toString('hex')}`;
          res.setHeader('Set-Cookie',`ensemble_session=${token}.${sign(token)}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800${config.secureCookie?'; Secure':''}`);
          res.writeHead(303,{Location:'/'}); return res.end();
        }
        if(path==='/logout') {res.setHeader('Set-Cookie','ensemble_session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0');res.writeHead(303,{Location:'/login'});return res.end();}
      }
      if(req.method!=='GET') return send(405,'Method not allowed');
      if(path==='/healthz') return send(200,'ok');
      if(path==='/login') return send(200,await readFile(new URL('../public/login.html',import.meta.url),'utf8'),'text/html; charset=utf-8');
      if(path==='/style.css') return send(200,await readFile(new URL('../public/style.css',import.meta.url),'utf8'),'text/css; charset=utf-8');
      if(!authenticated(req)) {if(path==='/api/sessions') return send(401,JSON.stringify({error:'Login required'}),'application/json');res.writeHead(303,{Location:'/login'});return res.end();}
      if(path==='/api/sessions') {
        if(!inFlight) {inFlight=readAllRecords(config.transport).then(rows=>({sessions:sessionsFromRecords(rows,config.names),recordCount:rows.length,refreshedAt:new Date().toISOString()}));inFlight.finally(()=>{inFlight=undefined;}).catch(()=>{});}
        let timer:ReturnType<typeof setTimeout>|undefined;
        try {const snapshot = await Promise.race([inFlight,new Promise((_,reject)=>{timer=setTimeout(()=>reject(new Error('timeout')),30000);})]);return send(200,JSON.stringify(snapshot),'application/json');}
        catch {return send(502,JSON.stringify({error:'Cannot read company PDS. Check service, credentials and Space membership; retrying automatically.'}),'application/json');}
        finally {clearTimeout(timer);}
      }
      const files:Record<string,[string,string]>={'/':['index.html','text/html'],'/app.js':['app.js','text/javascript'],'/style.css':['style.css','text/css']};
      const file=files[path||'']; if(!file) return send(404,'Not found');
      return send(200,await readFile(new URL(`../public/${file[0]}`,import.meta.url),'utf8'),`${file[1]}; charset=utf-8`);
    } catch {send(500,'Feed request failed');}
  });
}
