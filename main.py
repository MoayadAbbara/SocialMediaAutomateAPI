from flask import Flask, jsonify, request
import ScrapeData
import ImageServices
import InstagramServices
import TwitterServices
import DatabaseServices
import FacebookServices
app = Flask(__name__)


@app.route('/api/scrape', methods=['GET'])
def api_scrape_announcements():
    lastfive = ScrapeData.LastFiveAnnouncements()
    DatabaseServices.addNewAnnouncements(lastfive)
    return jsonify('Done')



@app.route('/api/fetchdata', methods=['GET'])
def get_announcement_data():
    data = request.get_json()
    if 'url' not in data:
        return jsonify({'error': 'Missing URL parameter'}), 400
    
    url = data['url']
    text, images_list = ScrapeData.AnnouncementsDetails(url)
    dicOfData = {
        'text': text,
        'images': images_list
    }
    return jsonify(dicOfData)



@app.route('/instagram_post', methods=['POST'])
def InstagramPost():
    images_paths = []
    data = request.get_json()
    if 'text' not in data or 'images' not in data:
        return jsonify({'error': 'Missing URL parameter'}), 400
    
    text = data['text']
    image_url = data['images']
    for url in image_url :
        print(url)
    if image_url : 
        images_paths = ImageServices.download_the_images(image_url)
    for path in images_paths :
        ImageServices.add_padding(path)
    InstagramServices.post_on_instagram(text , images_paths)
    ImageServices.delete_the_images(images_paths)
    return jsonify({'message': 'Image posted to Instagram successfully.'}), 200


@app.route('/twitter_post', methods=['POST'])
def TwitterPost():
    images_paths = []
    data = request.get_json()
    if 'text' not in data or 'images' not in data:
        return jsonify({'error': 'Missing URL parameter'}), 400
    
    text = data['text']
    image_url = data['images']
    if image_url : 
        images_paths = ImageServices.download_the_images(image_url)
    media_ids = TwitterServices.uploadMediaTwitter(images_paths)
    TwitterServices.post_on_twitter(text , media_ids)
    ImageServices.delete_the_images(images_paths)
    return jsonify({'message': 'Image posted to Twitter successfully.'}), 200



@app.route('/facebook_post', methods=['POST'])
def FacebookPost():
    images_paths = []
    data = request.get_json()
    if 'text' not in data or 'images' not in data:
        return jsonify({'error': 'Missing URL parameter'}), 400
    text = data['text']
    image_url = data['images']
    if image_url : 
        images_paths = ImageServices.download_the_images(image_url)
    FacebookServices.Post_On_Facebook(text , images_paths)
    ImageServices.delete_the_images(images_paths)
    return jsonify({'message': 'Image posted to Facebook successfully.'}), 200



if __name__ == '__main__':
    app.run(port=5001)