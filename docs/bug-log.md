# re9guide.it.com — Bug Log & Quality Checklist

> 用于记录抽查发现的 bug、修复方案，以及新页面交付前必须满足的 checklist。
> 目的：避免同类问题再次出现，建立可重复的质量基线。

---

## 1. 历史 bug 索引（按发现日期倒序）

### 2026-05-19 · 用户抽查 3 个 bug（Phase 21）

#### Bug 21.1 — Mr. X SVG 底部标签框被外边框裁切
**现象：** `/ko/how-to-beat-mr-x-super-tyrant.html`（及 EN 同款）SVG 底部第三个标签框 "머리 (패리 후)" 框的下边沿超出外层 viewBox 红色 border，最后一行文字 "Mortal Edge로 패리하여 노출" 与底部 border 视觉粘连/重叠；同时与 footer attribution 文字 "re9guide.it.com · 한국어판 · v1.02 검증 · 2026" 出现叠加。

**根因（坐标算错）：**
- viewBox 上限 `0 0 1200 630`，外层 border `rect x="20" y="20" width="1160" height="590"` → bottom 边在 y=610
- 底部标签框 `transform="translate(680, 540)"` + `rect height="80"` → 框底在 y=620（**超出 border 10px**）
- 框最后一行文字 y=68 偏移 → 绝对 y=608（紧贴 border）
- footer text 在 y=600 → 落在底部框内部（y=540-620 范围），叠加

**修复（已应用）：**
- 底部框上移 30px：`translate(680, 540)` → `translate(680, 510)`
- 头部引线 y 终点 580 → 540（仍指向新位置的底部框）
- 新布局：底部框 y=510-590（margin 20px 距 border），footer text y=600 落在框下方安全区
- EN/KO 两版同步修改，几何完全一致

**规则（追加进 SVG checklist）：**
> SVG 内任何 `<g transform="translate(x,y)">` + 子 `<rect height="h">` 必须满足：
> - `y + h ≤ outerBorderBottom − 10`（至少 10px 安全间距）
> - 引线 `<line>` 的 `x2/y2` 终点必须落在目标框 padding 内部（不要正好打在 border 上）
> - footer attribution `<text>` 的 y 坐标必须 > 所有 `<g>` 框的 `y + height`，且 < 外层 border y

#### Bug 21.2 — "영문" 标签使用不规范 + 已翻译页面未升级标签
**现象：**
- 全站使用 "영문" 一词，应统一为 "영어"（用户母语规范）
- bosses-hub.html / 等 KO 页面的 boss-card 标题仍标 `(영어)` 或裸标题，应统一为 `(영어/한국어)` 当 KO 版本存在时

**根因：** 早期翻译批次用了 "영문" 这个相对生硬的书面语；后续翻译进度更新时未同步刷新各 hub 页的卡片标签。

**修复（已应用）：**
1. 全局替换 `(영문)` → `(영어)` 或 `(영어/한국어)`：14 个 KO 文件,50 处替换
2. about.html 叙述性文字：`영문 위주`/`영문권`/`영문에서 단순` → `영어 위주`/`영어권`/`영어에서 단순`
3. bosses-hub.html 等所有卡片：href 指向 KO-existing 页面的,标签升级为 `(영어/한국어)`,共 10 张 boss 卡片全部对齐
4. **0 处 "영문" 残留**(grep 验证)

**规则（追加）：**
> - 韩文文档中表示语言时,**禁止用** "영문"。使用 "영어"
> - 任何 boss / guide / hub 卡片(`boss-card` / `hub-card` / `guide-card` / `coll-card` / `update-row`)的标题必须带语言标签:
>   - KO 不存在: `(영어)`
>   - KO 存在: `(영어/한국어)`
>   - **不允许** 裸标题(无标签)
> - 新翻译页面交付前,必须跑 `scripts/refresh-card-labels.py`(本仓库自带)同步所有卡片标签

#### Bug 21.3 — Bing IndexNow 未设置（影响 Bing 索引速度）
**现象：** Bing Webmaster Tools 报告 "Your site lacks inbound links from high-quality domains"（Moderate 严重度）。除外部反向链接外,关键短板是**未启用 IndexNow** → Bing 只能靠周期性爬取发现新页面,新发布内容索引延迟 1-4 周。

