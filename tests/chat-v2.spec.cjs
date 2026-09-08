const {test,expect}=require('@playwright/test');
const base='http://127.0.0.1:4173';
const errors=[];
test.beforeEach(async({page})=>{page.on('pageerror',error=>errors.push(error.message));await page.goto(base+'/');await page.evaluate(()=>document.fonts.ready);});
test.afterEach(async()=>{expect(errors.splice(0)).toEqual([])});

test('typed messages and original sheep remain functional',async({page})=>{
 const api=page.locator('body');await expect(page.locator('#cs2TimerDock')).toBeHidden();
 await expect(page.locator('.cs2-song')).toHaveCount(1);
 await page.evaluate(()=>window.ChatSpecialPreview.appendMessage({id:'test-one',role:'sheng',thoughtSummary:'正在整理这次的修改',toolCalls:[{id:'log-1',name:'share_song',status:'success'}],content:[{type:'text',text:'这首给你。'},{type:'song',track:window.ChaoshengChatV2.demoTrack}]}));
 const message=page.locator('[data-message-id="test-one"]');await expect(message.locator('.cs2-song')).toBeVisible();await message.locator('.sheep').click();await expect(message.locator('.details')).toHaveClass(/open/);await expect(message.locator('.details')).toContainText('share_song');
 await page.evaluate(()=>window.ChatSpecialPreview.appendMessage({id:'unknown',type:'unrecognized',role:'sheng'}));await expect(page.locator('[data-message-id="unknown"]')).toContainText('附件暂时无法打开');
 await page.evaluate(()=>window.ChatSpecialPreview.appendMessage({id:'unsafe',role:'sheng',content:[{type:'text',text:'<script>window.__executed=1</script><img src=x onerror="window.__executed=1">'}]}));expect(await page.evaluate(()=>window.__executed||0)).toBe(0);
});

test('music uses a real audio element and opens immersive player',async({page})=>{
 await page.locator('.cs2-song-open').first().click();await expect(page.locator('#cs2Player')).toBeVisible();await expect(page.locator('#cs2Player .cs2-player-info')).toContainText('月光奏鸣曲');
 await expect(page.locator('#cs2Player audio')).toHaveCount(0);
 const audio=await page.evaluate(()=>window.ChaoshengChatV2.services.media.audio instanceof HTMLAudioElement);expect(audio).toBe(true);
 await page.locator('#cs2Player .cs2-player-tabs button').last().click();await expect(page.locator('#cs2Player')).toHaveClass(/cs2-player-lyrics-mode/);
 await page.locator('#cs2Player .cs2-sheet-close').click();await expect(page.locator('#cs2Player')).toBeHidden();
});

test('local countdown pause resume and left-edge docking',async({page})=>{
 await page.setViewportSize({width:390,height:844});
 await page.locator('#cs2TimerDock').evaluate(n=>n.hidden=true);
 const card=page.locator('.cs2-timer').first();await card.locator('.cs2-timer-action').click();
 const dock=page.locator('#cs2TimerDock');await expect(dock).toBeVisible();await dock.locator('.cs2-dock-tab').evaluate(n=>n.click());await dock.locator('.cs2-dock-panel .cs2-soft').first().click();
 const state=await page.evaluate(()=>window.ChaoshengChatV2.services.timers.get('local-demo-timer'));expect(state.status).toBe('paused');
 await dock.locator('.cs2-dock-panel .cs2-soft').first().click();await expect.poll(async()=>page.evaluate(()=>window.ChaoshengChatV2.services.timers.get('local-demo-timer').status)).toBe('running');
 await dock.locator('.cs2-dock-panel .cs2-icon').click();const tab=dock.locator('.cs2-dock-tab');
 const before=await dock.boundingBox();const app=await page.locator('#app').boundingBox();expect(Math.abs(before.x-app.x)).toBeLessThan(2);
 const point={x:before.x+25,y:before.y+20};await page.mouse.move(point.x,point.y);await page.mouse.down();await page.waitForTimeout(350);await page.mouse.move(point.x+170,point.y-100,{steps:6});await page.mouse.up();
 const after=await dock.boundingBox();expect(Math.abs(after.x-app.x)).toBeLessThan(2);expect(after.y).toBeLessThan(before.y-20);
 await page.reload();const persisted=await dock.boundingBox();expect(Math.abs(persisted.x-app.x)).toBeLessThan(2);expect(Math.abs(persisted.y-after.y)).toBeLessThan(12);
 await page.keyboard.press('ArrowDown');
});

test('terminal never executes without adapter and accepts authorized bridge',async({page})=>{
 await page.locator('.cs2-attachment').filter({hasText:'小改一下'}).getByRole('button',{name:'打开终端'}).click();await expect(page.locator('#cs2Terminal')).toBeVisible();await expect(page.locator('#cs2Terminal .cs2-terminal-meta')).toContainText('尚未连接服务');
 await expect(page.locator('#cs2Terminal .cs2-terminal-row input')).toBeDisabled();
 await page.evaluate(()=>{window.__commands=[];window.ChatSpecialPreview.configure({openTerminal:async()=>({id:'test-session',cwd:'/workspace'}),sendTerminal:async({command})=>{window.__commands.push(command);return{output:'ok'}},closeTerminal:async()=>({})});});
 await page.locator('#cs2Terminal .cs2-terminal-row input').waitFor({state:'visible'});await page.locator('#cs2Terminal .cs2-terminal-row input').fill('pwd');await page.locator('#cs2Terminal .cs2-terminal-row button').click();await expect(page.locator('#cs2Terminal .cs2-terminal-log')).toContainText('ok');expect(await page.evaluate(()=>window.__commands)).toEqual(['pwd']);
});

test('responsive cards never overflow the viewport',async({page})=>{
 for(const width of [320,390,768]){await page.setViewportSize({width,height:800});await page.evaluate(()=>window.scrollTo(0,0));const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);expect(overflow).toBeLessThanOrEqual(1);for(const node of await page.locator('.cs2-attachment').all()){const r=await node.boundingBox();if(r)expect(r.width).toBeLessThanOrEqual(Math.min(width,520)+1)}}
});
