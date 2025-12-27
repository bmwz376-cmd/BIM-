# ダウンロード

BIM利用技術者試験 教科書シリーズの各種ファイルをダウンロードできます。

---

## 📕 VOL1: 2級対応（知識編）

### PDF版（印刷用）
- **ファイル名**: `vol1_2kyu.pdf`
- **サイズ**: 261 KB
- **ページ数**: 約30ページ
- **用途**: 印刷、タブレット閲覧、PDF注釈

[📥 VOL1_2級対応.pdf をダウンロード](dist/vol1_2kyu.pdf)

---

### PPTX版（講義用スライド）
- **ファイル名**: `vol1_2kyu.pptx`
- **サイズ**: 67 KB
- **スライド数**: 約50枚
- **用途**: 講義、セミナー、プレゼンテーション

[📥 VOL1_2級対応.pptx をダウンロード](dist/vol1_2kyu.pptx)

---

## 📗 VOL2: 準1級対応（実技編）

### PDF版（印刷用）
- **ファイル名**: `vol2_jun1kyu.pdf`
- **サイズ**: 306 KB
- **ページ数**: 約35ページ
- **用途**: 印刷、タブレット閲覧、PDF注釈

[📥 VOL2_準1級対応.pdf をダウンロード](dist/vol2_jun1kyu.pdf)

---

### PPTX版（講義用スライド）
- **ファイル名**: `vol2_jun1kyu.pptx`
- **サイズ**: 53 KB
- **スライド数**: 約45枚
- **用途**: 講義、セミナー、プレゼンテーション

[📥 VOL2_準1級対応.pptx をダウンロード](dist/vol2_jun1kyu.pptx)

---

## 🎨 図表（PNG画像）

全10種類の図表を個別にダウンロードできます：

1. [CAD vs BIM 比較図](assets/figs/cad_vs_bim.png)
2. [BIM情報の3層構造](assets/figs/info_layers.png)
3. [建築ライフサイクルフロー](assets/figs/lifecycle_flow.png)
4. [部材（Element）の構造](assets/figs/element_structure.png)
5. [LODマトリクス](assets/figs/lod_matrix.png)
6. [OPEN BIMとIFC連携図](assets/figs/openbim_ifc.png)
7. [レベル設定の誤り例と正解例](assets/figs/ng_ok_level_mistake.png)
8. [レベル設定ミスの詳細図](assets/figs/level_mistake_detail.png)
9. [壁の高さ設定ミスパターン](assets/figs/wall_mistake_patterns.png)
10. [床配置のよくある失敗例](assets/figs/floor_mistake_examples.png)

---

## 📦 一括ダウンロード（予定）

将来的に以下の形式での一括ダウンロードを提供予定です：

- **ZIP形式**: 全PDF・PPTX・図表をまとめたアーカイブ
- **EPUB形式**: 電子書籍リーダー向け
- **Markdown形式**: 原稿ファイル（編集可能）

---

## 🔄 自動生成について

これらのファイルは、`MASTER.md` を元に自動生成されています。

### 再生成方法

```bash
cd /home/user/webapp/bim-textbook-series
python src/build.py
```

以下のファイルが自動生成されます：
- PDF（VOL1、VOL2）
- PPTX（VOL1、VOL2）
- 図表（PNG × 10種類）
- 章ファイル（Markdown × 15ファイル）

---

## 📄 ライセンス

本教材は **MIT License** で公開されています。教育目的での利用、改変、再配布が可能です。

---

## 🤝 改善提案

内容の改善提案、誤字脱字の報告は、[GitHubリポジトリ](https://github.com/bmwz376-cmd/BIM-)までお願いします。

---

## 📊 ファイル一覧

| ファイル | 種類 | サイズ | 用途 |
|---------|------|--------|------|
| vol1_2kyu.pdf | PDF | 261 KB | 印刷・閲覧 |
| vol1_2kyu.pptx | PPTX | 67 KB | 講義・プレゼン |
| vol2_jun1kyu.pdf | PDF | 306 KB | 印刷・閲覧 |
| vol2_jun1kyu.pptx | PPTX | 53 KB | 講義・プレゼン |
| cad_vs_bim.png | PNG | 37 KB | 図表 |
| element_structure.png | PNG | 40 KB | 図表 |
| info_layers.png | PNG | 24 KB | 図表 |
| lifecycle_flow.png | PNG | 26 KB | 図表 |
| lod_matrix.png | PNG | 33 KB | 図表 |
| ng_ok_level_mistake.png | PNG | 22 KB | 図表 |
| openbim_ifc.png | PNG | 84 KB | 図表 |
| level_mistake_detail.png | PNG | 45 KB | 図表 |
| wall_mistake_patterns.png | PNG | 38 KB | 図表 |
| floor_mistake_examples.png | PNG | 41 KB | 図表 |

**合計サイズ**: 約1.0 MB

---

**最終更新**: 2024年12月  
**バージョン**: 1.0.0