**修复（已应用）：**
1. 在站根创建 IndexNow key file：`/cebd0f739339490594ae3738f31b5ed0.txt`（内容 = key 本身）
2. 添加 helper script `docs/indexnow-ping.sh`：
   ```bash
   ./indexnow-ping.sh                          # ping all sitemap URLs
   ./indexnow-ping.sh <url1> <url2> ...        # ping specific URLs
   ```
3. 脚本会自动构造 POST request 到 `https://api.indexnow.org/indexnow`,处理常见 HTTP 状态码

**部署清单（用户需在 Cloudflare/Hosting 端确认）：**
- [ ] key file `cebd0f739339490594ae3738f31b5ed0.txt` 部署到生产站点根目录,可访问 `https://www.re9guide.it.com/cebd0f739339490594ae3738f31b5ed0.txt`
- [ ] 第一次手动跑 `bash docs/indexnow-ping.sh` 提交全 sitemap
- [ ] 后续每次发布新页面,在 CI / pre-push hook 中调用 `./indexnow-ping.sh <new-url>`
- [ ] (可选) 在 Bing Webmaster Tools → "URL Submission" 标签验证 IndexNow 已激活
- [ ] Cloudflare 等 CDN 不要对 IndexNow key file 做 redirect / rewrite,直接静态返回

**规则（追加进发布 SOP）：**
> 每次新页面发布,必须执行 IndexNow ping（同时也可考虑 Google Search Console 的 "URL Inspection" + "Request Indexing"）。新页面进入 Bing 索引时间从 1-4 周降到 < 24 小时。

---

### 2026-05-19 · 用户抽查 3 个 bug（Phase 20）

#### Bug 20.1 — KO 首页 "카테고리별 공략" 链接标签错误
**现象：** `/ko/index.html` 的 "카테고리별 공략" 版块中，许多 boss / 攻略链接显示 `(영문)` 后缀，但其对应的 KO 版本实际上已经翻译完成。这会误导韩文用户以为页面只有英文版，跳出率上升。

**根因：** KO 首页是一次性手写的，没有跟着翻译进度动态更新；后续翻译完成后未同步刷新首页链接和标签。

**修复（已应用）：**
- 扫描 `/ko/index.html` 的所有 `<li><a href="../X.html">名称 (영문)</a></li>`
- 检查 `ko/X.html` 是否存在
- 存在 → href 改为相对路径 `X.html`，标签改为 `(영어/한국어)`
- 不存在 → 保持 `(영문)`
- 本次共修正 12 条链接

**规则（写入 SOP）：**
> 每次翻译完一个新 KO 页面后，**必须**重新跑首页扫描脚本，更新 (영문) → (영어/한국어) 标签和链接。建议把这步加进发布流程的 pre-commit hook。
>
> 翻译标签的正式表达：
> - 只有 EN 版：`(영문)` (= "영어")
> - EN + KO 都有：`(영어/한국어)`
> - 只有 KO 版（理论上很少出现）：`(한국어)`

#### Bug 20.2 — Mr. X 韩文版弱点图边框与内容重叠
**现象：** `/ko/how-to-beat-mr-x-super-tyrant.html` 的 inline SVG 中，右侧三个标签面板（"패리 불가능" / "맥동하는 심장" / "머리 (패리 후)") 的 X 坐标与左侧身体图的引线终点重叠，视觉上引线"刺进" 标签框边缘。

**根因：**
- KO SVG 是 Phase 15 单独建模的，与 Phase 17 重做的 EN SVG 几何不一致
- KO 版本中：身体图扩展到 x=470，心脏引线终点 x=700，标签框起点 x=700 → 完全贴边
- EN 版本中：身体图收窄到 x=440，引线终点 x=690，标签框起点 x=680 → 留 10px 安全间距

**修复（已应用）：** 直接采用 EN SVG 的几何坐标，仅替换标签文字为韩文。EN/KO 两版现在视觉完全一致，只有语言不同。

**规则：**
> 同一个 infographic 的多语言版本必须共享一套 SVG 几何坐标。语言差异**只允许**出现在 `<text>` / `<title>` / `<desc>` 元素的内容上，不允许微调坐标。
>
> 若需要为某种语言（如长字符串）调整坐标，必须**同步**到其他语言版本，保持视觉一致。

