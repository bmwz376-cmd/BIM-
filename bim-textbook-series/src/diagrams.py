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
    
    def generate_level_mistake_detail(self):
        """レベル設定の詳細な失敗例"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # 失敗例1: レベル名の誤り
        ax1.set_title('❌失敗例1: 日本語レベル名', fontsize=11, fontweight='bold', color='red')
        ax1.text(0.5, 0.7, 'レベル1\nレベル2\nレベル3', ha='center', va='center',
                fontsize=12, bbox=dict(boxstyle='round', facecolor='pink', alpha=0.7))
        ax1.text(0.5, 0.3, '問題: 文字化けの可能性', ha='center', fontsize=9, color='red')
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        
        # 正解例1
        ax2.set_title('✅正解: 英数字レベル名', fontsize=11, fontweight='bold', color='green')
        ax2.text(0.5, 0.7, '1FL\n2FL\n3FL', ha='center', va='center',
                fontsize=12, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        ax2.text(0.5, 0.3, '推奨: 統一された命名', ha='center', fontsize=9, color='green')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        
        # 失敗例2: 階高不統一
        ax3.set_title('❌失敗例2: 階高不統一', fontsize=11, fontweight='bold', color='red')
        ax3.plot([0.2, 0.2], [0.1, 0.1], 'k-', linewidth=2)  # GL
        ax3.plot([0.2, 0.2], [0.1, 0.4], 'r-', linewidth=2)  # 1FL (3m)
        ax3.plot([0.2, 0.2], [0.4, 0.75], 'r-', linewidth=2)  # 2FL (3.5m)
        ax3.plot([0.2, 0.2], [0.75, 1.0], 'r-', linewidth=2)  # 3FL (2.5m)
        ax3.text(0.1, 0.1, 'GL', fontsize=9)
        ax3.text(0.1, 0.4, '1FL', fontsize=9)
        ax3.text(0.1, 0.75, '2FL', fontsize=9)
        ax3.text(0.1, 1.0, 'RFL', fontsize=9)
        ax3.text(0.3, 0.25, '3.0m', fontsize=8, color='red')
        ax3.text(0.3, 0.575, '3.5m', fontsize=8, color='red')
        ax3.text(0.3, 0.875, '2.5m', fontsize=8, color='red')
        ax3.text(0.5, 0.05, '問題: 階高がバラバラ', ha='center', fontsize=9, color='red')
        ax3.set_xlim(0, 1)
        ax3.set_ylim(0, 1.1)
        ax3.axis('off')
        
        # 正解例2
        ax4.set_title('✅正解: 階高統一', fontsize=11, fontweight='bold', color='green')
        ax4.plot([0.2, 0.2], [0.1, 0.1], 'k-', linewidth=2)  # GL
        ax4.plot([0.2, 0.2], [0.1, 0.4], 'g-', linewidth=2)  # 1FL
        ax4.plot([0.2, 0.2], [0.4, 0.7], 'g-', linewidth=2)  # 2FL
        ax4.plot([0.2, 0.2], [0.7, 1.0], 'g-', linewidth=2)  # 3FL
        ax4.text(0.1, 0.1, 'GL', fontsize=9)
        ax4.text(0.1, 0.4, '1FL', fontsize=9)
        ax4.text(0.1, 0.7, '2FL', fontsize=9)
        ax4.text(0.1, 1.0, 'RFL', fontsize=9)
        ax4.text(0.3, 0.25, '3.0m', fontsize=8, color='green')
        ax4.text(0.3, 0.55, '3.0m', fontsize=8, color='green')
        ax4.text(0.3, 0.85, '3.0m', fontsize=8, color='green')
        ax4.text(0.5, 0.05, '推奨: 統一された階高', ha='center', fontsize=9, color='green')
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1.1)
        ax4.axis('off')
        
        plt.tight_layout()
        output_path = self.output_dir / "level_mistake_detail.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_wall_mistake_patterns(self):
        """壁の失敗パターン"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # 失敗1: 高さ設定
        ax1.set_title('❌失敗: 数値で高さ指定', fontsize=11, fontweight='bold', color='red')
        rect = patches.Rectangle((0.3, 0.3), 0.4, 0.35, linewidth=2, edgecolor='red', 
                                 facecolor='pink', alpha=0.5)
        ax1.add_patch(rect)
        ax1.text(0.5, 0.15, '高さ: 2700mm（固定）', ha='center', fontsize=9, color='red')
        ax1.text(0.5, 0.05, '→階高変更時に追随しない', ha='center', fontsize=8, style='italic')
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 0.8)
        ax1.axis('off')
        
        # 正解1
        ax2.set_title('✅正解: レベルで高さ指定', fontsize=11, fontweight='bold', color='green')
        rect = patches.Rectangle((0.3, 0.3), 0.4, 0.4, linewidth=2, edgecolor='green',
                                 facecolor='lightgreen', alpha=0.5)
        ax2.add_patch(rect)
        ax2.plot([0.15, 0.85], [0.7, 0.7], 'b--', linewidth=1.5)
        ax2.text(0.9, 0.7, '2FL', fontsize=9, color='blue')
        ax2.text(0.5, 0.15, '上端: 2FLレベル', ha='center', fontsize=9, color='green')
        ax2.text(0.5, 0.05, '→自動追随', ha='center', fontsize=8, style='italic')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 0.8)
        ax2.axis('off')
        
        # 失敗2: 位置ずれ
        ax3.set_title('❌失敗: グリッドからズレ', fontsize=11, fontweight='bold', color='red')
        ax3.plot([0.5, 0.5], [0.2, 0.7], 'b--', linewidth=1.5, label='Grid')
        ax3.plot([0.52, 0.52], [0.2, 0.7], 'r-', linewidth=3, label='Wall')
        ax3.text(0.5, 0.1, 'Grid', ha='center', fontsize=9, color='blue')
        ax3.text(0.52, 0.05, '+5mm', ha='center', fontsize=9, color='red')
        ax3.legend(loc='upper right')
        ax3.set_xlim(0.3, 0.7)
        ax3.set_ylim(0, 0.8)
        ax3.axis('off')
        
        # 正解2
        ax4.set_title('✅正解: グリッドに整列', fontsize=11, fontweight='bold', color='green')
        ax4.plot([0.5, 0.5], [0.2, 0.7], 'b--', linewidth=1.5, label='Grid')
        ax4.plot([0.5, 0.5], [0.2, 0.7], 'g-', linewidth=3, label='Wall')
        ax4.text(0.5, 0.1, 'Grid=Wall', ha='center', fontsize=9, color='green')
        ax4.text(0.5, 0.05, '0mm', ha='center', fontsize=9, color='green')
        ax4.legend(loc='upper right')
        ax4.set_xlim(0.3, 0.7)
        ax4.set_ylim(0, 0.8)
        ax4.axis('off')
        
        plt.tight_layout()
        output_path = self.output_dir / "wall_mistake_patterns.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_floor_mistake_examples(self):
        """床の失敗例"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # 失敗1: レベルミス
        ax1.set_title('❌失敗: 間違ったレベル', fontsize=11, fontweight='bold', color='red')
        ax1.plot([0.2, 0.8], [0.3, 0.3], 'k-', linewidth=2, label='1FL')
        ax1.plot([0.2, 0.8], [0.6, 0.6], 'b--', linewidth=2, label='2FL')
        rect = patches.Rectangle((0.25, 0.28), 0.5, 0.04, facecolor='red', alpha=0.5)
        ax1.add_patch(rect)
        ax1.text(0.5, 0.15, '2階の床を1FLに作成', ha='center', fontsize=9, color='red')
        ax1.legend(loc='upper right')
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0.1, 0.7)
        ax1.axis('off')
        
        # 正解1
        ax2.set_title('✅正解: 正しいレベル', fontsize=11, fontweight='bold', color='green')
        ax2.plot([0.2, 0.8], [0.3, 0.3], 'k-', linewidth=2, label='1FL')
        ax2.plot([0.2, 0.8], [0.6, 0.6], 'b-', linewidth=2, label='2FL')
        rect = patches.Rectangle((0.25, 0.58), 0.5, 0.04, facecolor='green', alpha=0.5)
        ax2.add_patch(rect)
        ax2.text(0.5, 0.15, '2階の床を2FLに作成', ha='center', fontsize=9, color='green')
        ax2.legend(loc='upper right')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0.1, 0.7)
        ax2.axis('off')
        
        # 失敗2: 境界線の隙間
        ax3.set_title('❌失敗: 境界線が閉じていない', fontsize=11, fontweight='bold', color='red')
        # 不完全な四角形（隙間あり）
        ax3.plot([0.3, 0.7, 0.7, 0.3], [0.3, 0.3, 0.7, 0.7], 'r-', linewidth=2)
        ax3.plot([0.699, 0.699], [0.3, 0.305], 'r-', linewidth=2)  # 隙間を強調
        circle = plt.Circle((0.7, 0.3), 0.02, color='red', fill=True)
        ax3.add_patch(circle)
        ax3.text(0.75, 0.25, '隙間!', fontsize=9, color='red', fontweight='bold')
        ax3.text(0.5, 0.15, 'エラー: 境界線が閉じていません', ha='center', fontsize=9, color='red')
        ax3.set_xlim(0.2, 0.8)
        ax3.set_ylim(0.1, 0.8)
        ax3.axis('off')
        
        # 正解2
        ax4.set_title('✅正解: 境界線が閉じている', fontsize=11, fontweight='bold', color='green')
        # 完全な四角形
        ax4.plot([0.3, 0.7, 0.7, 0.3, 0.3], [0.3, 0.3, 0.7, 0.7, 0.3], 'g-', linewidth=2)
        rect = patches.Rectangle((0.3, 0.3), 0.4, 0.4, facecolor='lightgreen', alpha=0.3)
        ax4.add_patch(rect)
        ax4.text(0.5, 0.15, '床が正常に作成される', ha='center', fontsize=9, color='green')
        ax4.set_xlim(0.2, 0.8)
        ax4.set_ylim(0.1, 0.8)
        ax4.axis('off')
        
        plt.tight_layout()
        output_path = self.output_dir / "floor_mistake_examples.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
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


    def generate_bep_flow(self):
        """BIM実行計画（BEP）のフロー図"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        bep_items = [
            ('1. プロジェクト概要', 0.9, '#FFE6E6'),
            ('2. BIM目標・ユースケース', 0.8, '#FFD9B3'),
            ('3. 組織体制・責任分担', 0.7, '#FFFFCC'),
            ('4. 情報要求事項', 0.6, '#D9FFD9'),
            ('5. 成果物仕様', 0.5, '#CCE5FF'),
            ('6. プロセス・ワークフロー', 0.4, '#E6D9FF'),
            ('7. 技術インフラ', 0.3, '#FFD9E6'),
            ('8. 品質管理', 0.2, '#E6FFE6')
        ]
        
        for i, (item, y, color) in enumerate(bep_items):
            # ボックス
            rect = patches.FancyBboxPatch((0.15, y-0.04), 0.7, 0.07,
                                         boxstyle="round,pad=0.01",
                                         edgecolor='black', facecolor=color,
                                         linewidth=2, alpha=0.8)
            ax.add_patch(rect)
            ax.text(0.5, y, item, ha='center', va='center',
                   fontsize=12, fontweight='bold')
            
            # 矢印（最後以外）
            if i < len(bep_items) - 1:
                ax.arrow(0.5, y-0.05, 0, -0.04, head_width=0.03,
                        head_length=0.02, fc='gray', ec='gray', linewidth=2)
        
        # サイドノート
        ax.text(0.92, 0.9, '企画段階', fontsize=10, color='red',
               bbox=dict(boxstyle='round', facecolor='pink', alpha=0.5))
        ax.text(0.92, 0.5, '設計段階', fontsize=10, color='blue',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        ax.text(0.92, 0.2, '施工段階', fontsize=10, color='green',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0.1, 1.0)
        ax.set_title('BIM実行計画（BEP）の構成', fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        output_path = self.output_dir / "bep_flow.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_4d_5d_bim(self):
        """4D/5D BIMの概念図"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 中央に3D BIM
        center_circle = plt.Circle((0.5, 0.5), 0.12, color='orange', alpha=0.6,
                                  linewidth=3, edgecolor='black')
        ax.add_patch(center_circle)
        ax.text(0.5, 0.5, '3D\nBIMモデル', ha='center', va='center',
               fontsize=12, fontweight='bold')
        
        # 4つの軸を追加
        dimensions = [
            ('4D\n時間軸\n(工程)', 0.5, 0.82, '#FFD9D9', '施工シミュレーション'),
            ('5D\nコスト軸\n(原価)', 0.82, 0.5, '#D9FFD9', '原価管理'),
            ('6D\n維持管理', 0.5, 0.18, '#D9D9FF', 'FM・設備管理'),
            ('7D\nサステナ\nビリティ', 0.18, 0.5, '#FFFFD9', '環境性能')
        ]
        
        for label, x, y, color, desc in dimensions:
            # 円
            circle = plt.Circle((x, y), 0.08, color=color, alpha=0.7,
                              linewidth=2, edgecolor='black')
            ax.add_patch(circle)
            ax.text(x, y, label, ha='center', va='center',
                   fontsize=10, fontweight='bold')
            
            # 接続線
            ax.plot([0.5, x], [0.5, y], 'b-', linewidth=2, alpha=0.5)
            
            # 説明
            if y > 0.5:  # 上
                ax.text(x, y+0.12, desc, ha='center', fontsize=8, style='italic')
            elif y < 0.5:  # 下
                ax.text(x, y-0.12, desc, ha='center', fontsize=8, style='italic')
            elif x > 0.5:  # 右
                ax.text(x+0.15, y, desc, ha='left', fontsize=8, style='italic')
            else:  # 左
                ax.text(x-0.15, y, desc, ha='right', fontsize=8, style='italic')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title('nD BIM - 多次元BIMの展開', fontsize=16, fontweight='bold', pad=20)
        ax.text(0.5, 0.02, '3D空間モデルに時間・コスト・維持管理・環境の軸を追加',
               ha='center', fontsize=10, style='italic', color='gray')
        ax.axis('off')
        
        output_path = self.output_dir / "4d_5d_bim.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_family_hierarchy_detail(self):
        """ファミリ階層の詳細図"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # レベル1: プロジェクト
        rect1 = patches.FancyBboxPatch((0.35, 0.85), 0.3, 0.08,
                                      boxstyle="round,pad=0.01",
                                      edgecolor='black', facecolor='lightblue',
                                      linewidth=3)
        ax.add_patch(rect1)
        ax.text(0.5, 0.89, 'プロジェクト', ha='center', va='center',
               fontsize=14, fontweight='bold')
        
        # レベル2: カテゴリ
        categories = [
            ('壁', 0.15, 0.7),
            ('ドア', 0.35, 0.7),
            ('窓', 0.55, 0.7),
            ('家具', 0.75, 0.7)
        ]
        
        for cat, x, y in categories:
            rect = patches.FancyBboxPatch((x-0.08, y-0.03), 0.16, 0.06,
                                         boxstyle="round,pad=0.005",
                                         edgecolor='blue', facecolor='lightgreen',
                                         linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, cat, ha='center', va='center',
                   fontsize=11, fontweight='bold')
            # 接続線
            ax.plot([0.5, x], [0.85, y+0.03], 'k-', linewidth=1.5)
        
        # レベル3: ファミリタイプ
        types = [
            ('RC200', 0.08, 0.52),
            ('LGS100', 0.22, 0.52),
            ('片開き', 0.28, 0.52),
            ('両開き', 0.42, 0.52),
            ('引違い', 0.48, 0.52),
            ('FIX', 0.62, 0.52),
            ('デスク', 0.68, 0.52),
            ('チェア', 0.82, 0.52)
        ]
        
        for typ, x, y in types:
            rect = patches.Rectangle((x-0.05, y-0.02), 0.1, 0.04,
                                    edgecolor='green', facecolor='lightyellow',
                                    linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x, y, typ, ha='center', va='center', fontsize=9)
            # 接続線（対応するカテゴリへ）
            if x < 0.25:
                ax.plot([0.15, x], [0.67, y+0.02], 'g-', linewidth=1)
            elif x < 0.45:
                ax.plot([0.35, x], [0.67, y+0.02], 'g-', linewidth=1)
            elif x < 0.65:
                ax.plot([0.55, x], [0.67, y+0.02], 'g-', linewidth=1)
            else:
                ax.plot([0.75, x], [0.67, y+0.02], 'g-', linewidth=1)
        
        # レベル4: インスタンス
        ax.text(0.5, 0.35, '▼ インスタンス（個別の要素）', ha='center',
               fontsize=12, fontweight='bold', color='purple')
        
        instances = [
            ('壁1\nID:123456', 0.08, 0.22),
            ('壁2\nID:123457', 0.22, 0.22),
            ('ドア1\nID:234567', 0.35, 0.22),
            ('窓1\nID:345678', 0.55, 0.22),
            ('デスク1\nID:456789', 0.75, 0.22)
        ]
        
        for inst, x, y in instances:
            ellipse = patches.Ellipse((x, y), 0.12, 0.08,
                                     edgecolor='purple', facecolor='lavender',
                                     linewidth=1.5)
            ax.add_patch(ellipse)
            ax.text(x, y, inst, ha='center', va='center', fontsize=8)
        
        # 凡例
        ax.text(0.1, 0.05, '■ 階層構造', fontsize=10, fontweight='bold')
        ax.text(0.1, 0.02, '  プロジェクト > カテゴリ > ファミリタイプ > インスタンス',
               fontsize=9)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title('Revitファミリの階層構造', fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        output_path = self.output_dir / "family_hierarchy_detail.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_worksharing_concept(self):
        """ワークシェアリングの概念図"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # 中央サーバー
        server_rect = patches.FancyBboxPatch((0.38, 0.6), 0.24, 0.15,
                                            boxstyle="round,pad=0.02",
                                            edgecolor='black', facecolor='lightblue',
                                            linewidth=3)
        ax.add_patch(server_rect)
        ax.text(0.5, 0.7, '中央ファイル\n(Central File)', ha='center', va='center',
               fontsize=13, fontweight='bold')
        ax.text(0.5, 0.63, 'サーバー上に配置', ha='center', fontsize=9, style='italic')
        
        # 設計者たち
        users = [
            ('意匠設計者A', 0.15, 0.35, 'lightgreen'),
            ('構造設計者B', 0.5, 0.35, 'lightyellow'),
            ('設備設計者C', 0.85, 0.35, 'lightcoral')
        ]
        
        for name, x, y, color in users:
            # ユーザーアイコン
            circle = plt.Circle((x, y), 0.06, color=color, alpha=0.7,
                              linewidth=2, edgecolor='black')
            ax.add_patch(circle)
            ax.text(x, y, name, ha='center', va='center', fontsize=9, fontweight='bold')
            
            # ローカルファイル
            rect = patches.Rectangle((x-0.08, y-0.18), 0.16, 0.06,
                                    edgecolor='gray', facecolor='white',
                                    linewidth=1.5, linestyle='--')
            ax.add_patch(rect)
            ax.text(x, y-0.15, 'ローカル\nコピー', ha='center', va='center', fontsize=8)
            
            # 同期矢印（上向き：Synchronize with Central）
            ax.annotate('', xy=(0.5, 0.6), xytext=(x, y+0.07),
                       arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
            ax.text((x+0.5)/2 + 0.05, (y+0.6)/2, 'Sync', fontsize=8, color='blue')
            
            # ダウンロード矢印（下向き：Reload Latest）
            ax.annotate('', xy=(x, y+0.07), xytext=(0.5, 0.6),
                       arrowprops=dict(arrowstyle='->', lw=1.5, color='green', linestyle='--'))
            ax.text((x+0.5)/2 - 0.05, (y+0.6)/2, 'Reload', fontsize=8, color='green')
        
        # ワークセット説明
        ax.text(0.5, 0.9, '■ ワークシェアリングの仕組み', ha='center',
               fontsize=14, fontweight='bold')
        ax.text(0.5, 0.05, '1. 各設計者がローカルコピーを編集\n' +
                          '2. 定期的に中央ファイルと同期（Sync）\n' +
                          '3. 他者の変更を取得（Reload Latest）',
               ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title('ワークシェアリング - 複数人での同時作業', fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        output_path = self.output_dir / "worksharing_concept.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_clash_detection(self):
        """干渉チェックの概念図"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # 干渉1: 配管と梁の干渉
        ax1.set_title('❌干渉検出: 配管と梁', fontsize=12, fontweight='bold', color='red')
        rect1 = patches.Rectangle((0.2, 0.5), 0.6, 0.15, facecolor='gray', alpha=0.5,
                                 edgecolor='black', linewidth=2, label='梁')
        ax1.add_patch(rect1)
        circle1 = plt.Circle((0.5, 0.575), 0.08, facecolor='blue', alpha=0.6,
                            edgecolor='blue', linewidth=2, label='配管')
        ax1.add_patch(circle1)
        # 干渉マーク
        ax1.plot([0.5], [0.575], 'r*', markersize=30, label='干渉！')
        ax1.text(0.5, 0.3, '問題: 配管が梁を貫通', ha='center', fontsize=10, color='red')
        ax1.legend(loc='upper right')
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0.2, 0.8)
        ax1.axis('off')
        
        # 解決策1
        ax2.set_title('✅解決策: 配管位置変更', fontsize=12, fontweight='bold', color='green')
        rect2 = patches.Rectangle((0.2, 0.5), 0.6, 0.15, facecolor='gray', alpha=0.5,
                                 edgecolor='black', linewidth=2, label='梁')
        ax2.add_patch(rect2)
        circle2 = plt.Circle((0.5, 0.35), 0.08, facecolor='blue', alpha=0.6,
                            edgecolor='blue', linewidth=2, label='配管（移動後）')
        ax2.add_patch(circle2)
        ax2.text(0.5, 0.75, '配管を下方へ移動', ha='center', fontsize=10, color='green')
        ax2.legend(loc='upper right')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0.2, 0.8)
        ax2.axis('off')
        
        # 干渉2: ダクトと壁の干渉
        ax3.set_title('❌干渉検出: ダクトと壁', fontsize=12, fontweight='bold', color='red')
        # 壁
        rect3 = patches.Rectangle((0.45, 0.2), 0.1, 0.6, facecolor='lightgray', alpha=0.7,
                                 edgecolor='black', linewidth=2, label='壁')
        ax3.add_patch(rect3)
        # ダクト
        rect4 = patches.Rectangle((0.3, 0.45), 0.4, 0.12, facecolor='yellow', alpha=0.6,
                                 edgecolor='orange', linewidth=2, label='ダクト')
        ax3.add_patch(rect4)
        # 干渉エリア
        rect5 = patches.Rectangle((0.45, 0.45), 0.1, 0.12, facecolor='red', alpha=0.5,
                                 linewidth=0, label='干渉！')
        ax3.add_patch(rect5)
        ax3.text(0.5, 0.1, '問題: ダクトが壁を貫通', ha='center', fontsize=10, color='red')
        ax3.legend(loc='upper right')
        ax3.set_xlim(0.2, 0.8)
        ax3.set_ylim(0, 0.9)
        ax3.axis('off')
        
        # 解決策2
        ax4.set_title('✅解決策: スリーブ設置', fontsize=12, fontweight='bold', color='green')
        # 壁
        rect6 = patches.Rectangle((0.45, 0.2), 0.1, 0.6, facecolor='lightgray', alpha=0.7,
                                 edgecolor='black', linewidth=2, label='壁')
        ax4.add_patch(rect6)
        # スリーブ（開口）
        rect7 = patches.Rectangle((0.45, 0.45), 0.1, 0.12, facecolor='white',
                                 edgecolor='blue', linewidth=2, linestyle='--', label='スリーブ')
        ax4.add_patch(rect7)
        # ダクト
        rect8 = patches.Rectangle((0.3, 0.45), 0.4, 0.12, facecolor='yellow', alpha=0.6,
                                 edgecolor='orange', linewidth=2, label='ダクト')
        ax4.add_patch(rect8)
        ax4.text(0.5, 0.1, 'スリーブを設置して貫通部を確保', ha='center', fontsize=10, color='green')
        ax4.legend(loc='upper right')
        ax4.set_xlim(0.2, 0.8)
        ax4.set_ylim(0, 0.9)
        ax4.axis('off')
        
        plt.suptitle('干渉チェック（Clash Detection）の例', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        output_path = self.output_dir / "clash_detection.png"
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
