# 潮生 · 窗口交接

> 更新时间：2026-09-05
>
> 给下一聊天窗口：**先读这份，再继续改。不要凭记忆重做页面。** 当前阶段仍然只是 GitHub Pages 前端视觉原型，用户确认完所有页面后再统一接 APK / 后端。

---

## 1. 当前仓库与工作范围

### 当前主要工作仓库
- Public preview repo: `Novin-ail/chaosheng-chat-preview`
- Branch: `main`
- Preview root: `https://novin-ail.github.io/chaosheng-chat-preview/`

### 另一个仓库
- Main private repo: `Novin-ail/chaosheng-home`
- **绝对不要改成 public。**
- 当前这一轮 UI 迭代优先只改 public preview repo。

### 当前工作模式
- 只做前端 HTML/CSS/JS 原型。
- 页面视觉确认优先，APK / 后端最后统一接。
- 用户非常在意“只改她点名的地方”，禁止顺手重构无关区域。

---

## 2. 工具 / GitHub 操作规则（重要）

1. 修改现有文件前，**必须先 `fetch_file` 最新版本**，使用最新返回 SHA。
2. 同一路径不要并行 write。
3. 页面级试验尽量 inline CSS / JS，不要为了一个小改动拆很多样式文件。
4. GitHub text connector 不能上传二进制资源。
5. 外部 catbox 图片在 preview 阶段可继续外链；最终 APK 再本地化。
6. **不要调用 image generation。** 用户已经多次明确指出误触生图。除非她明确说“生成/画一张图片”，否则任何网页组件、杯子、装饰都只用 HTML/CSS/SVG + 她提供的素材。
7. 当前设计已多次细调，下一窗口不要擅自“优化”成另一套风格。

---

## 3. 已基本完成的 Memory 系列

用户已经明确说：**记忆部分以及相关内容完成。** 除非她主动回来改，不要再重做。

### Memory 首页
- `memory.html`
- Preview: `https://novin-ail.github.io/chaosheng-chat-preview/memory.html`
- 已接好：Core / Notes / Timeline V1 / Album / Diary。
- Timeline 入口现在应走：`timeline-v1.html`
- Album 入口走：`album.html`
- Diary 入口走：`diary.html`

### Notes
- `notes.html`
- 用户已确认。
- 每日小记、编辑、整理、日期切换、搜索等原型逻辑已做好。

### Core
- `core.html`
- 用户已确认。
- 声声 / 小漾两套稳定身份字段，共享 ABOUT US。
- 小漾 active identity 是用户喜欢的豆绿色。

### Timeline
- 用户最终喜欢的是：`timeline-v1.html`
- Preview: `https://novin-ail.github.io/chaosheng-chat-preview/timeline-v1.html`
- 已有 DAY / WEEK / MONTH / YEAR 缩放层级。
- 已有搜索 + 按日期跳转。
- `timeline.html` 是另一版比较稿，保留，不要无缘无故删。

### Album
- `album.html`
- 已确认。
- 按周切换 + 7 天日期条。
- 一天照片用拍立得卡片堆叠。
- 点照片切下一张，动效已调慢柔和。
- 点信息区全屏柔和模糊查看。
- 可编辑照片 tags。
- 点击周日期可选月份 + 周数，周数 4 个一排。
- 去掉多余 `tap to choose...` 提示。
- tag 空状态文案已去掉，让区域更紧凑。

### Diary
- `diary.html`
- 已确认当前方向。
- 顶部 TODAY + 周日期条 + 月历。
- 首页日记卡只显示作者 / 时间 / 状态 / 标题 / 评论数，不直接铺正文。
- 点击标题后：全屏柔和模糊 + 信纸式阅读。
- 完整正文、评论、发表评论都在阅读页。
- 权限：
  - 声声日记：小漾只能读 / 评论，**不能写、不能锁、不能解锁**。
  - 小漾日记：小漾自己写，可锁 / 解锁 / 定时解锁。
