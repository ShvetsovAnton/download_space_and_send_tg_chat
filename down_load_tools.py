import os
import requests
from urllib.parse import urlparse
import urllib.parse


def download_image_in_folder(
        images_urls, path_for_download, file_extension, image_name
):
    for image_number, image_url in enumerate(images_urls):
        response = requests.get(image_url)
        response.raise_for_status()
        path = os.getcwd()
        filename = f"{image_name}{image_number}{file_extension}"
        file_path = f"{path}/{filename}"
        path_for_safe_image = f"{path_for_download}/{filename}"
        with open(filename, "wb") as image:
            image.write(response.content)
        os.replace(file_path, path_for_safe_image)


def make_folder(folder_name):
    folder_path = os.getcwd()
    os.makedirs(folder_name, exist_ok=True)
    path_for_download = os.path.join(folder_path, folder_name)
    return path_for_download


def take_file_extension_from_url(url):
    url_path = urlparse(url).path
    unquote_url_path = urllib.parse.unquote(url_path)
    filename = os.path.split(unquote_url_path)[-1]
    file_extension = os.path.splitext(filename)[-1]
    return file_extension
