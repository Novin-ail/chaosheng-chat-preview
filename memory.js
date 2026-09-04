const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const toast=$('#memoryToast');
function hint(text){toast.textContent=text;toast.classList.add('show');clearTimeout(window.__memToast);window.__memToast=setTimeout(()=>toast.classList.remove('show'),1300)}

$('#backBtn').onclick=()=>{location.href='index.html'};
$('#tinyHeart').onclick=()=>{const b=$('#tinyHeart');b.classList.remove('pulse');void b.offsetWidth;b.classList.add('pulse');hint('Memory · home')};

$('#coreEntry').onclick=()=>{location.href='core.html'};
$('#timelineEntry').onclick=()=>{location.href='timeline.html'};
$('#reviewBtn').onclick=e=>{e.stopPropagation();location.href='notes.html'};

$('#notesToggle').onclick=()=>{
  const stack=$('#notesStack'),open=stack.classList.toggle('spread');
  $('#notesToggle').setAttribute('aria-expanded',open?'true':'false');
};

$$('.note-paper').forEach(note=>note.onclick=e=>{
  e.stopPropagation();
  location.href='notes.html';
});