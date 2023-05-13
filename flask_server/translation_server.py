import six
from google.cloud import translate_v2 as translate
import os
import cv2
import pytesseract
from flask import Flask, request
import pyautogui
import warnings

# define tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'/bin/tesseract'

# ignore warnings
warnings.filterwarnings('ignore')

# define translation function to translate the text from kannada to english
def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    translate_client = translate.Client().from_service_account_json(os.environ['CRED_FILE_PATH'])

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)
    # return the translated text
    return result["translatedText"]

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    return 'Hello, this is the translation server!'

@app.route('/translate', methods=['POST'])
def translate_image():
    # get the image file from the request
    image_file = request.files['image']
    # save the image to disk
    image_path = 'image.jpg'
    image_file.save(image_path)
    # perform OCR on the image
    image = cv2.imread(image_path)

    # perform image resizing
    screen_width, screen_height = pyautogui.size()
    image_height, image_width, _= image.shape
    resize_metric = 0.8
    while(True):
        if(image_height<screen_height and image_width<screen_width):
            image = cv2.resize(image, (image_width, image_height),interpolation=cv2.INTER_AREA)
            break
        image_height = int(image_height*resize_metric)
        image_width = int(image_width*resize_metric)
    
    # convert the image to grayscale
    black_and_white = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kn_text = ''
    # OCR the image, supplying the country code as the language parameter
    for psm_value in range(7,13):
        # define the tesseract options
        # try different psm values to find one with the best result
        options = "-l {} --psm {} --oem {}".format('kan', psm_value, 1)
        new_kn_text = pytesseract.image_to_string(black_and_white, config=options)
        print(new_kn_text.replace('\n',' '))
        if(len(new_kn_text)>len(kn_text)):
            kn_text = new_kn_text
    # return the result of OCR
    kn_text = kn_text.replace('\n',' ')
    print(kn_text)
    # translate the text
    en_text = translate_text('en', kn_text)
    print(en_text)
    if(en_text.isspace()):
        return 'no text detected'
    # return the translated text
    return en_text

if __name__ == '__main__':
    app.run(debug=True)