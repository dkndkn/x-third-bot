import tweepy
import os
import pytz
import random
import time
from datetime import datetime

# --- 時間帯別の挨拶リスト（プロジェクト向け） ---
morning_greetings = [
    "おはようございます！今日のプロジェクトタスクを確認して、目標達成に向けてスタートしましょう！",
    "新しい朝です。今週のマイルストーンを見直して、今日の優先事項を決めましょう。",
    "プロジェクト進行中！リソースやスケジュールをチェックして、良い一日に。",
    "チームミーティングの準備はできていますか？今日もプロジェクトを前進させましょう！",
    "おはようございます！バグ修正と機能追加のバランスをとって、効率的に進めましょう。"
]

afternoon_greetings = [
    "こんにちは！進捗は順調ですか？午後もプロジェクトに注力しましょう。",
    "ランチ後はタスクレビューの時間です。Pull Requestの確認を忘れずに。",
    "午後の集中タイム。仕様書のアップデートやテストを進めていきましょう！",
    "ドキュメント作成はいかがですか？プロジェクトの品質向上に繋がります。",
    "プロジェクト管理ツールをチェックして、残タスクを整理しましょう。"
]

evening_greetings = [
    "一日お疲れさまです！今日の成果をチームチャットで共有しましょう。",
    "コミットを終えたら、明日のタスクをプランニングしてくださいね。",
    "今日のレビューを終えたら、プロジェクトの振り返りミーティングをセットしましょう。",
    "デプロイは無事完了しましたか？ログを確認して一日の終わりにしましょう。",
    "お疲れさまです！バグの再現手順をドキュメント化しておくと安心です。"
]

night_greetings = [
    "こんばんは！ナイトリリースの準備はOKですか？不具合チェックをお忘れなく。",
    "夜間作業は落ち着いて。バックログの整理やロードマップレビューに最適な時間です。",
    "深夜のドキュメント更新タイム、集中して取り組みましょう！",
    "静かな時間だからこそ、プロジェクトの新機能企画を練るチャンスです。",
    "夜のうちにチームへのサポートメッセージを送って、コミュニケーションを円滑に！"
]
# -----------------------------

def create_tweet_text():
    # 日本時間を取得
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst)
    h = now.hour

    # 時間帯ごとにリストを切り替え
    if 5 <= h < 12:
        greetings = morning_greetings
    elif 12 <= h < 17:
        greetings = afternoon_greetings
    elif 17 <= h < 22:
        greetings = evening_greetings
    else:
        greetings = night_greetings

    return random.choice(greetings)

def should_post():
    # 1日に4回の実行のうち 1 回だけ投稿する
    TOTAL_SLOTS = 4
    pick = random.randint(1, TOTAL_SLOTS)
    print(f"[debug] slot pick: {pick}/{TOTAL_SLOTS}")
    return pick == 1

def post_tweet():
    # 0～29分のランダムな待ち時間を入れる
    delay_minutes = random.randint(0, 29)
    print(f"[debug] delaying for {delay_minutes} minutes…")
    time.sleep(delay_minutes * 60)

    if not should_post():
        print("[info] this slot skipped. no tweet today.")
        return

    # GitHub Secrets からキーを読み込む
    consumer_key        = os.environ.get('X_API_KEY')
    consumer_secret     = os.environ.get('X_API_KEY_SECRET')
    access_token        = os.environ.get('X_ACCESS_TOKEN')
    access_token_secret = os.environ.get('X_ACCESS_TOKEN_SECRET')

    # X（旧Twitter）API 認証
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    text = create_tweet_text()
    try:
        resp = client.create_tweet(text=text)
        print(f"[info] Tweet posted! id={resp.data['id']}")
    except Exception as e:
        print(f"[error] failed to post: {e}")

if __name__ == "__main__":
    post_tweet()
