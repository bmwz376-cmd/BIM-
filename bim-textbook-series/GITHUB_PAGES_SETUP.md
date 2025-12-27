# GitHub Pages セットアップガイド

## 🌐 現在の状態

- **リポジトリURL**: https://github.com/bmwz376-cmd/BIM-
- **GitHub Pages URL**: https://bmwz376-cmd.github.io/BIM-/
- **デプロイ状況**: `gh-pages` ブランチ作成済み ✅

---

## ⚙️ GitHub Pages 有効化手順

### 1. GitHubリポジトリの設定ページを開く

https://github.com/bmwz376-cmd/BIM-/settings/pages

### 2. 設定を確認・変更

以下の設定にしてください：

**Source（ソース）**:
```
Branch: gh-pages
Folder: / (root)
```

設定後、「Save」ボタンをクリック

### 3. デプロイ完了を待つ

通常1～5分で以下のURLにアクセス可能になります：

**🌐 https://bmwz376-cmd.github.io/BIM-/**

---

## 📊 確認方法

### デプロイ状況の確認

1. リポジトリのActionsタブを開く：
   https://github.com/bmwz376-cmd/BIM-/actions

2. 「pages build and deployment」ワークフローを確認
   - ✅ 緑色のチェックマーク → デプロイ成功
   - 🔴 赤色のバツマーク → デプロイ失敗（エラー確認）

### サイトアクセステスト

数分後、以下のURLにアクセス：

```
https://bmwz376-cmd.github.io/BIM-/
```

正常な場合、MkDocs Materialのサイトが表示されます。

---

## 🔄 再デプロイ方法

### 方法1: GitHub Actionsで自動デプロイ

既に設定済みの`.github/workflows/build.yml`により、`main`ブランチへのpushで自動デプロイされます：

```bash
git add .
git commit -m "更新内容"
git push origin main
```

### 方法2: ローカルから手動デプロイ

```bash
cd /home/user/webapp/bim-textbook-series
mkdocs gh-deploy --force
```

---

## ❌ トラブルシューティング

### 404エラーが出る場合

**原因1**: GitHub Pages設定が有効化されていない
- **解決**: 上記「GitHub Pages 有効化手順」を実施

**原因2**: デプロイ完了前にアクセスしている
- **解決**: 5分ほど待ってから再度アクセス

**原因3**: `gh-pages`ブランチが存在しない
- **解決**: `mkdocs gh-deploy --force` を実行

### デプロイは成功しているのに404が出る場合

リポジトリ設定を確認：

1. https://github.com/bmwz376-cmd/BIM-/settings/pages
2. 「Source」が `gh-pages` / `/` (root) になっているか確認
3. 「Enforce HTTPS」がONになっているか確認

---

## 🎯 正常動作時の表示内容

以下のページが表示されます：

- **ホーム**: BIM利用技術者試験 教科書シリーズ
- **VOL1**: 2級対応（7章）
- **VOL2**: 準1級対応（6章）
- **図表一覧**: 15種類のPNG図表
- **ダウンロード**: PDF/PPTX配布

---

## 📝 メモ

- 初回デプロイは`mkdocs gh-deploy --force`で手動実行済み
- 以降はGitHub Actionsで自動デプロイ
- `gh-pages`ブランチは自動生成（手動編集不要）
- サイト更新は`main`ブランチにpushするだけでOK

---

**最終更新**: 2024年12月27日  
**ステータス**: デプロイ完了待ち（GitHub Pages設定確認中）
