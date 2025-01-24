import json
from datetime import timedelta, datetime
import requests
from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from .bot_utils.bot_urls import URL_WAREHOUSES, URL_DELIVERY_TYPE_CHECK, URL_GET_DATE, URL_TASK
from .bot_utils.bot_variables import DELIVERY_VOCABULARY, CRITERIA_WORD, WAREHOUSE_COLLECTION
from .bot_utils.texts import coefficiernt_text_return
from .commands import kill_state
from .keyboards.for_alarm_handler import create_warehouse_kb, create_alarm_clock_menu_kb, \
    create_alarm_clock_date_menu_kb, \
    available_dates_kb, create_coefficient_kb, warehouse_type_choice_kb, type_of_delivery_kb, confirm_date_kb, finish_kb
from ...create_bot import bot

router = Router()

class AlarmClockStates(StatesGroup):
    start = State()
    admin = State()

async def alarm_clock_again(callback: types.CallbackQuery, state: FSMContext) -> None:
    await kill_state(callback, state)
    await alarm_clock_menu(callback, state)


async def alarm_clock_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Этап 1 меню будильника"""
    await state.set_state(AlarmClockStates.start)
    alarm_clock_text = "Хотите добавить новое задание или посмотреть активные задания?"
    await callback.answer("Будильник")
    await callback.message.delete()
    await bot.send_message(callback.message.chat.id,
                           text=alarm_clock_text,
                           reply_markup=create_alarm_clock_menu_kb())


async def choice_type_of_warehouse_again(callback: types.CallbackQuery, state: FSMContext) -> None:
    await kill_state(callback, state)
    await state.set_state(AlarmClockStates.start)
    await choice_type_of_warehouse(callback)


async def choice_type_of_warehouse(callabak: types.CallbackQuery) -> None:
    """Этап 2 выбор типа склада СЦ или Основные"""
    await callabak.answer("Выберите тип склада")
    await callabak.message.delete()
    await bot.send_message(callabak.message.chat.id, "Выберите тип склада:", reply_markup=warehouse_type_choice_kb())


async def warehouse_choice(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Этап 3 выбор самого склада"""
    print('INFO PAGINATOR HANDLER start')
    page = callback.data.split("_")[2]

    if not page or page == "None":
        await callback.answer("Это последняя страница")
        return
    elif page == "init":
        url = URL_WAREHOUSES
        warehouse_collection_name = callback.data.split("_")[3]
        url += f"?warehouse_collection_name={warehouse_collection_name}"
        state_data = await state.get_data()
        state_data["warehouse_collection_name"] = warehouse_collection_name
        await state.update_data(state_data)
    else:
        state_data = await state.get_data()
        warehouse_collection_name = state_data.get("warehouse_collection_name")
        url = URL_WAREHOUSES
        url += f"?page={page}"
        url += f"&warehouse_collection_name={warehouse_collection_name}"

    response = requests.get(url)
    data = response.json()
    keyboard = create_warehouse_kb(data=data)
    current_page = data["current_page"]
    total_pages = data["total_pages"]
    total_items = data["total_items"]
    data = await state.get_data()
    wh_collection = data.get("warehouse_collection_name")
    await callback.answer("Успешно")
    text = f"Выберите {WAREHOUSE_COLLECTION[wh_collection]} склад. {current_page}/{total_pages} всего {total_items}"
    await bot.send_message(callback.message.chat.id, text=text,
                           reply_markup=keyboard)
    await callback.message.delete()


