#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py - BIM教科書シリーズ 一括ビルドスクリプト

1コマンドで以下を実行:
1. MASTER.mdを分割 → manuscript/
2. 図を自動生成 → assets/figs/
3. PDF/PPTXを生成 → dist/
"""

import sys
import time
from pathlib import Path

# 同じディレクトリのモジュールをインポート
from utils import ProjectPaths, logger, get_project_info
from split_master import split_master_to_chapters
from diagrams import generate_all_diagrams
from pdf_build import build_all_pdfs
from pptx_build import build_all_pptx


def print_banner():
    """バナー表示"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     BIM利用技術者試験 教科書シリーズ - 自動生成システム     ║
║                                                              ║
║         2級・準1級対応教材を1コマンドで完全生成              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)
    
    info = get_project_info()
    print(f"プロジェクト: {info['name']}")
    print(f"バージョン: {info['version']}")
    print(f"説明: {info['description']}")
    print()


def main():
    """メインビルド処理"""
    start_time = time.time()
    
    print_banner()
    
    try:
        # 1. 原稿分割
        logger.info("=" * 70)
        logger.info("STEP 1/4: MASTER.md を章ファイルに分割")
        logger.info("=" * 70)
        vol1_chapters, vol2_chapters = split_master_to_chapters()
        logger.info(f"✅ 分割完了: VOL1={len(vol1_chapters)}章, VOL2={len(vol2_chapters)}章\n")
        
        # 2. 図生成
        logger.info("=" * 70)
        logger.info("STEP 2/4: 図表を自動生成")
        logger.info("=" * 70)
        fig_count = generate_all_diagrams()
        logger.info(f"✅ 図生成完了: {fig_count}個\n")
        
        # 3. PDF生成
        logger.info("=" * 70)
        logger.info("STEP 3/4: PDF教科書を生成")
        logger.info("=" * 70)
        build_all_pdfs()
        logger.info("✅ PDF生成完了\n")
        
        # 4. PPTX生成
        logger.info("=" * 70)
        logger.info("STEP 4/4: PPTXスライドを生成")
        logger.info("=" * 70)
        build_all_pptx()
        logger.info("✅ PPTX生成完了\n")
        
        # 完了メッセージ
        elapsed_time = time.time() - start_time
        
        print()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                                                              ║")
        print("║                    🎉 ビルド完了！ 🎉                       ║")
        print("║                                                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        
        paths = ProjectPaths()
        
        print("📦 生成された成果物:")
        print()
        print("📄 原稿 (Markdown):")
        print(f"   • {paths.vol1_dir}/ - VOL1 (2級対応) 章ファイル")
        print(f"   • {paths.vol2_dir}/ - VOL2 (準1級対応) 章ファイル")
        print()
        print("🖼️  図表 (PNG):")
        print(f"   • {paths.figs}/ - 自動生成された図 ({fig_count}個)")
        print()
        print("📚 成果物:")
        print(f"   • {paths.dist}/vol1_2kyu.pdf - 2級教科書 (PDF)")
        print(f"   • {paths.dist}/vol2_jun1kyu.pdf - 準1級教科書 (PDF)")
        print(f"   • {paths.dist}/vol1_2kyu.pptx - 2級スライド (PPTX)")
        print(f"   • {paths.dist}/vol2_jun1kyu.pptx - 準1級スライド (PPTX)")
        print()
        print(f"⏱️  処理時間: {elapsed_time:.2f}秒")
        print()
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ ビルド中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
