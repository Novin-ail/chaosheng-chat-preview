const {test,expect}=require('@playwright/test');
const base='http://127.0.0.1:4173';
let errors=[];
test.beforeEach(async({page})=>{errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(base+'/');await page.evaluate(()=>document.fonts.ready)});
test.afterEach(async()=>expect(errors).toEqual([]));

test('original avatars, timestamps, sheep and plain assistant text are preserved',async({page})=>{
 const sample=page.locator('.msg.sheng:not(.cs2-msg)').first();
 const expected=await sample.locator('.assistant-meta').evaluate(n=>({classes:[...n.children].map(x=>x.className),sheep:n.querySelector('.sheep img')?.getAttribute('src')}));
 await page.evaluate(()=>window.ChatSpecialPreview.appendMessage({id:'shell-test',role:'sheng',timestamp:'2026-09-09T12:34:56+08:00',thoughtSummary:'已检查',toolCalls:[{id:'log-1',name:'share_song',status:'success'}],content:[{type:'text',text:'这首给你。'},{type:'song',track:window.ChaoshengChatV2.demoTrack}]}));
 const m=page.locator('[data-message-id="shell-test"]');
 expect(await m.locator('.assistant-meta').evaluate(n=>[...n.children].map(x=>x.className))).toEqual(expected.classes);
 expect(await m.locator('.sheep img').getAttribute('src')).toBe(expected.sheep);
 await expect(m.locator('.assistant-meta .time')).toContainText('12:34:56');
 await expect(m.locator('.avatar-sheng')).toBeVisible();
 expect(await m.locator('.rich-md').evaluate(n=>getComputedStyle(n).backgroundColor)).toBe('rgba(0, 0, 0, 0)');
 await m.locator('.sheep').click();await expect(m.locator('.details')).toHaveClass(/open/);await expect(m.locator('.details')).toContainText('share_song');
 await page.evaluate(()=>window.ChatSpecialPreview.appendMessage({id:'user-test',role:'me',content:[{type:'text',text:'这是我的消息'}]}));
 await expect(page.locator('[data-message-id="user-test"] .user-avatar')).toBeVisible();
 expect(await page.locator('[data-message-id="user-test"] .user-bubble').evaluate(n=>getComputedStyle(n).backgroundColor)).not.toBe('rgba(0, 0, 0, 0)');
});

test('sample cover loads locally and failed artwork has a clean fallback',async({page})=>{
 const cover=page.locator('.cs2-song .cs2-image-holder img').first();
 await expect.poll(()=>cover.evaluate(n=>n.complete&&n.naturalWidth>0)).toBe(true);
 await expect(cover).toHaveAttribute('src',/chat-moonlight\.svg/);
 await page.evaluate(()=>window.ChatSpecialPreview.appendMessage({id:'bad-art',role:'sheng',content:[{type:'song',track:{provider:'test',id:'bad-art',title:'没有封面的歌',artist:'测试',cover:'http://127.0.0.1:4173/no-such-cover.png',duration:30}}]}));
 const fallback=page.locator('[data-message-id="bad-art"] .cs2-image-holder');
 await expect(fallback.locator('.cs2-image-placeholder')).toBeVisible();
 await expect(fallback.locator('img')).toBeHidden();
 await page.locator('.cs2-song-open').first().click();await expect(page.locator('#cs2Player')).toBeVisible();
 await page.locator('#cs2Player .cs2-player-tabs button').last().click();await expect(page.locator('#cs2Player')).toHaveClass(/cs2-player-lyrics-mode/);
 await page.locator('#cs2Player .cs2-sheet-close').click();
});

test('expired countdown stays at zero and can only restart explicitly',async({page})=>{
 await page.evaluate(()=>{const t=window.ChaoshengChatV2.services.timers;t.upsert({id:'local-expiry-test',title:'休息一下',durationMs:2000,remainingMs:2000,status:'running',dueAt:Date.now()-1000,revision:1});window.ChatSpecialPreview.appendMessage({id:'expiry-message',role:'sheng',content:[{type:'timer',id:'local-expiry-test',title:'休息一下',durationMs:2000,status:'running',dueAt:Date.now()-1000,revision:1}]})});
 const card=page.locator('[data-message-id="expiry-message"]');
 await expect(card.locator('.cs2-timer-time')).toHaveText('00:00');await expect(card.locator('.cs2-timer-status')).toHaveText('时间到了');
 await expect(card.locator('.cs2-timer-action')).toHaveText('重新开始');
 expect(await page.evaluate(()=>window.ChaoshengChatV2.services.timers.remaining(window.ChaoshengChatV2.services.timers.get('local-expiry-test')))).toBe(0);
 await page.reload();
 expect(await page.evaluate(()=>window.ChaoshengChatV2.services.timers.get('local-expiry-test').status)).toBe('elapsed');
 await page.evaluate(()=>window.ChatSpecialPreview.appendMessage({id:'expiry-message',role:'sheng',content:[{type:'timer',id:'local-expiry-test',title:'休息一下',durationMs:2000,status:'elapsed',revision:2}]}));
 await expect(page.locator('[data-message-id="expiry-message"] .cs2-timer-time')).toHaveText('00:00');
 await page.locator('[data-message-id="expiry-message"] .cs2-timer-action').click();
 expect(await page.evaluate(()=>window.ChaoshengChatV2.services.timers.get('local-expiry-test').status)).toBe('running');
});

test('collapsed timer stays on the right and moves vertically only',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.locator('.cs2-timer-action').first().click();
 const dock=page.locator('#cs2TimerDock');await expect(dock).toBeVisible();await dock.locator('.cs2-dock-panel .cs2-icon').click();
 const before=await dock.boundingBox(),app=await page.locator('#app').boundingBox();
 expect(Math.abs(before.x+before.width-app.x-app.width)).toBeLessThan(2);
 const point={x:before.x+before.width/2,y:before.y+before.height/2};await page.mouse.move(point.x,point.y);await page.mouse.down();await page.waitForTimeout(350);await page.mouse.move(point.x-150,point.y-90,{steps:6});await page.mouse.up();
 const after=await dock.boundingBox();expect(Math.abs(after.x-before.x)).toBeLessThan(2);expect(after.y).toBeLessThan(before.y-20);
 await page.reload();const persisted=await dock.boundingBox();expect(Math.abs(persisted.x+persisted.width-app.x-app.width)).toBeLessThan(2);expect(Math.abs(persisted.y-after.y)).toBeLessThan(12);
 await dock.locator('.cs2-dock-tab').focus();await page.keyboard.press('ArrowDown');const moved=await dock.boundingBox();expect(moved.y).toBeGreaterThan(persisted.y);
});

test('right dock and attachment cards fit mobile and desktop widths',async({page})=>{
 for(const width of [320,390,768]){await page.setViewportSize({width,height:800});expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBeLessThanOrEqual(1);for(const node of await page.locator('.cs2-attachment').all()){const r=await node.boundingBox();if(r)expect(r.width).toBeLessThanOrEqual(Math.min(width,520)+1)}}
 await page.locator('.cs2-timer-action').first().click();await page.locator('#cs2TimerDock .cs2-dock-panel .cs2-icon').click();const dock=await page.locator('#cs2TimerDock').boundingBox(),app=await page.locator('#app').boundingBox();expect(Math.abs(dock.x+dock.width-app.x-app.width)).toBeLessThan(2);
});
