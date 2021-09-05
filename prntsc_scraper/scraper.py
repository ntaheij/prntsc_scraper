# Web scraper for prnt.sc
# Version: 1.0
# Date: 2021-09-05
# Author: NTaheij

import time
import requests
from bs4 import BeautifulSoup
import string
import argparse as argparser
import os

# Headers for requests copied from browser when accessing prnt.sc
headers = {
    'authority': 'prnt.sc',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

# List of all possible characters in a prnt.sc code, base stores the length of this.
# Using base 36 so all combinations of characters are possible.
code_chars = list(string.ascii_lowercase) + ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
base = len(code_chars)

# Converts digit to a letter based on character codes
def digit_to_char(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)

# Returns the string representation of a number in a given base.
def str_base(number, base):
    if number < 0:
        return '-' + str_base(-number, base)
    (d, m) = divmod(number, base)
    if d > 0:
        return str_base(d, base) + digit_to_char(m)
    return digit_to_char(m)

# Returns the next code given the current code
def next_code(curr_code):
    curr_code_num = int(curr_code, base)
    return str_base(curr_code_num + 1, base)

# Parses the HTML from the prnt.sc page to get the image URL.
def get_img_url(code):
    html = requests.get(f"http://prnt.sc/{code}", headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    img_url = soup.find_all('img', {'class': 'no-click screenshot-image'})
    return img_url[0]['src']

# Saves image from URL
def get_img(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{path}.png", 'wb') as f:
            f.write(response.content)
        return
    raise Exception(f"Response Code {response.status_code} for URL: {url} ")

def main():
    parser = argparser.ArgumentParser()
    parser.add_argument('--start_code', help='6 character string made up of lowercase letters and numbers which is '
                                             'where the scraper will start. e.g. abcdef -> abcdeg -> abcdeh',
                                        default='lj9me9')
    parser.add_argument('--timeout', help='The time out between requests.',
                                        default='5')
    parser.add_argument('--count', help='The number of images to scrape.', default='100')
    parser.add_argument('--output', help='The path where images will be stored.', default='output/')

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    code = args.start_code
    for i in range(int(args.count)+1):
        code = next_code(code)
        try:
            url = get_img_url(code)
            get_img(url, args.output + f"/{code}")
            print(f"Saved image number {i}/{args.count} with code: {code}")
        except Exception as e:
            print(f"Error with image: {code}. Error: {e}")
        time.sleep(int(args.timeout))

if __name__ == '__main__':
    main()