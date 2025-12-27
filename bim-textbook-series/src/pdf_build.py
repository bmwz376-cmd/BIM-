#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf_build.py - Markdown原稿からPDF生成
"""

import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

from utils import ProjectPaths, logger


class PDFBuilder:
    """PDF生成クラス"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # スタイル設定
        self.styles = getSampleStyleSheet()
        self.setup_styles()
    
    def setup_styles(self):
        """スタイル設定"""
        # タイトルスタイル
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#2E4053'),
            spaceAfter=30,
            alignment=1  # 中央揃え
        ))
        
        # 見出しスタイル
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1F618D'),
            spaceBefore=20,
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2874A6'),
            spaceBefore=15,
            spaceAfter=10
        ))
    
    def markdown_to_text(self, md_content: str) -> str:
        """簡易Markdown→テキスト変換"""
        # ヘッダーを除去
        text = re.sub(r'^#+\s+', '', md_content, flags=re.MULTILINE)
        # コードブロックをシンプル化
        text = re.sub(r'```[\s\S]*?```', '[コード省略]', text)
        # リストマーカーを整理
        text = re.sub(r'^\s*[-*]\s+', '• ', text, flags=re.MULTILINE)
        return text
    
    def build_pdf(self, volume_name: str, manuscript_dir: Path):
        """PDFを生成"""
        output_file = self.output_dir / f"{volume_name}.pdf"
        
        # SimpleDocTemplateを使用
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=A4,
            topMargin=20*mm,
            bottomMargin=20*mm,
            leftMargin=25*mm,
            rightMargin=25*mm
        )
        
        story = []
        
        # 表紙
        title = f"BIM利用技術者試験 教科書\n{volume_name}"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 30*mm))
        story.append(PageBreak())
        
        # 各章を追加
        chapter_files = sorted(manuscript_dir.glob("chapter_*.md"))
        for chapter_file in chapter_files:
            logger.info(f"  処理中: {chapter_file.name}")
            content = chapter_file.read_text(encoding='utf-8')
            
            # 簡易変換（実際にはmarkdown2などを使用すべき）
            text = self.markdown_to_text(content)
            story.append(Paragraph(text[:500] + "...", self.styles['BodyText']))
            story.append(PageBreak())
        
        # PDF生成
        doc.build(story)
        logger.info(f"✅ PDF生成完了: {output_file}")
        return output_file


def build_all_pdfs():
    """すべてのPDFを生成"""
    paths = ProjectPaths()
    paths.ensure_dirs()
    
    builder = PDFBuilder(paths.dist)
    
    # VOL1 (2級)
    logger.info("VOL1 (2級対応) PDF生成中...")
    pdf1 = builder.build_pdf("vol1_2kyu", paths.vol1_dir)
    
    # VOL2 (準1級)
    logger.info("VOL2 (準1級対応) PDF生成中...")
    pdf2 = builder.build_pdf("vol2_jun1kyu", paths.vol2_dir)
    
    logger.info("=" * 70)
    logger.info("✨ PDF生成完了")
    logger.info(f"📄 VOL1: {pdf1}")
    logger.info(f"📄 VOL2: {pdf2}")
    logger.info("=" * 70)


if __name__ == "__main__":
    try:
        build_all_pdfs()
    except Exception as e:
        logger.error(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
