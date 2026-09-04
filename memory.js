const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const toast=$('#memoryToast');
function hint(text){toast.textContent=text;toast.classList.add('show');clearTimeout(window.__memToast);window.__memToast=setTimeout(()=>toast.classList.remove('show'),1300)}

$('#backBtn').onclick=()=>{location.href='index.html'};
$('#tinyHeart').onclick=()=>{const b=$('#tinyHeart');b.classList.remove('pulse');void b.offsetWidth;b.classList.add('pulse');hint('Memory · 前端预览')};

$$('[data-toggle]').forEach(btn=>btn.onclick=()=>{
  const target=document.getElementById(btn.dataset.toggle),open=target.classList.toggle('open');
  btn.setAttribute('aria-expanded',open?'true':'false');
});

const notesToggle=$('#notesToggle');
const notesStack=$('#notesStack');
const reviewBtn=$('#reviewBtn');
let noteSwitching=false;

notesToggle.onclick=()=>{
  const open=notesStack.classList.toggle('spread');
  notesToggle.setAttribute('aria-expanded',open?'true':'false');
};

notesStack.onclick=e=>{
  const note=e.target.closest('.note-paper');
  if(!note||notesStack.classList.contains('spread')||noteSwitching)return;
  noteSwitching=true;
  const a=notesStack.querySelector('.note-a');
  const b=notesStack.querySelector('.note-b');
  const c=notesStack.querySelector('.note-c');
  if(!a||!b||!c){noteSwitching=false;return}

  a.classList.add('note-swap-out');
  window.setTimeout(()=>{
    a.classList.remove('note-a');a.classList.add('note-c');
    b.classList.remove('note-b');b.classList.add('note-a');
    c.classList.remove('note-c');c.classList.add('note-b');
    requestAnimationFrame(()=>{
      a.classList.remove('note-swap-out');
      window.setTimeout(()=>{noteSwitching=false},360);
    });
  },320);
};

reviewBtn.onclick=e=>{
  e.stopPropagation();
  location.href='notes.html';
};

$$('[data-memory] .memory-piece').forEach(btn=>btn.onclick=()=>{
  const entry=btn.closest('[data-memory]'),open=entry.classList.toggle('open');
  btn.setAttribute('aria-expanded',open?'true':'false');
});

$$('.scale-tabs button').forEach(btn=>btn.onclick=()=>{
  $$('.scale-tabs button').forEach(x=>x.classList.remove('active'));
  btn.classList.add('active');
  if(btn.dataset.scale!=='day') hint(`${btn.textContent} · 层级预览`);
});