#### Bug 20.3 — Victor Gideon 英文版用 PNG、韩文版用 inline SVG，两版风格不一致
**现象：** `/how-to-beat-victor-gideon.html` 使用 `<img src="infographic-victor-weakness.png">` 显示弱点图，而 `/ko/how-to-beat-victor-gideon.html` 使用 inline SVG。两版视觉风格、信息密度、颜色都不同。

**根因：** EN 版的 PNG 是早期手做的位图，KO 版的 SVG 是 Phase 9 重新设计的矢量图。两条线没合并。

**修复（已应用）：** 把 EN Victor Gideon 的 `<img>` 替换为与 KO 同几何的 inline SVG，标签改为英文。社交卡片预览（`og:image` / `twitter:image`）仍保留 PNG（因为社交分享需要静态位图）。

**规则：**
> 所有 boss / 攻略页的 weak-point infographic **统一用 inline SVG**，禁止用 PNG 嵌入正文。原因：
> 1. SVG 矢量缩放清晰，移动端不糊
> 2. SVG 是 HTML 文本，可被搜索引擎抓取（PNG 不能）
> 3. SVG 多语言版本只需替换 `<text>` 内容，不需重做位图
>
> PNG 只用于：
> - `og:image` / `twitter:image` 社交卡片（1200×630 静态位图）
> - favicon 系列
> - 真实截图、照片素材

---

### 2026-05-18 · GSC 抽查 2 个 SEO 阻断 bug（Phase 18）

#### Bug 18.1 — sitemap.xml 引用不存在的页面（4xx / "已发现 - 尚未编入索引"）
**现象：** Google Search Console 报告 23 个 URL "已发现 - 尚未编入索引"。其中 2 个 URL（`/ark-facility-complete-walkthrough.html` 和 `/insanity-chapter-walkthrough.html`）实际上**文件不存在**，但被 `sitemap.xml` 和 `index.html` 引用。

**影响：** Google 跟着 sitemap 抓取得到 404 → 该 URL 永远进不了索引；同时拖低整站的 sitemap 健康度（信任分下降），影响其他正常页面的抓取频率。

**修复（已应用）：**
- 从 `sitemap.xml` 删除两个不存在的 `<url>` 块
- `index.html` 中 5 处引用替换为已存在页面或 PLANNED 状态

**规则：**
> 每次发布前，**必须**跑 sitemap 完整性检查：扫描 `sitemap.xml` 所有 `<loc>`，验证文件存在。本仓库已有内建检查脚本（见末尾 SOP 章节）。
>
> 同样规则：每次新建页面后，必须同步更新 sitemap.xml。每次删除页面后，必须从 sitemap 删除条目 + 在引用处用 301 重定向或移除引用。

#### Bug 18.2 — `all-25-mr-raccoon-locations.html` 内部死链
**现象：** Mr. Raccoon 收集品页底部 "RELATED COLLECTIBLE GUIDES" CTA 引用 4 个旧文件名（`all-safe-codes.html` / `all-antique-coins.html` / `all-files.html` / `trophy-guide.html`），但实际页面用新文件名（`all-5-safe-codes-guide.html` / `all-22-antique-coins-locations.html` 等）。

**根因：** 早期重命名后没全量回填引用。

**修复（已应用）：** 4 处链接已更新为正确路径。

**规则：**
> 任何页面重命名后，**必须**全局搜索旧文件名 (`grep -rn "old-name.html" *.html ko/*.html sitemap.xml`)，确认没有残留引用。

---

### 2026-05-17 · KO 内容深度不齐 bug（Phase 17 / 18 用户报告）

#### Bug 17.1 — KO 翻译是"概要版"而非"对齐版"
**现象：** 用户抽查 `/ko/how-to-beat-plant-43.html` 发现 KO 内容只有 EN 的 ~46%，h2 数量 4 vs EN 7。KO 写的"农포 wave 系统"在 EN 中根本不存在，是早期翻译者凭印象写的虚构内容。

**根因：** 第一轮 KO 翻译是赶进度做的 stub（占位翻译），并不是对照 EN 完整翻译。

**修复（Phase 18 已应用）：** 9 个 KO 页面全部重写，h2 与 EN 完全对应，行数误差 ±50 以内。

