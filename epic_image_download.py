import os

import requests
from datetime import datetime
from dotenv import load_dotenv
from down_load_tools import take_file_extension_from_url, \
    download_image_in_folder, make_folder


def fetch_epic_image(nasa_token):
    url = "https://api.nasa.gov/EPIC/api/natural"
    payload = {"api_key": nasa_token}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response_json = response.json()
    for description_photo in response_json:
        date = datetime.fromisoformat(description_photo["date"])
        image_name = description_photo["image"]
        epic_image_url = (
            f"https://api.nasa.gov/EPIC/archive/natural/"
            f"{date:%Y/%m/%d}/png/{image_name}.png"
        )
        response = requests.get(epic_image_url, params=payload)
        yield response.url


def main():
    load_dotenv()
    nasa_token = os.environ["NASA_API_KEY"]
    image_name = "Nasa_EPIC_"
    epic_images_urls = fetch_epic_image(nasa_token)
    for url in epic_images_urls:
        file_extension = take_file_extension_from_url(url)
        path_for_download = make_folder(folder_name="image")
        download_image_in_folder(
            epic_images_urls, path_for_download, file_extension, image_name
        )


if __name__ == '__main__':
    main()
