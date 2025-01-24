from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from django.conf import settings
from bot.management.bot_core.handlers.keyboards.for_advertising_handler import start_adv_way_kb, send_task_kb
from bot.management.create_bot import bot
import aiohttp
from io import BytesIO

router = Router()


class AdvState(StatesGroup):
    catch = State()
    admin = State()


async def admin_start(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    await callback.answer('Работа с рекламой')
    await callback.message.delete()
    keyboard = start_adv_way_kb()
    text = "Вы в меню исследования рекламы. Для отправки запроса потребуется заполненный excel файл."
    await bot.send_message(callback.message.chat.id, text=text, reply_markup=keyboard)


async def send_task(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Отправка задания')

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f'{settings.BASE_LOCALHOST_URL}bot/check_for_tasks/',
                                    data={'user_id': callback.from_user.id}) as response:
                if response.status == 200:
                    await callback.message.delete()
                    text = "Теперь отправьте excel файл с заданием или используйте кнопки меню."
                    await state.set_state(AdvState.catch)
                    await bot.send_message(callback.message.chat.id, text=text, reply_markup=send_task_kb())
                else:
                    await callback.message.answer(
                        f'Ваше предыдущее задание в обработке. Пожалуйста дождитесь завершения. {response.status}')
        except aiohttp.ClientError as e:
            await callback.message.answer(f'Ошибка соединения с сервером: {str(e)}')


async def send_file_to_api(file, api_url, file_name, user_id,session):
    file_stream = BytesIO(file)
    data = aiohttp.FormData()
    data.add_field('file', file_stream, filename=file_name)
    data.add_field('user_id', str(user_id))  # Преобразуем user_id в строку, если он числовой
    async with session.post(api_url, data=data) as response:
        return response.status


async def catch_task_file(message: types.Message,
                          state: FSMContext):
    if message.document:
        await message.answer('Файл получен ща будет проверять')
        user_id = message.from_user.id
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'
        file_name = f"{message.from_user.id}_task.xlsx"

        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                file = await response.read()
                api_url = f'{settings.BASE_LOCALHOST_URL}bot/create_task_lex/'
                response_text = await send_file_to_api(file, api_url, file_name, user_id,session)
                await message.answer(f'Файл успешно отправлен. Ответ от API status: {response_text}')
                await state.clear()
    else:
        await message.answer('Пожалуйста, отправьте файл.')


router.callback_query.register(admin_start, F.data == "advertising_type_start")
router.callback_query.register(send_task, F.data == "advertising_start")
router.message.register(catch_task_file, StateFilter(AdvState.catch))
