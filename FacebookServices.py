import requests
import consts

# Your access token
auth_token = consts.auth_token
page_id = consts.page_id

# List of photo paths to upload
img_list = ['laravel8530.jpg', 'Python-logo-notext.svg.png']




def postImage(img):
    url = f"https://graph.facebook.com/{page_id}/photos?access_token=" + auth_token
    files = {
        'file': open(img, 'rb'),
    }
    data = {
        "published": False  # Upload without publishing
    }
    id = requests.post(url, files=files, data=data).json()
    return id



def Post_On_Facebook(text , imagelist):
    imgs_id = []
    for img in imagelist:
        post_id = postImage(img)
        imgs_id.append(post_id['id'])

    args = {
        "message": text
    }
    for idx, img_id in enumerate(imgs_id):
        key = f"attached_media[{idx}]"
        args[key] = f"{{'media_fbid': '{img_id}'}}"

    url = f"https://graph.facebook.com/{page_id}/feed?access_token=" + auth_token
    response = requests.post(url, data=args).json()
    
    if 'id' in response:
        print("Successfully posted the photos. Post ID:", response['id'])
    else:
        print("Failed to post. Response:", response)

