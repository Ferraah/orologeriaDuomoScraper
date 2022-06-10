import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import sys

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    
    
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")

        if not img_url:
            # if img does not contain src attribute, just skip
            continue

        if "phpfiles" in img_url:
            # make the URL absolute by joining domain with the URL that is just extracted
            img_url = urljoin("https://www.orologeriaduomo.com/", img_url)
            urls.append(img_url)
            print(img_url)

    return urls


def download(url, pathname, index):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    
    filename = os.path.join(pathname, str(index))
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


def main(url, path):
    # get all images
    imgs = get_all_images(url)

    i=0
    for img in imgs:
        # for each image, download it
        download(img, path, i)
        i+=1

nome_script, url, ref = sys.argv

main(url, ref)