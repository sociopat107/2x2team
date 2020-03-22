import pyqrcode
from pyqrcode import QRCode
import sys
from PIL import Image
from pyzbar.pyzbar import decode
import uuid

LOGO_IMAGE = 'crop.jpg'

def gen_qrcode(txt,rez):
    # Generate QR code from string
    url = pyqrcode.create(txt)

    # save rezult
    url.png(rez, scale = 8)

    im = Image.open(rez)
    im = im.convert("RGBA")
    logo = Image.open(LOGO_IMAGE)
    box = (120,120,200,200)
    im.crop(box)
    region = logo
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    im.paste(region,box)
    im.save(rez)


def scan_qrcode(img):
    #Decoding qr-image
    data = decode(Image.open('img'))
    print(data)

    #return rezult
    txt = data[0].data.decode('ascii')
    return txt

def gen_random_hash_for_order():
    return uuid.uuid4().hex

def main():
    #Example generate qr-code with first argument string and second png filename
    gen_qrcode(sys.argv[1],sys.argv[2])

if __name__ == "__main__":
    main()
