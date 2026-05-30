# Index 重复 bug 最终修复包

## 问题
Phase 36 wire 脚本有 bug，在两个 index 都插入了同一条目两次：
- EN index "Trophies & Speedrun" 列: "Difficulty comparison" 重复 2 次
- KO index "입문 / 캐릭터" 列: "난이도 비교" 重复 2 次

## 解决方案
本包只含 2 个文件 — 直接覆盖即可：
- index.html  ← 替换 https://www.re9guide.it.com/index.html
- ko/index.html  ← 替换 https://www.re9guide.it.com/ko/index.html

## 验证
部署后浏览器打开主页 + KO 主页，相关列只应该出现 1 次 "Difficulty comparison" / "난이도 비교"。
