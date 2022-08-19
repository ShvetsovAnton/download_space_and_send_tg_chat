import os
import requests
import argparse
from dotenv import load_dotenv
from down_load_tools import take_file_extension_from_url, \
    download_image_in_folder, make_folder


def fetch_nasa_images(nasa_token, number_of_photos_to_upload ):
    url = "https://api.nasa.gov/planetary/apod"
    payload = {"count": number_of_photos_to_upload, "api_key": nasa_token}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response_json = response.json()
    for image in response_json:
        if image.get("hdurl"):
            yield image["hdurl"]


def main():
    load_dotenv()
    nasa_token = os.environ["NASA_API_KEY"]
    image_name = "Nasa_apod_"
    args_parse = argparse.ArgumentParser(
        description="Укажите сколько фото скачать"
    )
    args_parse.add_argument(
        "--number_of_photos_to_upload", type=int,
        help="Введите сколько фото хотите скачать", default=15
    )
    args = args_parse.parse_args()
    number_of_photos_to_upload = args.number_of_photos_to_upload
    nasa_images_urls = fetch_nasa_images(
        nasa_token, number_of_photos_to_upload
    )
    for url in nasa_images_urls:
        file_extension = take_file_extension_from_url(url)
        path_for_download = make_folder(folder_name="image")
        download_image_in_folder(
            nasa_images_urls, path_for_download, file_extension, image_name,
        )


if __name__ == '__main__':
    main()
