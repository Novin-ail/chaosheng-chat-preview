(()=>{
'use strict';
const C=window.ChaoshengChatV2;if(!C)throw Error('Chat core is required');const $=s=>document.querySelector(s),messages=$('#messages'),input=$('#input');
const uid=()=> 'local-'+Date.now()+'-'+Math.random().toString(36).slice(2,8);
function shareSong(track,role='me',caption=''){const t=C.services.media.remember(track);if(!t)return null;return C.appendMessage({id:uid(),role,content:[...(caption?[{type:'text',text:caption}]:[]),{type:'song',track:t}]})}
C.shareSong=shareSong;
async function sendRich(){const value=input.value.trim();if(!value)return;const content=/^https?:\/\//i.test(value)&&C.validUrl(value)?[{type:'web',url:value}]:[{type:'text',text:value}];const message={id:uid(),role:'me',timestamp:new Date().toISOString(),content};C.appendMessage(message);input.value='';if(typeof resizeInput==='function')resizeInput();window.__playSendMorph?.();if(typeof C.services.adapter?.sendMessage==='function'){try{const result=await C.call('sendMessage',message);const items=Array.isArray(result)?result:Array.isArray(result?.messages)?result.messages:result?.message?[result.message]:result?.content?[result]:[];for(const item of items)C.appendMessage(item)}catch(err){C.notify(C.sourceStatus(err))}}}
$('#send').onclick=sendRich;input.onkeydown=e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();sendRich()}};
function demo(){C.demo=true;const marker=document.createElement('p');marker.className='cs2-preview-badge';marker.textContent='消息组件预览';messages.append(marker);const first=marker;
C.appendMessage({id:'demo-song',role:'sheng',timestamp:'2026-09-09T12:00:00+09:00',content:[{type:'text',text:'这首曲子想和你一起听。'},{type:'song',track:C.demoTrack}]});
C.appendMessage({id:'demo-timer',role:'sheng',content:[{type:'text',text:'给你两分钟，先休息一下。'},{type:'timer',...(C.services.timers.get('local-demo-timer')||{id:'local-demo-timer',title:'休息一下',durationMs:120000,status:'idle'})}]});
C.appendMessage({id:'demo-terminal',role:'sheng',content:[{type:'text',text:'这个小地方可以自己改，我把终端留给你。'},{type:'terminal',title:'小改一下',description:'临时工作会话',diff:'border-radius: 30px;\n→ border-radius: 12px;'}]});
C.appendMessage({id:'demo-web',role:'sheng',content:[{type:'text',text:'这篇可以打开看看。'},{type:'web',url:'https://example.com/',title:'Example Domain',description:'一个简单的网页示例'}]});
C.appendMessage({id:'demo-reminder',role:'sheng',content:[{type:'reminder',id:'local-demo-reminder',text:'忙完记得休息一下。'}]});
C.appendMessage({id:'demo-code',role:'sheng',content:[{type:'text',text:'小纸条也可以直接放在聊天里。'},{type:'html',title:'一张小纸条',description:'HTML / CSS',html:'<div class="note">今天也一起慢慢来 ♡</div>',css:'.note{padding:24px;color:#906f79;background:#f4e5e9;border-radius:18px 6px 18px 18px;}'}]});
C.appendMessage({id:'demo-markdown',role:'sheng',content:[{type:'text',text:'**今天的小便签**\n\n> 慢慢来，我陪你。\n\n- [x] 把喜欢的歌分享给你\n- [ ] 一起听完'}]});
requestAnimationFrame(()=>messages.scrollTo({top:Math.max(0,first.offsetTop-messages.offsetTop-14),behavior:'instant'}))}
function importShare(){try{const raw=sessionStorage.getItem('chaosheng-song-share-preview');if(!raw)return false;sessionStorage.removeItem('chaosheng-song-share-preview');const s=JSON.parse(raw);if(!s||typeof s!=='object')return false;const track=s.track||s;const id=String(track.id||track.songId||('legacy:'+String(track.title||''))).slice(0,160);if(!track.title||!id)return false;shareSong({...track,id,provider:track.provider||'legacy'},'me');return true}catch{return false}}
const bootstrap=window.ChaoshengChatBootstrap;if(bootstrap&&typeof bootstrap==='object'&&bootstrap.adapter){C.configure(bootstrap.adapter);C.demo=false;if(Array.isArray(bootstrap.messages))C.replaceMessages(bootstrap.messages);else if(typeof bootstrap.loadMessages==='function')Promise.resolve(bootstrap.loadMessages()).then(C.replaceMessages).catch(err=>C.notify(C.sourceStatus(err)))}else demo();importShare();
Object.assign(window.ChatSpecialPreview,{appendMessage:C.appendMessage,renderMessage:C.appendMessage,replaceMessages:C.replaceMessages,configure:C.configure,openPlayer:C.openPlayer,openTerminal:C.openTerminal,openWeb:C.openWeb,shareSong,createTimer:C.services.timers.createTimer,updateTimer:C.services.timers.upsert});
})();
