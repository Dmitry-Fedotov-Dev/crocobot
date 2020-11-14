import telebot
import requests
import codecs
import json
from telebot import types

def getCategoryFunc(category):
	if category == "cat1":
		url = "http://my.rest.api/posts"
		drug_list = requests.get(url)
		return json.dumps(drug_list.json(), ensure_ascii = False)
	if category == "cat2":
		return "Пока низя"
	if category == "cat3":
		return "Ещё не готово"



bot = telebot.TeleBot('1443865969:AAGgoDOGnW7q2j1WGprdLP0gR6trtWNLyoA');

@bot.message_handler(commands=['start'])
def welcome(message):
	# Клавиатура
	markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
	item11 = types.KeyboardButton('Поиск лекарства💊')
	item12 = types.KeyboardButton('Поиск аптеки🚑')
	item13 = types.KeyboardButton('Моя корзина🛒')

	markup1.add(item11, item12)
	markup1.add(item13)

	bot.send_photo(message.from_user.id, "https://www.prikol.ru/wp-content/gallery/october-2019/prikol-25102019-001.jpg", reply_markup = markup1)


@bot.message_handler(content_types=['text'])
def other_windows(message):
	markup2 = types.ReplyKeyboardMarkup(resize_keyboard = True)
	item21 = types.KeyboardButton('В начало◀')
	markup2.add(item21)

	# Ветка "поиск лекарства"
	if message.text == 'Поиск лекарства💊':
		bot.send_message(message.from_user.id, 'Введите название интересующего вас товара:')
		bot.register_next_step_handler(message, set_product)
		
	# Ветка "поиск аптеки"
	elif message.text == 'Поиск аптеки🚑':
		bot.send_message(message.from_user.id, 'Введите ваш адрес (город, улица):')
		bot.register_next_step_handler(message, set_adress)
		
	# Ветка "моя корзина"
	elif message.text == 'Моя корзина🛒':
		bot.send_message(message.from_user.id, 'В вашей корзине🛒:\n\n' + '№|Название|Производитель|Аптека|Цена', reply_markup = markup2)
		
	# Кнопка "в начало"
	elif message.text == 'В начало◀':
		return welcome(message)
		
	# Остальное
	else:
		bot.send_message(message.from_user.id, "Я не  понимаю 😢")


def set_adress(message):
	markup3 = types.InlineKeyboardMarkup()
	item31 = types.InlineKeyboardButton('Да', callback_data = 'yes')
	item32 = types.InlineKeyboardButton('Нет', callback_data = 'no_adress')

	markup3.add(item31)
	markup3.add(item32)

	bot.send_message(message.from_user.id, 'Вы ввели: ' + message.text + '\nДанные верны?', reply_markup = markup3)


def set_product(message):
	markup4 = types.InlineKeyboardMarkup()
	item41 = types.InlineKeyboardButton('Да', callback_data = 'yes')
	item42 = types.InlineKeyboardButton('Нет', callback_data = 'no_product')

	markup4.add(item41)
	markup4.add(item42)

	bot.send_message(message.from_user.id, 'Вы ввели: ' + message.text + '\nДанные верны?', reply_markup = markup4)



@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == 'yes':
		bot.send_message(call.message.chat.id, 'Запомню : )');
	elif call.data == 'no_adress':
		# ответ
		pass
	elif call.data == 'no_product':
		# ответ
		pass


bot.polling(none_stop=True, interval=0)
