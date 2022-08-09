import argparse

import requests

from down_load_tools import take_file_extension_from_url, \
    download_image_in_folder, make_folder


def fetch_spacex_id_launch(launch_id):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    original_size_image = response.json()["links"]["flickr"]["original"]
    if original_size_image:
        return original_size_image


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
    try:
        spacex_images_urls = fetch_spacex_id_launch(launch_id)
        if spacex_images_urls:
            for url in spacex_images_urls:
                file_extension = take_file_extension_from_url(url)
                path_for_download = make_folder(folder_name="Spacex_launch")
                download_image_in_folder(
                    spacex_images_urls, path_for_download, file_extension,
                    image_name
                )
        else:
            print(
                "На последнем запуске не делали фото, "
                "попробуйте скачать по ID"
            )
    except requests.exceptions.HTTPError:
        print("По данному ID нет фотографий")



if __name__ == '__main__':
    main()
