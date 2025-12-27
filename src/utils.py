#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIM利用技術者試験 教科書シリーズ - ユーティリティモジュール
"""

import os
import re
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProjectPaths:
    """プロジェクトのパス管理"""
    
    def __init__(self, root_dir: Optional[Path] = None):
        if root_dir is None:
            # スクリプトの場所から推測
            self.root = Path(__file__).parent.parent
        else:
            self.root = Path(root_dir)
        
        self.src = self.root / "src"
        self.manuscript = self.root / "manuscript"
        self.assets = self.root / "assets"
        self.figs = self.assets / "figs"
        self.dist = self.root / "dist"
        self.master_file = self.root / "MASTER.md"
        
        # VOL別ディレクトリ
        self.vol1_dir = self.manuscript / "vol1_2kyu"
        self.vol2_dir = self.manuscript / "vol2_jun1kyu"
    
    def ensure_dirs(self):
        """必要なディレクトリを作成"""
        for dir_path in [
            self.manuscript,
            self.vol1_dir,
            self.vol2_dir,
            self.figs,
            self.dist
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)
        logger.info("ディレクトリ構造を確認しました")


class ChapterInfo:
    """章情報を管理するクラス"""
    
    def __init__(self, volume: str, chapter_num: int, title: str, content: str):
        self.volume = volume  # "VOL1" or "VOL2"
        self.chapter_num = chapter_num
        self.title = title
        self.content = content
        self.filename = f"chapter_{chapter_num:02d}.md"
    
    def __repr__(self):
        return f"<Chapter {self.volume}-{self.chapter_num}: {self.title}>"


def parse_master_markdown(master_path: Path) -> Tuple[List[ChapterInfo], List[ChapterInfo]]:
    """
    MASTER.mdを解析してVOL1とVOL2の章に分割
    
    Returns:
        (vol1_chapters, vol2_chapters)
    """
    if not master_path.exists():
        raise FileNotFoundError(f"MASTER.md が見つかりません: {master_path}")
    
    content = master_path.read_text(encoding='utf-8')
    
    vol1_chapters = []
    vol2_chapters = []
    
    # VOLセクションで分割
    vol_pattern = r'## (VOL\d+):\s*(.+?)(?=## VOL\d+:|## 付録|---END_OF_MASTER---|$)'
    vol_matches = re.finditer(vol_pattern, content, re.DOTALL)
    
    for vol_match in vol_matches:
        vol_name = vol_match.group(1)  # "VOL1" or "VOL2"
        vol_content = vol_match.group(2).strip()
        
        # 章で分割（新フォーマット対応）
        chapter_pattern = r'### 第(\d+)章｜(.+?)\n(.*?)(?=---CHAPTER_END---|### 第\d+章｜|## VOL\d+:|## 付録|$)'
        chapter_matches = re.finditer(chapter_pattern, vol_content, re.DOTALL)
        
        for chapter_match in chapter_matches:
            chapter_num = int(chapter_match.group(1))
            chapter_title = chapter_match.group(2).strip()
            chapter_content = chapter_match.group(3).strip()
            
            # 章の完全なコンテンツ（タイトル含む）
            full_content = f"# 第{chapter_num}章｜{chapter_title}\n\n{chapter_content}"
            
            chapter_info = ChapterInfo(
                volume=vol_name,
                chapter_num=chapter_num,
                title=chapter_title,
                content=full_content
            )
            
            if vol_name == "VOL1":
                vol1_chapters.append(chapter_info)
            elif vol_name == "VOL2":
                vol2_chapters.append(chapter_info)
    
    logger.info(f"VOL1: {len(vol1_chapters)}章, VOL2: {len(vol2_chapters)}章を検出")
    
    return vol1_chapters, vol2_chapters


def extract_figure_references(content: str) -> List[str]:
    """
    マークダウンから図の参照を抽出
    
    例: ![FIG:cad_vs_bim]()
    → "cad_vs_bim"
    """
    pattern = r'!\[FIG:(\w+)\]\(\)'
    matches = re.findall(pattern, content)
    return list(set(matches))  # 重複を除去


def get_all_figure_references(chapters: List[ChapterInfo]) -> List[str]:
    """全章から図の参照を抽出"""
    all_refs = []
    for chapter in chapters:
        refs = extract_figure_references(chapter.content)
        all_refs.extend(refs)
    return list(set(all_refs))


def format_file_size(size_bytes: int) -> str:
    """ファイルサイズを人間が読みやすい形式に"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def create_table_of_contents(chapters: List[ChapterInfo], volume_name: str) -> str:
    """目次を生成"""
    toc = f"# {volume_name} - 目次\n\n"
    for chapter in chapters:
        toc += f"{chapter.chapter_num}. {chapter.title}\n"
    return toc


def sanitize_filename(filename: str) -> str:
    """ファイル名から不正な文字を除去"""
    # Windowsで使えない文字を除去
    invalid_chars = r'[<>:"/\\|?*｜]'
    return re.sub(invalid_chars, '_', filename)


def get_project_info() -> Dict[str, str]:
    """プロジェクト情報を取得"""
    return {
        'name': 'BIM利用技術者試験 教科書シリーズ',
        'version': '1.0.0',
        'description': 'BIM利用技術者試験2級・準1級対応教科書',
        'author': 'BIM教育チーム',
        'license': 'MIT'
    }


if __name__ == "__main__":
    # テスト実行
    paths = ProjectPaths()
    print(f"プロジェクトルート: {paths.root}")
    print(f"MASTER.md: {paths.master_file}")
    
    if paths.master_file.exists():
        vol1, vol2 = parse_master_markdown(paths.master_file)
        print(f"\nVOL1: {len(vol1)}章")
        for ch in vol1:
            print(f"  - {ch}")
        print(f"\nVOL2: {len(vol2)}章")
        for ch in vol2:
            print(f"  - {ch}")
        
        # 図の参照を抽出
        all_figs = get_all_figure_references(vol1 + vol2)
        print(f"\n必要な図: {len(all_figs)}個")
        for fig in sorted(all_figs):
            print(f"  - {fig}")
