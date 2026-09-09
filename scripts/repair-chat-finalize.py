from pathlib import Path

def change(path,old,new):
    p=Path(path);s=p.read_text();assert s.count(old)==1,(path,old);p.write_text(s.replace(old,new,1))

# Keep image elements in layout while the request is pending. A display:none
# lazy image never begins loading, so waiting for its load event deadlocks.
change('chat-special-v2-core.js',"img.addEventListener('load',()=>{placeholder.hidden=true;img.hidden=false});", "img.addEventListener('load',()=>{placeholder.hidden=true;img.hidden=false;img.style.visibility='visible'});")
change('chat-special-v2-core.js',"img.hidden=true;img.src=u;holder.append(img);return holder;", "img.style.visibility='hidden';img.src=u;holder.append(img);return holder;")
change('styles/chat-special-feedback.css','left:auto!important;right:0!important;bottom:auto!important;','left:auto!important;right:0;bottom:auto!important;')
# The product uses the device timezone; the CI runner happens to use UTC.
p=Path('tests/chat-feedback.spec.cjs');s=p.read_text()
s=s.replace("await expect(m.locator('.assistant-meta .time')).toContainText('12:34:56');", "const expectedTime=await page.evaluate(()=>{const d=new Date('2026-09-09T12:34:56+08:00');return [d.getHours(),d.getMinutes(),d.getSeconds()].map(x=>String(x).padStart(2,'0')).join(':')});await expect(m.locator('.assistant-meta .time')).toContainText(expectedTime);")
assert 'const expectedTime=' in s
p.write_text(s)
p=Path('tests/chat-v2.spec.cjs');s=p.read_text()
assert 'left-edge docking' in s
s=s.replace('left-edge docking','right-edge docking')
s=s.replace('Math.abs(before.x-app.x)','Math.abs(before.x+before.width-app.x-app.width)')
s=s.replace('Math.abs(after.x-app.x)','Math.abs(after.x+after.width-app.x-app.width)')
s=s.replace('Math.abs(persisted.x-app.x)','Math.abs(persisted.x+persisted.width-app.x-app.width)')
p.write_text(s)
print('Image loading, timezone-safe test, and right-edge geometry updated.')