**规则：**
> KO 翻译必须满足两个硬指标：
> 1. `grep -c '<h2' ko/X.html` **必须等于** `grep -c '<h2' X.html`
> 2. `wc -l ko/X.html` **必须在** `wc -l X.html` ±50 行以内
>
> 翻译完成后必须跑对齐审计脚本。任何不达标的页面视为"未完成"，不计入翻译进度。

---

## 2. 新页面/翻译交付 checklist（必经）

下方清单按 `pre-commit` 顺序排列。每一项不达标 = 不能合并。

### A. EN 新页面交付
1. [ ] `<title>`、`<meta name="description">`、`og:title`、`og:description`、`twitter:title`、`twitter:description` 全部填写，且不超过 60 / 160 字符
2. [ ] `<link rel="canonical">` 指向自身完整 URL
3. [ ] 至少 1 个 `<h1>`，且与 title 一致
4. [ ] 结构化数据 JSON-LD：`Article` + `BreadcrumbList`（boss 页加 `HowTo`，FAQ 页加 `FAQPage`）
5. [ ] 内部链接全部解析（用 broken-link 检查脚本）
6. [ ] 加入 `sitemap.xml`，优先级合理（首页 1.0 / 王牌页 0.9 / 攻略页 0.7-0.85 / 法律页 0.3）
7. [ ] `<img>` 全部带 `alt` 属性 + `width` / `height` + `loading="lazy"`（首屏图用 `loading="eager"` + `fetchpriority="high"`）
8. [ ] favicon 系列、`apple-touch-icon`、`site.webmanifest` 引用齐全
9. [ ] 移动端响应式：`<meta name="viewport">` + 最窄列 < 360px 不溢出
10. [ ] 加入首页 "카테고리별 공략" / "Updates" / roadmap 等相关版块

### B. KO 翻译页交付
所有 A 的项目 + 以下额外要求：

11. [ ] `<html lang="ko">`
12. [ ] canonical 指向 `/ko/X.html`，且有 3 条 `<link rel="alternate" hreflang>`（en / ko / x-default）
13. [ ] 字体栈：`font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic","맑은 고딕",sans-serif;`
14. [ ] Nav 块包含 EN / 한국어 语言切换器
15. [ ] 标题、面包屑、所有 h2 / h3 / p / ul / ol / table / button / footer 文字**全部翻译**，不留 stub
16. [ ] h2 数量 **=** EN h2 数量（exact match）
17. [ ] 行数 **在** EN 行数 ±50 以内
18. [ ] Footer 链接用绝对路径 `/contact.html` 等（避免浏览器误解析为 `/ko/contact.html`）
19. [ ] JSON-LD 包含 `"inLanguage": "ko-KR"`
20. [ ] **更新 `/ko/index.html` 的链接** —— 把对应的 `(영문)` 改为 `(영어/한국어)` 并指向 `/ko/X.html`
21. [ ] EN 同名页加上 `<link rel="alternate" hreflang="ko">` 指向 KO 版本（双向 hreflang）

### C. SVG infographic 交付
22. [ ] 所有 boss 弱点图必须是 inline SVG（**禁止** `<img src="*.png">` 嵌入正文）
23. [ ] EN / KO 版必须**共享同一套几何坐标**，只允许 `<text>` 内容差异
24. [ ] viewBox 统一 `0 0 1200 630`，外层 `<rect>` 边框 `stroke="#c0392b"` 一致
25. [ ] 标签框与引线终点之间留 ≥ 10px 安全间距，防止重叠
26. [ ] SVG 内 `<title>` / `<desc>` 元素填写（屏幕阅读器无障碍）
27. [ ] 同时仍生成 `1200×630` PNG 文件，用于 `og:image` / `twitter:image`（社交卡片）

---

## 3. SEO 优化指南（参考 Google + Bing 官方文档）

来源：
- Google SEO Starter Guide — https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Bing Webmaster Tools / IndexNow — https://www.bing.com/webmasters/

