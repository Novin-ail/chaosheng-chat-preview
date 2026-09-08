# 潮生 Chat · 结构化附件 v2

这份文件供后端和声声的工具接入使用，不作为用户页面说明。前端组件属于聊天消息正文，不放进加号菜单。默认保留旧聊天布局及时间后的小羊入口。

## 1. 消息协议

后端负责生成并持久化消息 ID、角色、时间、结构化内容与工具调用关联。声声调用工具，不手写 XML、正则标签或可执行 HTML。只有经过校验的工具结果进入持久化消息。前端使用固定组件渲染，未知类型降级为不可打开的附件，不影响同一消息的其他内容。

```json
{
  "id": "msg-123",
  "role": "sheng",
  "timestamp": "2026-09-09T21:00:00+09:00",
  "content": [
    {"type": "text", "text": "这首歌给你听听。"},
    {"type": "song", "track": {"provider": "netease", "id": "123456", "title": "歌曲名", "artist": "歌手", "duration": 240}}
  ],
  "thoughtSummary": "可选的、允许公开的思路摘要",
  "toolCalls": [{"id": "call-123", "name": "share_song", "status": "success"}]
}
```

正式消息不依赖示例 ID。不要将隐藏的原始推理、密钥或未经筛选的工具输出送入可视化详情。小羊只展示实际可提供的摘要与工具调用状态。日志点击时调用 `getToolLog({id})`，未取得记录时不生成模拟记录。

前端入口：`window.ChaoshengChatV2`，兼容别名 `window.ChatSpecialPreview`。可用 `configure(adapter)`、`appendMessage(message)`、`replaceMessages(messages)`。可在新脚本加载前提供 `window.ChaoshengChatBootstrap={adapter,messages}`，或用 `loadMessages()` 异步获取历史。历史数据应由后端保存，浏览器本地示例不得覆盖它们。相同消息 ID 的替换应由统一消息存储层管理；未来增量更新应避免重建正在播放的媒体或用户正在编辑的内容。

## 2. 工具与消息是两种不同的数据

工具调用是动作，不是聊天正文。工具成功后由服务端创建带资源 ID 的消息附件。工具失败时保存失败日志，声声可以重试或解释；不把未创建的任务显示成成功。工具参数由后端 schema 约束，前端仅使用经过校验的资源数据。

建议能力：`share_song`、`share_web`、`create_timer`、`schedule_reminder`、`offer_terminal`。工具名称可由后端实现决定，消息类型及资源身份保持稳定。工具箱未来从后端能力注册表读取工具名称、可用状态、授权范围和最近调用记录，不使用静态假状态。

## 3. 音乐

歌曲身份为 `provider + id`，与歌名分离。歌曲信息字段：`title`、`artist`、`cover`、`duration`（秒）、`lyrics`（LRC 或有时间的行数组）、`source`、`sourceUrl`。前端可直接播放经过授权的 `audioUrl`，否则调用：

```js
resolveTrack({provider, id})
// → {title, artist, cover, duration, audioUrl, source, sourceUrl, lyrics?}
resolveLyrics({provider, id})
// → {lyrics: "[00:12.00]..."} 或 {lines:[{time:12,text:"..."}]}
```

音频 URL 可以有时效，生产后端应按授权与有效期刷新，不把网易云登录 Cookie、API token、受保护的原始资源永久写进公开消息。播放失败保持错误状态，不假装进度前进。只有真实歌词才同步滚动。Chat、唱片室、底部小播放器应最终共用一份播放队列和 Audio 引擎，避免多个播放器同时发声。原始聊天消息保留歌曲资源 ID，不依赖临时 URL。

## 4. 倒计时与 Cron

倒计时用绝对 `dueAt`（ISO8601 带时区或 Unix 毫秒）、`durationMs`、`remainingMs`、`status`、`revision`。暂停由服务端保存剩余时间；恢复计算新的截止时间。前端不反复重置截止时间，不以浏览器 interval 作为真实通知调度。

```js
createTimer({title, seconds, ...})
// → {id, title, status, durationMs, remainingMs, dueAt, revision}
updateTimer({id, action:'start'|'pause'|'resume'|'restart'|'done'|'cancel', revision})
// → 最新完整任务
listTimers()
// → {tasks:[...]}
subscribeTimers(callback)
// → unsubscribe()
ackReminder({id})
```

服务端负责通知、重试、幂等、状态同步与设备投递。短倒计时结束不自动代表喝水/待办已经完成；确认、完成和 Home 事实写入是独立动作。Cron 的每日/一次/表达式调度保留自身服务，聊天卡片引用同一个任务 ID，不再创建第二份任务。

收起的倒计时位置是前端偏好，不是后端任务状态。固定贴在 App 左边缘，只允许纵向移动。长按260ms后拖动，释放时存储归一化纵向位置。视口、键盘、横竖屏变化时重新约束在顶部栏以下、输入框以上的可见区域。提供键盘上下方向键及折叠/展开，拖动不触发完成或取消。未来 APK 原生浮窗必须重新使用原生屏幕边界和安全区，不能直接假定浏览器坐标等于设备屏幕。

## 5. 临时终端

终端会话由授权后端创建并返回不透明 ID。前端不直接执行用户输入、不能依赖模拟器输出。接口：

```js
openTerminal({sessionId?})
// → {id,cwd,output?}
subscribeTerminal(sessionId, outputCallback)
sendTerminal({sessionId,command})
// → {output?,error?}
closeTerminal({sessionId})
```

实际实现应限定用户身份、工作目录、允许访问的服务与会话生命周期。浏览器关闭窗口不等于结束服务器会话；“结束会话”才调用关闭。执行命令、写文件等动作按授权策略处理。敏感参数、环境变量、令牌以及个人设备画面在日志和截图中都须服务端脱敏；浏览器红字替换只作为第二层保护。小改动可以附差异，实际应用前按风险及授权确定是否需要确认。

## 6. 网页、HTML 与错误

网页卡片包含 `url/title/description/image`，后端获取元数据时应限制私有网络、回环地址、重定向、数据体大小与超时，避免把抓取能力变成内网访问入口。浏览器预览受目标网站的 CSP/X-Frame-Options 限制，必须保留外部打开或授权原生 WebView fallback。不能承诺所有网站均可嵌入。

普通 Markdown 使用安全渲染。用户或模型提供的 HTML/CSS 作品仅在隔离预览容器执行允许的静态标记和受约束样式，不能拥有应用同源权限、脚本/表单/网络访问或读取真实聊天数据的能力。正式项目应使用经过审计的 sanitizer 与 CSS 隔离策略。未知附件、错误数据、服务掉线都不能令整条聊天崩溃。

工具日志至少包含 ID、工具、开始时间、耗时、结果、错误代码、允许展示的错误信息和关联消息/任务 ID。日志由执行器生成而非声声手写。错误详情不包含原始密钥、完整授权头或私人监控数据。前端错误应有稳定可读状态和重试入口，技术详情在工具箱查看，不把开发文案铺进每张卡片。

## 7. 本轮范围

当前公共预览不连接真实 CC、网易云账号、监控、共感娃娃或服务器终端；不修改私有生产仓库。提供可接入的组件与浏览器交互，真实音频样例单独标记。接线前需根据现有后端实际接口做映射、验证、权限和可靠性测试。不能将前端模拟行为当作生产服务完成。
