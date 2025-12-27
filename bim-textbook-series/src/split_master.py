#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
split_master.py - MASTER.mdを章ごとのファイルに分割
"""

import sys
from pathlib import Path
from utils import (
    ProjectPaths,
    parse_master_markdown,
    logger,
    create_table_of_contents
)


def split_master_to_chapters():
    """MASTER.mdを章ファイルに分割"""
    paths = ProjectPaths()
    
    # ディレクトリ確保
    paths.ensure_dirs()
    
    # MASTER.mdを解析
    logger.info(f"MASTER.mdを読み込み中: {paths.master_file}")
    vol1_chapters, vol2_chapters = parse_master_markdown(paths.master_file)
    
    # VOL1の章を保存
    logger.info(f"VOL1 (2級対応): {len(vol1_chapters)}章をファイル化")
    for chapter in vol1_chapters:
        output_path = paths.vol1_dir / chapter.filename
        output_path.write_text(chapter.content, encoding='utf-8')
        logger.info(f"  ✓ {chapter.filename} - {chapter.title} ({len(chapter.content)}文字)")
    
    # VOL1の目次を作成
    toc_vol1 = create_table_of_contents(vol1_chapters, "VOL1: BIM利用技術者試験2級対応")
    (paths.vol1_dir / "00_toc.md").write_text(toc_vol1, encoding='utf-8')
    logger.info(f"  ✓ 00_toc.md - 目次")
    
    # VOL2の章を保存
    logger.info(f"VOL2 (準1級対応): {len(vol2_chapters)}章をファイル化")
    for chapter in vol2_chapters:
        output_path = paths.vol2_dir / chapter.filename
        output_path.write_text(chapter.content, encoding='utf-8')
        logger.info(f"  ✓ {chapter.filename} - {chapter.title} ({len(chapter.content)}文字)")
    
    # VOL2の目次を作成
    toc_vol2 = create_table_of_contents(vol2_chapters, "VOL2: BIM利用技術者試験準1級対応")
    (paths.vol2_dir / "00_toc.md").write_text(toc_vol2, encoding='utf-8')
    logger.info(f"  ✓ 00_toc.md - 目次")
    
    # サマリー
    logger.info("=" * 70)
    logger.info("✨ 分割完了！")
    logger.info(f"📚 VOL1 (2級対応): {len(vol1_chapters)}章 → {paths.vol1_dir}")
    logger.info(f"📚 VOL2 (準1級対応): {len(vol2_chapters)}章 → {paths.vol2_dir}")
    logger.info("=" * 70)
    
    return vol1_chapters, vol2_chapters


if __name__ == "__main__":
    try:
        split_master_to_chapters()
    except Exception as e:
        logger.error(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
