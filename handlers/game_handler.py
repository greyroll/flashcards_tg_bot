import requests
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, ReplyKeyboardRemove

from loguru import logger

from classes.user_status import UserStatus
from config import BACKEND_URL, API_KEY
from funcs import create_keyboard


class GameHandler:

	@staticmethod
	async def start_command(message: Message, state: FSMContext):
		"""Отправляет запрос на сервер для получения доступных колод."""

		logger.info(f"Отправка GET-запроса на {BACKEND_URL}/decks/names, получение доступных колод")
		response = requests.get(f"{BACKEND_URL}/decks/names", headers={"X-API-Key": API_KEY})

		if response.status_code == 200:
			data = response.json()
			logger.info(f"Получены данные: {data}")
			await message.answer(text="Привет! Добро пожаловать в бота для изучения слов.")
			await message.answer(
				text="Выберите колоду:",
				reply_markup=create_keyboard(data["decks_names"])
			)
			await state.set_state(UserStatus.picking_deck)
		else:
			logger.error(f"Ошибка запроса: {requests.RequestException}, статус: {response.status_code}, ответ: {response.text}")
			await message.answer(text=f"{response.status_code}, {response.text}")

	@staticmethod
	async def approve_deck(message: Message, state: FSMContext):
		"""Запрашивает у пользователя подтверждение выбранной колоды."""

		logger.info(f"Пользователь: {message.from_user.full_name}, выбрана колода: {message.text}. Ожидание подтверждения от пользователя.")
		deck = message.text

		await message.answer(text=f"Выбранная колода: {deck}")
		await message.answer(
			text="Начать игру?",
			reply_markup=create_keyboard(["Да", "Вернуться обратно"])
		)
		await state.set_data({"deck_name": deck})
		await state.set_state(UserStatus.approving_deck)

	@staticmethod
	async def start_session(message: Message, state: FSMContext):
		"""
		Запускает сессию для выбранной колоды.
		Отправляет запрос с данными о пользователе и колоде на сервер.
		Перенаправляет на UserHandlers.show_front
		"""

		result = await state.get_data()
		deck_name = result["deck_name"]
		user_name = message.from_user.full_name
		logger.info(f"Начало сессии для {user_name} с колодой {deck_name}")

		response = requests.post(
			url=f"{BACKEND_URL}/session/start",
			json={"user_name": user_name, "deck_name": deck_name},
			headers={"X-API-Key": API_KEY},
		)

		if response.status_code == 200:
			data = response.json()
			session_id: int = data.get("session_id", "Ошибка: сессия не найдена")
			logger.info(f"Сессия запущена, session_id: {session_id}")
			await state.update_data({"session_id": session_id})
			await GameHandler.show_front(message, state)
		else:
			await message.answer(text=f"{response.status_code}, {response.text}")
			logger.error(f"Ошибка запроса: {requests.RequestException}, статус: {response.status_code}, ответ: {response.text}")


	@staticmethod
	async def show_front(message: Message, state: FSMContext):
		"""Запрашивает у сервера фронт-карту для текущей сессии."""

		result = await state.get_data()
		session_id = result["session_id"]
		logger.info(f"Запрос на фронт-карту сессии {session_id}")

		headers = {"Authorization": f"Bearer {session_id}", "X-API-Key": API_KEY}
		response = requests.get(f"{BACKEND_URL}/session/front", headers=headers)

		if response.status_code == 200:
			data = response.json()
			card_front = data.get("card_front", "Ошибка: карта не найдена")
			logger.info(f"Получены данные: {data}")
			await message.answer(
				text=f"Вопрос:\n{card_front}",
				reply_markup=create_keyboard(["Перевернуть", "Завершить сессию"])
			)
			await state.set_state(UserStatus.session_front)
		else:
			await message.answer(text=f"{response.status_code}, {response.text}")
			logger.error(f"Ошибка запроса: {requests.RequestException}, статус: {response.status_code}, ответ: {response.text}")

	@staticmethod
	async def show_back(message: Message, state: FSMContext):
		"""Запрашивает у сервера бэк-карту для текущей сессии."""

		result = await state.get_data()
		session_id = result["session_id"]
		logger.info(f"Запрос на бэк-карту сессии {session_id}")

		headers = {"Authorization": f"Bearer {session_id}", "X-API-Key": API_KEY}
		response = requests.get(f"{BACKEND_URL}/session/back", headers=headers)

		if response.status_code == 200:
			data = response.json()
			card_back = data.get("card_back", "Ошибка: карта не найдена")
			logger.info(f"Получены данные: {data}")
			await message.answer(
				text=f"Ответ:\n{card_back}",
				reply_markup=create_keyboard(["Знаю", "Повторить", "Завершить сессию"])
			)
			await state.set_state(UserStatus.session_back)
		else:
			await message.answer(text=f"{response.status_code}, {response.text}")
			logger.error(f"Ошибка запроса: {requests.RequestException}, статус: {response.status_code}, ответ: {response.text}")


	@staticmethod
	async def check_answer_and_show_next_card(message: Message, state: FSMContext):
		"""
		Отправляет на сервер ответ пользователя по карточке. Проверяет завершена ли сессия.
		Перенаправляет на UserHandlers.finish_session_show_stats если завершена.
		Перенаправляет на UserHandlers.show_front если не завершена.
		"""

		answer = message.text
		is_card_studied = False
		if answer == "Знаю":
			is_card_studied = True

		result = await state.get_data()
		session_id = result["session_id"]
		logger.info(f"Отправка ответа на карту: {is_card_studied}, сессия: {session_id}")

		headers = {"Authorization": f"Bearer {session_id}", "X-API-Key": API_KEY}
		response = requests.post(f"{BACKEND_URL}/session/check_answer", headers=headers, json={"is_card_studied": is_card_studied})

		if response.status_code == 200:
			data = response.json()
			is_finished = data.get("is_finished", False)
			if is_finished:
				logger.info(f"Сессия {session_id} завершена, показываем статистику")
				await GameHandler.finish_session_show_stats(message, state)
			else:
				await GameHandler.show_front(message, state)
		else:
			await message.answer(text=f"{response.status_code}, {response.text}")
			logger.error(f"Ошибка запроса: {requests.RequestException}, статус: {response.status_code}, ответ: {response.text}")

	@staticmethod
	async def finish_session_show_stats(message: Message, state: FSMContext):
		"""Завершает сессию и показывает статистику."""

		result = await state.get_data()
		session_id = result["session_id"]
		logger.info(f"Запрос на завершение сессии {session_id}")

		headers = {"Authorization": f"Bearer {session_id}", "X-API-Key": API_KEY}
		response = requests.get(f"{BACKEND_URL}/session/finish", headers=headers)

		if response.status_code == 200:
			data = response.json()
			studied_cards_number = data["studied_cards_number"]
			logger.info(f"Сессия завершена. Изучено карт: {studied_cards_number}")
			await message.answer(
				text=f"Колода:\n{result['deck_name']}\nКоличество изученных карточек: {studied_cards_number}",
				reply_markup=ReplyKeyboardRemove()
			)
		else:
			await message.answer(text=f"{response.status_code}, {response.text}")
			logger.error(f"Ошибка запроса: {requests.RequestException}, статус: {response.status_code}, ответ: {response.text}")

