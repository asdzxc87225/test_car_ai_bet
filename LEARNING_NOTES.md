# GitHub 學習與練習紀錄（LEARNING_NOTES.md）

## 📌 2024-05-04 練習 Pull Request 流程
- 建立 feature 分支：feature/test-pr-practice
- 小改動（加一行註解）
- push → PR → Review → Merge
- 學到：
  - PR 描述中加上 `Closes #X` 可以自動關閉 Issue
  - Merge 後記得 git pull 更新本地 dev

## 📌 2024-05-04 練習 Milestone 建立
- 建立 v1.1 里程碑
- 把資料中心重構、Q表擴充兩個 Issue 加進去
- 學到：
  - Milestone 可以追蹤進度，超有成就感！

## 📌 2024-05-04 遇到的錯誤紀錄
- `error: src refspec xxx does not match any`
  - 原因：分支名打錯 or 沒有 commit
  - 解法：確定分支存在，且至少有一次 commit 再 push！

## 📌 Git 基本指令筆記
```bash
# 建立 feature 分支
git checkout dev
git checkout -b feature/xxx

# 上傳 feature 分支
git push -u origin feature/xxx