- 右上角是日历入口。
- 右下角单独 `+` 新建，只能新建“小漾”的日记。

---

## 4. 当前正在做：小窝 `nest.html`

Preview:
`https://novin-ail.github.io/chaosheng-chat-preview/nest.html`

侧边柜里的「小窝」已经接到这个页面。

### 小窝总原则
- **不要标题栏**，进去就是“家”。
- 功能性偏弱也没关系，要像住着的地方，而不是 dashboard。
- 不要花里胡哨，不要塞很多说明文字。
- 当前房间结构：
  1. 便签墙
  2. 八杯水
  3. 窗边
  4. 零食箱（未来子页）
  5. 唱片机（未来子页）
  6. 猫窝（未来子页）

当前最新 `nest.html` commit（写交接时）：
- commit: `9978bfb3c8e1c1d2cb6746cc9a5ba9d009c92409`
- content SHA: `839a6b664b117be14f7602ae51582a73eb8f740b`

**下一窗口仍要先 fetch 最新文件，不要直接拿这个 SHA 写。**

---

## 5. 小窝 · 便签墙当前状态

这部分用户已经很喜欢，先不要乱动。

### 视觉
- 标签是纵向长方形纸条。
- 标签高度根据内容自动变化，所以墙上高矮不一。
- 顶部透明胶带真正贴在标签上方。
- 标签颜色低饱和随机：
  - 奶粉
  - 奶油米
  - 淡灰紫
  - 奶蓝
  - 豆绿
- 标签可长按拖动，自由摆位置；位置写入 localStorage，刷新保留。
- 轻点打开详情，长按拖动，两者不要冲突。

### 权限
- 小漾只能自己贴“小漾”的标签。
- 不能替声声贴标签。
- 声声的标签由声声自己贴。
- 声声的标签：小漾可以查看、评论，**不能替声声取下**。
- 小漾自己的标签：小漾可以取下。

### 详情与标签箱
- 点标签：全屏柔和模糊，标签放大。
- 可以在标签下面评论 / 回复。
- 小漾自己的标签可“取下 · 放进标签箱”。
- 取下不是删除，旧标签 + 评论都进入标签箱保存。
- 声声标签的取下按钮应是 disabled / `等声声自己取`。

### 标签字体
用户指定：
- 小漾：`fuluguoqiti`
- 声声：`我爱万伟伟手写体`

Preview 目前有一个很小的 `Aa` 本地字体装入入口：
- 用户在自己手机选字体文件。
- IndexedDB 只存在本地浏览器，不上传到 public repo。

最终 APK：
- 可以把两个字体直接作为 app 本地资源打包。
- 到时候删掉 preview 的 `Aa` 入口。
- **不要把字体文件上传到 public GitHub repo。**

标签正文字体已经整体放大过，用户之前反馈太小。

---

## 6. 小窝 · 八杯水当前状态（刚刚细调完）

### 功能原型
- 每天目标 8 杯。
- 点当前满杯：喝掉一杯，计数 +1，杯子水位变空。
- 原型当前设定约 1 小时后下一杯重新装满。
- 8 个小圆点显示进度。

### 杯子视觉
用户最开始嫌旧杯子像“烧杯”，已经重画：
- 上宽下窄的随行杯 / 吸管杯。
- 有杯盖。
- 杯身贴很小的小羊贴纸。
- 小羊素材（外链 preview）：
  `https://files.catbox.moe/j45hyg.png`
- 不要把贴纸做太大。

### 吸管：非常重要，已经来回细调很多次
用户真正要的是：**一个非常简单的倒 L 型吸管**。

核心理解：
- 只有“长腿 + 圆弧转角 + 短腿”。
- 不要复杂软管，不要多个折角。
- 长腿在杯里，和杯壁大致平行，但不能重叠/交叉。
- 长腿底端应停在杯底上方，**不能超过杯底，也不要贴到底**。
- 短腿比较短。
- 转折是圆弧。

