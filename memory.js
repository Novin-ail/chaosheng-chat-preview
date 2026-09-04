const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const toast=$('#memoryToast');
function hint(text){toast.textContent=text;toast.classList.add('show');clearTimeout(window.__memToast);window.__memToast=setTimeout(()=>toast.classList.remove('show'),1300)}

$('#backBtn').onclick=()=>{location.href='index.html'};
$('#tinyHeart').onclick=()=>{const b=$('#tinyHeart');b.classList.remove('pulse');void b.offsetWidth;b.classList.add('pulse');hint('Memory · 前端预览')};

$$('[data-toggle]').forEach(btn=>btn.onclick=()=>{
  const target=document.getElementById(btn.dataset.toggle),open=target.classList.toggle('open');
  btn.setAttribute('aria-expanded',open?'true':'false');
});

$('#notesToggle').onclick=()=>{
  const stack=$('#notesStack'),open=stack.classList.toggle('spread');
  $('#notesToggle').setAttribute('aria-expanded',open?'true':'false');
};
$('#reviewBtn').onclick=()=>{
  const stack=$('#notesStack');
  stack.classList.add('spread');
  $('#notesToggle').setAttribute('aria-expanded','true');
  stack.scrollIntoView({behavior:'smooth',block:'center'});
};
$$('.note-paper').forEach(note=>note.onclick=()=>hint('小记编辑 · 下一步再接 ouo'));

$$('[data-memory] .memory-piece').forEach(btn=>btn.onclick=()=>{
  const entry=btn.closest('[data-memory]'),open=entry.classList.toggle('open');
  btn.setAttribute('aria-expanded',open?'true':'false');
});

$$('.scale-tabs button').forEach(btn=>btn.onclick=()=>{
  $$('.scale-tabs button').forEach(x=>x.classList.remove('active'));
  btn.classList.add('active');
  if(btn.dataset.scale!=='day') hint(`${btn.textContent} · 层级预览`);
});