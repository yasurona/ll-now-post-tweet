import json
from generate_message import *


def post_tweet(twitter, bucket):
    url_media = 'https://upload.twitter.com/1.1/media/upload.json'
    url_post = 'https://api.twitter.com/1.1/statuses/update.json'

    # 画像をアップロード
    files = {'media': open('/tmp/post_image.png', 'rb')}
    res_media = twitter.post(url_media, files=files)

    # レスポンスを確認
    if res_media.status_code != 200:
        print('Failed to upload media: {}'.format(res_media.text))
        exit()

    # media_id を取得
    media_id = json.loads(res_media.text)['media_id']

    # 投稿文を生成
    message = generate_message(bucket)

    # アップロードした画像を添付したツイートを投稿
    params = {'status': message, 'media_ids': [media_id]}
    res_post = twitter.post(url_post, params=params)

    # レスポンスを確認
    if res_post.status_code == 200:
        print("Successfully posted.")
    else:
        print("Failed.")
        print(" - Response Status Code : {}".format(res_post.status_code))
        print(" - Error Code : {}".format(res_post.json()["errors"][0]["code"]))
        print(" - Error Message : {}".format(res_post.json()["errors"][0]["message"]))