async def catch_warehouse_and_type_of_delivery_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Этап 4 выбор типа поставки с конкретного склада"""
    state_data = await state.get_data()

    await callback.answer("Выберите тип поставки")
    warehouse_id = callback.data.split("_")[1]
    await state.update_data(warehouse_id=warehouse_id)
    url = URL_DELIVERY_TYPE_CHECK
    post_data_available_types = {"warehouse_id": warehouse_id}
    response = requests.post(url, data=post_data_available_types)
    available_delivery_types = response.json()
    url = URL_WAREHOUSES + f"{warehouse_id}/"
    response = requests.get(url)
    warehouse_data = response.json()
    warehouse_name = warehouse_data.get("name")
    warehouse_collection = state_data.get("warehouse_collection_name")
    text = (f"Тип склада: <b>{WAREHOUSE_COLLECTION[warehouse_collection]}</b>\n"
            f"Склад: <b>{warehouse_name}</b> \n"
            f"Выберите тип поставки:")

    state_data = await state.get_data()
    state_data["warehouse_name"] = warehouse_name
    state_data["warehouse"] = warehouse_id
    state_data["available_delivery_types"] = available_delivery_types

    await state.update_data(data=state_data)
    await bot.send_message(callback.message.chat.id, text=text,
                           reply_markup=type_of_delivery_kb(data=available_delivery_types))
    await callback.message.delete()


async def catch_delivery_type_and_coefficients_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Этап 5 выбор коэффициентов приемки callback income delivery_type_QR_send_korobs"""

    delivery_type = callback.data.split("_", 2)[2]
    state_data = await state.get_data()
    warehouse_name = state_data.get("warehouse_name")
    available_delivery_types = state_data.get("available_delivery_types")
    keys = available_delivery_types.keys()
    if delivery_type not in keys:
        send_response = await bot.send_message(callback.message.chat.id, f"⚠️На ближайшие 14 дней \n"
                                                                         f"<b>{warehouse_name}</b>  данный тип "
                                                                         f"поставки имеет\n"
                                                                         f"статус: {CRITERIA_WORD}\n"
                                                                         f"Скорее всего склад не имеет такого типа "
                                                                         f"поставки.")
        target_id = send_response.message_id
        killing_list = state_data.get("killing_list", [])
        killing_list.append(target_id)
        await state.update_data(killing_list=killing_list)
    warehouse_id = state_data.get("warehouse_id")
    keyboard = create_coefficient_kb(warehouse_id)
    state_data["delivery_type"] = delivery_type
    await state.update_data(state_data)

    warehouse_collection = state_data.get("warehouse_collection_name")
    text = (f"Тип склада: <b>{WAREHOUSE_COLLECTION[warehouse_collection]}</b>\n"
            f"Склад: <b>{warehouse_name}</b>\n"
            f"Тип поставки: <b>{DELIVERY_VOCABULARY[delivery_type]}</b> \n"
            f"Выбирайте приемлемый коэффициент приемки")
    await bot.send_message(callback.message.chat.id, text=text, reply_markup=keyboard)
    await callback.message.delete()


async def catch_coefficients_and_date_menu(callback: types.CallbackQuery, state: FSMContext) -> None:

    """
    Этап 6. меню по выбору даты:
    -выбор ближайшие 7 дней
    -выбор когда получится
    -выбрать дату
    """

    print("INFO CATCH WAREHOUSE AND DATA MENU")

    coefficient = callback.data.split("_")[1]
    state_data = await state.get_data()
    state_data["coefficient"] = coefficient
    delivery_type = state_data.get("delivery_type")
    await state.update_data(state_data)
    warehouse_name = state_data.get("warehouse_name")
    await callback.answer("Успешно")
    warehouse_collection_name = state_data.get("warehouse_collection_name")
    text = (f"Тип склада: <b>{WAREHOUSE_COLLECTION[warehouse_collection_name]}</b>\n"
            f"Склад: <b>{warehouse_name}</b>\n"
            f"Тип поставки: <b>{DELIVERY_VOCABULARY.get(delivery_type)}</b>\n"
            f"Коэффициент: <b>{coefficiernt_text_return(coefficient)}</b>\n"
            f"<b>Когда искать?</b>")

    await bot.send_message(callback.message.chat.id, text=text,
                           reply_markup=create_alarm_clock_date_menu_kb(delivery_type))
    await callback.message.delete()


