#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diagrams.py - BIM教科書用図表の自動生成
"""

import sys
import matplotlib
matplotlib.use('Agg')  # GUIなし環境対応
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
import numpy as np

from utils import (
    ProjectPaths,
    parse_master_markdown,
    get_all_figure_references,
    logger
)

# 日本語フォント設定
try:
    import japanize_matplotlib
    japanize_matplotlib.japanize()
except ImportError:
    # japanize-matplotlibがない場合のフォールバック
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'sans-serif']

plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['figure.figsize'] = (10, 6)


class DiagramGenerator:
    """図表生成クラス"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all(self, figure_refs: list):
        """すべての図を生成"""
        logger.info(f"図表生成開始: {len(figure_refs)}個")
        
        for fig_ref in sorted(figure_refs):
            method_name = f"generate_{fig_ref}"
            if hasattr(self, method_name):
                logger.info(f"  生成中: {fig_ref}.png")
                method = getattr(self, method_name)
                method()
            else:
                logger.warning(f"  ⚠️  未実装: {fig_ref}")
                self.generate_placeholder(fig_ref)
        
        logger.info("図表生成完了")
    
    def generate_placeholder(self, fig_ref: str):
        """プレースホルダー図を生成"""
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(0.5, 0.5, f"図: {fig_ref}\n（自動生成予定）", 
                ha='center', va='center', fontsize=14,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        output_path = self.output_dir / f"{fig_ref}.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    # ========== VOL1: 2級対応 ==========
    
    def generate_cad_vs_bim(self):
        """CAD vs BIM比較図"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # CAD側
        ax1.set_title('従来のCAD', fontsize=14, fontweight='bold')
        ax1.text(0.5, 0.8, '平面図', ha='center', fontsize=12,
                bbox=dict(boxstyle='round', facecolor='lightblue'))
        ax1.text(0.5, 0.5, '立面図', ha='center', fontsize=12,
                bbox=dict(boxstyle='round', facecolor='lightblue'))
        ax1.text(0.5, 0.2, '断面図', ha='center', fontsize=12,
                bbox=dict(boxstyle='round', facecolor='lightblue'))
        ax1.text(0.5, 0.05, '（個別に作図・管理）', ha='center', fontsize=10, style='italic')
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        
        # BIM側
        ax2.set_title('BIM', fontsize=14, fontweight='bold')
        circle = plt.Circle((0.5, 0.5), 0.2, color='orange', alpha=0.3)
        ax2.add_patch(circle)
        ax2.text(0.5, 0.5, 'BIMモデル\n（単一の情報源）', ha='center', va='center', 
                fontsize=11, fontweight='bold')
        
        # 矢印と派生図面
        ax2.arrow(0.5, 0.3, -0.3, -0.15, head_width=0.03, head_length=0.05, fc='gray', ec='gray')
        ax2.text(0.15, 0.1, '平面図', fontsize=9, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        
        ax2.arrow(0.5, 0.7, -0.3, 0.15, head_width=0.03, head_length=0.05, fc='gray', ec='gray')
        ax2.text(0.15, 0.88, '立面図', fontsize=9, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        
        ax2.arrow(0.5, 0.5, 0.3, 0, head_width=0.03, head_length=0.05, fc='gray', ec='gray')
        ax2.text(0.82, 0.5, '断面図', fontsize=9, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        
        ax2.text(0.5, 0.02, '（自動生成・整合性保証）', ha='center', fontsize=10, style='italic')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        
        plt.tight_layout()
        output_path = self.output_dir / "cad_vs_bim.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_info_layers(self):
        """BIM情報の3層構造"""
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # 3層のボックス
        layers = [
            ('形状情報\n(Geometry)', 0.7, 'lightblue'),
            ('属性情報\n(Property)', 0.45, 'lightgreen'),
            ('関係情報\n(Relationship)', 0.2, 'lightyellow')
        ]
        
        for i, (label, y, color) in enumerate(layers):
            rect = patches.Rectangle((0.2, y-0.08), 0.6, 0.15, 
                                     linewidth=2, edgecolor='black', 
                                     facecolor=color, alpha=0.7)
            ax.add_patch(rect)
            ax.text(0.5, y, label, ha='center', va='center', 
                   fontsize=12, fontweight='bold')
        
        # 説明テキスト
        ax.text(0.05, 0.7, '• 長さ、幅、高さ\n• 3D形状', fontsize=9, va='center')
        ax.text(0.05, 0.45, '• 材質、仕上げ\n• コスト、性能', fontsize=9, va='center')
        ax.text(0.05, 0.2, '• 接続、配置\n• 階層構造', fontsize=9, va='center')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title('BIMモデルの構成要素', fontsize=14, fontweight='bold', pad=20)
        ax.axis('off')
        
        output_path = self.output_dir / "info_layers.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_lifecycle_flow(self):
        """建築ライフサイクルフロー"""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        phases = ['企画', '設計', '施工', '維持管理']
        lods = ['LOD 100', 'LOD 200-300', 'LOD 400', 'LOD 500']
        colors = ['#FFE6E6', '#E6F3FF', '#E6FFE6', '#FFF9E6']
        
        for i, (phase, lod, color) in enumerate(zip(phases, lods, colors)):
            x = i * 0.23 + 0.1
            rect = patches.FancyBboxPatch((x, 0.6), 0.18, 0.25,
                                         boxstyle="round,pad=0.01",
                                         edgecolor='black', facecolor=color,
                                         linewidth=2)
            ax.add_patch(rect)
            ax.text(x + 0.09, 0.72, phase, ha='center', va='center',
                   fontsize=12, fontweight='bold')
            ax.text(x + 0.09, 0.65, lod, ha='center', va='center',
                   fontsize=9, style='italic')
            
            # 矢印（最後以外）
            if i < len(phases) - 1:
                ax.arrow(x + 0.19, 0.72, 0.03, 0, head_width=0.03, 
                        head_length=0.02, fc='gray', ec='gray')
        
        # BIMモデルの継続性を示す線
        ax.plot([0.1, 0.92], [0.45, 0.45], 'b-', linewidth=3, label='BIMモデルの継続')
        ax.text(0.51, 0.48, '同一モデルの段階的詳細化', ha='center', 
               fontsize=11, color='blue', fontweight='bold')
        
        # 従来手法の分断を示す
        for i in range(4):
            x = i * 0.23 + 0.19
            ax.plot([x-0.09, x+0.09], [0.3, 0.3], 'r--', linewidth=2)
            if i < 3:
                ax.text(x+0.12, 0.25, '断絶', fontsize=8, color='red')
        ax.text(0.51, 0.33, '従来手法: 各段階で情報が分断', ha='center',
               fontsize=10, color='red', style='italic')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0.15, 0.95)
        ax.set_title('建築生産プロセスとBIM', fontsize=14, fontweight='bold', pad=20)
        ax.axis('off')
        ax.legend(loc='lower right')
        
        output_path = self.output_dir / "lifecycle_flow.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_element_structure(self):
        """部材(Element)の構造"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 中央にElementボックス
        main_box = patches.FancyBboxPatch((0.35, 0.6), 0.3, 0.15,
                                         boxstyle="round,pad=0.02",
                                         edgecolor='black', facecolor='orange',
                                         linewidth=3, alpha=0.5)
        ax.add_patch(main_box)
        ax.text(0.5, 0.675, '壁オブジェクト\n(Element)', ha='center', va='center',
               fontsize=13, fontweight='bold')
        
        # 形状情報ブランチ
        geo_box = patches.Rectangle((0.05, 0.35), 0.25, 0.15,
                                    edgecolor='blue', facecolor='lightblue',
                                    linewidth=2, alpha=0.7)
        ax.add_patch(geo_box)
        ax.text(0.175, 0.465, '形状情報', ha='center', fontsize=11, fontweight='bold', color='blue')
        ax.text(0.175, 0.42, '• 長さ: 5,000mm\n• 高さ: 2,700mm\n• 厚さ: 200mm', 
               ha='center', va='top', fontsize=9)
        ax.arrow(0.35, 0.65, -0.12, -0.13, head_width=0.02, head_length=0.03, 
                fc='blue', ec='blue', linewidth=2)
        
        # 属性情報ブランチ
        prop_box = patches.Rectangle((0.7, 0.35), 0.25, 0.15,
                                     edgecolor='green', facecolor='lightgreen',
                                     linewidth=2, alpha=0.7)
        ax.add_patch(prop_box)
        ax.text(0.825, 0.465, '属性情報', ha='center', fontsize=11, fontweight='bold', color='green')
        ax.text(0.825, 0.42, '• 材質: RC\n• 仕上: EP-1\n• コスト: ¥85,000/㎡', 
               ha='center', va='top', fontsize=9)
        ax.arrow(0.65, 0.65, 0.12, -0.13, head_width=0.02, head_length=0.03,
                fc='green', ec='green', linewidth=2)
        
        # 派生物
        ax.text(0.5, 0.18, '↓ 自動生成 ↓', ha='center', fontsize=11, 
               fontweight='bold', color='purple')
        
        outputs = ['平面図', '立面図', '断面図', '数量表', '集計表']
        for i, output in enumerate(outputs):
            x = 0.1 + i * 0.18
            output_box = patches.Rectangle((x, 0.05), 0.14, 0.08,
                                          edgecolor='purple', facecolor='lavender',
                                          linewidth=1.5, alpha=0.6)
            ax.add_patch(output_box)
            ax.text(x + 0.07, 0.09, output, ha='center', va='center', fontsize=9)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 0.85)
        ax.set_title('BIM部材（Element）の構造', fontsize=14, fontweight='bold', pad=20)
        ax.axis('off')
        
        output_path = self.output_dir / "element_structure.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_lod_matrix(self):
        """LODマトリクス図"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        lod_data = [
            ('LOD 100', '企画', '概念モデル', 'ボリューム・配置', '#FFE6E6'),
            ('LOD 200', '基本設計', '概略モデル', '主要部材の位置・サイズ', '#FFD9B3'),
            ('LOD 300', '実施設計', '詳細モデル', '詳細形状・主要属性', '#FFFFCC'),
            ('LOD 400', '施工図', '製作モデル', '製作・施工詳細', '#D9FFD9'),
            ('LOD 500', '竣工・維持管理', '竣工モデル', '実測値・as-built', '#CCE5FF')
        ]
        
        for i, (lod, phase, model, content, color) in enumerate(lod_data):
            y = 0.8 - i * 0.15
            
            # LODボックス
            rect1 = patches.Rectangle((0.05, y-0.05), 0.15, 0.08,
                                     edgecolor='black', facecolor=color,
                                     linewidth=2, alpha=0.8)
            ax.add_patch(rect1)
            ax.text(0.125, y, lod, ha='center', va='center',
                   fontsize=11, fontweight='bold')
            
            # フェーズ
            ax.text(0.25, y, phase, va='center', fontsize=10)
            
            # モデルタイプ
            ax.text(0.45, y, model, va='center', fontsize=10, style='italic')
            
            # 内容
            ax.text(0.65, y, content, va='center', fontsize=9)
        
        # タイトル行
        ax.text(0.125, 0.9, 'LOD', ha='center', fontsize=12, fontweight='bold')
        ax.text(0.25, 0.9, 'フェーズ', fontsize=12, fontweight='bold')
        ax.text(0.45, 0.9, 'モデルタイプ', fontsize=12, fontweight='bold')
        ax.text(0.65, 0.9, '内容', fontsize=12, fontweight='bold')
        
        # 矢印（詳細化の流れ）
        ax.annotate('', xy=(0.92, 0.1), xytext=(0.92, 0.75),
                   arrowprops=dict(arrowstyle='->', lw=3, color='blue'))
        ax.text(0.95, 0.425, '詳細化\n↓', fontsize=11, color='blue', 
               fontweight='bold', va='center')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title('LOD（Level of Development）マトリクス', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.axis('off')
        
        output_path = self.output_dir / "lod_matrix.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_openbim_ifc(self):
        """OPEN BIMとIFC連携図"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # ソフトウェア配置
        softwares = [
            ('Revit\n(意匠)', 0.2, 0.7, 'lightblue'),
            ('ArchiCAD\n(意匠)', 0.5, 0.7, 'lightblue'),
            ('Rebro\n(設備)', 0.8, 0.7, 'lightgreen'),
            ('積算ソフト', 0.2, 0.3, 'lightyellow'),
            ('構造解析', 0.5, 0.3, 'lightcoral'),
            ('BIM360\n(施工)', 0.8, 0.3, 'lavender')
        ]
        
        for name, x, y, color in softwares:
            rect = patches.FancyBboxPatch((x-0.08, y-0.05), 0.16, 0.08,
                                         boxstyle="round,pad=0.01",
                                         edgecolor='black', facecolor=color,
                                         linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x, y, name, ha='center', va='center', fontsize=9)
        
        # 中央にIFC
        ifc_circle = plt.Circle((0.5, 0.5), 0.12, color='orange', alpha=0.6, 
                               linewidth=3, edgecolor='black')
        ax.add_patch(ifc_circle)
        ax.text(0.5, 0.5, 'IFC\n(共通フォーマット)', ha='center', va='center',
               fontsize=11, fontweight='bold')
        
        # 接続線（双方向）
        connections = [
            ((0.2, 0.7), (0.5, 0.5)),
            ((0.5, 0.7), (0.5, 0.5)),
            ((0.8, 0.7), (0.5, 0.5)),
            ((0.2, 0.3), (0.5, 0.5)),
            ((0.5, 0.3), (0.5, 0.5)),
            ((0.8, 0.3), (0.5, 0.5))
        ]
        
        for (x1, y1), (x2, y2) in connections:
            ax.plot([x1, x2], [y1, y2], 'b--', linewidth=1.5, alpha=0.5)
            # 矢印（双方向）
            dx, dy = x2 - x1, y2 - y1
            length = np.sqrt(dx**2 + dy**2)
            if length > 0:
                dx, dy = dx/length * 0.05, dy/length * 0.05
                ax.arrow(x1, y1, dx*2, dy*2, head_width=0.015, 
                        head_length=0.02, fc='blue', ec='blue', alpha=0.5)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0.15, 0.85)
        ax.set_title('OPEN BIM - IFCによるソフトウェア間連携', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.text(0.5, 0.1, '※ IFCを中心に異なるソフトウェア間でデータ交換', 
               ha='center', fontsize=10, style='italic', color='gray')
        ax.axis('off')
        
        output_path = self.output_dir / "openbim_ifc.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    # ========== VOL2: 準1級対応 ==========
    
    def generate_ng_ok_level_mistake(self):
        """レベル設定の誤り例と正解例"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # NG例
        ax1.set_title('❌NG例: レベル設定ミス', fontsize=12, fontweight='bold', color='red')
        ax1.plot([0.2, 0.2], [0, 0.6], 'k-', linewidth=2)  # 1階床
        ax1.plot([0.2, 0.8, 0.8, 0.2, 0.2], [0.6, 0.6, 0.9, 0.9, 0.6], 'r-', linewidth=2)  # 壁（誤）
        ax1.text(0.1, 0.6, '2FL', fontsize=10, ha='right')
        ax1.text(0.1, 0, '1FL', fontsize=10, ha='right')
        ax1.text(0.5, 0.75, '壁の上端を\n数値で指定\n(2700)', ha='center', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        ax1.text(0.5, 0.3, '問題: 階高変更時に\n追随しない', ha='center', fontsize=10,
                color='red', fontweight='bold')
        ax1.set_xlim(0, 1)
        ax1.set_ylim(-0.1, 1)
        ax1.axis('off')
        
        # OK例
        ax2.set_title('✅OK例: 正しいレベル設定', fontsize=12, fontweight='bold', color='green')
        ax2.plot([0.2, 0.2], [0, 0.6], 'k-', linewidth=2)  # 1階床
        ax2.plot([0.2, 0.8, 0.8, 0.2, 0.2], [0.6, 0.6, 1.0, 1.0, 0.6], 'g-', linewidth=2)  # 壁（正）
        ax2.plot([0.15, 0.85], [1.0, 1.0], 'b--', linewidth=1.5)  # 3FLレベル線
        ax2.text(0.1, 1.0, '3FL', fontsize=10, ha='right', color='blue')
        ax2.text(0.1, 0.6, '2FL', fontsize=10, ha='right')
        ax2.text(0.1, 0, '1FL', fontsize=10, ha='right')
        ax2.text(0.5, 0.8, '壁の上端を\n「3FL」で指定', ha='center', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        ax2.text(0.5, 0.3, '利点: 階高変更に\n自動追随', ha='center', fontsize=10,
                color='green', fontweight='bold')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(-0.1, 1.1)
        ax2.axis('off')
        
        plt.tight_layout()
        output_path = self.output_dir / "ng_ok_level_mistake.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()


def generate_all_diagrams():
    """すべての図を生成"""
    paths = ProjectPaths()
    paths.ensure_dirs()
    
    # 必要な図のリストを取得
    vol1, vol2 = parse_master_markdown(paths.master_file)
    all_chapters = vol1 + vol2
    figure_refs = get_all_figure_references(all_chapters)
    
    # 図を生成
    generator = DiagramGenerator(paths.figs)
    generator.generate_all(figure_refs)
    
    logger.info(f"✨ 図表生成完了: {paths.figs}")
    return len(figure_refs)


if __name__ == "__main__":
    try:
        count = generate_all_diagrams()
        logger.info(f"📊 合計 {count} 個の図を生成しました")
    except Exception as e:
        logger.error(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
