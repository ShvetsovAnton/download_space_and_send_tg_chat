import argparse
import os

import requests
from dotenv import load_dotenv
from down_load_tools import take_file_extension_from_url, \
    download_image_in_folder, make_folder


def fetch_epic_image(nasa_token):
    url = "https://api.nasa.gov/EPIC/api/natural"
    payload = {"api_key": nasa_token}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response_json = response.json()
    for key in response_json:
        if key["date"]:
            date = key["date"]
            yy_mm_dd = date.split()[0]
            yy, mm, dd = yy_mm_dd.split("-")
        if key["image"]:
            image_name = key["image"]
        epic_image_url = (
            f"https://api.nasa.gov/EPIC/archive/natural/"
            f"{yy}/{mm}/{dd}/png/{image_name}.png"
        )
        response = requests.get(epic_image_url, params=payload)
        image_url = response.url
        yield image_url


def main():
    load_dotenv()
    nasa_token = os.environ["NASA_API_KEY"]
    args_parser = argparse.ArgumentParser(
        description="Загружаем фото земли с 'NASA'"
    )
    args_parser.add_argument("token_nasa", type=str, help="Введи 'token'",
                             default=nasa_token)
    args = args_parser.parse_args()
    nasa_token = args.token_nasa
    image_name = "Nasa_EPIC_"
    try:
        epic_images_urls = fetch_epic_image(nasa_token)
        for url in epic_images_urls:
            file_extension = take_file_extension_from_url(url)
            path_for_download = make_folder(folder_name="Nasa_EPIC")
            download_image_in_folder(
                epic_images_urls, path_for_download, file_extension, image_name
            )
    except requests.exceptions.HTTPError:
        print("Неверный токен или сайт недоступен")


if __name__ == '__main__':
    main()
