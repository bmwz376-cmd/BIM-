# BIM利用技術者試験 教科書シリーズ - 自動生成システム

**BIM利用技術者試験（2級・準1級）対応の教科書を1コマンドで自動生成するシステムです。**

## 🎯 特徴

- **1ファイル原稿管理**: `MASTER.md`に全章の原稿を記述
- **自動分割**: 章ごとのMarkdownファイルに自動分割
- **図表自動生成**: Pythonで図をPNG形式で自動生成
- **PDF/PPTX出力**: 教科書とスライドを一括生成
- **試験対策重視**: BIMの本質理解を促す構成

## 📁 ディレクトリ構造

```
bim-textbook-series/
├── README.md                 # このファイル
├── requirements.txt          # Python依存関係
├── MASTER.md                 # 全章の原稿（ここに執筆）★
├── src/
│   ├── build.py              # メインビルドスクリプト ★
│   ├── split_master.py       # 原稿分割
│   ├── diagrams.py           # 図の自動生成
│   ├── pdf_build.py          # PDF生成
│   ├── pptx_build.py         # PPTX生成
│   └── utils.py              # ユーティリティ
├── manuscript/
│   ├── vol1_2kyu/            # 2級用原稿（自動生成）
│   └── vol2_jun1kyu/         # 準1級用原稿（自動生成）
├── assets/
│   └── figs/                 # 図（自動生成PNG）
└── dist/
    ├── vol1_2kyu.pdf         # 2級教科書PDF
    ├── vol2_jun1kyu.pdf      # 準1級教科書PDF
    ├── vol1_2kyu.pptx        # 2級スライド
    └── vol2_jun1kyu.pptx     # 準1級スライド
```

## 🚀 使い方

### 1. 環境セットアップ

```bash
# 依存パッケージのインストール
pip install -r requirements.txt
```

### 2. 原稿を執筆

`MASTER.md`に全章の原稿を記述します：

```markdown
# BIM利用技術者試験 教科書シリーズ - マスター原稿

## VOL1: BIM利用技術者試験2級対応

### 第1章｜BIMとは何か

#### 1. 章のねらい
本章では、BIMの本質的な定義を理解します。
...

---CHAPTER_END---

### 第2章｜建築生産とBIM
...

---CHAPTER_END---

## VOL2: BIM利用技術者試験準1級対応

### 第1章｜建築をBIMで表現するとは
...
```

### 3. 一括ビルド（★ここが最重要★）

```bash
cd bim-textbook-series
python src/build.py
```

**このコマンド1つで以下を実行**:
1. `MASTER.md`を分割 → `manuscript/vol1_2kyu/`, `manuscript/vol2_jun1kyu/`
2. 図を自動生成 → `assets/figs/*.png`
3. PDF/PPTXを生成 → `dist/*.pdf`, `dist/*.pptx`

### 個別実行も可能

```bash
# 原稿分割のみ
python src/split_master.py

# 図生成のみ
python src/diagrams.py

# PDF生成のみ
python src/pdf_build.py

# PPTX生成のみ
python src/pptx_build.py
```

## 📝 原稿フォーマット

### 章の区切り

```markdown
## VOL1: BIM利用技術者試験2級対応

### 第1章｜タイトル
本文...

---CHAPTER_END---

### 第2章｜タイトル
本文...

---CHAPTER_END---
```

### 図の挿入

```markdown
![FIG:cad_vs_bim]()
```

→ `diagrams.py`の`generate_cad_vs_bim()`メソッドで自動生成されます

**実装済みの図**:
- `cad_vs_bim` - CAD vs BIM比較図
- `info_layers` - BIM情報の3層構造
- `lifecycle_flow` - 建築ライフサイクルフロー
- `element_structure` - 部材(Element)の構造
- `lod_matrix` - LODマトリクス
- `openbim_ifc` - OPEN BIMとIFC連携図
- `ng_ok_level_mistake` - レベル設定の誤り例と正解例

