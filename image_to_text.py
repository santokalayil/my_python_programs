# don't forget to install pytessereact libarary and its dependencies

import os
from PIL import Image
import pytesseract
import subprocess
subprocess = subprocess.Popen('which tesseract', shell=True, stdout=subprocess.PIPE)
path_binary = subprocess.stdout.read().decode('UTF-8').strip()

pytesseract.pytesseract.tesseract_cmd = path_binary  #"/usr/bin/tesseract"


def image2text(image_url):
    return pytesseract.image_to_string(Image.open(image_url))


if __name__ == "__main__":
    image_url = "tweetpic_1.jpg"
    converted_text = image2text(image_url)
    print(converted_text)
