#!/bin/bash
# BIM教科書 図解自動デプロイスクリプト
# 使用方法: ./scripts/deploy_diagrams.sh

set -e

WORK_DIR="/home/user/webapp/bim-textbook-series"
FIGS_DIR="$WORK_DIR/assets/figs"
DOCS_FIGS_DIR="$WORK_DIR/docs/assets/figs"

echo "🚀 BIM教科書 図解デプロイスクリプト"
echo "======================================"

# ディレクトリ確認
echo "📁 ディレクトリ確認..."
if [ ! -d "$FIGS_DIR" ]; then
    echo "❌ エラー: $FIGS_DIR が存在しません"
    exit 1
fi

if [ ! -d "$DOCS_FIGS_DIR" ]; then
    echo "📂 $DOCS_FIGS_DIR を作成します"
    mkdir -p "$DOCS_FIGS_DIR"
fi

# 図表ファイル一覧
DIAGRAMS=(
    "cad_vs_bim.png"
    "info_layers.png"
    "lifecycle_flow.png"
    "lod_matrix.png"
    "element_structure.png"
    "openbim_ifc.png"
    "4d_5d_bim.png"
    "bep_flow.png"
    "worksharing_concept.png"
    "family_hierarchy_detail.png"
    "clash_detection.png"
    "ng_ok_level_mistake.png"
    "level_mistake_detail.png"
    "wall_mistake_patterns.png"
    "floor_mistake_examples.png"
)

# ファイルコピー
echo ""
echo "📋 図表ファイルをコピー..."
COPIED=0
MISSING=0

for diagram in "${DIAGRAMS[@]}"; do
    SOURCE="$FIGS_DIR/$diagram"
    DEST="$DOCS_FIGS_DIR/$diagram"
    
    if [ -f "$SOURCE" ]; then
        cp "$SOURCE" "$DEST"
        echo "  ✅ $diagram"
        COPIED=$((COPIED + 1))
    else
        echo "  ⚠️  $diagram (未作成)"
        MISSING=$((MISSING + 1))
    fi
done

echo ""
echo "======================================"
echo "📊 コピー結果"
echo "  成功: $COPIED / ${#DIAGRAMS[@]}"
echo "  未作成: $MISSING / ${#DIAGRAMS[@]}"

# Git操作
if [ $COPIED -gt 0 ]; then
    echo ""
    echo "📦 Gitにコミット..."
    cd "$WORK_DIR"
    git add assets/figs/*.png docs/assets/figs/*.png
    
    # コミットメッセージ
    COMMIT_MSG="feat: 外部ツールで作成した高品質図解を追加 ($COPIED/$((${#DIAGRAMS[@]})))"
    git commit -m "$COMMIT_MSG" || echo "⚠️  コミットするファイルがありません"
    
    echo ""
    echo "🚀 GitHubにプッシュ..."
    git push origin main
    
    echo ""
    echo "🌐 MkDocsサイトをビルド..."
    mkdocs build --clean
    
    echo ""
    echo "🎉 デプロイ完了！"
    echo ""
    echo "📍 公開URL:"
    echo "   https://bmwz376-cmd.github.io/BIM-/figures/"
    echo ""
else
    echo ""
    echo "⚠️  コピーされたファイルがないため、デプロイはスキップされました"
fi

echo ""
echo "✅ スクリプト実行完了"