## 🛠️ カスタマイズ

### 新しい図の追加

`src/diagrams.py`に以下のようなメソッドを追加：

```python
def generate_your_figure(self):
    """あなたの図を生成"""
    fig, ax = plt.subplots(figsize=(10, 6))
    # 図の描画処理
    # ...
    output_path = self.output_dir / "your_figure.png"
    plt.savefig(output_path, bbox_inches='tight', facecolor='white')
    plt.close()
```

MASTER.mdで参照：
```markdown
![FIG:your_figure]()
```

### PDFスタイル変更

`src/pdf_build.py`の`setup_styles()`メソッドを編集

### PPTXテーマ変更

`src/pptx_build.py`の`PPTXBuilder`クラスを編集

## 📚 対応コンテンツ

### VOL1: BIM利用技術者試験2級対応
1. 第1章｜BIMとは何か
2. 第2章｜建築生産とBIM
3. 第3章｜BIMモデルの中身
4. 第4章｜LODの考え方
5. 第5章｜IFCとOPEN BIM
6. 第6章｜BIM導入の効果と注意点
7. 第7章｜2級試験対策

### VOL2: BIM利用技術者試験準1級対応
1. 第1章｜建築をBIMで表現するとは
2. 第2章｜BIMモデリングの考え方（後工程を考える）
3. 第3章｜試験で評価されるポイント（採点者目線）
4. 第4章｜よくある失敗例（レベル・壁・床）
5. 第5章｜試験環境対策（初期設定・制約）
6. 第6章｜準1級 模擬課題（自己チェックリスト付き）

## 🎓 教育方針

本教材は、BIMを「3D操作」ではなく、「情報設計」「建築生産プロセス」として理解させることを目的としています。

**重視する点**:
- ✅ BIMの本質的な概念理解
- ✅ よくある誤解の整理
- ✅ 実務での活用イメージ
- ✅ 試験対策（2級・準1級）

**避ける点**:
- ❌ ソフトの操作手順のみ
- ❌ 暗記中心の学習
- ❌ 表面的な理解

## 🔧 技術スタック

- **Python 3.8+**
- **図生成**: matplotlib, Pillow
- **PDF生成**: ReportLab
- **PPTX生成**: python-pptx

## 📊 生成例

### 実行ログ
```
╔══════════════════════════════════════════════════════════════╗
║     BIM利用技術者試験 教科書シリーズ - 自動生成システム     ║
╚══════════════════════════════════════════════════════════════╝

STEP 1/4: MASTER.md を章ファイルに分割
✅ 分割完了: VOL1=7章, VOL2=6章

STEP 2/4: 図表を自動生成
✅ 図生成完了: 10個

STEP 3/4: PDF教科書を生成
✅ PDF生成完了

STEP 4/4: PPTXスライドを生成
✅ PPTX生成完了

🎉 ビルド完了！ 🎉
```

## 📄 ライセンス

MIT License

## 🤝 貢献

Issue・PRを歓迎します！

### 貢献方法

1. このリポジトリをFork
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにPush (`git push origin feature/amazing-feature`)
5. Pull Requestを作成

### 原稿への貢献

- `MASTER.md`の内容改善
- 新しい章の追加
- 誤字・脱字の修正
- わかりやすい説明への改善

### コードへの貢献

- 新しい図の生成機能
- PDF/PPTXの見た目改善
- バグ修正
- パフォーマンス改善

## 📧 お問い合わせ

質問や提案がある場合は、Issueを作成してください。

## 🔗 関連リンク

- [一般社団法人 buildingSMART Japan](https://www.building-smart.or.jp/)
- [国土交通省 BIM/CIM活用ガイドライン](https://www.mlit.go.jp/tec/tec_tk_000084.html)
- [建築BIM利用技術者試験 公式サイト](https://www.building-smart.or.jp/certification/)

---

**作成者**: BIM教育チーム  
**バージョン**: 1.0.0  
**最終更新**: 2025-12-27
