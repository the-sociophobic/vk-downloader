#!/usr/bin/python3
# Original project page: https://github.com/sergei-bondarenko/vk-downloader

import sys
import os
import re
import pyperclip
from urllib.request import urlopen, urlretrieve
from colorama import init, Fore, Back, Style

init(convert=True)


def main():
    
    URL = sys.argv[1]
    if "vk.com" and "video" and "_" not in URL or URL is None:
        print()
        print("[" + Fore.RED + "-" + Style.RESET_ALL + "]" + " ERROR!!!\n"
              "Put video URL as argument.\n"
              "URL Sample: https://vk.com/video1315763_456239439")
        sys.exit(2)
    # converting part
    if "http://" in URL:
        URL = URL.replace("http", "https")
    if "z=" in URL:
        URL = URL.split("z=", 1)[-1]
        URL = URL.split("%2F", 1)[0]
        URL = "https://vk.com/" + URL

    print("")
    page = urlopen(URL)
    content = page.read()
    page.close()
    link = content.decode('utf-8', "ignore")
    urls = re.findall('<source src=\"([^"]*)\"', link)

    for i in ['1080.mp4', '720.mp4', '360.mp4', '240.mp4']:
        for url in urls:
            if i in url:
                source = url.replace('\\/', '/')
                reg = re.compile(r'/([^/]*\.mp4)')
                name = reg.findall(source)[0]
                path = "videos/"
                # checks if folder exists
                if not os.path.exists(path):
                    os.makedirs(path)
                fullpath = os.path.join(path, name)
                if os.path.exists(fullpath):
                    print("[" + Fore.RED + "-" + Style.RESET_ALL + "] " + name + " already exists")
                    sys.exit(0)
                print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "]" + " Downloading...")
                urlretrieve(source, fullpath)
                print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "]" + " Saved as " + name)
                sys.exit(0)

    print("[" + Fore.RED + "-" + Style.RESET_ALL + "] " + "Can't find video.")
    sys.exit(2)


if __name__ == '__main__':
    main()
