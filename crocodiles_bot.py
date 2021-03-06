import telebot
import requests
import codecs
import json
from telebot import types
from math import ceil


def SearchFunc(string):
    url = "http://my.rest.api/search/" + string
    drug_list = requests.get(url)
    drug_list = drug_list.json()
    mylist = [];
    for item in drug_list:
       for value in item.values():
            mylist.append(value)
    mystring = " | ".join(mylist)
    my_beauty_string = mystring.title()
    my_beauty_list = my_beauty_string.split(" | ")
    
    lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    my_beauty_list = lol(my_beauty_list, 5)
    return my_beauty_list

bot = telebot.TeleBot('1443865969:AAGgoDOGnW7q2j1WGprdLP0gR6trtWNLyoA');

cur_basket = []
search_name = ''
char_list = ['1️⃣','2️⃣','3️⃣','4️⃣']

# Keyboards
# 1
markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
item11 = types.KeyboardButton('Поиск лекарства 💊')
item12 = types.KeyboardButton('Помощь 👨‍💻')
item13 = types.KeyboardButton('Моя корзина 🛒')
markup1.add(item11, item12)
markup1.add(item13)
# 2
markup2 = types.ReplyKeyboardMarkup(resize_keyboard = True)
item21 = types.KeyboardButton('В начало 🔼')
item22 = types.KeyboardButton('Очистить корзину ♻')
item23 = types.KeyboardButton('Отправить запрос 📝', request_contact = True)
markup2.add(item22, item21, item23)
# 5,6,7
markup5 = types.ReplyKeyboardMarkup(resize_keyboard = True)
item_ch1 = types.KeyboardButton(char_list[0])
item_ch2 = types.KeyboardButton(char_list[1])
item_ch3 = types.KeyboardButton(char_list[2])
item_ch4 = types.KeyboardButton(char_list[3])
item51 = types.KeyboardButton('◀')
item52 = types.KeyboardButton('▶')
markup5.add(item_ch1, item_ch2, item_ch3, item_ch4)
markup5.add(item52)
markup5.add(item21)
markup6 = types.ReplyKeyboardMarkup(resize_keyboard = True)
markup6.add(item_ch1, item_ch2, item_ch3, item_ch4)
markup6.add(item51,item52)
markup6.add(item21)
markup7 = types.ReplyKeyboardMarkup(resize_keyboard = True)
markup7.add(item_ch1, item_ch2, item_ch3, item_ch4)
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

	# Ветка "помощь"
	elif message.text == 'Помощь 👨‍💻':
		documentation_help(message)
	
	# Ветка "моя корзина"
	elif message.text == 'Моя корзина 🛒':
		basket(message)

	# Кнопка "в начало"
	elif message.text == 'В начало 🔼':
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



def set_product(message):
	search_name = message.text
	markup4 = types.InlineKeyboardMarkup()
	item41 = types.InlineKeyboardButton('Да', callback_data = 'yes_product,{}'.format(search_name))
	item42 = types.InlineKeyboardButton('Нет', callback_data = 'no_product')

	markup4.add(item41)
	markup4.add(item42)

	bot.send_message(message.chat.id, 'Вы ввели: ' + search_name + '\nДанные верны?', reply_markup = markup4)


def win_outsearch_product(message, search_name):
	out = SearchFunc(search_name)
	cur_page = ''
	pages = ceil(len(out) / 4)
	Ncur_page = 0
	if len(out) == 1: k = 1
	elif len(out) == 2: k = 2
	elif len(out) == 3: k = 3
	elif len(out) == 4: k = 4
	else: k = 4
	for i in range(k):
		cur_page += char_list[i] + ' ' + ' '.join(out[i][1:3]) + ' (' + out[i][4] + 'руб.)\n'
	bot.send_message(message.chat.id, 'Вот что я нашёл:\n' + cur_page + '\n\nВыведена страница 1/' + str(pages) + '\n\nДля добавления товара в корзину введите его номер из списка:', reply_markup = markup5)
	bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))

