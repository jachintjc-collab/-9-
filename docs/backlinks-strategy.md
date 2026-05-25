# Backlinks 修复策略

Bing Webmaster Tools 报：
> **Moderate severity**: Your site lacks inbound links from high-quality domains.

这是 SEO 长期挑战，**技术上无法快速修**（不能伪造反向链接，否则被搜索引擎惩罚）。
本文档列出 4 周内可执行的具体 outreach 行动，按 ROI 从高到低排序。

---

## 🥇 优先级 1：Reddit（最快见效，48 小时内有效果）

Reddit 帖子的内嵌链接不传递 SEO 权重（rel=nofollow），但：
1. Reddit 自身被 Bing/Google 高度索引 → 你的 URL 出现在 Reddit 帖子里 = 间接被搜索引擎"发现"
2. 真人点进帖子点到你的链接 = referrer traffic（Bing/GSC 都能识别）
3. 一旦点击量大，Reddit 帖子会进 Google search snippets → 自然反向链接增长

**目标 subreddits：**

| Subreddit | 订阅人数 | 发什么 |
|---|---|---|
| r/residentevil | 600k+ | "I made a complete RE9 endings guide — all 8 explained" + 链接到 endings 文章 |
| r/REGames | 80k | "RE9 vs RE8 Village — which should you play first?" + 链接到对比文章 |
| r/ResidentEvil2 | 200k | "RE9 vs RE2 Remake comparison from someone who loves both" + 链接 |
| r/Trophies | 300k | "Full RE9 Platinum trophy roadmap (49 trophies)" + 链接 |
| r/SpeedRun | 200k | "Sub-4-hour RE9 speedrun route + Insanity tips" + 链接 |

**发帖规则（避免被删）：**
- ✓ 70% 在帖子正文给免费价值（贴一段实际内容截图/总结），30% 在末尾留链接 "Full guide here: re9guide.it.com/xxx.html"
- ✓ 选择该 sub 的非高峰时段发（一般周末早上美国时间最优）
- ✗ 不要标题党，不要刷屏
- ✗ 同一篇文章不要 24 小时内发 3 个 sub
- ✗ 一定不要在帖子里 disclose "我建了个网站请帮我推广"

**实际操作（每周 1 次）：**
- 周一发 1 篇 endings → r/residentevil
- 周三发 1 篇 vs RE8 对比 → r/REGames  
- 周五发 1 篇 trophy 指南 → r/Trophies
- 24-48 小时观察评论，回复每个问题（提升你帐号 karma）

---

## 🥈 优先级 2：GameFAQs（中长期 SEO 强烈推动）

GameFAQs 是 Google/Bing 都极度信任的游戏域名，且**允许在指南末尾留外部链接**。

**目标：**
1. https://gamefaqs.gamespot.com/games/resident-evil-requiem 论坛
2. 发布一个简洁的 "FAQ 摘要" 帖子，标题如 "Quick reference: all RE9 safe codes / puzzle solutions"
3. 在末尾留：`Full version + Korean translation: https://www.re9guide.it.com/`
4. GameFAQs 编辑会保留这种内容（如果质量足够），且会出现在 Google "site:gamefaqs.com RE9 safe codes" 搜索

---

## 🥉 优先级 3：Twitter/X（虽小但快）

X 帖子的链接是 nofollow，但被 Google 实时索引（Twitter 数据 feed）。

**操作（每天 1 条）：**
- 每天发一条围绕一个具体游戏问题的 thread（3-5 推）
- thread 第一推：吸引人的问题
- thread 中间几推：实际有用的答案
- thread 最后一推：链接到完整指南

**示例 thread：**
> 🧵 RE9 has 8 endings. Most players only see 2.
> 
> Grace has 4 (True / Bad / Secret / Insanity). Leon has 4 same structure.
> But here's the catch — Leon's True Ending REQUIRES finishing Grace's True first.
> 
> So if you played Leon's campaign first and got "The Hero's End" thinking it was the main ending, surprise: that's actually Leon's BAD ending.
> 
> Full unlock table for all 8: re9guide.it.com/re9-all-endings-explained.html

---

## 优先级 4：与其他 RE 攻略博主交换链接

**找目标：** Google site:youtube.com "RE9 walkthrough", site:medium.com "Resident Evil Requiem"
有大量小型攻略写手发同质内容 → 主动邮件提议 "我引用你的视频，你能在文章里 mention 我的页面吗？"

---

## ❌ 千万不要做的事

| 错误做法 | 后果 |
|---|---|
| 买 Fiverr "100 backlinks for $5" 套餐 | 99% 是 link farm，Google 会反向惩罚 |
| 在不相关论坛 spam 评论留链 | IP 被 marked as spam，长期 SEO 损失 |
| Private Blog Network (PBN) | 这是 Black Hat，会被 manual penalty 永久剔除 |
| 同一文章一天发 5 个 subreddit | Reddit 会 shadow-ban 你 |

---

## 4 周目标

| 周次 | 行动 | 预期 backlinks 增量 |
|---|---|---|
| 第 1 周 | 5 篇 Reddit 帖（不同 sub）+ 1 篇 GameFAQs + 7 条 X thread | 3-5 referring domains |
| 第 2 周 | 5 篇 Reddit + 5 条 X + 邮件联系 3 个 RE youtuber | 5-8 referring domains |
| 第 3 周 | 5 篇 Reddit + Medium / Substack 发完整文章 + 链回主站 | 10-15 referring domains |
| 第 4 周 | 跟进 GSC + BWT 看哪些 URL 已被搜索引擎重新爬取 | 检查 Moderate 警告是否降为 Low |

**当 referring domains 达到 ~20 个高质量域名时，Bing 的 Moderate 警告会自动消失。**

---

## 监控

每周一查：
- **BWT → Backlinks** — 看具体哪些域名链了你
- **GSC → Links → External links** — Google 视角的反向链接
- **Ahrefs Free Webmaster Tools**（免费用 Google Search Console 登录）— 显示完整 backlinks profile
