#!/usr/bin/env python3
"""Apply the September 9 Chat feedback without rewriting unrelated pages."""
from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'index.html': 'face88701452a404c5695546baff61f76b6d4800',
    'chat-special-v2-core.js': '7c03c983b49645221c63725907d72fd96002ebe2',
    'chat-special-v2-timer.js': 'cf4461241c096847b7267242f85faf2d741f504c',
    'chat-special-v2-music.js': '54965f113bf05e0bbb8b5436de120dd09805c5ad',
}

def blob_sha(text):
    data = text.encode('utf-8')
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def read(name):
    s = (ROOT/name).read_text()
    assert blob_sha(s) == EXPECTED[name], f'Unexpected source: {name}'
    return s

def replace_once(s, old, new):
    assert s.count(old) == 1, f'Expected one occurrence: {old[:90]}'
    return s.replace(old, new, 1)

def replace_between(s, start, end, new):
    assert s.count(start) == 1 and s.count(end) == 1, (start,end)
    a=s.index(start); b=s.index(end,a)
    return s[:a]+new+'\n'+s[b:]

core=read('chat-special-v2-core.js')
# Take the existing message shell from the original page. Do not invent new
# metadata, avatar, sheep, or user bubble markup in the attachment renderer.
core=replace_once(core,"const C={version:2,services:{},demo:false};", "const C={version:2,services:{},demo:false};\nconst originalSheng=document.querySelector('#messages .msg.sheng')?.cloneNode(true);\nconst originalMe=document.querySelector('#messages .msg.me')?.cloneNode(true);")
core=replace_between(core,'function renderShell(message){','function renderBlock(part){', '''function renderShell(message){
 const template=message.role==='me'?originalMe:originalSheng;
 const article=template?template.cloneNode(true):element('article','msg '+message.role);
 article.classList.add('cs2-msg');article.dataset.messageId=message.id;
 const body=article.querySelector(message.role==='me'?'.user-bubble':'.assistant-text')||element('div',message.role==='me'?'user-bubble':'assistant-text');
 body.replaceChildren();
 if(message.role==='sheng'){
  const meta=article.querySelector('.assistant-meta');
  const time=meta?.querySelector('.time');const d=new Date(message.timestamp);
  if(time)time.textContent=Number.isFinite(d.getTime())?`${d.getMonth()+1}/${d.getDate()} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}:${String(d.getSeconds()).padStart(2,'0')}`:'';
  const sheep=meta?.querySelector('.sheep');const details=article.querySelector('.details');
  const card=details?.querySelector('.card');
  if(card){card.replaceChildren();const makeLine=(label,content)=>{const row=element('div','line');row.append(element('div','label',label),element('div','detail',content));return row};
   if(message.thoughtSummary)card.append(makeLine('Thinking',message.thoughtSummary));
   if(message.toolCalls.length){for(const item of message.toolCalls){const row=makeLine('Tool',text(item.name||item.tool,100)+' · '+text(item.status||'',60));if(item.id)row.append(button('查看记录',()=>C.openToolLog?.(item.id),'cs2-plain'));card.append(row)}}else card.append(makeLine('Tool','未调用工具'));
  }
  if(sheep&&details){sheep.setAttribute('aria-label','查看本次思路与工具');sheep.setAttribute('aria-expanded','false');sheep.onclick=()=>{const open=details.classList.toggle('open');sheep.setAttribute('aria-expanded',String(open))}}
 }
 if(!body.parentNode)article.append(body);
 return{article,body};
}''')
# A failed thumbnail must never expose the browser's broken-image glyph.
core=replace_once(core,"const paths={", "const paths={")
core=replace_once(core,'function markdown(value,target){', '''function safeImage(url,cls,alt='',fallback='image'){
 const holder=element('div',cls+' cs2-image-holder');
 const placeholder=element('div','cs2-image-placeholder');placeholder.append(icon(fallback));holder.append(placeholder);
 const u=validUrl(url);if(!u)return holder;
 const img=element('img');img.alt=alt;img.loading='lazy';img.decoding='async';
 img.addEventListener('load',()=>{placeholder.hidden=true;img.hidden=false});
 img.addEventListener('error',()=>{img.hidden=true;placeholder.hidden=false});
 img.hidden=true;img.src=u;holder.append(img);return holder;
}
function markdown(value,target){''')
core=replace_once(core,"C.sourceStatus=sourceStatus;C.records=records;", "C.sourceStatus=sourceStatus;C.records=records;C.safeImage=safeImage;")
core=replace_between(core,'function webCard(part){',"register('web',webCard);",'''function webCard(part){const u=validUrl(part.url);if(!u)return element('div','cs2-attachment cs2-sub','网址无效');const root=element('div','cs2 cs2-attachment'),open=button('',()=>C.openWeb(u),'cs2-web-open');
 if(validUrl(part.image))open.append(safeImage(part.image,'cs2-web-cover','', 'globe'));
 const row=element('div','cs2-row'),ico=element('div','cs2-icon');ico.append(icon('globe'));const copy=element('div','cs2-grow');copy.append(element('div','cs2-title',text(part.title,200)||new URL(u).hostname),element('div','cs2-sub',text(part.description,400)||new URL(u).hostname));row.append(ico,copy,icon('chevron'));open.append(row);root.append(open);return root}
''')
core=replace_once(core,"register('web',webCard);", "register('web',webCard);")
core=replace_between(core,'function imageCard(part){',"register('image',imageCard);",'''function imageCard(part){const u=validUrl(part.url);if(!u)return null;const root=element('div','cs2 cs2-attachment');const open=button('',()=>{const sheet=createSheet('cs2Image-'+Math.random().toString(36).slice(2),'图片');const big=safeImage(u,'cs2-image-large',text(part.title,200));sheet.body.append(big);sheet.dialog.addEventListener('close',()=>sheet.dialog.remove(),{once:true});openSheet(sheet.dialog)},'cs2-web-open');open.append(safeImage(u,'cs2-image-preview',text(part.title,200)));root.append(open);if(part.title)root.append(element('div','cs2-sub',text(part.title,200)));return root}
''')
# Note: preserve the registration and all terminal/HTML functions.
(ROOT/'chat-special-v2-core.js').write_text(core)

