# Bing IndexNow 急救包

## 问题诊断

Bing Webmaster Tools 报：
- 🔴 High severity: "Learn how IndexNow boosts site visibility with easy setup"
- "用户未经授权" 出现在 URL Submission / Block URLs 页面

## 根本原因

IndexNow key 文件 (`cebd0f739339490594ae3738f31b5ed0.txt`) 已上传到站点根目录，
但 **IndexNow API 从未被调用过**。Bing 只把"调用过 API 一次以上"的站点视为
IndexNow-active，所以发出 High 警告 + 限制其他写操作功能。

## 修复步骤（按顺序执行）

### 1. 部署更新后的 robots.txt
本包内有更新的 `robots.txt`，新增了 IndexNow key 文件位置声明。
覆盖部署到 `https://www.re9guide.it.com/robots.txt`。

### 2. 确认 key 文件可访问
浏览器打开：
```
https://www.re9guide.it.com/cebd0f739339490594ae3738f31b5ed0.txt
```
应该看到一行：`cebd0f739339490594ae3738f31b5ed0`

如果 404，把本包内的同名文件也上传到站点根目录。

### 3. 执行 IndexNow 一键 ping（关键步骤！）
本包内的 `ping-all-new.sh` 会一次性推送 15 个 URL（Phase 27/28/29 全部新页 + index + sitemap）给 Bing/Yandex IndexNow 端点。

```bash
chmod +x ping-all-new.sh
./ping-all-new.sh
```

期望输出：`✓ HTTP 200` 或 `✓ HTTP 202`。

### 4. 等待 24-48 小时
Bing 收到 IndexNow 调用后会：
- 验证 key 文件
- 把你的站点标记为 "IndexNow active"
- 移除 BWT Suggestions 页面的 High 警告
- 解除 "用户未经授权" 状态
- 开始爬取本批 URL

### 5. 验证修复成功
24-48 小时后回到 Bing Webmaster Tools：
- "建议" 页面应该不再有 IndexNow High 警告
- "URL Submission" 应该显示配额数字而不是 "用户未经授权"
- "搜索性能" 页面 3-7 天内开始有 impression 增长

## 关于第 2 个 Moderate 警告

> "Your site lacks inbound links from high-quality domains"

这是反向链接问题，**短期没法靠技术修复**。长期方案：
- 在 Reddit r/residentevil, r/REGames 发优质内容时附上指向具体页面的链接
- 在 GameFAQs 评论留 URL（被允许的板块）
- 与其他独立 RE 攻略博主交换友情链接
- Twitter/X 发 thread 时把 URL 放进去（少量 backlinks 但 indexable）

这部分不在本包修复范围。

## 文件清单

- `robots.txt` — 更新后的版本（新增 IndexNow key 位置注释）
- `cebd0f739339490594ae3738f31b5ed0.txt` — IndexNow key 文件（备份）
- `ping-all-new.sh` — 一键 ping 15 个 URL 的脚本
- `README-bing-fix.md` — 本文档
