import argparse
import os
import random

import telegram
from dotenv import load_dotenv

from down_load_tools import take_file_extension_from_url, \
    download_image_in_folder, make_folder
from epic_image_download import fetch_epic_image
from nasa_image_download import fetch_nasa_images
from send_file_in_telegram import send_image, \
    search_files_and_path_by_folder_name
from spacex_image_download import fetch_spacex_id_launch


def main():
    args_parser = argparse.ArgumentParser(
        description="Загружаем фото космической тематики"
    )
    args_parser.add_argument(
        "--delay_before_send", type=int,
        help="Введи задержку перед отправкой", default=14400
    )
    args_parser.add_argument(
        "--folder_name", type=str,
        help="Введи имя папки из которой будем отправлять фото",
        default="Image"
    )
    args_parser.add_argument(
        "nasa_token", type=str,
        help="Введи токен"
    )
    args = args_parser.parse_args()
    delay_before_send = args.delay_before_send
    folder_name = args.folder_name
    path_for_download = make_folder(folder_name)
    load_dotenv()
    telegram_token = os.environ["TELEGRAM_BOT_KEY"]
    channel_id = os.environ["TELEGRAM_CHAT_ID"]
    nasa_token = os.environ["NASA_API_KEY"]
    params = "5eb87d47ffd86e000604b38a"
    spacex_url = f"https://api.spacexdata.com/v5/launches/{params}"
    spacex_images_urls = fetch_spacex_id_launch(spacex_url)
    for url in spacex_images_urls:
        file_extensions = take_file_extension_from_url(url)
        download_image_in_folder(spacex_images_urls, path_for_download,
                             file_extensions, image_name="Spacex_")
    nasa_images_urls = fetch_nasa_images(nasa_token)
    for url in nasa_images_urls:
        file_extensions = take_file_extension_from_url(url)
        download_image_in_folder(nasa_images_urls, path_for_download,
                             file_extensions, image_name="nasa_apod_")
    epic_image_urls = fetch_epic_image(nasa_token)
    for url in epic_image_urls:
        file_extensions = take_file_extension_from_url(url)
        download_image_in_folder(epic_image_urls, path_for_download,
                             file_extensions, image_name="EPIC_")
    image_send_path = search_files_and_path_by_folder_name(folder_name)
    try:
        for files, paths in image_send_path:
            for file in files:
                send_image(paths, file, channel_id, telegram_token,
                           delay_before_send)
                if files[-1]:
                    while True:
                        random.shuffle(files)
                        for file in files:
                            send_image(
                                paths, file, channel_id, telegram_token,
                                delay_before_send
                            )
    except telegram.error.NetworkError:
        print("Не могу отправить файл, Телеграм не отвечает")


if __name__ == '__main__':
    main()
