import urllib.request

def download_image(image_url, save_path):
    urllib.request.urlretrieve(image_url, save_path)
