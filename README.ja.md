# Hook Preference Cards

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português (Brasil)](README.pt-BR.md)

文章の導入、タイトル、発想練習向けのローカルなカード式選好ページです。好き・嫌い・スキップ・無効な導入の指定、取り消し、進捗の保存と再開、特徴統計、JSON/CSV 出力に対応します。Python 標準ライブラリのサーバーと通常の HTML/CSS/JavaScript を使い、フロントエンド依存の導入は不要です。

## 必要な環境

Python 3.10+; HTML/CSS/JavaScript

## 設定とエントリーポイント

`data/hooks.json`, `runtime/`, `--port`, `--state`, `http://127.0.0.1:8769`

## 導入と使用方法

```shell
git clone https://github.com/southingchina/hook-preference-cards.git
cd hook-preference-cards
python server.py --port 8769
```


```shell
python -m unittest discover -s tests -v
```


## 公開範囲と制限

起動後は http://127.0.0.1:8769 を開きます。選択は runtime/ に保存され、--port と --state でポートと保存先を変更できます。ループバックのみで待ち受け、公開向けの複数ユーザー認証はありません。data/hooks.json は独自に作成した合成例 20 件で、実在クリエイターの素材や反応数ではありません。ID を重複させず、review.status=approved のカードを使います。カード集を変える際は新しい状態ファイルを指定してください。統計は個人の選択を示すもので、視聴者の反応予測ではありません。

## 検証記録

2026-10-24 · Python / HTTP: 14 ✓

## ライセンスと出典

[MIT](LICENSE)

これらは文書の言語版です。アプリ画面、CLI 出力、実行ファイルは現在の実装に従います。

[中国語の詳細リファレンス](README.zh-CN.md) · [言語版の保守方針](docs/LOCALIZATION.md)

[Issues](https://github.com/southingchina/hook-preference-cards/issues) — 再現できる問題は合成データで報告し、ログの認証情報や個人情報を除いてください。
