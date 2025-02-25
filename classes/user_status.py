from aiogram.fsm.state import StatesGroup, State


class UserStatus(StatesGroup):
	"""
	Класс для управления состояниями пользователя в процессе взаимодействия с ботом.
	"""
	picking_deck = State() # Пользователь выбирает колоду/тему вопросов
	approving_deck = State() # Пользователь подтверждает выбор колоды
	session_front = State() # Пользователь видит вопрос
	session_back = State() # Пользователь видит верный ответ и оценивает свой ответ

