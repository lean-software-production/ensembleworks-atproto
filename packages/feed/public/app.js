const $ = s => document.querySelector(s);
const node = (tag,text,cls) => {const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;};
const formatTime = s => s ? (Number.isNaN(Date.parse(s)) ? s : new Date(s).toLocaleString()) : 'Time not recorded';
let sessions=[],selected,loading=false,signature='';
function showDetails() {
  const host=$('#detail'); host.replaceChildren();
  const session=sessions.find(s=>s.key===selected);
  if(!session) {host.append(node('h2','Choose a session'),node('p','Select a card to inspect the complete event stream.'));return;}
  host.append(node('p',session.author,'eyebrow'),node('h2',session.title),node('p',session.project||'Project not recorded','project'),node('p',`${session.events.length} events · Session ${session.id}`,'meta'),node('p','Chronological order with source order for ties. Branch, parent and stream fields remain in record metadata.','meta'));
  for(const event of session.events) {
    const article=node('article',undefined,'event');
    article.append(node('h3',event.type),node('p',`${formatTime(event.time)} · line ${event.envelope.sourceLine??'?'} · ${event.envelope.sourcePath||event.stream||'Unknown source'}`,'meta'));
    const native=event.native;
    const content=native?.message?.content??native?.content;
    if(typeof content==='string') article.append(node('pre',content,'message'));
    if(Array.isArray(content)) for(const block of content) {
      if(block?.type==='text') article.append(node('pre',block.text,'message'));
      else {article.append(node('h4',block?.type||'Content block'));article.append(node('pre',JSON.stringify(block,null,2)));}
    }
    const details=node('details'); details.dataset.event=event.uri;
    details.append(node('summary','Complete native event'),node('pre',typeof event.envelope.payloadJson==='string'?event.envelope.payloadJson:JSON.stringify(native,null,2)));
    const metadata=node('details');metadata.dataset.event=`${event.uri}/metadata`;metadata.append(node('summary','Record, ordering & branch metadata'),node('pre',JSON.stringify({uri:event.uri,cid:event.cid,value:event.value},null,2)));
    article.append(details,metadata);host.append(article);
  }
}
function render() {
  const open = new Set([...document.querySelectorAll('details[open]')].map(x=>x.dataset.event));
  const cards=$('#cards');cards.replaceChildren();
  if(!sessions.length) {cards.append(node('h2','No shared sessions yet'),node('p','Events will appear when a member publishes to the company Space.'));}
  for(const session of sessions) {
    const card=node('button',undefined,'card');card.setAttribute('aria-pressed',String(session.key===selected));
    card.append(node('span',session.author,'eyebrow'),node('h2',session.title),node('p',session.project||'Project not recorded','project'),node('p',formatTime(session.startTime),'meta'),node('p',session.prompt||'No text prompt recorded','preview'),node('span',`${session.events.length} events`,'count'));
    card.onclick=()=>{selected=session.key;render();};cards.append(card);
  }
  showDetails();for(const details of document.querySelectorAll('details'))details.open=open.has(details.dataset.event);
}
async function refresh() {
  if(loading)return;loading=true;$('#refresh').disabled=true;$('#status').textContent='Refreshing from company PDS…';
  try {
    const response=await fetch('/api/sessions',{signal:AbortSignal.timeout(35000)});
    if(response.status===401){location.assign('/login');return;}
    const data=await response.json();if(!response.ok)throw new Error(data.error||'PDS connection failed');
    $('#error').hidden=true;
    const nextSignature=JSON.stringify(data.sessions);
    if(signature!==nextSignature){sessions=data.sessions;signature=nextSignature;if(!sessions.some(s=>s.key===selected))selected=sessions[0]?.key;render();}
    $('#status').textContent=`${sessions.length} sessions · ${data.recordCount} events · Updated ${formatTime(data.refreshedAt)}`;
  } catch(error) {$('#error').hidden=false;$('#error').textContent=error.message;$('#status').textContent='Connection error · Showing last successful snapshot · Retrying every 5 seconds';}
  finally {loading=false;$('#refresh').disabled=false;}
}
$('#refresh').onclick=refresh;refresh();setInterval(refresh,5000);
