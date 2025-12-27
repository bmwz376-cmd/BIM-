#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf_build.py - Markdown原稿からPDF生成（日本語対応版）
"""

import sys
from pathlib import Path
import markdown2
from weasyprint import HTML, CSS
import re

from utils import ProjectPaths, logger


class PDFBuilder:
    """PDF生成クラス（日本語対応・WeasyPrint版）"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # CSSスタイル
        self.css_style = """
        @page {
            size: A4;
            margin: 25mm 20mm;
            @top-center {
                content: "BIM利用技術者試験 教科書";
                font-size: 10pt;
                color: #666;
            }
            @bottom-center {
                content: counter(page);
                font-size: 10pt;
            }
        }
        
        body {
            font-family: "Noto Sans JP", "Hiragino Kaku Gothic Pro", "ヒラギノ角ゴ Pro", 
                         "Meiryo", "メイリオ", sans-serif;
            font-size: 11pt;
            line-height: 1.8;
            color: #333;
        }
        
        h1 {
            font-size: 24pt;
            color: #2E4053;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 20px;
            page-break-after: avoid;
        }
        
        h2 {
            font-size: 18pt;
            color: #1F618D;
            margin-top: 25px;
            margin-bottom: 15px;
            page-break-after: avoid;
        }
        
        h3 {
            font-size: 14pt;
            color: #2874A6;
            margin-top: 20px;
            margin-bottom: 12px;
        }
        
        h4 {
            font-size: 12pt;
            color: #34495e;
            margin-top: 15px;
            margin-bottom: 10px;
        }
        
        p {
            margin: 8px 0;
            text-align: justify;
        }
        
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Courier New", Consolas, monospace;
            font-size: 10pt;
        }
        
        pre {
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-left: 3px solid #3498db;
            padding: 12px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 10pt;
            line-height: 1.4;
            page-break-inside: avoid;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-left: 0;
            color: #555;
            font-style: italic;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            page-break-inside: avoid;
        }
        
        th {
            background-color: #3498db;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: bold;
        }
        
        td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        ul, ol {
            margin: 10px 0;
            padding-left: 25px;
        }
        
        li {
            margin: 5px 0;
        }
        
        .cover-page {
            text-align: center;
            padding-top: 100px;
        }
        
        .cover-title {
            font-size: 32pt;
            font-weight: bold;
            color: #2E4053;
            margin-bottom: 30px;
        }
        
        .cover-subtitle {
            font-size: 18pt;
            color: #555;
            margin-bottom: 50px;
        }
        
        .chapter-break {
            page-break-before: always;
        }
        """
    
    def markdown_to_html(self, md_content: str) -> str:
        """Markdown→HTML変換（日本語対応）"""
        # markdown2で変換（日本語対応）
        html = markdown2.markdown(
            md_content,
            extras=[
                'tables',
                'fenced-code-blocks',
                'strike',
                'task_list',
                'header-ids'
            ]
        )
        return html
    
    def build_pdf(self, volume_name: str, manuscript_dir: Path):
        """PDFを生成（日本語対応）"""
        output_file = self.output_dir / f"{volume_name}.pdf"
        
        # HTMLコンテンツを構築
        html_parts = []
        
        # 表紙
        if "vol1" in volume_name:
            title = "BIM利用技術者試験2級対応"
            subtitle = "教科書"
        else:
            title = "BIM利用技術者試験準1級対応"
            subtitle = "教科書"
        
        html_parts.append(f'''
        <div class="cover-page">
            <div class="cover-title">{title}</div>
            <div class="cover-subtitle">{subtitle}</div>
            <p style="font-size: 14pt; color: #777;">
                BIM教育チーム 編<br>
                Version 1.0.0
            </p>
        </div>
        <div class="chapter-break"></div>
        ''')
        
        # 目次
        toc_file = manuscript_dir / "00_toc.md"
        if toc_file.exists():
            toc_content = toc_file.read_text(encoding='utf-8')
            html_parts.append(self.markdown_to_html(toc_content))
            html_parts.append('<div class="chapter-break"></div>')
        
        # 各章を追加
        chapter_files = sorted(manuscript_dir.glob("chapter_*.md"))
        for chapter_file in chapter_files:
            logger.info(f"  処理中: {chapter_file.name}")
            content = chapter_file.read_text(encoding='utf-8')
            html = self.markdown_to_html(content)
            html_parts.append(html)
            html_parts.append('<div class="chapter-break"></div>')
        
        # 完全なHTML
        full_html = f'''
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>{self.css_style}</style>
        </head>
        <body>
            {"".join(html_parts)}
        </body>
        </html>
        '''
        
        # WeasyPrintでPDF生成
        HTML(string=full_html, base_url=str(manuscript_dir)).write_pdf(
            str(output_file)
        )
        
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
