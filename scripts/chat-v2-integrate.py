from pathlib import Path
import subprocess

EXPECTED = {
    'index.html': '54829298558291c8fe2eaa8eedfe4c8a92edaf9b',
    'chat-special-v2-core.js': '572ac94285f7a404970b906bba87849134508d96',
    'chat-special-v2-music.js': '22bf75b5f1eac7aa15ad408587d6a1b26582fb0c',
    'chat-special-v2-timer.js': '139585959cf8ce924dbbdde387ab624289ceb180',
}
for path, expected in EXPECTED.items():
    actual = subprocess.check_output(['git', 'hash-object', path], text=True).strip()
    if actual != expected:
        raise SystemExit(f'Refusing to overwrite changed file: {path} ({actual})')

def change(path, old, new):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    if s.count(old) != 1:
        raise SystemExit(f'Expected exactly one match in {path}: {old[:100]}')
    p.write_text(s.replace(old, new, 1), encoding='utf-8')

def section(path, start, end, new):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    if s.count(start) != 1 or s.count(end) != 1:
        raise SystemExit(f'Unexpected source boundaries in {path}: {start}')
    a = s.index(start)
    b = s.index(end, a + len(start))
    p.write_text(s[:a] + new.rstrip() + '\n' + s[b:], encoding='utf-8')

change('index.html',
       '<link rel="stylesheet" href="styles/chat-rich.css?v=20260907-3"/>',
       '<link rel="stylesheet" href="styles/chat-rich.css?v=20260907-3"/>\n<link rel="stylesheet" href="styles/chat-special-v2.css?v=20260909-1"/>')
change('index.html',
       '<script src="chat-rich.js?v=20260907-3"></script>',
       '<script src="chat-special-v2-core.js?v=20260909-1"></script>\n<script src="chat-special-v2-music.js?v=20260909-1"></script>\n<script src="chat-special-v2-timer.js?v=20260909-1"></script>\n<script src="chat-special-v2-boot.js?v=20260909-1"></script>')

change('chat-special-v2-core.js',
       "adapter=next;C.services.adapter=next;return true",
       "adapter=next;C.services.adapter=next;C.demo=false;window.dispatchEvent(new Event('chaosheng:adapter'));return true")
change('chat-special-v2-core.js',
       "function sourceStatus(error){return error?.message||'操作失败，请稍后重试'}",
       "function sourceStatus(error){return text(error?.userMessage||error?.message,300).replace(/((?:api[_-]?key|access[_-]?token|authorization|password|secret)\\s*[:=]\\s*)[^\\s,;]+/ig,'$1[已隐藏]')||'操作失败，请稍后重试'}")
change('chat-special-v2-core.js',
       "terminalForm.onsubmit=e=>{e.preventDefault();sendTerminal()};async function closeTerminal()",
       "terminalForm.onsubmit=e=>{e.preventDefault();sendTerminal()};terminalStatus('未连接');async function closeTerminal()")
change('chat-special-v2-core.js',
       "const items=Array.isArray(result)?result:Array.isArray(result?.messages)?result.messages:result?.message?[result.message]:[]",
       "const items=Array.isArray(result)?result:Array.isArray(result?.messages)?result.messages:result?.message?[result.message]:result?.content?[result]:[]") if False else None

