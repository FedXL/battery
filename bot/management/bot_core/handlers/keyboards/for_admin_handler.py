from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def task_manager_kb(callback_delete_task: str, callback_open_task:str=None) -> ReplyKeyboardMarkup:
    """меню для управления заданиями пока просто кнопка убить задание"""
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Убить задание ☠️", callback_data=callback_delete_task))
    if callback_open_task:
        builder.add(types.InlineKeyboardButton(text="↕️", callback_data=callback_open_task))
    builder.adjust(2)
    keyboard = builder.as_markup()
    return keyboard


def comeback_kb() -> ReplyKeyboardMarkup:
    """меню для возврата в главное меню"""
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Добавить задание 🆕", callback_data="start_task_again"))
    builder.add(types.InlineKeyboardButton(text="Главное меню ↩️", callback_data="main_menu"))
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard
