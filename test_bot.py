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

	markup1.add(item11, item12, item13)
	


	bot.send_photo(message.from_user.id, "https://www.prikol.ru/wp-content/gallery/october-2019/prikol-25102019-001.jpg", reply_markup= markup1)


@bot.message_handler(content_types=['text'])
def other_windows(message):
	if message.chat.type == 'private':
		if message.text == 'Поиск лекарства💊':
			bot.send_message(message.from_user.id, 'Введите название интересующего вас товара')
		elif message.text == 'Поиск аптеки🚑':
			bot.send_message(message.from_user.id, '')
		elif message.text == 'Моя корзина🛒':
			markup2 = types.ReplyKeyboardMarkup(resize_keyboard = True)
			item21 = types.KeyboardButton('В начало◀')
			markup2.add(item21)
			bot.send_message(message.from_user.id, 'В вашей корзине🛒:\n\n' + '№|Название|Производитель|Аптека|Цена', reply_markup = markup2)
		elif message.text == 'В начало◀':
			return welcome(message)
		else:
			bot.send_message(message.from_user.id, "Я не  понимаю 😢")

	#elif message.text == "1":
	#	bot.send_message(message.from_user.id, "Вот что есть в наличии: ")
	#	category = "cat1"
	#	bot.send_message(message.from_user.id, getCategoryFunc(category))	
	#elif message.text == "2":
	#	category = "cat2"
	#	bot.send_message(message.from_user.id, getCategoryFunc(category))
	#elif message.text == "3":
	#	category = "cat3"
	#	bot.send_message(message.from_user.id, getCategoryFunc(category))
	#else: 
	#	bot.send_message(message.from_user.id, "Я не  понимаю 😢")

bot.polling(none_stop=True, interval=0)
