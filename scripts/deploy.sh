#!/bin/bash
# BIM教科書 GitHub Pagesデプロイスクリプト
# .nojekyllを確実に含めてデプロイ

set -e

WORK_DIR="/home/user/webapp/bim-textbook-series"

echo "🚀 BIM教科書 GitHub Pagesデプロイ"
echo "====================================="

cd "$WORK_DIR"

echo "📦 MkDocsビルド中..."
mkdocs build --clean

echo "📝 .nojekyllファイルを追加..."
touch site/.nojekyll

echo "🌐 GitHub Pagesにデプロイ中..."
ghp-import -n -p -f site

echo ""
echo "✅ デプロイ完了！"
echo ""
echo "📍 公開URL:"
echo "   日本語: https://bmwz376-cmd.github.io/BIM-/"
echo "   English: https://bmwz376-cmd.github.io/BIM-/en/"
echo ""
echo "⏳ GitHub Pagesの反映には2-3分かかります"
