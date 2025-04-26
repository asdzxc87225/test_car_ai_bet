# 開發規範與流程（DEVELOPMENT.md）

## 分支命名規則
- `main`：穩定版（只放已發佈功能）
- `dev`：開發版（所有功能在這裡整合）
- `feature/功能名稱`：開發新功能用
- `bugfix/錯誤名稱`：修 Bug 用

## Pull Request 規則
1. 從 `dev` 分支開 feature/xxx 分支
2. 完成功能後開 PR，base: dev，compare: feature/xxx
3. PR 描述中標註關聯 Issue，例如：`Closes #5`
4. 自我 Review，確認沒問題後 Merge

## Label 使用規則
- `feature`：新增功能
- `bug`：錯誤修正
- `refactor`：重構優化
- `discussion`：設計討論事項

## Milestone 規劃
- 每個版本（如 v1.1）建一個 Milestone
- 將相關 Issue 加入 Milestone，追蹤完成進度

## Release 流程
- 重大功能開發完成後，打 Release（Tag）
- 發佈版號如：v1.1、v1.2
- 更新 CHANGELOG.md