### 3.1 Crawlability（爬虫可达性）
- **`robots.txt`**：允许 `Googlebot` / `Bingbot` 抓取所有内容页，禁止 `/admin/` `/draft/` 等管理路径
- **`sitemap.xml`**：包含所有可索引页面，每次新增/删除页面后同步更新；`lastmod` 用 ISO 8601 真实日期
- **内链结构**：从首页能通过 ≤ 3 跳到达任何页面（hub 页 → 子分类 → 详情页）
- **死链清零**：定期跑全站 broken-link 扫描；任何 4xx 立即修

### 3.2 On-page SEO
- **title 标签**：≤ 60 字符，自然包含主关键词，**每个页面唯一**
- **meta description**：120-155 字符，自然描述页面价值，包含 1-2 个关键词，**每个页面唯一**
- **h1**：每页 1 个，与 title 高度一致但不完全相同
- **h2 / h3 层级**：用于分段，不要跳级（h1 → h3 直接跳是 bug）
- **关键词密度**：自然分布，避免堆砌；boss 名 / 武器名等长尾词在 lead / 第一个 h2 / 首段出现

### 3.3 结构化数据
- 文章页：`Article` schema（`headline` / `datePublished` / `dateModified` / `author` / `image`）
- Boss 攻略：加 `HowTo` schema（步骤列表 → 富摘要展示）
- FAQ 模块：加 `FAQPage` schema（搜索结果直接展开）
- 面包屑：`BreadcrumbList` schema（搜索结果显示 home > 分类 > 文章）
- 视频：`VideoObject` schema（如有）
- 工具：用 https://search.google.com/test/rich-results 验证

### 3.4 Multi-language（hreflang）
- 每个语言版本都需要 3 条 `<link rel="alternate" hreflang>`：自己 + 对应语言 + `x-default`
- `x-default` 永远指向英文版（语言中性 fallback）
- canonical 指向**自己**，不要交叉指向

### 3.5 Performance（核心 Web 指标 / Core Web Vitals）
- **LCP (Largest Contentful Paint)** < 2.5s
  - 首屏图用 `loading="eager"` + `fetchpriority="high"` + 显式 `width`/`height`
  - 字体用 `font-display: swap`
  - CSS 内联关键样式
- **CLS (Cumulative Layout Shift)** < 0.1
  - 所有 `<img>` / `<svg>` / `<video>` 写明 `width`/`height` 或 aspect-ratio
  - 字体加载不要导致文字位移（用 `size-adjust`）
- **INP (Interaction to Next Paint)** < 200ms
  - JS 拆分；首屏不阻塞
  - 用 `defer` / `async` 加载非关键脚本

### 3.6 Mobile-first
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- 触摸目标 ≥ 44×44px
- 表格在移动端用横向滚动包裹，不要溢出

### 3.7 Bing IndexNow
- 每次发布新页面 / 重大更新后，主动 ping IndexNow API（让 Bing 立即来抓）
- 端点：`https://api.indexnow.org/indexnow?url=https://www.re9guide.it.com/X.html&key=<key>`
- key 文件放在站点根目录（`<key>.txt`，内容是 key 本身）

### 3.8 内容质量（E-E-A-T）
- **Experience（经验）**：作者真实游玩过游戏，attribution 注明 "verified by author on PS5/PC"
- **Expertise（专业度）**：游戏术语准确，引用官方版本号
- **Authoritativeness（权威）**：作者页有 bio + 头像 + 社交链接
- **Trustworthiness（可信）**：日期标记清晰（`datePublished` / `dateModified`），有 contact / privacy / DMCA 法律页

### 3.9 反例（避免做的事）
- ❌ 关键词堆砌 / cloaking / doorway pages
- ❌ 自动翻译（Google Translate）不做人工校对 → 直接被判低质
- ❌ 大量 thin content（< 300 字的水文）
- ❌ 引用不存在的 URL（404 / 软 404）
- ❌ 同一 title / description 重复使用
- ❌ 把社交卡片 PNG 当作正文图

---

## 4. SOP：发布前自检脚本

