import telebot;
import requests
import codecs
import json

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

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
	if message.text == "/start":
		bot.send_message(message.from_user.id, 'В наличии есть 3 категории:1 - Противовирусные 2 - Противовоспалительные 3 - Препараты первой помощи Напишите номер нужной категории')


	elif message.text == "1":
		bot.send_message(message.from_user.id, "Вот что есть в наличии: ")
		category = "cat1"
		bot.send_message(message.from_user.id, getCategoryFunc(category))	
	elif message.text == "2":
		category = "cat2"
		bot.send_message(message.from_user.id, getCategoryFunc(category))
	elif message.text == "3":
		category = "cat3"
		bot.send_message(message.from_user.id, getCategoryFunc(category))
	else: 
		bot.send_message(message.from_user.id, "Я не  понимаю 😢")

bot.polling(none_stop=True, interval=0)



