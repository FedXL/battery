from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_adv_way_kb() -> ReplyKeyboardMarkup:
    """меню для управления заданиями пока просто кнопка убить задание"""
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Как это работает", callback_data="advertising_help"))
    builder.add(types.InlineKeyboardButton(text="Скачать форму для отправки", callback_data="advertising_form"))
    builder.add(types.InlineKeyboardButton(text="Отправить задание ", callback_data="advertising_start"))
    builder.add(types.InlineKeyboardButton(text="Главное меню ↩️", callback_data="main_menu"))
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard

def send_task_kb() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Назад", callback_data="advertising_type_start"))
    builder.add(types.InlineKeyboardButton(text="Главное меню ↩️", callback_data="main_menu"))
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard