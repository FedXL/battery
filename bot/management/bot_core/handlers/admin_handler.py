import requests
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from bot.management.bot_core.handlers.bot_utils.bot_variables import DELIVERY_VOCABULARY, COOL_NUM
from bot.management.bot_core.handlers.keyboards.for_admin_handler import task_manager_kb, comeback_kb
from bot.management.create_bot import bot
from bot.management.bot_core.handlers.bot_utils import bot_urls as urls
from fusion_core.bot_settings import send_message
from fusion_core.settings import fedor_id

router = Router()


async def admin_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Управление заданиями.')
    url = urls.URL_TASK
    comeback_keyboard = comeback_kb()
    url += f"?client={callback.message.chat.id}"
    response = requests.get(url)
    user_tasks = response.json()
    state_data = await state.get_data()
    killing_list = state_data.get("killing_list", [])

    if not user_tasks:
        text = "У вас нет активных заданий. Но вы их можете добавить."
        await callback.answer('Пусто')
        await bot.send_message(chat_id=callback.message.chat.id,
                               text=text,
                               reply_markup=comeback_keyboard)
        await callback.message.delete()
        return
    counter = 1
    for task in user_tasks:
        cool_number = str(COOL_NUM[counter])
        text = f"{cool_number}\n"
        text += f"ID: {task['id']}\n"
        url = urls.URL_WAREHOUSES + f"{task['warehouse']}/"
        response = requests.get(url)
        warehouse = response.json()
        text += f"Склад: <b>{warehouse['name']}</b>\n"
        text += f"Коэффициент: <b>{'Только бесплатно' if task['find_coefficient'] == 0 else task['find_coefficient']}</b>\n"
        delivery_type = DELIVERY_VOCABULARY.get(task['delivery_type'])
        text += f"Тип доставки: <b>{delivery_type}</b>\n"
        text += f"Дни для поиска:\n"
        days = task['days']
        if_points = "..." if len(days) > 1 else ""
        task_id = task['id']
        text += f"{days[0]['search_day']}   {if_points}\n"
        callback_text_delete = "delete_task_" + str(task['id'])
        callback_text_open = "open_task_" + str(task_id) + "_" + str(counter)
        keyboard = task_manager_kb(callback_text_delete, callback_text_open)
        response = await bot.send_message(chat_id=callback.message.chat.id,
                                          text=text, reply_markup=keyboard)
        counter += 1
        killing_list.append(response.message_id)
    await state.update_data(killing_list=killing_list)
    await callback.message.delete()
    comeback_text = ("Тут отображен список активных заданий на текущий момент.\n При нажатии на кнопку 'Убить задание' "
                     "задание будет удалено.\nВсего на один аккаунт лимит 10 заданий. При достижении лимита "
                     "публикация новых заданий станет невозможна.")

    await bot.send_message(chat_id=callback.message.chat.id,
                           text=comeback_text,
                           reply_markup=comeback_keyboard)


async def delete_task(callback: types.CallbackQuery, state: FSMContext):
    task_id = callback.data.split("_")[2]
    url = urls.URL_TASK + f"{int(task_id)}/?client={callback.message.chat.id}"
    response = requests.delete(url)
    if response.status_code == 204:
        await callback.answer("Задание удалено.")
        id_message = callback.message.message_id
        state_dict = await state.get_data()
        killing_list = state_dict.get("killing_list")
        if id_message in killing_list:
            killing_list.remove(id_message)
            await state.update_data(killing_list=killing_list)
            await callback.message.delete()
    else:
        await callback.answer("Ошибка удаления задания.")
        await callback.message.reply("Ошибка в удалении задания, попробуйте еще раз")
        send_message(fedor_id,
                     f"ERROR delete_task from admin_handlers: не могу удалить у пользователя {callback.message.chat.id} задание {task_id}")


async def open_task(callback: types.CallbackQuery, state: FSMContext):
    task_id = callback.data.split("_")[2]
    id_num = callback.data.split("_")[3]
    cool_num = COOL_NUM[int(id_num)]
    url = urls.URL_TASK + f"{int(task_id)}/?client={callback.message.chat.id}"
    response = requests.get(url)
    task = response.json()

    text = f"{cool_num}\n"
    text += f"ID: {task['id']}\n"
    url = urls.URL_WAREHOUSES + f"{task['warehouse']}/"
    response = requests.get(url)
    warehouse = response.json()
    text += f"Склад: <b>{warehouse['name']}</b>\n"
    text += f"Коэффициент: <b>{'Только бесплатно' if task['find_coefficient'] == 0 else task['find_coefficient']}</b>\n"
    delivery_type = DELIVERY_VOCABULARY.get(task['delivery_type'])
    text += f"Тип доставки: <b>{delivery_type}</b>\n"
    text += f"Дни для поиска:\n"
    for day in task['days']:
        text += f"{day['search_day']}\n"
    callback_text_delete = "delete_task_" + str(task['id'])
    keyboard = task_manager_kb(callback_text_delete)
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text=text,
                                reply_markup=keyboard)


router.callback_query.register(admin_start, F.data == "admin")
router.callback_query.register(delete_task, F.data.startswith("delete_task_"))
router.callback_query.register(open_task, F.data.startswith("open_task_"))
