'''
    @Author : subhendu.r.mishra@gmail.com
    
    @Description : Download APOD and set as desktop background
'''
from __future__ import print_function
import sys
import os
import ctypes
import argparse
import requests
from bs4 import BeautifulSoup

apod_base = "https://apod.nasa.gov/apod/"
apod_home = apod_base + "astropix.html"


def main():
    parser = argparse.ArgumentParser(description='Download APOD and set as desktop background')

    parser.add_argument(
        '--save-only',
        '-s',
        action='store_true',
        help='Only save the downloaded image in current directory')

    args = parser.parse_args()
    image_path = download_image()
    print("Image downloaded . Saved path {}".format(image_path))
    if not args.save_only:
        print(" Tryng to set desktop background")
        set_background(image_path)


def download_image():
    '''
        Download APOD image
    '''
    image_path = None
    try:
        r = requests.get(apod_home)
        print("Http Status : {}".format(r.status_code))
        if r.status_code in (200, 204):
            image_url = parse_apod_html(r.text)
            image_path = save_image(image_url)
    except Exception as e:
        print(e)

    return image_path


def parse_apod_html(html_text):
    '''
        Prase APOD HTML and find the High Quality image url
    '''
    image_url = None
    soup = BeautifulSoup(html_text, 'html.parser')
    for a in soup.find_all('a'):
        if list(a.find_all("img")):
            _image_url = a.get("href")
            ext = list(_image_url.split("."))[-1]
            if ext in ("jpg", "jpeg", "png"):
                image_url = apod_base + _image_url
                break

    print("Image url : " + image_url)
    return image_url


def save_image(image_url):
    '''
        Download and save the High Quality APOD image to disk
    '''
    image_name = list(image_url.split("/"))[-1]
    print("Image name : " + image_name)
    try:
        response = requests.get(image_url)
        with open(image_name, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(e)

    return image_name


def set_background(image_path):
    '''
        Set desktop background 
    '''
    print("Current platform : {}".format(sys.platform))
    if sys.platform.startswith("win"):
        print("You are using windows")
        set_win_background(image_path=image_path)
    else:
        print("This only works in Windows !!!")


def set_win_background(image_path=None):
    '''
        Set windows desktop background
    '''
    # Import wintypes
    from ctypes import wintypes

    if (image_path is None):
        print(" Internal error . Downloaded image path is null")
        return

    # Set constants
    SPI_SETDESKWALLPAPER = 0x0014
    SPIF_UPDATEINIFILE = 0x0001
    SPIF_SENDWININICHANGE = 0x0002

    user32 = ctypes.WinDLL('user32')
    SystemParametersInfo = user32.SystemParametersInfoW
    SystemParametersInfo.argtypes = ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint
    SystemParametersInfo.restype = wintypes.BOOL
    resp = SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, image_path,
                                SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
    if resp:
        print("Background set successfully !!")
    else:
        print("Background could not be set .")


if __name__ == "__main__":
    main()