music=read('chat-special-v2-music.js')
music=replace_once(music,"duration:307,cover:''", "duration:307,cover:'assets/chat-moonlight.svg'")
music=replace_once(music,"const art=el('div','cs2-player-art'),disc=el('div','cs2-player-disc'),cover=el('img','cs2-cover-img');cover.alt='';const hole=el('i','cs2-disc-hole');art.append(disc,cover,hole);", "const art=el('div','cs2-player-art'),disc=el('div','cs2-player-disc'),cover=el('img','cs2-cover-img');cover.alt='';cover.addEventListener('error',()=>{cover.hidden=true});const hole=el('i','cs2-disc-hole');art.append(disc,cover,hole);")
music=replace_once(music,"if(t?.cover)cover.src=t.cover;else cover.removeAttribute('src');cover.hidden=!t?.cover;", "if(t?.cover){if(cover.getAttribute('src')!==t.cover){cover.hidden=false;cover.src=t.cover}}else cover.removeAttribute('src');cover.hidden=!t?.cover||Boolean(cover.getAttribute('src')&&cover.complete&&cover.naturalWidth===0);")
music=replace_once(music,"const row=el('div','cs2-song-main'),coverEl=t.cover?el('img','cs2-cover'):el('div','cs2-cover fallback');if(t.cover){coverEl.src=t.cover;coverEl.alt='';coverEl.loading='lazy'}else coverEl.append(icon('music'));", "const row=el('div','cs2-song-main'),coverEl=C.safeImage(t.cover,'cs2-cover','', 'music');")
(ROOT/'chat-special-v2-music.js').write_text(music)