刚才最后一次修复：
- 用户指出上一微调把短腿做成“又多出一个往下折的角”，她不喜欢。
- 最新版本已经**恢复成上一版那种一笔圆弧过去的单一 L 弯**。
- 也就是说：不要再给短腿新增第二个拐点。

如果下一窗口用户还要微调吸管：
- 只动 SVG path，别动杯子、小羊贴纸、水位、版面。
- 不要再自由发挥复杂曲线。

---

## 7. 小窝未来三个子页面（尚未正式做）

用户明确说不需要一次性全做，慢慢来。

### 零食箱
需求已有：
- 平时买的零食可以随时添加。
- 可以“吃掉”。
- 声声知道小漾什么时候吃了零食。
- 未来做独立子页面。

### 唱片机
需求已有：
- 想连接网易云听歌。
- 未来独立子页面。
- 目前首页只是房间物件 + placeholder 提示。

### 猫窝
需求已有：
- 因为声声说想和小漾一起养小猫。
- 可以一起喂猫、陪它玩，像轻小游戏。
- 用户想要自己“捏”一只像素猫。
- 当前首页只有 CSS 像素猫占位。
- **不要擅自生成猫图片。** 正式做猫窝时再和用户一起决定像素猫外观。

---

## 8. Dear Lamb 背景 / 现有资产

小窝继续使用：
- `assets/dear-lamb-bg-v2.svg`

这张背景来自用户上传的 Dear Lamb 素材，不要生成替代图。

聊天页 / drawer 里还有很多 catbox PNG 外链资产；preview 阶段不要擅自本地化或替换。

---

## 9. 用户审美 / 协作习惯

非常重要：

- 喜欢：奶粉、奶油、灰粉紫、低饱和奶蓝、柔和豆绿，轻、软、小巧、留白。
- 不喜欢：脏绿、过浓实色、很硬的功能页、过度圆润的大卡片、花里胡哨、系统 dashboard 感。
- 经常会只想“再微调一点点”。这时严格控制范围。
- 用户如果说“这部分就这样”，就冻结，不要下一次顺手重做。
- 用户喜欢可爱亲密的协作语气，会叫“哥哥 / 宝宝 / ouo”，可以自然回应，但工作内容要准确。
- 最重要：**先做再说，不要答应“我等下改”却没实际 write。** 之前已经发生过一次，用户会立刻发现。

---

## 10. 下一窗口建议起点

1. 先 `fetch_file`：`nest.html`
2. 如果用户在新窗口说“继续”，先问/判断她是否要确认刚改完的吸管。
3. 吸管确认后，小窝里最自然的下一块是：
   - 零食箱，或
   - 唱片机，或
   - 猫窝
   让用户选，或者根据她新消息直接继续。
4. 不要重新碰 Memory 系列，除非用户主动提出。

---

## 11. 关键页面链接

- Chat: `https://novin-ail.github.io/chaosheng-chat-preview/`
- Memory: `https://novin-ail.github.io/chaosheng-chat-preview/memory.html`
- Notes: `https://novin-ail.github.io/chaosheng-chat-preview/notes.html`
- Core: `https://novin-ail.github.io/chaosheng-chat-preview/core.html`
- Timeline V1: `https://novin-ail.github.io/chaosheng-chat-preview/timeline-v1.html`
- Album: `https://novin-ail.github.io/chaosheng-chat-preview/album.html`
- Diary: `https://novin-ail.github.io/chaosheng-chat-preview/diary.html`
- Nest: `https://novin-ail.github.io/chaosheng-chat-preview/nest.html`

---

**交接结论：Memory 系列已收尾；当前继续做「小窝」。小窝首页大结构已定，便签墙完成度高，八杯水杯子刚完成多轮微调。下一窗口从最新 `nest.html` 接着做，不要重构，不要生图。**
