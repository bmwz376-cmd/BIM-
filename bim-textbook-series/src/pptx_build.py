#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pptx_build.py - Markdown原稿からPPTX（スライド）生成
"""

import sys
import re
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

from utils import ProjectPaths, logger


class PPTXBuilder:
    """PPTX生成クラス"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_title_slide(self, prs: Presentation, title: str, subtitle: str = ""):
        """タイトルスライド作成"""
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        
        title_shape = slide.shapes.title
        subtitle_shape = slide.placeholders[1]
        
        title_shape.text = title
        if subtitle:
            subtitle_shape.text = subtitle
        
        return slide
    
    def create_content_slide(self, prs: Presentation, title: str, content: str):
        """コンテンツスライド作成"""
        bullet_slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(bullet_slide_layout)
        
        shapes = slide.shapes
        title_shape = shapes.title
        body_shape = shapes.placeholders[1]
        
        title_shape.text = title
        
        # コンテンツを箇条書きに
        tf = body_shape.text_frame
        lines = content.split('\n')[:10]  # 最大10行
        for line in lines:
            if line.strip():
                p = tf.add_paragraph()
                p.text = line.strip()[:100]  # 最大100文字
                p.level = 0
        
        return slide
    
    def build_pptx(self, volume_name: str, manuscript_dir: Path):
        """PPTXを生成"""
        output_file = self.output_dir / f"{volume_name}.pptx"
        
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        
        # 表紙
        if "vol1" in volume_name:
            title = "BIM利用技術者試験2級対応"
            subtitle = "教科書・講義スライド"
        else:
            title = "BIM利用技術者試験準1級対応"
            subtitle = "教科書・講義スライド"
        
        self.create_title_slide(prs, title, subtitle)
        
        # 各章からスライド作成
        chapter_files = sorted(manuscript_dir.glob("chapter_*.md"))
        for chapter_file in chapter_files:
            logger.info(f"  処理中: {chapter_file.name}")
            content = chapter_file.read_text(encoding='utf-8')
            
            # 章タイトル抽出
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if title_match:
                chapter_title = title_match.group(1)
            else:
                chapter_title = chapter_file.stem
            
            # セクションごとにスライド作成
            sections = re.split(r'####\s+', content)[1:6]  # 最大5セクション
            for section in sections:
                lines = section.split('\n')
                section_title = lines[0] if lines else "内容"
                section_content = '\n'.join(lines[1:20])  # 最大20行
                
                self.create_content_slide(
                    prs,
                    f"{chapter_title} - {section_title}",
                    section_content
                )
        
        # 保存
        prs.save(str(output_file))
        logger.info(f"✅ PPTX生成完了: {output_file}")
        return output_file


def build_all_pptx():
    """すべてのPPTXを生成"""
    paths = ProjectPaths()
    paths.ensure_dirs()
    
    builder = PPTXBuilder(paths.dist)
    
    # VOL1 (2級)
    logger.info("VOL1 (2級対応) PPTX生成中...")
    pptx1 = builder.build_pptx("vol1_2kyu", paths.vol1_dir)
    
    # VOL2 (準1級)
    logger.info("VOL2 (準1級対応) PPTX生成中...")
    pptx2 = builder.build_pptx("vol2_jun1kyu", paths.vol2_dir)
    
    logger.info("=" * 70)
    logger.info("✨ PPTX生成完了")
    logger.info(f"📊 VOL1: {pptx1}")
    logger.info(f"📊 VOL2: {pptx2}")
    logger.info("=" * 70)


if __name__ == "__main__":
    try:
        build_all_pptx()
    except Exception as e:
        logger.error(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