timer=read('chat-special-v2-timer.js')
timer=replace_once(timer,"POS='chaosheng-countdown-left-position-v2'", "POS='chaosheng-countdown-right-position-v3'")
timer=replace_once(timer,"['idle','running','paused','done','cancelled']", "['idle','running','paused','elapsed','done','cancelled']")
timer=replace_once(timer,"if(status==='running'&&!dueAt)status='idle';", "if(status==='running'&&!dueAt)status='idle';if(status==='running'&&key.startsWith('local-')&&dueAt<=Date.now())status='elapsed';")
timer=replace_once(timer,"remainingMs:Number.isFinite(value.remainingMs)?clamp(value.remainingMs,0,durationMs):durationMs", "remainingMs:status==='elapsed'?0:Number.isFinite(value.remainingMs)?clamp(value.remainingMs,0,durationMs):durationMs")
timer=replace_between(timer,'function remaining(t,now=Date.now()){','function upsert(value){', '''function remaining(t,now=Date.now()){if(t.status==='elapsed')return 0;if(t.status==='running')return Math.max(0,t.dueAt-now);return Math.max(0,t.remainingMs)}
function effectiveStatus(t,now=Date.now()){return t.status==='running'&&t.dueAt<=now?'elapsed':t.status}
function timeText(t){if(t.status==='done')return '已完成';if(t.status==='cancelled')return '已取消';return fmt(Math.ceil(remaining(t)/1000))}
function statusText(t){const s=effectiveStatus(t);if(s==='idle')return '还没有开始';if(s==='paused')return '已暂停';if(s==='elapsed')return '时间到了';if(s==='done')return '已完成';if(s==='cancelled')return '已取消';return '正在倒计时'}
function expireLocal(now=Date.now()){
 let changed=false;
 for(const [key,t] of tasks){if(key.startsWith('local-')&&t.status==='running'&&t.dueAt<=now){const next={...t,status:'elapsed',remainingMs:0,dueAt:null,revision:t.revision+1};tasks.set(key,next);changed=true;window.dispatchEvent(new CustomEvent('chaosheng:timer-elapsed',{detail:{id:key,title:t.title}}))}}
 if(changed)save();return changed;
}
''')
timer=replace_once(timer,"if(action==='start'||action==='restart'){", "if(action==='start'||action==='restart'){")
timer=replace_once(timer,"else if(action==='pause'&&t.status==='running'){", "else if(action==='pause'&&effectiveStatus(t,now)==='running'){")
timer=replace_once(timer,"else if(action==='resume'&&t.status==='paused'){", "else if(action==='resume'&&t.status==='paused'&&t.remainingMs>0){")
timer=replace_once(timer,"else if(action==='done'){", "else if(action==='expire'&&effectiveStatus(t,now)==='elapsed'){next.status='elapsed';next.remainingMs=0;next.dueAt=null}else if(action==='done'){")
timer=replace_once(timer,"if(!t||busy.has(taskId))return false;busy.add(taskId);", "if(!t||busy.has(taskId))return false;if(action==='pause'&&effectiveStatus(t)!=='running')return false;if(action==='resume'&&(t.status!=='paused'||t.remainingMs<=0))return false;busy.add(taskId);")
timer=replace_once(timer,"if(t&&!['done','cancelled','idle'].includes(t.status))return t;return[...tasks.values()].find(t=>['running','paused'].includes(t.status))||null", "if(t&&!['done','cancelled','idle'].includes(t.status))return t;return[...tasks.values()].find(t=>['running','paused','elapsed'].includes(t.status))||null")
timer=replace_once(timer,"const panelHint=el('div','cs2-dock-hint','长按左侧小标签，可上下移动');", "const panelHint=el('div','cs2-dock-hint','长按右侧小标签，可上下移动');")
timer=replace_once(timer,"// Dock coordinates are always relative to the application's left edge.", "// Dock coordinates are always relative to the application's right edge.")
timer=replace_once(timer,"return{left:Math.max(0,app.left),min,max:Math.max(min,bottom-height),available:Math.max(0,bottom-min)}", "return{right:Math.max(0,innerWidth-app.right),min,max:Math.max(min,bottom-height),available:Math.max(0,bottom-min)}")
timer=replace_once(timer,"dock.style.left=b.left+'px';dock.style.top=top+'px';dock.style.right='auto';", "dock.style.right=b.right+'px';dock.style.top=top+'px';dock.style.left='auto';")
timer=replace_once(timer,"const t=activeTask();if(!t){dock.hidden=true;return}selected=t.id;dock.hidden=false;const remain=remaining(t),overtime=t.status==='running'&&remain<0;", "expireLocal();const t=activeTask();if(!t){dock.hidden=true;return}selected=t.id;dock.hidden=false;const remain=remaining(t),overtime=effectiveStatus(t)==='elapsed';")
timer=replace_once(timer,"panelPause.textContent=t.status==='paused'?'继续':'暂停';for(const b of [panelPause,panelFinish,panelEnd])b.disabled=busy.has(t.id);", "panelPause.textContent=t.status==='paused'?'继续':'暂停';panelPause.disabled=busy.has(t.id)||effectiveStatus(t)==='elapsed';for(const b of [panelFinish,panelEnd])b.disabled=busy.has(t.id);")
timer=replace_once(timer,"t.status==='running'&&remaining(t)<0", "effectiveStatus(t)==='elapsed'")
timer=replace_once(timer,"const action=t.status==='idle'||['done','cancelled'].includes(t.status)?'start':t.status==='paused'?'resume':'pause';", "const action=['idle','elapsed','done','cancelled'].includes(effectiveStatus(t))?'start':t.status==='paused'?'resume':'pause';")
timer=replace_once(timer,"main.textContent=action==='start'?'开始':action==='resume'?'继续':'暂停';", "main.textContent=action==='start'?(t.status==='idle'?'开始':'重新开始'):action==='resume'?'继续':'暂停';")
timer=replace_once(timer,"main.disabled=busy.has(t.id)", "main.disabled=busy.has(t.id)")
timer=replace_once(timer,"btn('收起到左侧',", "btn('收起到右侧',")
timer=replace_once(timer,"const ticker=setInterval(()=>{if(!document.hidden)paint()},500);document.addEventListener('visibilitychange',()=>{if(!document.hidden)paint()});", "const ticker=setInterval(()=>{expireLocal();if(!document.hidden)paint()},500);document.addEventListener('visibilitychange',()=>{expireLocal();if(!document.hidden)paint()});")
timer=replace_once(timer,"remaining,bounds,clamp,get:", "remaining,effectiveStatus,expireLocal,bounds,clamp,get:")
(ROOT/'chat-special-v2-timer.js').write_text(timer)

index=read('index.html')
index=replace_once(index,'styles/chat-special-v2.css?v=20260909-1', 'styles/chat-special-v2.css?v=20260909-1')
index=replace_once(index,'<link rel="stylesheet" href="styles/cron-sheet.css?v=20260907-2"/>', '<link rel="stylesheet" href="styles/chat-special-feedback.css?v=20260909-3"/>\n<link rel="stylesheet" href="styles/cron-sheet.css?v=20260907-2"/>')
for name in ['core','music','timer']:
    index=replace_once(index,f'chat-special-v2-{name}.js?v=20260909-1',f'chat-special-v2-{name}.js?v=20260909-3')
index=replace_once(index,'<script src="chat-special-v2-boot.js?v=20260909-1"></script>', '<script src="chat-special-v2-boot.js?v=20260909-1"></script>')
(ROOT/'index.html').write_text(index)
print('Guarded patch applied to core, music, timer and index. All other files preserved.')
