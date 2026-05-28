# KO 部署补丁包 (Phase 33-38)

## 问题诊断

线上验证发现：
- **EN 端：99% 已部署**，含 Phase 27-38 所有内容（修复了 1 个 Trophies 列重复 bug）
- **KO 端：严重落后 6 个 Phase**，停留在 Phase 30/32 时代

**线上 KO 当前缺失：**
- 10 个 KO 文章页面
- KO index.html 缺整个 "스토리 & LORE" section
- KO index 缺多个 NEW 入口（NG+, Difficulty, vs RE7, Mia Featured 等）

**根本原因：** 之前部署 Phase 33-38 时只覆盖了 EN 文件（根目录），KO 文件夹没同步更新。

---

## 修复指南

### 步骤 1：覆盖根目录文件
把这些文件覆盖到站点根目录：
- index.html  (修复了 Trophies 列重复 bug)
- sitemap.xml (121 个 URL)
- robots.txt
- 14 个 EN 页面（含 Phase 33-38 的 CTA 反链更新）

### 步骤 2：覆盖 KO 文件夹（关键！）
把 ko/ 文件夹完整内容覆盖到站点的 ko/ 目录：

新增 10 个 KO 页面（之前从未部署过）：
- ko/mia-winters-re9-re7-connection.html
- ko/ada-wong-re9-reversal-arc.html
- ko/eveline-re9-foreshadowing-explained.html
- ko/bsaa-re9-new-direction.html
- ko/chunk-origin-mystery-explained.html
- ko/re9-new-game-plus-complete-guide.html
- ko/re9-hidden-easter-eggs-list.html
- ko/re9-difficulty-comparison-which-to-play.html
- ko/re9-vs-re7-biohazard-which-to-play.html
- ko/eveline-character-profile-complete.html

更新 1 个 KO 页面：
- ko/index.html  (完整结构 + 스토리 & LORE 7 entries)

### 步骤 3：验证部署成功
浏览器打开这些应该都正常：
- https://www.re9guide.it.com/ko/index.html  (拉到下面应该有 스토리 & LORE section)
- https://www.re9guide.it.com/ko/mia-winters-re9-re7-connection.html  (不再弹「한국어판 준비 중」)
- https://www.re9guide.it.com/ko/eveline-character-profile-complete.html
- https://www.re9guide.it.com/ko/re9-new-game-plus-complete-guide.html

### 步骤 4：IndexNow ping
部署后用 ping-all-new.sh 推送所有新 KO URL 给 Bing。

---

## 长期防止再发生

部署时务必同时上传 EN 和 KO 两个文件夹。
推荐用 rsync -av phase[N]-final/ /var/www/ 一次覆盖整个目录树。
