from pathlib import Path
p=Path('styles/chat-special-feedback.css')
s=p.read_text()
old='left:auto!important;right:0!important;bottom:auto!important;'
assert s.count(old)==1
s=s.replace(old,'left:auto!important;right:0;bottom:auto!important;')
p.write_text(s)
p=Path('tests/chat-v2.spec.cjs')
s=p.read_text()
assert "left-edge docking" in s
s=s.replace('left-edge docking','right-edge docking')
s=s.replace('Math.abs(before.x-app.x)','Math.abs(before.x+before.width-app.x-app.width)')
s=s.replace('Math.abs(after.x-app.x)','Math.abs(after.x+after.width-app.x-app.width)')
s=s.replace('Math.abs(persisted.x-app.x)','Math.abs(persisted.x+persisted.width-app.x-app.width)')
p.write_text(s)
print('Right-edge geometry and existing regression expectations updated.')
