import io
import os
import sys
import pyperclip
import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.abspath(os.path.join(sys._MEIPASS, relative))
    return os.path.abspath(os.path.join(relative))


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
    bin_dir = resource_path('bin')
    os.environ['PATH'] += '{0}{1}{0}'.format(os.pathsep, bin_dir)
    # os.environ['TESSDATA_PREFIX'] = bin_dir

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
                sep = '----------------------------------------'
                print('\n{1}\n{0}\n{1}\n'.format(text, sep))
                print('The above text has been copied to your clipboard.')
                pyperclip.copy(text)
            except (KeyboardInterrupt, SystemExit):
                print('Caught exit signal. Shutting down...')
                sys.exit(0)
            except Exception as error:
                print('Caught Exception: {}'.format(error))
                print('Please try something different...')
                continue
