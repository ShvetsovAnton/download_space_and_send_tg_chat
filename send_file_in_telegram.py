import argparse
import os
import random
import time

import telegram
from dotenv import load_dotenv
from pathlib import Path


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


def send_one_image(
        image_name, channel_id, telegram_token, files_names,
        folder_from_which_send
):
    for file_name in files_names:
        if file_name == image_name:
            send_image(
                folder_from_which_send, file_name, channel_id,
                telegram_token, delay_before_send=0
            )


def send_images_from_folder(
        folder_from_which_send, channel_id, telegram_token,
        delay_before_send, files_names
):
    while True:
        for file_name in files_names:
            send_image(
                folder_from_which_send, file_name, channel_id,
                telegram_token,
                delay_before_send
            )
        random.shuffle(files_names)


def main():
    args_parser = argparse.ArgumentParser(
        description="Отправляем фото в канал Telegram"
    )
    args_parser.add_argument(
        "--folder_name", type=str,
        help="Введи имя папки из которой будем отправлять фото",
        default="image"
    )
    args_parser.add_argument(
        "--delay_before_send", type=int,
        help="Введи задержку перед отправкой", default=14400
    )
    args_parser.add_argument(
        "--image_name", type=str,
        help="Введи название файла с указанием расширения"
    )
    args = args_parser.parse_args()
    delay_before_send = args.delay_before_send
    folder_name = args.folder_name
    image_name = args.image_name
    load_dotenv()
    telegram_token = os.environ["TELEGRAM_BOT_KEY"]
    channel_id = os.environ["TELEGRAM_CHAT_ID"]
    folder_from_which_send = Path.cwd() / folder_name
    files_names = os.listdir(folder_name)
    delay_before_trying_to_connect = 10
    while True:
        try:
            if image_name:
                send_one_image(
                    image_name, channel_id, telegram_token, files_names,
                    folder_from_which_send
                )
                break
            else:
                send_images_from_folder(
                    folder_from_which_send, channel_id,
                    telegram_token, delay_before_send, files_names
                )
        except telegram.error.NetworkError:
            print("Не могу отправить файл, Телеграм не отвечает")
            time.sleep(delay_before_trying_to_connect)
        delay_before_trying_to_connect = 100


if __name__ == '__main__':
    main()
