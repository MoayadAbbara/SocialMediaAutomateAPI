from instagrapi import Client
import consts
def post_on_instagram (postCaption , images_path) :

    # Create an Instagrapi client
    client = Client(request_timeout=7)
    client.login(consts.InstagramUserName, consts.InstagramPassword)

    if len(images_path) == 1 :
    # Specify the path to the photo you want to upload
        photo_path = images_path[0]
        # Upload the photo
        client.photo_upload(photo_path, caption=postCaption)
    elif len(images_path) > 1 :
        client.album_upload(paths= images_path , caption=postCaption)
    # Close the client session
    client.logout()