async def catch_data_choice(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Этп 7 получить дату поиска или сформировать меню для выбора кастомный даты"""

    print("INFO CATCH DATA CHOICE")
    data_choice = callback.data.split("_")[2]
    url = URL_GET_DATE
    state_data = await state.get_data()
    if data_choice == "custom":
        await callback.answer("Выберите дату")
        state_date = "custom"
        data = {"data_choice": "custom"}
    elif data_choice == "7days":
        await callback.answer("На этой неделе")
        state_date = "this_week"
        data = {"data_choice": "this_week"}
    elif data_choice == "any":
        await callback.answer("Когда появится")
        state_date = "any"
        data = {"data_choice": "any"}
    else:
        raise ValueError("Неправильный выбор")

    response = requests.post(url, data=data)
    response_data = response.json()
    first_date = response_data.get("first_date")
    last_date = response_data.get("last_date")

    state_data["date"] = state_date
    state_data["first_date"] = first_date
    state_data["last_date"] = last_date
    await state.update_data(state_data)

    if data_choice == "custom":
        coef = state_data.get("coefficient")
        keyboard = available_dates_kb(response_data, coefficient=coef)
        warehouse_name = state_data.get("warehouse_name")
        warehouse_collection_name = state_data.get("warehouse_collection_name")
        delivery_type = state_data.get("delivery_type")
        coefficient = state_data.get("coefficient")

        text = (f"Тип склада: <b>{WAREHOUSE_COLLECTION[warehouse_collection_name]}</b>\n"
                f"Склад: <b>{warehouse_name}</b>\n"
                f"Тип поставки: <b>{DELIVERY_VOCABULARY[delivery_type]}</b>\n"
                f"Коэффициент: <b>{coefficiernt_text_return(coefficient)}</b>\n"
                f"<b>Выберите дату или даты.</b>")

        await bot.send_message(callback.message.chat.id, text=text, reply_markup=keyboard)
        await callback.message.delete()
        return

    await confirm_date(callback=callback, state=state)
    await callback.message.delete()


async def custom_data_choice_continue(callback: types.CallbackQuery, state: FSMContext):
    """Этап 7.5 выбор кастомный даты модернизация меню после выбора"""
    print("CONTINUE CUSTOM DATA CHOICE")
    await callback.answer("Дата добавлена")

    add_kill_date = callback.data.split("_")[3]
    state_data = await state.get_data()
    killing = state_data.get("kill_date")
    if not killing:
        state_data["kill_date"] = {}

    state_data["kill_date"][add_kill_date] = "kill"
    await state.update_data(state_data)

    request_data = {"data_choice": "custom"}
    url = URL_GET_DATE
    response = requests.post(url, data=request_data)
    response_data = response.json()
    kill_date = state_data.get("kill_date")
    coef = state_data.get("coefficient")
    keyboard = available_dates_kb(data=response_data, kill_dict=kill_date, coefficient=coef)
    warehouse_name = state_data.get("warehouse_name")
    warehouse_collection_name = state_data.get("warehouse_collection_name")
    delivery_type = state_data.get("delivery_type")
    coefficient = state_data.get("coefficient")
    text = (f"Тип склада: <b>{WAREHOUSE_COLLECTION[warehouse_collection_name]}</b>\n"
            f"Склад: <b>{warehouse_name}</b>\n"
            f"Тип поставки: <b>{DELIVERY_VOCABULARY[delivery_type]}</b>\n"
            f"Коэффициент: <b>{coefficiernt_text_return(coefficient)}</b>\n"
            f"<b>Выберите дату или даты</b>")



    if kill_date is not None:
        text += "\n\n<b>Уже выбрано:</b>\n"
        for date in kill_date.keys():
            text += f"\n{date}"

    await bot.send_message(callback.message.chat.id, text, reply_markup=keyboard)
    await callback.message.delete()


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


async def confirm_date(callback: types.CallbackQuery, state: FSMContext):
    """Этап 8. Подтверждение выбора данных"""
    await callback.answer("Меню подтверждения")

    state_data = await state.get_data()
    await callback.message.delete()
    warehouse = state_data.get("warehouse_name")
    delivery_type = state_data.get("delivery_type")
    coefficient = state_data.get("coefficient")
    warehouse_collection_name = state_data.get("warehouse_collection_name")

    date = state_data.get("date")
    text = (f"🔔🔔🔔Проверьте корректность задания. \n\n"
            f"Тип склада: <b>{WAREHOUSE_COLLECTION[warehouse_collection_name]}</b>\n"
            f"Склад: <b>{warehouse}</b>\n"
            f"Тип поставки: <b>{DELIVERY_VOCABULARY[delivery_type]}</b> \n"
            f"Коэффициент: <b>{coefficiernt_text_return(coefficient)}</b>\n"
            )

    if date != 'custom':
        start_date = datetime.strptime(state_data.get("first_date"), "%Y-%m-%d")
        end_date = datetime.strptime(state_data.get("last_date"), "%Y-%m-%d")
        dates_list = [date.strftime("%Y-%m-%d") for date in daterange(start_date, end_date)]
        state_data['days_for_result'] = dates_list
        text += f"Дата: {state_data.get('first_date')} - {state_data.get('last_date')}"
    else:
        text += f"Искать слоты на следующие даты: "
        chosen_dates = state_data.get("kill_date")
        dates_list = list(chosen_dates.keys())
        state_data["days_for_result"] = dates_list
        for dat in chosen_dates.keys():
            text += f"\n{dat}"
    await state.update_data(state_data)
    keyboard = confirm_date_kb()
    await bot.send_message(callback.message.chat.id, text=text, reply_markup=keyboard)


async def alarm_clock_finish(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Этап 9. Завершение будильника"""
    await callback.answer("Подтверждение получено")
    message = await bot.send_message(callback.message.chat.id, "Загружаем данные ...")
    state_data = await state.get_data()
    days_list = [{"search_day": day} for day in state_data.get("days_for_result")]
    if state_data.get('delivery_type') == "monopolets":
        delivery_type_send = "monopollet"
    else:
        delivery_type_send = state_data.get('delivery_type')
    result_data = {"warehouse": state_data.get("warehouse"),
                   "client": callback.message.chat.id,
                   "find_coefficient": state_data.get("coefficient"),
                   "delivery_type": delivery_type_send,
                   "days": days_list}
    url = URL_TASK
    d = json.dumps(result_data)
    response = requests.post(url, data=d, headers={"Content-Type": "application/json"})
    print(response.status_code)
    if response.status_code != 201:
        await bot.send_message(callback.message.chat.id, "Произошла ошибка при добавлении задания")
        return
    response_data = response.json()
    print(response_data)
    await message.delete()
    success_finish_text = ("🆗 Ваше задание успешно добавлено.\n\nКак только появится подходящий слот на "
                           "склад, вам придет уведомление.\n\n"
                           "После отправки уведомления считается,что задача выполнена и она удаляется из "
                           "списка активных задач.")
    keyboard = finish_kb()
    await bot.send_message(callback.message.chat.id, text=success_finish_text, reply_markup=keyboard)
    await callback.message.delete()


router.callback_query.register(alarm_clock_menu, F.data == "alarm_clock_start")
router.callback_query.register(alarm_clock_again, F.data == "alarm_clock_again")
router.callback_query.register(choice_type_of_warehouse_again, F.data == "start_task_again")
router.callback_query.register(choice_type_of_warehouse, F.data == "type_of_warehouse",
                               StateFilter(AlarmClockStates.start))
router.callback_query.register(warehouse_choice,
                               F.data.startswith("pagination_warehouse_"),
                               StateFilter(AlarmClockStates.start))
router.callback_query.register(catch_warehouse_and_type_of_delivery_menu, F.data.startswith("warehouse_"),
                               StateFilter(AlarmClockStates.start))
router.callback_query.register(catch_delivery_type_and_coefficients_menu,
                               F.data.startswith("delivery_type_"),
                               StateFilter(AlarmClockStates.start))
router.callback_query.register(catch_coefficients_and_date_menu,
                               F.data.startswith("coefficient_"),
                               StateFilter(AlarmClockStates.start))
router.callback_query.register(catch_data_choice, F.data.startswith("data_choice_"),
                               StateFilter(AlarmClockStates.start))
router.callback_query.register(custom_data_choice_continue, F.data.startswith("custom_date_choice_"))
router.callback_query.register(confirm_date, F.data == "confirm_date",
                               StateFilter(AlarmClockStates.start))
router.callback_query.register(alarm_clock_finish, F.data == "alarm_finish")
router.callback_query.register(alarm_clock_menu, F.data == "main_menu")
