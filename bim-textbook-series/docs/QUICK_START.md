# クイックスタートガイド

## 🚀 今すぐ試す

### 1. 必要なパッケージをインストール
```bash
pip install matplotlib pillow reportlab python-pptx
```

### 2. ビルド実行
```bash
cd bim-textbook-series
python src/build.py
```

### 3. 生成物の確認
```bash
# 章ファイル（Markdown）
ls manuscript/vol1_2kyu/
ls manuscript/vol2_jun1kyu/

# 図表（PNG）
ls assets/figs/

# PDF・PPTX
ls dist/
```

## 📝 原稿の編集

`MASTER.md`を編集して、再度`python src/build.py`を実行するだけ！

## 🎯 このシステムの特徴

1. **1ファイル管理**: MASTER.mdに全章を記述
2. **自動分割**: 章ごとのファイルに自動分割
3. **図の自動生成**: Pythonで図をPNG生成
4. **PDF/PPTX出力**: 教科書とスライドを一括生成

## 📚 コンテンツ

### VOL1: 2級対応（7章）
1. BIMとは何か
2. 建築生産とBIM
3. BIMモデルの中身
4. LODの考え方
5. IFCとOPEN BIM
6. BIM導入の効果と注意点
7. 2級試験対策

### VOL2: 準1級対応（6章）
1. 建築をBIMで表現するとは
2. BIMモデリングの考え方
3. 試験で評価されるポイント
4. よくある失敗例
5. 試験環境対策
6. 準1級 模擬課題

## 💡 ヒント

- 図を追加したい場合は`src/diagrams.py`にメソッドを追加
- PDFスタイルは`src/pdf_build.py`で変更
- PPTXテーマは`src/pptx_build.py`で変更

詳細は`README.md`をご覧ください。
