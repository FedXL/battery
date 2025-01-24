from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.management.bot_core.handlers.texts.texts import extract_page_number


def type_of_delivery_kb(data: dict) -> ReplyKeyboardMarkup:
    """с проверкой на наличие доставки
    callback example delivery_type_QR_send_korobs"""
    builder = InlineKeyboardBuilder()
    callback_prefix = 'delivery_type_'


    button_data = [
        ("Короба", "korobs"),
        ("Монопаллеты", "monopolets"),
        ("Суперсейф", "supersafe"),
        ("QR отправка коробов", "QR_send_korobs")
    ]
    income = data.keys()
    for text, key in button_data:
        prefix = "✅" if key in income else "❌"
        builder.add(types.InlineKeyboardButton(text=f"{text} {prefix}", callback_data=f"{callback_prefix}{key}"))
    builder.add(types.InlineKeyboardButton(text="Назад ⤴️", callback_data="pagination_warehouse_1"))
    builder.adjust(1)

    return builder.as_markup()


def warehouse_type_choice_kb() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="🔸Основные🔸", callback_data="pagination_warehouse_init_MAIN"))
    builder.add(types.InlineKeyboardButton(text="🔹СЦ склады🔹", callback_data="pagination_warehouse_init_SC"))
    builder.add(types.InlineKeyboardButton(text="Главное меню ↩️", callback_data="main_menu"))
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def finish_kb() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Еще задание 🆕", callback_data="alarm_clock_again"))
    builder.add(types.InlineKeyboardButton(text="Главное меню ↩️", callback_data="main_menu"))
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def confirm_date_kb() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Всё правильно ✅", callback_data="alarm_finish"))
    builder.add(types.InlineKeyboardButton(text="Ошибся, еще раз ⛔️", callback_data="alarm_clock_again"))
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def create_alarm_clock_menu_kb() -> ReplyKeyboardMarkup:
    """меню будильника"""
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Добавить задание 🆕", callback_data="type_of_warehouse"))
    builder.add(types.InlineKeyboardButton(text="Активные  задания ↔️", callback_data="admin"))
    builder.add(types.InlineKeyboardButton(text="Назад ↩️", callback_data="main_menu"))
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def create_alarm_clock_date_menu_kb(delivery_type):
    """меню для выбора дат будильника"""
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Выбор даты", callback_data="data_choice_custom"))
    builder.add(types.InlineKeyboardButton(text="Ближайшие 7 дней", callback_data="data_choice_7days"))
    builder.add(types.InlineKeyboardButton(text="Как только появится", callback_data="data_choice_any"))
    builder.add(types.InlineKeyboardButton(text="Назад ⤴️", callback_data=f"delivery_type_{delivery_type}"))
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def available_dates_kb(data: dict, kill_dict={}, coefficient=None) -> ReplyKeyboardMarkup:
    """меню для выбора дат будильника
    callback example 7 июн. -> custom_date_choice_2024-06-07"""
    if kill_dict is None:
        kill_dict = {}
    builder = InlineKeyboardBuilder()
    dates = data["dates_list"]

    for date, datetime in dates.items():
        if datetime in kill_dict:
            continue
        builder.add(types.InlineKeyboardButton(text=date, callback_data=f"custom_date_choice_{datetime}"))
    builder.adjust(3)
    builder2 = InlineKeyboardBuilder()
    if len(kill_dict) > 0:
        builder2.add(types.InlineKeyboardButton(text="Закончить выбор", callback_data="confirm_date"))
    builder2.add(types.InlineKeyboardButton(text="Назад ⤴️", callback_data=f"coefficient_{coefficient}"))
    builder.attach(builder2)
    keyboard = builder.as_markup()
    return keyboard


def create_coefficient_kb(warehouse_id):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Только бесплатно", callback_data="coefficient_0"))
    builder.adjust(1)
    builder2 = InlineKeyboardBuilder()
    for num in range(1, 13):
        builder2.add(types.InlineKeyboardButton(text=f"<=Х{num}", callback_data=f"coefficient_{num}"))
    builder2.add(types.InlineKeyboardButton(text=f"Назад ⤴️", callback_data=f"warehouse_{warehouse_id}"))
    builder2.adjust(4)
    builder.attach(builder2)
    keyboard = builder.as_markup()
    return keyboard


def create_warehouse_kb(data: dict) -> ReplyKeyboardMarkup:
    warehouse_builder = InlineKeyboardBuilder()
    warehouses = data["results"]
    for warehouse in warehouses:
        warehouse_builder.add(types.InlineKeyboardButton(text=warehouse["name"],
                                                         callback_data=f"warehouse_{warehouse['id']}"))

    warehouse_builder.adjust(1)
    navigation_builder = InlineKeyboardBuilder()
    print(data)
    next_value = extract_page_number(data["links"]["next"])
    back_value = extract_page_number(data["links"]["previous"])
    print("[INFO][PAGINATOR]","next_value", next_value, "back_value", back_value, sep=" | ")
    navigation_builder.add(types.InlineKeyboardButton(text="⏪",
                                                      callback_data=f"pagination_warehouse_{back_value}"))
    navigation_builder.add(types.InlineKeyboardButton(text="Назад ⤴️", callback_data="type_of_warehouse"))
    navigation_builder.add(types.InlineKeyboardButton(text="⏩",
                                                      callback_data=f"pagination_warehouse_{next_value}"))
    navigation_builder.adjust(4)
    warehouse_builder.attach(navigation_builder)
    keyboard = warehouse_builder.as_markup()
    return keyboard
