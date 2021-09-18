# 自動APIドキュメントGenerator : auto_api_doc_gen
![出力イメージ](https://user-images.githubusercontent.com/19645346/133891392-0abbfb2f-a0c7-44bf-96c8-05604a5e2cdc.png)

自然言語で記載した処理名から自動でAPI仕様書を途中まで作成します。

形態素解析して翻訳APIで英語化して決められた形式で出力します。


## 自動出力してくれるもの
- API一覧ファイルのリスト
    - お気に入り登録・削除・一覧はお気に入り関連.yamlにまとまるイメージ
- 各APIのURL、各種パラメータ設定
- 各APIごとに必要と思われる400系のエラーレスポンス
    - レスポンスの中身はcommon/ErrorResponse.yamlを参照するようにしています
- 簡単なリクエストボディ・レスポンスのSchema
    - Schemaは自動で推測が困難なためid, nameのみにしています。
        - 更新・登録系ならリクエストボディあり
        - 取得系ならレスポンスあり

## 対応形式
OpenAPI(Yaml v3.1)のみ対応


## セットアップ
```
git clone https://github.com/pei223/auto_apidoc_gen
pip install -r requirements.txt
```

## Run
```
python generate_api_doc.py --doc=<処理名をまとめたファイルのパス> --out=<出力フォルダパス> --setting=<設定ファイルパス>

# サンプル実行
python generate_api_doc.py --doc=sample_process_list_file.txt --out=docs --setting=sample_setting.json
```


## 処理名をまとめたファイルの形式
以下のように自然言語で記載した処理名を改行区切りでまとめたファイル。

sample_process_list_file.txtを参照。
```
店舗情報詳細を取得する
店舗情報の一覧を取得する
ユーザーを登録する
ユーザー情報を取得する
ユーザー情報を更新する
```

## 設定ファイルについて
以下のjson形式のファイル。

sample_setting.jsonを参照。
```
{
  "authorization": {  // 認証関連
    "required": true,  // 認証必須かどうか
    "token_type": "bearer"  // トークンの種類
  },
  "error_response_model": {  // エラーレスポンスのモデル。ここの内容はyamlのOpenAPI形式でそのままファイル出力される。
    "title": "エラーレスポンス",
    "type": "object",
    "properties": {
      "errors": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "code": {
              "type": "string"
            }
          },
          "required": [
            "code"
          ]
        }
      }
    },
    "required": [
      "errors"
    ]
  },
  "is_rest": true,  // RESTかどうか
  "add_internal_error": false,  // 内部エラーのレスポンスを各APIに記載するか
  "server_url": "http://localhost:3000",  // サーバーのURL
  "custom_translate_dict": {  // 使用者がカスタマイズできる翻訳辞書(日本語 -> 英語)
    "確定": "save"
  }
}
```


## 注意点
- !!!単純な文のみ認識します!!!
- 「注文履歴とユーザー情報を取得する」など複数の対象データ(注文履歴、ユーザー情報)が入っている場合はうまく動作しません。
- 「ユーザーの通知情報を取得する」のような入れ子になるとうまく動作しません。


## うまく出力するには
以下の形式で記載すると望ましい出力になりやすいです。
findではなくread系は～一覧、～リストなどと明示してください。
```
[対象データ名(お気に入りや注文履歴など)]を[登録、削除、取得]する
```





