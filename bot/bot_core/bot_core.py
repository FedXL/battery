import logging
import os
from dotenv import load_dotenv
from telebot import types
import telebot

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

bot_logger = logging.getLogger('bot_logger')
bot_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
bot_logger.addHandler(console_handler)

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def send_message(self, chat_id, text, reply_markup=None):
        try:
            message = self.bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode='HTML')
            return message,None
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
            return False ,f'Ошибка при отправке сообщения: {e}'

    def delete_message(self, chat_id, message_id):
        try:
            message = self.bot.delete_message(chat_id, message_id)
            return message
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")
            return None

    def update_message(self, chat_id, message_id, text):
        try:
            message = self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='HTML')
            return message
        except Exception as e:
            print(f"Ошибка при обновлении сообщения: {e}")
            return None

    def send_photo(self, chat_id, photo, caption=None):
        try:
            message = self.bot.send_photo(chat_id, photo, caption=caption, parse_mode='HTML')
            return message
        except Exception as e:
            print(f"Ошибка при отправке фото: {e}")
            return None

    def send_gif(self, chat_id, gif, caption=None):
        try:
            message = self.bot.send_animation(chat_id, gif, caption=caption, parse_mode='HTML')
            return message
        except Exception as e:
            print(f"Ошибка при отправке GIF: {e}")
            return None

    def extract_photo_by_id(self, photo_id):
        try:
            file_info = self.bot.get_file(photo_id)
            file_path = file_info.file_path

            downloaded_file = self.bot.download_file(file_path)
            return downloaded_file, None
        except Exception as e:
            print(f"Ошибка при получении фото: {e}")
            return None, e

    def send_document(self,chat_id,document,caption=None):
        try:
            message = self.bot.send_document(chat_id,document,caption=caption,parse_mode='HTML')
            return message, False
        except Exception as e:
            print(f"Ошибка при отправке документа: {e}")
            return None, str(e)

sync_bot = TelegramBot(bot_token)



