import os
import requests
from datetime import datetime, timedelta
import boto3

# 環境変数を取得
NOTION_TOKEN = os.environ['NOTION_TOKEN']
DATABASE_ID = os.environ['DATABASE_ID']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2021-05-13",
        "Content-Type": "application/json"
    }

    # 1ヶ月前の日付を取得
    one_month_ago = datetime.now() - timedelta(days=30)

    # データベースからアイテムを取得
    read_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(read_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to read database: {response.text}")

    # アイテムを確認し、古いものを削除
    for item in response.json().get("results", []):
        # 作成日時を取得
        created_time = item.get("created_time")
        if created_time:
            created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            if created_time < one_month_ago:
                # アーカイブする
                page_id = item.get("id")
                archive_url = f"https://api.notion.com/v1/pages/{page_id}"
                data = {"archived": True}
                archive_response = requests.patch(archive_url, json=data, headers=headers)
                if archive_response.status_code != 200:
                    raise Exception(f"Failed to archive page: {archive_response.text}")

    # SNS送信処理
    sns = boto3.client('sns')
    # メッセージの送信
    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message='NotionDB自動アーカイブプログラムが実行されました。',
        Subject='Lambda実行通知'
    )

    return {
        'statusCode': 200,
        'body': 'Old pages archived successfully'
    }
