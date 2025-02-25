from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_keyboard(options: list) -> ReplyKeyboardMarkup:
	"""
	Создаёт клавиатуру с кнопками на основе переданного списка опций.

	:param options: Список строк, каждая из которых будет текстом на отдельной кнопке клавиатуры.
	:return: ReplyKeyboardMarkup: Объект клавиатуры с кнопками, которые соответствуют элементам списка `options`.
	"""
	buttons = []
	for button in options:
		buttons.append(KeyboardButton(text=button))
	keyboard = ReplyKeyboardMarkup(keyboard=[buttons])
	return keyboard