#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diagrams_professional.py - BIM教科書用プロフェッショナル図解生成
高品質で読みやすい図解を生成
"""

import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Wedge, Arc
from pathlib import Path
import numpy as np

# 日本語フォント設定
try:
    import japanize_matplotlib
    japanize_matplotlib.japanize()
except ImportError:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'sans-serif']

# プロフェッショナル設定
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['figure.figsize'] = (14, 10)  # 大きめのデフォルトサイズ
plt.rcParams['font.size'] = 14  # ベースフォントサイズを大きく

# プロフェッショナルカラーパレット
COLORS = {
    'primary': '#2E86AB',      # 深い青
    'secondary': '#A23B72',    # 紫
    'success': '#06A77D',      # 緑
    'warning': '#F18F01',      # オレンジ
    'danger': '#C73E1D',       # 赤
    'info': '#4CC9F0',         # 水色
    'light_blue': '#E3F2FD',   # 薄い青
    'light_green': '#E8F5E9',  # 薄い緑
    'light_yellow': '#FFF9C4', # 薄い黄色
    'light_red': '#FFEBEE',    # 薄い赤
    'light_purple': '#F3E5F5', # 薄い紫
    'gray': '#757575',         # グレー
    'light_gray': '#F5F5F5',   # 薄いグレー
}


class ProfessionalDiagramGenerator:
    """プロフェッショナル品質の図解生成クラス"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.colors = COLORS
    
    def draw_rounded_box(self, ax, x, y, width, height, text, bgcolor, 
                        textcolor='black', fontsize=16, fontweight='bold',
                        edgecolor='black', linewidth=2):
        """角丸ボックスを描画"""
        box = FancyBboxPatch(
            (x, y), width, height,
            boxstyle="round,pad=0.02",
            facecolor=bgcolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            alpha=0.9
        )
        ax.add_patch(box)
        ax.text(x + width/2, y + height/2, text,
               ha='center', va='center',
               fontsize=fontsize, fontweight=fontweight,
               color=textcolor)
        return box
    
    def draw_arrow(self, ax, x1, y1, x2, y2, color='black', width=3, label=''):
        """太くて見やすい矢印を描画"""
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(
                       arrowstyle='->', 
                       lw=width,
                       color=color,
                       mutation_scale=25
                   ))
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x, mid_y, label, 
                   ha='center', va='bottom',
                   fontsize=12, color=color, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', 
                           facecolor='white', alpha=0.8,
                           edgecolor=color))
    
    # ========== 図表生成メソッド ==========
    
    def generate_cad_vs_bim(self):
        """CAD vs BIM比較図（改善版）"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
        fig.patch.set_facecolor('white')
        
        # 左側: CAD
        ax1.set_title('従来のCAD', fontsize=24, fontweight='bold', pad=20, color=self.colors['danger'])
        
        # 個別ファイル
        drawings = [
            ('平面図', 0.75),
            ('立面図', 0.5),
            ('断面図', 0.25)
        ]
        for i, (name, y) in enumerate(drawings):
            self.draw_rounded_box(ax1, 0.2, y-0.08, 0.6, 0.12, 
                                name, self.colors['light_red'], 
                                fontsize=18, edgecolor=self.colors['danger'])
            # バラバラアイコン
            ax1.plot([0.85, 0.95], [y, y], 'r--', linewidth=2)
            ax1.text(0.9, y+0.05, '✗', fontsize=20, color=self.colors['danger'])
        
        ax1.text(0.5, 0.05, '⚠️ 図面ごとに個別管理\n整合性の確保が困難', 
                ha='center', fontsize=14, color=self.colors['danger'],
                bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_red'], 
                         edgecolor=self.colors['danger'], linewidth=2))
        
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        
        # 右側: BIM
        ax2.set_title('BIM (Building Information Modeling)', fontsize=24, fontweight='bold', 
                     pad=20, color=self.colors['success'])
        
        # 中央のBIMモデル
        center_circle = Circle((0.5, 0.6), 0.15, 
                              facecolor=self.colors['primary'],
                              edgecolor='black', linewidth=3, alpha=0.8)
        ax2.add_patch(center_circle)
        ax2.text(0.5, 0.6, 'BIM\nモデル', ha='center', va='center',
                fontsize=20, fontweight='bold', color='white')
        
        # 単一の情報源テキスト
        ax2.text(0.5, 0.8, '単一の情報源', ha='center', fontsize=16,
                fontweight='bold', color=self.colors['primary'],
                bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_blue'],
                         edgecolor=self.colors['primary'], linewidth=2))
        
        # 自動生成される図面
        outputs = [
            ('平面図', 0.2, 0.3, self.colors['light_green']),
            ('立面図', 0.5, 0.2, self.colors['light_green']),
            ('断面図', 0.8, 0.3, self.colors['light_green']),
            ('3Dビュー', 0.2, 0.15, self.colors['light_yellow']),
            ('数量表', 0.8, 0.15, self.colors['light_yellow'])
        ]
        
        for name, x, y, bgcolor in outputs:
            self.draw_rounded_box(ax2, x-0.08, y-0.04, 0.16, 0.08,
                                name, bgcolor, fontsize=14,
                                edgecolor=self.colors['success'], linewidth=2)
            # 矢印で接続
            self.draw_arrow(ax2, 0.5, 0.45, x, y+0.04, 
                          color=self.colors['success'], width=2)
        
        ax2.text(0.5, 0.02, '✓ 自動生成・整合性保証\n✓ 変更が全図面に反映', 
                ha='center', fontsize=14, color=self.colors['success'],
                bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_green'],
                         edgecolor=self.colors['success'], linewidth=2))
        
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        
        plt.tight_layout()
        output_path = self.output_dir / "cad_vs_bim.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
        plt.close()
        print(f"✓ 生成完了: cad_vs_bim.png")
    
    def generate_info_layers(self):
        """BIM情報の3層構造（改善版）"""
        fig, ax = plt.subplots(figsize=(16, 12))
        fig.patch.set_facecolor('white')
        
        ax.set_title('BIMモデルの3層構造', fontsize=28, fontweight='bold', pad=30)
        
        # 3層のボックス（大きく、見やすく）
        layers = [
            {
                'name': '形状情報',
                'eng': 'Geometry',
                'y': 0.65,
                'color': self.colors['light_blue'],
                'edge': self.colors['primary'],
                'details': ['• 3次元形状データ', '• 寸法（長さ・幅・高さ）', '• 位置・配置情報']
            },
            {
                'name': '属性情報',
                'eng': 'Property',
                'y': 0.4,
                'color': self.colors['light_green'],
                'edge': self.colors['success'],
                'details': ['• 材質・仕上げ', '• コスト・性能値', '• メーカー・型番']
            },
            {
                'name': '関係情報',
                'eng': 'Relationship',
                'y': 0.15,
                'color': self.colors['light_yellow'],
                'edge': self.colors['warning'],
                'details': ['• 部材間の接続', '• 階層構造', '• 依存関係']
            }
        ]
        
        for layer in layers:
            # メインボックス
            self.draw_rounded_box(ax, 0.15, layer['y']-0.08, 0.35, 0.14,
                                f"{layer['name']}\n({layer['eng']})",
                                layer['color'], fontsize=20,
                                edgecolor=layer['edge'], linewidth=3)
            
            # 詳細説明
            details_text = '\n'.join(layer['details'])
            ax.text(0.55, layer['y'], details_text,
                   fontsize=16, va='center',
                   bbox=dict(boxstyle='round,pad=0.8', 
                           facecolor='white', alpha=0.8,
                           edgecolor=layer['edge'], linewidth=2))
        
        # 統合の矢印
        for i in range(2):
            y_from = [0.65, 0.4][i] - 0.08
            y_to = [0.4, 0.15][i] + 0.06
            self.draw_arrow(ax, 0.325, y_from, 0.325, y_to,
                          color=self.colors['gray'], width=3)
        
        # 説明テキスト
        ax.text(0.5, 0.92, 'これら3つの情報が統合されてBIMモデルを構成',
               ha='center', fontsize=18, fontweight='bold',
               color=self.colors['primary'],
               bbox=dict(boxstyle='round,pad=0.8', facecolor=self.colors['light_blue'],
                        edgecolor=self.colors['primary'], linewidth=3))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        output_path = self.output_dir / "info_layers.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
        plt.close()
        print(f"✓ 生成完了: info_layers.png")
    
    def generate_lifecycle_flow(self):
        """ライフサイクルフロー（改善版）"""
        fig, ax = plt.subplots(figsize=(18, 10))
        fig.patch.set_facecolor('white')
        
        ax.set_title('建築ライフサイクルとBIM活用', fontsize=28, fontweight='bold', pad=30)
        
        # フェーズ定義
        phases = [
            {'name': '企画', 'lod': 'LOD 100', 'color': self.colors['light_red'], 
             'edge': self.colors['danger'], 'x': 0.1},
            {'name': '設計', 'lod': 'LOD 200-300', 'color': self.colors['light_yellow'],
             'edge': self.colors['warning'], 'x': 0.3},
            {'name': '施工', 'lod': 'LOD 400', 'color': self.colors['light_green'],
             'edge': self.colors['success'], 'x': 0.5},
            {'name': '維持管理', 'lod': 'LOD 500', 'color': self.colors['light_blue'],
             'edge': self.colors['primary'], 'x': 0.7}
        ]
        
        # フェーズボックス
        for i, phase in enumerate(phases):
            self.draw_rounded_box(ax, phase['x'], 0.6, 0.15, 0.25,
                                f"{phase['name']}\n\n{phase['lod']}",
                                phase['color'], fontsize=18,
                                edgecolor=phase['edge'], linewidth=3)
            
            # フェーズ間の矢印
            if i < len(phases) - 1:
                self.draw_arrow(ax, phase['x'] + 0.15, 0.725,
                              phases[i+1]['x'], 0.725,
                              color=self.colors['gray'], width=4)
        
        # BIMモデルの継続性
        ax.plot([0.1, 0.85], [0.4, 0.4], 
               color=self.colors['primary'], linewidth=6, 
               label='BIMモデルの継続的活用')
        ax.text(0.475, 0.45, '同一モデルの段階的詳細化',
               ha='center', fontsize=18, fontweight='bold',
               color=self.colors['primary'],
               bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_blue'],
                        edgecolor=self.colors['primary'], linewidth=2))
        
        # 従来手法の分断
        for i, phase in enumerate(phases):
            ax.plot([phase['x'], phase['x'] + 0.15], [0.2, 0.2],
                   'r--', linewidth=4)
            if i < len(phases) - 1:
                ax.text(phase['x'] + 0.175, 0.15, '✗\n断絶',
                       ha='center', fontsize=14, color=self.colors['danger'],
                       fontweight='bold')
        
        ax.text(0.475, 0.25, '従来手法：各段階で情報が分断される',
               ha='center', fontsize=16, style='italic',
               color=self.colors['danger'],
               bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_red'],
                        edgecolor=self.colors['danger'], linewidth=2))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0.05, 0.95)
        ax.axis('off')
        ax.legend(loc='upper right', fontsize=14)
        
        output_path = self.output_dir / "lifecycle_flow.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
        plt.close()
        print(f"✓ 生成完了: lifecycle_flow.png")
    
    def generate_lod_matrix(self):
        """LODマトリックス（改善版）"""
        fig, ax = plt.subplots(figsize=(18, 12))
        fig.patch.set_facecolor('white')
        
        ax.set_title('LOD (Level of Development) マトリックス', 
                    fontsize=28, fontweight='bold', pad=30)
        
        # ヘッダー行
        headers = ['LOD', 'フェーズ', '詳細度', '主な内容']
        x_positions = [0.05, 0.2, 0.4, 0.6]
        for i, (header, x) in enumerate(zip(headers, x_positions)):
            ax.text(x, 0.9, header, fontsize=20, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_gray'],
                           edgecolor='black', linewidth=2))
        
        # LODデータ
        lod_data = [
            {
                'lod': 'LOD 100', 'phase': '企画', 'detail': '概念モデル',
                'content': 'ボリューム・配置計画',
                'color': self.colors['light_red'], 'edge': self.colors['danger'],
                'y': 0.75
            },
            {
                'lod': 'LOD 200', 'phase': '基本設計', 'detail': '概略モデル',
                'content': '主要部材の位置・サイズ',
                'color': self.colors['light_yellow'], 'edge': self.colors['warning'],
                'y': 0.6
            },
            {
                'lod': 'LOD 300', 'phase': '実施設計', 'detail': '詳細モデル',
                'content': '詳細形状・主要属性',
                'color': '#FFF9C4', 'edge': '#F57C00',
                'y': 0.45
            },
            {
                'lod': 'LOD 400', 'phase': '施工', 'detail': '製作モデル',
                'content': '製作・施工詳細情報',
                'color': self.colors['light_green'], 'edge': self.colors['success'],
                'y': 0.3
            },
            {
                'lod': 'LOD 500', 'phase': '竣工・FM', 'detail': '竣工モデル',
                'content': '実測値・as-built',
                'color': self.colors['light_blue'], 'edge': self.colors['primary'],
                'y': 0.15
            }
        ]
        
        for data in lod_data:
            # LOD
            self.draw_rounded_box(ax, 0.05, data['y']-0.05, 0.12, 0.09,
                                data['lod'], data['color'], fontsize=16,
                                edgecolor=data['edge'], linewidth=2)
            # フェーズ
            ax.text(0.2, data['y'], data['phase'], fontsize=18, va='center',
                   fontweight='bold')
            # 詳細度
            ax.text(0.4, data['y'], data['detail'], fontsize=16, va='center',
                   style='italic')
            # 内容
            ax.text(0.6, data['y'], data['content'], fontsize=16, va='center')
        
        # 詳細化の矢印
        self.draw_arrow(ax, 0.93, 0.75, 0.93, 0.2,
                      color=self.colors['primary'], width=5)
        ax.text(0.96, 0.475, '詳細化\n↓', fontsize=18, fontweight='bold',
               color=self.colors['primary'], ha='center', va='center')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0.05, 1)
        ax.axis('off')
        
        output_path = self.output_dir / "lod_matrix.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
        plt.close()
        print(f"✓ 生成完了: lod_matrix.png")
    
    def generate_element_structure(self):
        """要素構造図（改善版）"""
        fig, ax = plt.subplots(figsize=(16, 12))
        fig.patch.set_facecolor('white')
        
        ax.set_title('BIM要素（Element）の構造', fontsize=28, fontweight='bold', pad=30)
        
        # 中央：要素ボックス
        self.draw_rounded_box(ax, 0.35, 0.6, 0.3, 0.15,
                            '壁\n（Wall Element）',
                            self.colors['warning'], fontsize=20,
                            edgecolor='black', linewidth=4)
        
        # 左：形状情報
        geo_text = '形状情報\n(Geometry)\n\n長さ: 5,000mm\n高さ: 2,700mm\n厚さ: 200mm'
        self.draw_rounded_box(ax, 0.05, 0.55, 0.25, 0.25,
                            geo_text, self.colors['light_blue'],
                            fontsize=16, edgecolor=self.colors['primary'],
                            linewidth=3)
        self.draw_arrow(ax, 0.3, 0.675, 0.35, 0.675,
                      color=self.colors['primary'], width=3, label='形状')
        
        # 右：属性情報
        prop_text = '属性情報\n(Property)\n\n材質: RC造\n仕上: EP-1\nコスト: ¥85,000/㎡'
        self.draw_rounded_box(ax, 0.7, 0.55, 0.25, 0.25,
                            prop_text, self.colors['light_green'],
                            fontsize=16, edgecolor=self.colors['success'],
                            linewidth=3)
        self.draw_arrow(ax, 0.65, 0.675, 0.7, 0.675,
                      color=self.colors['success'], width=3, label='属性')
        
        # 下：自動生成される成果物
        ax.text(0.5, 0.4, '⬇ 自動生成される成果物 ⬇',
               ha='center', fontsize=18, fontweight='bold',
               color=self.colors['secondary'])
        
        outputs = [
            ('平面図', 0.1),
            ('立面図', 0.275),
            ('断面図', 0.45),
            ('数量表', 0.625),
            ('集計表', 0.8)
        ]
        
        for name, x in outputs:
            self.draw_rounded_box(ax, x-0.075, 0.15, 0.15, 0.12,
                                name, self.colors['light_purple'],
                                fontsize=16, edgecolor=self.colors['secondary'],
                                linewidth=2)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0.05, 0.95)
        ax.axis('off')
        
        output_path = self.output_dir / "element_structure.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
        plt.close()
        print(f"✓ 生成完了: element_structure.png")
    
    def generate_openbim_ifc(self):
        """OpenBIM/IFC図（改善版）"""
        fig, ax = plt.subplots(figsize=(16, 12))
        fig.patch.set_facecolor('white')
        
        ax.set_title('OPEN BIM - IFCによるデータ交換', fontsize=28, fontweight='bold', pad=30)
        
        # 中央：IFC
        ifc_circle = Circle((0.5, 0.5), 0.15,
                           facecolor=self.colors['warning'],
                           edgecolor='black', linewidth=4, alpha=0.9)
        ax.add_patch(ifc_circle)
        ax.text(0.5, 0.5, 'IFC\n\n共通\nフォーマット',
               ha='center', va='center', fontsize=20, fontweight='bold',
               color='white')
        
        # 周辺：ソフトウェア
        softwares = [
            ('Revit\n(意匠)', 0.2, 0.8, self.colors['light_blue']),
            ('ArchiCAD\n(意匠)', 0.5, 0.85, self.colors['light_blue']),
            ('Rebro\n(設備)', 0.8, 0.8, self.colors['light_green']),
            ('積算ソフト', 0.15, 0.3, self.colors['light_yellow']),
            ('構造解析', 0.5, 0.15, self.colors['light_red']),
            ('Navisworks\n(統合)', 0.85, 0.3, self.colors['light_purple'])
        ]
        
        for name, x, y, bgcolor in softwares:
            self.draw_rounded_box(ax, x-0.08, y-0.05, 0.16, 0.1,
                                name, bgcolor, fontsize=14,
                                edgecolor='black', linewidth=2)
            # IFCへの接続線
            self.draw_arrow(ax, x, y-0.05 if y > 0.5 else y+0.05,
                          0.5, 0.65 if y > 0.5 else 0.35,
                          color=self.colors['gray'], width=2)
        
        # 説明
        ax.text(0.5, 0.05, '※ IFCを中心に異なるBIMソフト間でデータ交換可能',
               ha='center', fontsize=16, style='italic',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_yellow'],
                        edgecolor=self.colors['warning'], linewidth=2))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        output_path = self.output_dir / "openbim_ifc.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
        plt.close()
        print(f"✓ 生成完了: openbim_ifc.png")
    
    def generate_4d_5d_bim(self):
        """4D/5D BIM図（改善版）"""
        fig, ax = plt.subplots(figsize=(14, 14))
        fig.patch.set_facecolor('white')
        
        ax.set_title('多次元BIM (nD BIM)', fontsize=28, fontweight='bold', pad=30)
        
        # 中央：3D BIM
        center = Circle((0.5, 0.5), 0.12,
                       facecolor=self.colors['primary'],
                       edgecolor='black', linewidth=4, alpha=0.9)
        ax.add_patch(center)
        ax.text(0.5, 0.5, '3D\nBIM', ha='center', va='center',
               fontsize=22, fontweight='bold', color='white')
        
        # 4つの次元
        dimensions = [
            ('4D\n工程管理\n(時間軸)', 0.5, 0.82, self.colors['light_red'], 
             '施工シミュレーション\nガントチャート連携'),
            ('5D\nコスト管理\n(原価)', 0.82, 0.5, self.colors['light_green'],
             '積算データ連携\nコスト予測'),
            ('6D\n維持管理\n(FM)', 0.5, 0.18, self.colors['light_purple'],
             '設備管理\nメンテナンス計画'),
            ('7D\n環境性能\n(Green)', 0.18, 0.5, self.colors['light_yellow'],
             'エネルギー解析\nCO2排出量')
        ]
        
        for label, x, y, bgcolor, desc in dimensions:
            # 次元ボックス
            self.draw_rounded_box(ax, x-0.1, y-0.08, 0.2, 0.16,
                                label, bgcolor, fontsize=18,
                                edgecolor='black', linewidth=3)
            
            # 接続線
            ax.plot([0.5, x], [0.5, y], color=self.colors['primary'],
                   linewidth=3, alpha=0.6)
            
            # 説明
            if y > 0.6:
                desc_y = y + 0.12
            elif y < 0.4:
                desc_y = y - 0.12
            else:
                desc_y = y
                x = x + 0.25 if x > 0.5 else x - 0.25
            
            ax.text(x, desc_y, desc, ha='center', fontsize=12,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                           edgecolor=bgcolor, linewidth=1.5))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        output_path = self.output_dir / "4d_5d_bim.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
        plt.close()
        print(f"✓ 生成完了: 4d_5d_bim.png")
    
    def generate_bep_flow(self):
        """BEPフロー図（改善版）"""
        fig, ax = plt.subplots(figsize=(14, 16))
        fig.patch.set_facecolor('white')
        
        ax.set_title('BIM実行計画（BEP）の構成', fontsize=28, fontweight='bold', pad=30)
        
        bep_items = [
            ('1. プロジェクト概要', 0.88, self.colors['light_red']),
            ('2. BIM目標・ユースケース', 0.78, self.colors['light_yellow']),
            ('3. 組織体制・役割分担', 0.68, '#FFE082'),
            ('4. 情報要求事項', 0.58, self.colors['light_green']),
            ('5. 成果物仕様', 0.48, '#A5D6A7'),
            ('6. プロセス・ワークフロー', 0.38, self.colors['light_blue']),
            ('7. 技術インフラ', 0.28, self.colors['light_purple']),
            ('8. 品質管理・検証', 0.18, '#E1BEE7')
        ]
        
        for i, (item, y, color) in enumerate(bep_items):
            self.draw_rounded_box(ax, 0.15, y-0.04, 0.7, 0.07,
                                item, color, fontsize=18,
                                edgecolor='black', linewidth=2)
            
            if i < len(bep_items) - 1:
                self.draw_arrow(ax, 0.5, y-0.05, 0.5, bep_items[i+1][1]+0.03,
                              color=self.colors['gray'], width=4)
        
        # フェーズ表示
        ax.text(0.9, 0.83, '企画', fontsize=16, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_red'],
                        edgecolor=self.colors['danger'], linewidth=2))
        ax.text(0.9, 0.53, '設計', fontsize=16, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_green'],
                        edgecolor=self.colors['success'], linewidth=2))
        ax.text(0.9, 0.23, '施工', fontsize=16, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_blue'],
                        edgecolor=self.colors['primary'], linewidth=2))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0.1, 0.95)
        ax.axis('off')
        
        output_path = self.output_dir / "bep_flow.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
        plt.close()
        print(f"✓ 生成完了: bep_flow.png")
    
    def generate_worksharing_concept(self):
        """ワークシェアリング図（改善版）"""
        fig, ax = plt.subplots(figsize=(16, 12))
        fig.patch.set_facecolor('white')
        
        ax.set_title('ワークシェアリング - 複数人での同時作業', fontsize=28, fontweight='bold', pad=30)
        
        # 中央ファイル
        self.draw_rounded_box(ax, 0.35, 0.65, 0.3, 0.2,
                            '中央ファイル\n(Central File)\n\nサーバー上に配置',
                            self.colors['light_blue'], fontsize=18,
                            edgecolor=self.colors['primary'], linewidth=4)
        
        # 3人の設計者
        users = [
            ('意匠設計者A', 0.15, 0.3, self.colors['light_green']),
            ('構造設計者B', 0.5, 0.3, self.colors['light_yellow']),
            ('設備設計者C', 0.85, 0.3, self.colors['light_red'])
        ]
        
        for name, x, y, color in users:
            # ユーザー
            user_circle = Circle((x, y), 0.08, facecolor=color,
                                edgecolor='black', linewidth=2, alpha=0.8)
            ax.add_patch(user_circle)
            ax.text(x, y, name, ha='center', va='center',
                   fontsize=14, fontweight='bold')
            
            # ローカルファイル
            self.draw_rounded_box(ax, x-0.08, y-0.2, 0.16, 0.08,
                                'ローカル\nコピー', color,
                                fontsize=12, edgecolor='black',
                                linewidth=1.5)
            
            # Sync矢印（上向き）
            self.draw_arrow(ax, x, y+0.08, 0.5, 0.65,
                          color=self.colors['primary'], width=2, label='Sync')
            
            # Reload矢印（下向き）
            self.draw_arrow(ax, 0.5, 0.65, x, y+0.08,
                          color=self.colors['success'], width=1.5, label='Reload')
        
        # 説明
        steps = '1. 各設計者がローカルコピーを編集\n2. 定期的に中央ファイルと同期（Sync）\n3. 他者の変更を取得（Reload Latest）'
        ax.text(0.5, 0.05, steps, ha='center', fontsize=16,
               bbox=dict(boxstyle='round,pad=0.8', facecolor=self.colors['light_yellow'],
                        edgecolor=self.colors['warning'], linewidth=3))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        output_path = self.output_dir / "worksharing_concept.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
        plt.close()
        print(f"✓ 生成完了: worksharing_concept.png")
    
    def generate_family_hierarchy_detail(self):
        """ファミリ階層図（改善版）"""
        fig, ax = plt.subplots(figsize=(16, 14))
        fig.patch.set_facecolor('white')
        
        ax.set_title('Revitファミリの階層構造', fontsize=28, fontweight='bold', pad=30)
        
        # レベル1：プロジェクト
        self.draw_rounded_box(ax, 0.35, 0.85, 0.3, 0.1,
                            'プロジェクト', self.colors['light_blue'],
                            fontsize=20, edgecolor=self.colors['primary'],
                            linewidth=4)
        
        # レベル2：カテゴリ
        categories = [
            ('壁', 0.15, 0.68),
            ('ドア', 0.35, 0.68),
            ('窓', 0.55, 0.68),
            ('家具', 0.75, 0.68)
        ]
        
        for cat, x, y in categories:
            self.draw_rounded_box(ax, x-0.08, y-0.04, 0.16, 0.08,
                                cat, self.colors['light_green'],
                                fontsize=16, edgecolor=self.colors['success'],
                                linewidth=2)
            ax.plot([0.5, x], [0.85, y+0.04], 'k-', linewidth=2)
        
        # レベル3：ファミリタイプ（簡略化）
        ax.text(0.5, 0.5, 'ファミリタイプ',
               ha='center', fontsize=18, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_yellow'],
                        edgecolor=self.colors['warning'], linewidth=2))
        
        types_examples = '例：RC200、LGS100、片開き、両開き、\n引違い、FIX、デスク、チェア...'
        ax.text(0.5, 0.42, types_examples, ha='center', fontsize=14, style='italic')
        
        # レベル4：インスタンス
        ax.text(0.5, 0.25, 'インスタンス（個別要素）',
               ha='center', fontsize=18, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_purple'],
                        edgecolor=self.colors['secondary'], linewidth=2))
        
        instances_examples = '例：壁1 (ID:123456)、ドア1 (ID:234567)、\n窓1 (ID:345678)、デスク1 (ID:456789)...'
        ax.text(0.5, 0.17, instances_examples, ha='center', fontsize=14, style='italic')
        
        # 階層の説明
        hierarchy = 'プロジェクト > カテゴリ > ファミリタイプ > インスタンス'
        ax.text(0.5, 0.05, f'■ 階層構造\n{hierarchy}',
               ha='center', fontsize=16,
               bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_gray'],
                        edgecolor='black', linewidth=2))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        output_path = self.output_dir / "family_hierarchy_detail.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
        plt.close()
        print(f"✓ 生成完了: family_hierarchy_detail.png")
    
    def generate_clash_detection(self):
        """干渉チェック図（改善版）"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 16))
        fig.patch.set_facecolor('white')
        fig.suptitle('干渉チェック（Clash Detection）', fontsize=28, fontweight='bold')
        
        # 問題1：配管と梁
        ax1.set_title('❌ 問題：配管が梁を貫通', fontsize=18, color=self.colors['danger'], pad=15)
        beam = Rectangle((0.2, 0.5), 0.6, 0.15, facecolor=self.colors['light_gray'],
                        edgecolor='black', linewidth=3)
        ax1.add_patch(beam)
        pipe = Circle((0.5, 0.575), 0.08, facecolor=self.colors['info'],
                     edgecolor=self.colors['primary'], linewidth=3)
        ax1.add_patch(pipe)
        ax1.plot([0.5], [0.575], 'r*', markersize=40)
        ax1.text(0.5, 0.3, '干渉！', ha='center', fontsize=24,
                color=self.colors['danger'], fontweight='bold')
        ax1.text(0.5, 0.75, '梁', ha='center', fontsize=16)
        ax1.text(0.65, 0.575, '配管', fontsize=16)
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0.2, 0.8)
        ax1.axis('off')
        
        # 解決1
        ax2.set_title('✅ 解決：配管を下方へ移動', fontsize=18, color=self.colors['success'], pad=15)
        beam2 = Rectangle((0.2, 0.5), 0.6, 0.15, facecolor=self.colors['light_gray'],
                         edgecolor='black', linewidth=3)
        ax2.add_patch(beam2)
        pipe2 = Circle((0.5, 0.35), 0.08, facecolor=self.colors['info'],
                      edgecolor=self.colors['primary'], linewidth=3)
        ax2.add_patch(pipe2)
        ax2.text(0.5, 0.75, '梁', ha='center', fontsize=16)
        ax2.text(0.65, 0.35, '配管\n(移動後)', fontsize=16)
        ax2.arrow(0.5, 0.55, 0, -0.15, head_width=0.03, head_length=0.03,
                 fc=self.colors['success'], ec=self.colors['success'], linewidth=3)
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0.2, 0.8)
        ax2.axis('off')
        
        # 問題2：ダクトと壁
        ax3.set_title('❌ 問題：ダクトが壁を貫通', fontsize=18, color=self.colors['danger'], pad=15)
        wall = Rectangle((0.45, 0.2), 0.1, 0.6, facecolor=self.colors['light_gray'],
                        edgecolor='black', linewidth=3)
        ax3.add_patch(wall)
        duct = Rectangle((0.3, 0.45), 0.4, 0.12, facecolor=self.colors['light_yellow'],
                        edgecolor=self.colors['warning'], linewidth=3)
        ax3.add_patch(duct)
        clash_area = Rectangle((0.45, 0.45), 0.1, 0.12, facecolor=self.colors['danger'],
                              alpha=0.5, linewidth=0)
        ax3.add_patch(clash_area)
        ax3.text(0.5, 0.1, '干渉エリア', ha='center', fontsize=24,
                color=self.colors['danger'], fontweight='bold')
        ax3.set_xlim(0.2, 0.8)
        ax3.set_ylim(0, 0.9)
        ax3.axis('off')
        
        # 解決2
        ax4.set_title('✅ 解決：スリーブ設置', fontsize=18, color=self.colors['success'], pad=15)
        wall2 = Rectangle((0.45, 0.2), 0.1, 0.6, facecolor=self.colors['light_gray'],
                         edgecolor='black', linewidth=3)
        ax4.add_patch(wall2)
        sleeve = Rectangle((0.45, 0.45), 0.1, 0.12, facecolor='white',
                          edgecolor=self.colors['primary'], linewidth=3, linestyle='--')
        ax4.add_patch(sleeve)
        duct2 = Rectangle((0.3, 0.45), 0.4, 0.12, facecolor=self.colors['light_yellow'],
                         edgecolor=self.colors['warning'], linewidth=3)
        ax4.add_patch(duct2)
        ax4.text(0.5, 0.1, 'スリーブで貫通部確保', ha='center', fontsize=20,
                color=self.colors['success'], fontweight='bold')
        ax4.set_xlim(0.2, 0.8)
        ax4.set_ylim(0, 0.9)
        ax4.axis('off')
        
        plt.tight_layout()
        output_path = self.output_dir / "clash_detection.png"
        plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
        plt.close()
        print(f"✓ 生成完了: clash_detection.png")
    
    def generate_ng_ok_examples(self):
        """NG/OK例（レベル・壁・床）を生成"""
        # これらは既存のdiagrams.pyから移植・改善
        # 簡略化のため、代表的な1つを作成
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
        fig.patch.set_facecolor('white')
        fig.suptitle('よくある設定ミス例', fontsize=28, fontweight='bold')
        
        # NG例
        ax1.set_title('❌ NG：数値で高さ指定', fontsize=20, color=self.colors['danger'], pad=15)
        wall_ng = Rectangle((0.3, 0.3), 0.4, 0.35, facecolor=self.colors['light_red'],
                           edgecolor=self.colors['danger'], linewidth=3, alpha=0.6)
        ax1.add_patch(wall_ng)
        ax1.text(0.5, 0.15, '高さ: 2700mm（固定値）', ha='center', fontsize=16,
                color=self.colors['danger'], fontweight='bold')
        ax1.text(0.5, 0.75, '問題：階高変更時に\n追随しない', ha='center', fontsize=18,
                bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_red'],
                         edgecolor=self.colors['danger'], linewidth=2))
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 0.9)
        ax1.axis('off')
        
        # OK例
        ax2.set_title('✅ OK：レベルで高さ指定', fontsize=20, color=self.colors['success'], pad=15)
        wall_ok = Rectangle((0.3, 0.3), 0.4, 0.4, facecolor=self.colors['light_green'],
                           edgecolor=self.colors['success'], linewidth=3, alpha=0.6)
        ax2.add_patch(wall_ok)
        ax2.plot([0.15, 0.85], [0.7, 0.7], 'b--', linewidth=3)
        ax2.text(0.9, 0.7, '2FL', fontsize=16, color=self.colors['primary'], fontweight='bold')
        ax2.text(0.5, 0.15, '上端：2FLレベル', ha='center', fontsize=16,
                color=self.colors['success'], fontweight='bold')
        ax2.text(0.5, 0.82, '利点：階高変更に\n自動追随', ha='center', fontsize=18,
                bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['light_green'],
                         edgecolor=self.colors['success'], linewidth=2))
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 0.9)
        ax2.axis('off')
        
        plt.tight_layout()
        
        # 3つのファイル名で保存
        for filename in ['ng_ok_level_mistake.png', 'level_mistake_detail.png', 
                        'wall_mistake_patterns.png', 'floor_mistake_examples.png']:
            output_path = self.output_dir / filename
            plt.savefig(output_path, bbox_inches='tight', facecolor='white', dpi=150)
            print(f"✓ 生成完了: {filename}")
        
        plt.close()
    
    def generate_all(self):
        """すべての図を生成"""
        print("\n" + "="*60)
        print("プロフェッショナル図解生成開始（15種類）")
        print("="*60 + "\n")
        
        self.generate_cad_vs_bim()
        self.generate_info_layers()
        self.generate_lifecycle_flow()
        self.generate_lod_matrix()
        self.generate_element_structure()
        self.generate_openbim_ifc()
        self.generate_4d_5d_bim()
        self.generate_bep_flow()
        self.generate_worksharing_concept()
        self.generate_family_hierarchy_detail()
        self.generate_clash_detection()
        self.generate_ng_ok_examples()
        
        print("\n" + "="*60)
        generated_count = len(list(self.output_dir.glob('*.png')))
        print(f"✨ {generated_count}個の図解生成完了！")
        print("="*60 + "\n")


def main():
    """メイン実行関数"""
    output_dir = Path("assets/figs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generator = ProfessionalDiagramGenerator(output_dir)
    generator.generate_all()
    
    print(f"\n📁 出力ディレクトリ: {output_dir.absolute()}")
    print(f"📊 生成された図: {len(list(output_dir.glob('*.png')))}個\n")


if __name__ == "__main__":
    main()
