import pyqrcode
from pyqrcode import QRCode
import sys
from PIL import Image
from pyzbar.pyzbar import decode


def gen_qrcode(txt,rez):
    # Generate QR code from string
    url = pyqrcode.create(txt)

    # save rezult
    url.png(rez, scale = 8)


def scan_qrcode(img):
    data = decode(Image.open('img'))
    print(data)



    return txt



def main():
    #Example generate qr-code
    gen_qrcode(sys.argv[1],sys.argv[2])

if __name__ == "__main__":
    main()
