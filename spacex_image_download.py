import argparse

import requests

from down_load_tools import take_file_extension_from_url, \
    download_image_in_folder, make_folder


def fetch_spacex_id_launch(launch_id):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["links"]["flickr"]["original"]


def main():
    image_name = "Spacex_"
    args_parser = argparse.ArgumentParser(
        description="Загружаем фото запуска ракет 'Space_X'"
    )
    args_parser.add_argument(
        "--launch_id", type=str, help="Введи Id запуска", default="latest"
    )
    args = args_parser.parse_args()
    launch_id = args.launch_id
    spacex_images_urls = fetch_spacex_id_launch(launch_id)
    for url in spacex_images_urls:
        file_extension = take_file_extension_from_url(url)
        path_for_download = make_folder(folder_name="image")
        download_image_in_folder(
            spacex_images_urls, path_for_download, file_extension,
            image_name
        )
    if not spacex_images_urls:
        print("На последнем запуске не делали фото.")


if __name__ == '__main__':
    main()
