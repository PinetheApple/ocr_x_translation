import six
from google.cloud import translate_v2 as translate
import os
import cv2
import pytesseract

# define tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'/bin/tesseract'

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
    # display the translated text
    print(u"Translation: {}".format(result["translatedText"]))

def ocr(path):
    image = cv2.imread(path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # OCR the image, supplying the country code as the language parameter
    options = "-l {} --psm {}".format('kan', 3)
    kn_text = pytesseract.image_to_string(rgb, config=options)
    # return the result of OCR
    return kn_text

# call the ocr function to find the text in the image
text = ocr('../../Pictures/kannada_OCR.png')

# call the function to translate the detected text
translate_text('en',text)