def table(message, out, Ncur_page, pages, cur_page):
	if message.text == '▶':
		cur_page = ''
		Ncur_page += 1
		for i in range(4):
			if i+4*Ncur_page < len(out):
				cur_page += char_list[i] + ' ' + ' '.join(out[i+4*Ncur_page][1:3]) + ' (' + out[i+4*Ncur_page][4] + 'руб.)\n'
		if Ncur_page == 0:
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
				cur_page += char_list[i] + ' ' + ' '.join(out[4*Ncur_page - i][1:3]) + ' (' + out[4*Ncur_page - i][4] + 'руб.)\n'
		if Ncur_page == 0:
			gen_table(message, 0, out, Ncur_page, pages, cur_page)
		elif Ncur_page == pages:
			gen_table(message, 2, out, Ncur_page, pages, cur_page)
		else:
			gen_table(message, 1, out, Ncur_page, pages, cur_page)
	elif message.text == 'В начало 🔼':
		welcome(message)
	elif message.text == char_list[0]:
		cur_basket.append(out[4*Ncur_page])
		if Ncur_page == 0:
			gen_table(message, 0, out, Ncur_page, pages, cur_page)
		elif Ncur_page == pages:
			gen_table(message, 2, out, Ncur_page, pages, cur_page)
		else:
			gen_table(message, 1, out, Ncur_page, pages, cur_page)
		bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))
	elif message.text == char_list[1]:
		cur_basket.append(out[1 + 4*Ncur_page])
		if Ncur_page == 0:
			gen_table(message, 0, out, Ncur_page, pages, cur_page)
		elif Ncur_page == pages:
			gen_table(message, 2, out, Ncur_page, pages, cur_page)
		else:
			gen_table(message, 1, out, Ncur_page, pages, cur_page)
		bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))
	elif message.text == char_list[2]:
		cur_basket.append(out[2 + 4*Ncur_page])
		if Ncur_page == 0:
			gen_table(message, 0, out, Ncur_page, pages, cur_page)
		elif Ncur_page == pages:
			gen_table(message, 2, out, Ncur_page, pages, cur_page)
		else:
			gen_table(message, 1, out, Ncur_page, pages, cur_page)
		bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))
	elif message.text == char_list[3]:
		cur_basket.append(out[3 + 4*Ncur_page])
		if Ncur_page == 0:
			gen_table(message, 0, out, Ncur_page, pages, cur_page)
		elif Ncur_page == pages:
			gen_table(message, 2, out, Ncur_page, pages, cur_page)
		else:
			gen_table(message, 1, out, Ncur_page, pages, cur_page)
		bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))
		


def gen_table(message, toggle, out, Ncur_page, pages, cur_page):
	if toggle == 0:
		tmp_markup = markup5
		
	elif toggle == 1:
		tmp_markup = markup6
		
	elif toggle == 2:
		tmp_markup = markup7
		
	msg = 'Вот что я нашёл:\n' + cur_page + '\n\nВыведена страница ' + str(Ncur_page + 1) + '/' + str(pages) + '\n\nДля добавления товара в корзину введите его номер из списка:'
	bot.send_message(message.chat.id, msg, reply_markup = tmp_markup)
	bot.register_next_step_handler(message, lambda mm: table(mm, out, Ncur_page, pages, cur_page))

def documentation_help(message):
	bot.send_message(message.chat.id, 'Чтобы было легче разобраться, я приготовил для тебя небольшую инструкцию!\nЧтобы с ней ознакомиться, перейди по ссылке:\n\n https://telegra.ph/Crocobot-here-11-15')


def basket(message):
	bb = '\n'
	if len(cur_basket) > 0:
		for i in range(len(cur_basket)):
			bb += str(i+1) + ' | ' + ' | '.join(cur_basket[i][1:3]) + ' | ' + cur_basket[i][4] + 'руб.\n'
	bot.send_message(message.chat.id, 'В вашей корзине 🛒:\n\n' + '№ | Название | Производитель | Цена' + bb + '\nДля удаления товара из корзины введите их номера через запятую (1,2,3):', reply_markup = markup2)
	bot.register_next_step_handler(message, delete_item_from_basket)


def delete_item_from_basket(message):
	if message.text == 'Очистить корзину ♻':
		cur_basket.clear()
		basket(message)
	elif message.text == 'Отправить запрос 📝':
		bot.send_message(message.chat.id, '🏢 Ваш запрос успешно отправлен на наш сервер 🏢\n📞 С вами скоро свяжется наш специалист 📞\n❤ Спасибо, что выбираете нас ❤')
		#send_basket()
		cur_basket.clear()
	elif message.text == 'В начало 🔼':
		welcome(message)
	else:
		if len(message.text) > 0:
			dels = message.text.split(',')
			for i in dels:
				cur_basket.pop(int(i)-1)
			basket(message)
			


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data.split(',')[0] == 'yes_product':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		win_outsearch_product(call.message, call.data.split(',')[1])
	elif call.data == 'no_product':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		win_search_product(call.message)
	

bot.polling(none_stop=True, interval=0)