# The source-backed tool log sheet is available from the existing tiny sheep.
change('chat-special-v2-core.js',
       "C.openWeb=openWeb;",
       "C.openWeb=openWeb;\nlet toolLogSheet=null;async function openToolLog(id){if(!toolLogSheet)toolLogSheet=createSheet('cs2ToolLog','工具记录');const body=toolLogSheet.body;body.replaceChildren(element('p','cs2-sheet-note','正在读取…'));openSheet(toolLogSheet.dialog);try{const result=await call('getToolLog',{id});body.replaceChildren();if(!result||typeof result!=='object')throw Error('没有找到这条记录');const fields=[['工具',result.name||result.tool],['时间',result.timestamp],['状态',result.status],['耗时',result.durationMs!=null?result.durationMs+' ms':''],['错误',result.error?.message||result.error]];for(const[label,value]of fields){if(value===undefined||value===null||value==='')continue;const row=element('div','cs2-row');row.style.marginBottom='9px';row.append(element('span','cs2-sub',label),element('span','cs2-grow',text(String(value),1000)));body.append(row)}const detail=element('details');detail.append(element('summary','cs2-sub','详细记录'));const pre=element('pre','cs2-terminal-log');pre.textContent=JSON.stringify(result,null,2).replace(/\\\"(?:apiKey|accessToken|authorization|password|secret|token)\\\"\\s*:\\s*\\\"[^\\\"]*\\\"/ig,'\"[已隐藏]\": \"[已隐藏]\"');detail.append(pre);body.append(detail)}catch(err){body.replaceChildren(element('p','cs2-sheet-note',sourceStatus(err)))}}C.openToolLog=openToolLog;")

change('chat-special-v2-music.js', "audio.crossOrigin='anonymous';", "")
change('chat-special-v2-music.js',
       "let active=null,loading=false,error='',generation=0,lyricLines=[],lyricsFor=null,lyricsMode=false,sourceUrl=null;",
       "let active=null,loading=false,error='',generation=0,lyricLines=[],lyricsFor=null,lyricsMode=false,sourceUrl=null,mediaSessionKey=null,renderedLyricsKey='',renderedActive=-2;")
change('chat-special-v2-music.js',
       "function pause(){audio.pause();loading=false;renderAll()}",
       "function pause(){generation++;audio.pause();loading=false;renderAll()}")
section('chat-special-v2-music.js', 'function setMediaSession(){', 'function parseLyrics(', '''function setMediaSession(){
 if(!('mediaSession'in navigator))return;const t=current();if(!t)return;
 try{if(mediaSessionKey!==t.key){mediaSessionKey=t.key;navigator.mediaSession.metadata=new MediaMetadata({title:t.title,artist:t.artist,album:'潮生',artwork:t.cover?[{src:t.cover}]:[]});navigator.mediaSession.setActionHandler('play',()=>play(current()));navigator.mediaSession.setActionHandler('pause',pause);navigator.mediaSession.setActionHandler('seekto',e=>seek(e.seekTime));navigator.mediaSession.setActionHandler('previoustrack',()=>next(-1));navigator.mediaSession.setActionHandler('nexttrack',()=>next(1))}navigator.mediaSession.playbackState=audio.paused?'paused':'playing'}catch{}
}
''')
change('chat-special-v2-music.js',
       "const lyrics=el('div','cs2-lyrics'),empty=el('div','cs2-lyrics-empty','暂无歌词'),source=el('div','cs2-sheet-note');source.style.textAlign='center';source.style.paddingBottom='8px';",
       "const lyrics=el('div','cs2-lyrics'),empty=el('div','cs2-lyrics-empty','暂无歌词'),source=el('div','cs2-sheet-note'),sourceLabel=el('span');source.style.textAlign='center';source.style.paddingBottom='8px';source.append(sourceLabel);")
change('chat-special-v2-music.js',
       "source.firstChild.textContent=t?.source||'';",
       "sourceLabel.textContent=t?.source||'';")
change('chat-special-v2-music.js',
       "cover.src=t?.cover||'';cover.hidden=!t?.cover;",
       "if(t?.cover)cover.src=t.cover;else cover.removeAttribute('src');cover.hidden=!t?.cover;")
