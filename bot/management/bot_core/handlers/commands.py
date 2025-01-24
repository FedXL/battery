import os

import django
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.models import UserTelegram

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fusion_core.settings')
django.setup()

router = Router()


def command_menu_kb(user_id: int = None) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(text="Будильник⏰",
                                           callback_data="alarm_clock_start"))
    try:
        user_id = int(user_id)
        if user_id in [716336613, 683289468]:
            builder.add(types.InlineKeyboardButton(text="Тип рекламы по Фразам",
                                           callback_data="advertising_type_start"))
    except:
        print('vah vah')
    builder.add(types.InlineKeyboardButton(text="Поддержать проект",
                                           callback_data="donate_callback"))
    builder.add(types.InlineKeyboardButton(text="Обратная связь",
                                           url="https://t.me/Supkz"))
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


async def kill_state(message_or_callback, state: FSMContext) -> None:
    """ в основном нужна что бы очищать с листа лишние сообщения,
     что хранятся в state_data killing list"""
    state_dict = await state.get_data()
    killing_list = state_dict.get("killing_list", [])
    if killing_list:
        for message_id in killing_list:
            try:
                await bot.delete_message(chat_id=message_or_callback.from_user.id, message_id=message_id)
            except:
                print("message not found")
    await state.clear()


@router.message(Command("state"))
async def state(message: types.Message, state: FSMContext) -> None:
    state_name = await state.get_state()
    if state_name is None:
        state_name = "No state is set."
    await message.answer(state_name)


async def command_start_handler(message_or_callback: [types.Message or types.CallbackQuery], state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    hello_text = (f"Приветствую, !\n"
                  f"Я помогаю поставщикам Wildberries отслеживать коэффициент приемки товара по типу поставки, датам и складам.\n"
                  f"Со мной вы сможете оптимизировать расходы на логистику. ")

    if isinstance(message_or_callback, types.Message):
        user, created = UserTelegram.objects.get_or_create(telegram_id=message_or_callback.from_user.id)
        user, created = await sync_to_async(UserTelegram.objects.get_or_create)(
            telegram_id=message.from_user.id,
            defaults={'username': message.from_user.username}
        )
        if created:
            await message.reply("Welcome, new user!")
        else:
            await message.reply("Welcome back!")
        await message_or_callback.answer(hello_text)


async def kill_myself(callback: types.CallbackQuery) -> None:
    await callback.answer("Удаление сообщения")
    await callback.message.delete()


router.callback_query.register(command_start_handler, F.data == "main_menu")
router.message.register(command_start_handler, Command("start"))
