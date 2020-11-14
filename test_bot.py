import telebot
import requests
import codecs
import json
from telebot import types
from math import ceil

def getCategoryFunc(category):
	if category == "cat1":
		url = "http://my.rest.api/posts"
		drug_list = requests.get(url)
		return json.dumps(drug_list.json(), ensure_ascii = False)
	if category == "cat2":
		return "Пока низя"
	if category == "cat3":
		return "Ещё не готово"

def SearchFunc(msg = ''):
	out=[]
	if msg == '':
		return out
	else:
		for k in range(50):
			out.append('{} second text'.format(k+1))
		return out

bot = telebot.TeleBot('1443865969:AAGgoDOGnW7q2j1WGprdLP0gR6trtWNLyoA');


# Клавиатура
# 1
markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
item11 = types.KeyboardButton('Поиск лекарства💊')
item12 = types.KeyboardButton('Поиск аптеки🚑')
item13 = types.KeyboardButton('Моя корзина🛒')
markup1.add(item11, item12)
markup1.add(item13)
# 2
markup2 = types.ReplyKeyboardMarkup(resize_keyboard = True)
item21 = types.KeyboardButton('В начало🔼')
markup2.add(item21)
# 5
markup5 = types.ReplyKeyboardMarkup(resize_keyboard = True)
item51 = types.KeyboardButton('◀')
item52 = types.KeyboardButton('▶')
# hide
hideBoard = types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_photo(message.chat.id, "https://www.prikol.ru/wp-content/gallery/october-2019/prikol-25102019-001.jpg", reply_markup = markup1)


@bot.message_handler(content_types=['text'])
def other_windows(message):
	# Ветка "поиск лекарства"
	if message.text == 'Поиск лекарства💊':
		win_search_product(message)

	# Ветка "поиск аптеки"
	elif message.text == 'Поиск аптеки🚑':
		win_search_adress(message)
	
	# Ветка "моя корзина"
	elif message.text == 'Моя корзина🛒':
		bot.send_message(message.chat.id, 'В вашей корзине🛒:\n\n' + '№|Название|Производитель|Аптека|Цена', reply_markup = markup2)
		
	# Кнопка "в начало"
	elif message.text == 'В начало🔼':
		welcome(message)
		
	# Остальное
	else:
		bot.send_message(message.chat.id, "Я не  понимаю 😢\nИспользуйте /start чтобы начать сначала")

def win_search_product(message):
	bot.send_message(message.chat.id, 'Введите название интересующего вас товара:', reply_markup = hideBoard)
	bot.register_next_step_handler(message, set_product)


def win_search_adress(message):
	bot.send_message(message.chat.id, 'Введите ваш адрес (город, улица):', reply_markup = hideBoard)
	bot.register_next_step_handler(message, set_adress)


def set_adress(message):
	markup3 = types.InlineKeyboardMarkup()
	item31 = types.InlineKeyboardButton('Да', callback_data = 'yes_adress')
	item32 = types.InlineKeyboardButton('Нет', callback_data = 'no_adress')

	markup3.add(item31)
	markup3.add(item32)

	bot.send_message(message.chat.id, 'Вы ввели: ' + message.text + '\nДанные верны?', reply_markup = markup3)


def set_product(message):
	markup4 = types.InlineKeyboardMarkup()
	item41 = types.InlineKeyboardButton('Да', callback_data = 'yes_product')
	item42 = types.InlineKeyboardButton('Нет', callback_data = 'no_product')

	markup4.add(item41)
	markup4.add(item42)

	bot.send_message(message.chat.id, 'Вы ввели: ' + message.text + '\nДанные верны?', reply_markup = markup4)


def win_outsearch_product(message):
	out = SearchFunc(message.text)
	cur_page = ''
	pages = ceil(out.count() / 4)
	for i in range(4):
		cur_page += i+1 + out[i][1:] + '\n'
	tmp_markup = markup5
	tmp_markup.add(item52)
	tmp_markup.add(item21)
	bot.send_message(message.chat.id, 'Вот что я нашёл:\n' + cur_page + '\n\nВыведена страница 1/' + pages + '\n\nДля добавления товара в корзину введите его номер из списка:', reply_markup = tmp_markup)
	bot.register_next_step_handler(message, table(out = out, Ncur_page = 1, pages = pages))

	
def table(message, out, Ncur_page, pages):
	if message.text == '▶':
		cur_page = ''
		Ncur_page += 1
		for i in range(4):
			if i+4*Ncur_page < out.count:
				cur_page += i+1 + out[i+4*Ncur_page][1:] + '\n'
		if Ncur_page == 1:
			gen_table(message, 0, cur_page, Ncur_page, pages)
		elif Ncur_page == pages:
			gen_table(message, 2, cur_page, Ncur_page, pages)
		else:
			gen_table(message, 1, cur_page, Ncur_page, pages)
	elif message.text == '◀':
		cur_page = ''
		Ncur_page -= 1
		for i in range(4):
			if 4*Ncur_page - i > 0:
				cur_page += i+1 + out[4*Ncur_page - i][1:] + '\n'
		if Ncur_page == 1:
			gen_table(message, 0, cur_page, Ncur_page, pages)
		elif Ncur_page == pages:
			gen_table(message, 2, cur_page, Ncur_page, pages)
		else:
			gen_table(message, 1, cur_page, Ncur_page, pages)
	elif message.text == 'В начало🔼':
		return welcome(message)

def gen_table(message, toggle, cur_page, Ncur_page, pages):
	if toggle == 0:
		tmp_markup = markup5
		tmp_markup.add(item52)
		tmp_markup.add(item21)
		
	elif toggle == 1:
		tmp_markup = markup5
		tmp_markup.add(item51,item52)
		tmp_markup.add(item21)
		
	elif toggle == 2:
		tmp_markup = markup5
		tmp_markup.add(item51)
		tmp_markup.add(item21)
	msg = 'Вот что я нашёл:\n' + cur_page + '\n\nВыведена страница ' + Ncur_page + '/' + pages + '\n\nДля добавления товара в корзину введите его номер из списка:'
	bot.edit_message_text(text = msg, chat_id = message.chat.id, message_id = message.message_id, reply_markup = tmp_markup)

def win_outsearch_adress(message):
	out = SearchFunc(message.text)
	msg = ''
	for i in out:
		msg += i + '\n'
	bot.send_message(message.chat.id, 'Вот что я нашёл:\n' + msg + '\nДля добавления товара в корзину введите его номер из списка:', reply_markup = markup5)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == 'yes_adress':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		win_outsearch_adress(call.message)
	elif call.data == 'yes_product':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		win_outsearch_product(call.message)
	elif call.data == 'no_adress':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		win_search_adress(call.message)
	elif call.data == 'no_product':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		win_search_product(call.message)

bot.polling(none_stop=True, interval=0)