section('chat-special-v2-music.js', 'function renderLyrics(){', 'function setPlayIcon(', '''function renderLyrics(){
 const t=current(),key=(t?.key||'')+':'+lyricLines.length+':'+(lyricLines[0]?.text||'');
 if(key!==renderedLyricsKey){renderedLyricsKey=key;renderedActive=-2;lyrics.replaceChildren();if(!t||!lyricLines.length){lyrics.append(empty.cloneNode(true));return}for(const line of lyricLines)lyrics.append(el('p','',line.text||'　'))}
 if(!t||!lyricLines.length)return;
 let activeIndex=-1;const position=audio.currentTime||0;lyricLines.forEach((l,i)=>{if(l.time!==null&&l.time<=position)activeIndex=i});
 if(activeIndex===renderedActive)return;renderedActive=activeIndex;
 [...lyrics.children].forEach((p,i)=>p.classList.toggle('active',i===activeIndex));
 if(lyricsMode&&activeIndex>=0){const node=lyrics.children[activeIndex];if(node){const top=node.offsetTop-lyrics.offsetTop-lyrics.clientHeight/2+node.clientHeight/2;lyrics.scrollTo({top:Math.max(0,top),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'})}}
}
''')
change('chat-special-v2-music.js',
       "if(active!==t.key){active=t.key;audio.pause();audio.removeAttribute('src');audio.load();lyricsFor=null;lyricLines=[]}",
       "if(active!==t.key){generation++;active=t.key;audio.pause();audio.removeAttribute('src');audio.load();loading=false;error='';lyricsFor=null;lyricLines=[];renderedLyricsKey=''}")
change('chat-special-v2-music.js',
       "lyricsFor=null;lyricLines=[];loadLyrics(resolved)",
       "lyricsFor=null;lyricLines=[];renderedLyricsKey='';loadLyrics(resolved)")
change('chat-special-v2-music.js',
       "if(lyricLines.length||typeof C.services.adapter?.resolveLyrics!=='function')return;",
       "if(lyricLines.length||typeof C.services.adapter?.resolveLyrics!=='function')return;") if False else None

# Preserve stable records when a timer event contains only a partial update.
section('chat-special-v2-timer.js', 'function upsert(value){', 'function localTransition(', '''function upsert(value){
 if(!value||typeof value!=='object')return null;const key=text(value.id||value.taskId,160);const old=key?tasks.get(key):null;
 const incoming={...old,...value};if(old&&!Number.isFinite(value.revision))incoming.revision=old.revision;
 const t=normalize(incoming);if(!t)return null;if(old&&t.revision<old.revision)return old;
 tasks.set(t.id,t);if(t.id.startsWith('local-'))save();if(selected===t.id||!selected&&['running','paused'].includes(t.status))selected=t.id;paint();return t
}
''')
section('chat-special-v2-timer.js', 'async function transition(taskId,action){', 'function createLocal(', '''async function transition(taskId,action){
 const t=tasks.get(taskId);if(!t||busy.has(taskId))return false;busy.add(taskId);paint();
 try{if(t.id.startsWith('local-'))localTransition(t,action);else{const result=await call('updateTimer',{id:t.id,action,revision:t.revision});if(!result||typeof result!=='object')throw Error('没有收到定时任务状态');upsert(result)}return true}catch(err){notify(sourceStatus(err));return false}finally{busy.delete(taskId);paint()}
}
''')
change('chat-special-v2-timer.js',
       "const panelStatus=el('div','cs2-sub'),panelActions=el('div','cs2-actions');const panelHint=",
       "const panelStatus=el('div','cs2-sub'),panelActions=el('div','cs2-actions'),panelPause=btn('暂停',()=>{const t=activeTask();if(t)transition(t.id,t.status==='paused'?'resume':'pause')},'cs2-soft'),panelFinish=btn('完成',()=>{const t=activeTask();if(t)transition(t.id,'done')},'cs2-soft alt'),panelEnd=btn('结束',()=>{const t=activeTask();if(t)transition(t.id,'cancel')},'cs2-plain');panelActions.append(panelPause,panelFinish,panelEnd);const panelHint=")
