import argparse
import os
import random
import time

import telegram
from dotenv import load_dotenv


def search_files_and_path_by_folder_name(folder_to_send):
    files_path = os.walk(folder_to_send)
    for path, folder, files in files_path:
        yield files, path


def find_path_by_file_name(files_and_path, image_name):
    for files, path in files_and_path:
        for image in files:
            if image == image_name:
                return path


def send_image(
        path_to_image, image_name, channel_id, telegram_token,
        delay_before_send
):
    bot = telegram.Bot(token=telegram_token)
    document = f"{path_to_image}/{image_name}"
    with open(document, "rb") as image:
        bot.send_document(
            chat_id=channel_id,
            document=image
        )
        time.sleep(delay_before_send)


def sed_one_image(file_name, channel_id, telegram_token):
    folder_from_which_send = os.path.abspath(f"{os.getcwd()}")
    files_and_path = search_files_and_path_by_folder_name(
        folder_from_which_send
    )
    path = find_path_by_file_name(files_and_path, file_name)
    send_image(
        path, file_name, channel_id, telegram_token,
        delay_before_send=0
    )


def send_images_from_folder(
        folder_from_which_send, channel_id, telegram_token,
        delay_before_send, files_and_paths
):
    for files, paths in files_and_paths:
        while True:
            for file in files:
                send_image(
                    folder_from_which_send, file, channel_id,
                    telegram_token,
                    delay_before_send
                )
                if files[-1]:
                    random.shuffle(files)
                    continue


def main():
    args_parser = argparse.ArgumentParser(
        description="Отправляем фото в канал Telegram"
    )
    args_parser.add_argument(
        "--folder_name", type=str,
        help="Введи имя папки из которой будем отправлять фото",
    )
    args_parser.add_argument(
        "--delay_before_send", type=int,
        help="Введи задержку перед отправкой", default=14400
    )
    args_parser.add_argument(
        "--file_name", type=str,
        help="Введи название файла с указанием расширения"
    )
    args = args_parser.parse_args()
    delay_before_send = args.delay_before_send
    folder_name = args.folder_name
    file_name = args.file_name
    load_dotenv()
    telegram_token = os.environ["TELEGRAM_BOT_KEY"]
    channel_id = os.environ["TELEGRAM_CHAT_ID"]
    folder_from_which_send = os.path.abspath(f"{os.getcwd()}/{folder_name}")
    files_and_paths = search_files_and_path_by_folder_name(
        folder_from_which_send
    )
    try:
        if file_name:
            sed_one_image(file_name, channel_id, telegram_token)
        else:
            send_images_from_folder(
                folder_from_which_send, channel_id,
                telegram_token, delay_before_send, files_and_paths
            )
    except telegram.error.NetworkError:
        print("Не могу отправить файл, Телеграм не отвечает")


if __name__ == '__main__':
    main()
