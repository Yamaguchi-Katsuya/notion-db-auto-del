# notion-db-auto-del
notionAPIとAWS lambdaを用いた、notionDBで古くなったpageの自動アーカイブプログラム  
2023/11月時点ではnotionAPIでの削除はできないためアーカイブで代用

## lambda使用方法
- lambda > 関数ページにてプロジェクト直下の `lambda.zip` をアップロード

## 補足
- `lambda_function.py` でSNS送信処理を記載しているが、通知が必要ない場合は削除で問題なし
- メールなどでの通知をしたい場合は別途AWS SNSのトピック作成が必要
- [参考リンク](https://repost.aws/ja/knowledge-center/sns-topic-lambda)