change('chat-special-v2-timer.js',
       "panel.style.maxHeight=Math.max(130,bounds(0).available)+'px';",
       "panel.style.maxHeight=Math.max(0,bounds(0).available)+'px';")
section('chat-special-v2-timer.js', 'function paint(){', 'function updateCard(', '''function paint(){
 const t=activeTask();if(!t){dock.hidden=true;return}selected=t.id;dock.hidden=false;const remain=remaining(t),overtime=t.status==='running'&&remain<0;
 dock.classList.toggle('cs2-overtime',overtime);tabTitle.textContent=t.title;tabTime.textContent=timeText(t);panelTitle.textContent=t.title;panelTime.textContent=timeText(t);panelStatus.textContent=statusText(t);
 panelFill.style.width=clamp(1-Math.max(0,remain)/t.durationMs,0,1)*100+'%';panelPause.textContent=t.status==='paused'?'继续':'暂停';for(const b of [panelPause,panelFinish,panelEnd])b.disabled=busy.has(t.id);
 panel.hidden=!expanded;tab.hidden=expanded;if(!drag?.armed)place();document.querySelectorAll('.cs2-timer[data-timer-id]').forEach(updateCard)
}
''')
change('chat-special-v2-timer.js',
       "transition(t.id,action).then(()=>{if(action==='start'||action==='resume')selectTimer(t.id,true)})",
       "transition(t.id,action).then(ok=>{if(ok&&(action==='start'||action==='resume'))selectTimer(t.id,true)})")
change('chat-special-v2-timer.js',
       "cancelHold();drag=null}return}e.preventDefault();place(drag.baseY+e.clientY-drag.startY)",
       "cancelHold();drag=null;suppressClick=true;setTimeout(()=>suppressClick=false,0)}return}e.preventDefault();place(drag.baseY+e.clientY-drag.startY)")
change('chat-special-v2-timer.js',
       "panel.style.maxHeight=Math.max(130,bounds(0).available)+'px';place()",
       "panel.style.maxHeight=Math.max(0,bounds(0).available)+'px';place()")
change('chat-special-v2-timer.js',
       "if(typeof C.services.adapter?.subscribeTimers==='function')unsubscribe=C.services.adapter.subscribeTimers(upsert)||null;",
       "if(typeof C.services.adapter?.subscribeTimers==='function'){const stop=C.services.adapter.subscribeTimers(upsert);unsubscribe=typeof stop==='function'?stop:null}")
change('chat-special-v2-timer.js',
       "function reminderCard(part){const root=el('div','cs2 cs2-attachment')",
       "function reminderCard(part){part={...part,id:text(part.id,160)||id()};const root=el('div','cs2 cs2-attachment')")
change('chat-special-v2-timer.js',
       "register('reminder',reminderCard);if(reminder){pinText.textContent=reminder.text;pin.hidden=false}",
       "register('reminder',reminderCard);if(reminder){pinText.textContent=reminder.text;pin.hidden=false}paint()")

change('chat-special-v2-boot.js',
       "result?.message?[result.message]:[]",
       "result?.message?[result.message]:result?.content?[result]:[]")

with Path('styles/chat-special-v2.css').open('a', encoding='utf-8') as f:
    f.write('\n.cs2-lyrics{max-height:min(40dvh,340px);overscroll-behavior:contain}.cs2-player-lyrics-mode .cs2-lyrics{max-height:min(48dvh,420px)}.cs2-dock-panel{overscroll-behavior:contain}\n')

# No other page, route, or legacy implementation is changed.
index=Path('index.html').read_text(encoding='utf-8')
assert index.count('chat-special-v2-core.js')==1
assert index.count('chat-rich.js?v=20260907-3')==0
assert index.count('data-route="mind"')==1
assert index.count('data-route="cron"')==1
assert index.count('id="messages"')==1
assert index.count('id="todoSheetLayer"')==1
print('PASS: guarded Chat v2 integration; existing Chat shell, Cron, Mind and other pages preserved.')