```bash
cd /path/to/phase-final

# 1. 死链扫描
python3 << 'PY'
import re
from pathlib import Path
d = Path(".")
broken = {}
for f in list(d.glob("*.html")) + list((d/"ko").glob("*.html")):
    txt = f.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r'href="(/?(?:ko/)?[a-z0-9][\w-]*\.html)(?:#[^"]*)?"', txt):
        link = m.group(1); is_ko = f.parent.name == "ko"
        if link.startswith("/"): target = d / link.lstrip("/")
        elif link.startswith("ko/"): target = d / link
        else: target = (d/"ko"/link) if is_ko else (d/link)
        if not target.exists():
            broken.setdefault(str(target.relative_to(d)), []).append(str(f.relative_to(d)))
print(f"{'✓ No broken links' if not broken else f'✗ {len(broken)} broken targets'}")
for k,v in broken.items(): print(f"  {k} ← {len(v)} ref(s)")
PY

# 2. sitemap 完整性检查
python3 -c "
import re
from pathlib import Path
d = Path('.')
miss = []
for m in re.finditer(r'<loc>https://www\.re9guide\.it\.com/([^<]+)</loc>', (d/'sitemap.xml').read_text()):
    p = m.group(1)
    if p and not (d/p).exists(): miss.append(p)
print('✓ sitemap clean' if not miss else f'✗ {len(miss)} sitemap entries point to missing files')
for p in miss: print(f'  {p}')
"

# 3. KO 翻译对齐审计
for f in ko/*.html; do
  bn=$(basename $f)
  if [ -f "$bn" ]; then
    el=$(wc -l <"$bn"); kl=$(wc -l <"$f")
    eh=$(grep -c '<h2' "$bn"); kh=$(grep -c '<h2' "$f")
    flag=""
    [ $el -gt 200 ] && [ $kl -lt $((el / 2)) ] && flag="${flag} ⚠STUB"
    [ "$kh" -lt $((eh - 1)) ] && flag="${flag} SECTIONS!"
    [ -n "$flag" ] && printf "%-50s EN=%d KO=%d h2=%d/%d%s\n" "$bn" "$el" "$kl" "$eh" "$kh" "$flag"
  fi
done

# 4. KO 首页 (영문) 标签是否过期
python3 << 'PY'
import re
from pathlib import Path
d = Path(".")
ko_existing = {f.name for f in (d/"ko").glob("*.html")}
html = (d/"ko"/"index.html").read_text(encoding="utf-8")
stale = []
for m in re.finditer(r'<li><a href="\.\./([a-z][a-z0-9\-]*\.html)">([^<]+?)\s*\(영문\)</a></li>', html):
    if m.group(1) in ko_existing:
        stale.append(m.group(1))
print(f'{"✓ KO index labels current" if not stale else f"✗ {len(stale)} stale (영문) labels (KO exists, label not updated)"}')
for s in stale: print(f"  {s}")
PY
```

四步全绿，才可发布。

---

## 5. 修复执行记录（Changelog）

| 日期 | Phase | Bug | 状态 |
|---|---|---|---|
| 2026-05-19 | 21 | Mr. X SVG 底部框被外 border 裁切 | ✓ 修复（box 上移 30px） |
| 2026-05-19 | 21 | "영문" 应改为 "영어" + KO 已译页签升级 | ✓ 修复（50 处替换 + 10 卡片对齐） |
| 2026-05-19 | 21 | Bing IndexNow 未启用 | ✓ key file + ping 脚本就绪（生产端需部署） |
| 2026-05-19 | 20 | KO index (영문) 标签未同步 | ✓ 修复（12 条更新） |
| 2026-05-19 | 20 | Mr. X KO SVG 边框重叠 | ✓ 修复（沿用 EN 几何） |
| 2026-05-19 | 20 | Victor Gideon EN/KO 图风格不一致 | ✓ 修复（EN 改 inline SVG） |
| 2026-05-18 | 18 | sitemap 引用不存在的 walkthrough 页 | ✓ 修复（删除 sitemap 条目 + index 引用） |
| 2026-05-18 | 18 | mr-raccoon 页 4 条内部死链 | ✓ 修复 |
| 2026-05-18 | 18 | 9 个 KO 页内容是 stub | ✓ 修复（全部重译至对齐） |
| 2026-05-17 | 17 | EN Mr. X 用 PNG，需转 inline SVG | ✓ 修复 |
| 2026-05-17 | 17 | KO 仅 12 页翻译 | ✓ 推进到 36/44 |

---

**维护者**：发布每个 phase 后必须更新本表。文档放在 `/docs/bug-log.md`，不进 sitemap、不公开访问，仅团队内部参考。
