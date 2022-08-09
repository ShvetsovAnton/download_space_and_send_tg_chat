import argparse
import os
import requests
from dotenv import load_dotenv
from down_load_tools import take_file_extension_from_url, \
    download_image_in_folder, make_folder


def fetch_nasa_images(nasa_token):
    url = "https://api.nasa.gov/planetary/apod"
    payload = {"count": 15, "api_key": nasa_token}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response_json = response.json()
    for image in response_json:
        if image.get("hdurl"):
            yield image["hdurl"]


def main():
    load_dotenv()
    nasa_token = os.environ["NASA_API_KEY"]
    args_parser = argparse.ArgumentParser(
        description="Загружаем фото земли с 'NASA'"
    )
    args_parser.add_argument("token_nasa", type=str, help="Введи 'token'",
                             default=nasa_token)
    args = args_parser.parse_args()
    nasa_token = args.token
    image_name = "Nasa_apod"
    try:
        nasa_images_urls = fetch_nasa_images(nasa_token)
    except requests.exceptions.HTTPError:
        print("Сайт не доступен")
    for url in nasa_images_urls:
        file_extension = take_file_extension_from_url(url)
        path_for_download = make_folder(folder_name="Nasa_apod")
        download_image_in_folder(
            nasa_images_urls, path_for_download, file_extension, image_name
        )


if __name__ == '__main__':
    main()
