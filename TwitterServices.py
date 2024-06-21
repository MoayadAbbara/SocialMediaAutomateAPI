from requests_oauthlib import OAuth1Session
import pyshorteners
import base64
import consts


def shorurl(long_url) : 
    #TinyURL shortener service
    type_tiny = pyshorteners.Shortener()
    return type_tiny.tinyurl.short(long_url)



# Prepare OAuth1 session
oauth = OAuth1Session(
    consts.consumer_key,
    client_secret=consts.consumer_secret,
    resource_owner_key=consts.access_token,
    resource_owner_secret=consts.access_token_secret,
)


def uploadMediaTwitter(image_paths) :
    media_ids = []
    for media_file_path in image_paths:
        with open(media_file_path, 'rb') as file:
            media_data = base64.b64encode(file.read()).decode('utf-8')

        media_payload = {'media_data': media_data}
        response = oauth.post(consts.upload_url, data=media_payload)

        if response.status_code == 200:
            media_id = response.json()['media_id']
            media_ids.append(str(media_id))
        else:
            print(f'Error uploading media: {response.status_code} {response.text}')
            exit()
    return media_ids


def post_on_twitter(caption , media_ids) :
    tweet_payload = {
        'text': caption,
        'media': {'media_ids': media_ids}
    }
    tweet_response = oauth.post(consts.tweet_url, json=tweet_payload)
    return tweet_response