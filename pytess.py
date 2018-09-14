import io
import os
import sys
import pyperclip
import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter


def get_text(resource):
    if os.path.isfile(resource):
        image = Image.open(resource)
    else:
        r = requests.get(resource)
        image = Image.open(io.BytesIO(r.content))
    image.filter(ImageFilter.SHARPEN)
    text = pytesseract.image_to_string(image)
    return text


if __name__ == '__main__':
    bin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bin'))
    os.environ['PATH'] += '{}{}'.format(os.pathsep, bin_dir)

    if len(sys.argv) > 1:
        text = get_text(sys.argv[1])
        print(text)
        pyperclip.copy(text)
    else:
        print('Welcome to PyTess OCR.\n')
        while True:
            try:
                resource = input('\nImage URL or File: ')
                text = get_text(resource)
                print('\n{}\n'.format(text))
                print('The above text has been copied to your clipboard.')
                pyperclip.copy(text)
            except (KeyboardInterrupt, SystemExit):
                print('Caught exit signal. Shutting down...')
                sys.exit(0)
            except Exception as error:
                print('Caught Exception: {}'.format(error))
                print('Please try something different...')
                continue
