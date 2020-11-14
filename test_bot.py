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

#def SearchFunc(msg = ''):
#	out=[]
#	if msg == '':
#		return out
#	else:
#		for k in range(50):
#			out.append('  second text {}'.format(k+1))
#		return out

def SearchFunc(string):
    url = "http://my.rest.api/search/" + string
    drug_list = requests.get(url)
    drug_list = drug_list.json()
    mylist = [];
    for item in drug_list:
       for value in item.values():
            mylist.append(value)

    lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    mylist = lol(mylist, 5)
    return mylist

bot = telebot.TeleBot('1443865969:AAGgoDOGnW7q2j1WGprdLP0gR6trtWNLyoA');

cur_basket = []
search_name = ''

# Клавиатура
# 1
markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
item11 = types.KeyboardButton('Поиск лекарства 💊')
item12 = types.KeyboardButton('Поиск аптеки 🚑')
item13 = types.KeyboardButton('Моя корзина 🛒')
markup1.add(item11, item12)
markup1.add(item13)
# 2
markup2 = types.ReplyKeyboardMarkup(resize_keyboard = True)
item21 = types.KeyboardButton('В начало🔼')
markup2.add(item21)
# 5,6,7
markup5 = types.ReplyKeyboardMarkup(resize_keyboard = True)
item51 = types.KeyboardButton('◀')
item52 = types.KeyboardButton('▶')
markup5.add(item52)
markup5.add(item21)
markup6 = types.ReplyKeyboardMarkup(resize_keyboard = True)
markup6.add(item51,item52)
markup6.add(item21)
markup7 = types.ReplyKeyboardMarkup(resize_keyboard = True)
markup7.add(item51)
markup7.add(item21)
# hide
hideBoard = types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_photo(message.chat.id, "https://yadi.sk/i/U39tZCQRbk-K4A", reply_markup = markup1)


@bot.message_handler(content_types=['text'])
def other_windows(message):
	# Ветка "поиск лекарства"
	if message.text == 'Поиск лекарства 💊':
		win_search_product(message)

	# Ветка "поиск аптеки"
	elif message.text == 'Поиск аптеки 🚑':
		win_search_adress(message)
	
	# Ветка "моя корзина"
	elif message.text == 'Моя корзина 🛒':
		basket(message)
		#bot.send_message(message.chat.id, 'В вашей корзине🛒:\n\n' + '№|Название|Производитель|Аптека|Цена', reply_markup = markup2)
		
	# Кнопка "в начало"
	elif message.text == 'В начало 🔼':
		return welcome(message)
		
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
	search_name = message.text
	markup4 = types.InlineKeyboardMarkup()
	item41 = types.InlineKeyboardButton('Да', callback_data = 'yes_product')
	item42 = types.InlineKeyboardButton('Нет', callback_data = 'no_product')

	markup4.add(item41)
	markup4.add(item42)

	

	bot.send_message(message.chat.id, 'Вы ввели: ' + searh_name + '\nДанные верны?', reply_markup = markup4)


def win_outsearch_product(message):
	out = SearchFunc(search_name)
	cur_page = ''
	pages = ceil(len(out) / 4)
	Ncur_page = 1
	for i in range(4):
		cur_page += str(i+1) + ' ' + ' '.join(out[i][1:]) + '\n'
	bot.send_message(message.chat.id, 'Вот что я нашёл:\n' + cur_page + '\n\nВыведена страница 1/' + str(pages) + '\n\nДля добавления товара в корзину введите его номер из списка:', reply_markup = markup5)
	bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))

	
def table(message, out, Ncur_page, pages, cur_page):
	if message.text == '▶':
		cur_page = ''
		Ncur_page += 1
		for i in range(4):
			if i+4*Ncur_page < len(out):
				cur_page += str(i+1) + ' '.join(out[i+4*Ncur_page][1:]) + '\n'
		if Ncur_page == 1:
			gen_table(message, 0, out, Ncur_page, pages, cur_page)
		elif Ncur_page == pages:
			gen_table(message, 2, out, Ncur_page, pages, cur_page)
		else:
			gen_table(message, 1, out, Ncur_page, pages, cur_page)
	elif message.text == '◀':
		cur_page = ''
		Ncur_page -= 1
		for i in range(4):
			if 4*Ncur_page - i >= 0:
				cur_page += str(i+1) + ' '.join(out[4*Ncur_page - i][1:]) + '\n'
		if Ncur_page == 1:
			gen_table(message, 0, out, Ncur_page, pages, cur_page)
		elif Ncur_page == pages:
			gen_table(message, 2, out, Ncur_page, pages, cur_page)
		else:
			gen_table(message, 1, out, Ncur_page, pages, cur_page)
	elif message.text == 'В начало 🔼':
		welcome(message)
	elif message.text == '1':
		cur_basket.append(out[1 + 4*Ncur_page])
		bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))
	elif message.text == '2':
		cur_basket.append(out[2 + 4*Ncur_page])
		bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))
	elif message.text == '3':
		cur_basket.append(out[3 + 4*Ncur_page])
		bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))
	elif message.text == '4':
		cur_basket.append(out[4 + 4*Ncur_page])
		bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))


def gen_table(message, toggle, out, Ncur_page, pages, cur_page):
	if toggle == 0:
		tmp_markup = markup5
		
	elif toggle == 1:
		tmp_markup = markup6
		
	elif toggle == 2:
		tmp_markup = markup7
		
	msg = 'Вот что я нашёл:\n' + cur_page + '\n\nВыведена страница ' + str(Ncur_page) + '/' + str(pages) + '\n\nДля добавления товара в корзину введите его номер из списка:'
	#bot.edit_message_text(chat_id = message.chat.id, message_id = message.message_id - 1, text = msg, reply_markup = tmp_markup) -не работает
	bot.send_message(message.chat.id, msg, reply_markup = tmp_markup)
	bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))



def win_outsearch_adress(message):
	out = SearchFunc(message.text)
	cur_page = ''
	pages = ceil(len(out) / 4)
	Ncur_page = 1
	for i in range(4):
		cur_page += str(i+1) + ' '.join(out[i][1:]) + '\n'
	bot.send_message(message.chat.id, 'Вот что я нашёл:\n' + cur_page + '\n\nВыведена страница 1/' + str(pages) + '\n\nДля добавления товара в корзину введите его номер из списка:', reply_markup = markup5)
	bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))


def basket(message):
	bb = '\n'
	for i in range(len(cur_basket)):
		bb += str(i+1) + ' '.join(cur_basket[i][1:]) + '\n'
	bot.send_message(message.chat.id, 'В вашей корзине 🛒:\n\n' + '№ | Название | Производитель | Аптека | Цена' + bb, reply_markup = markup2)



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
