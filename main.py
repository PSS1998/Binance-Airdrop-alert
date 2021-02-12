import urllib.request
import time
import json

import schedule
import bs4 as bs
import telegram



TOKEN='Insert your telgram token here'


def send_notification(text):
	global bot
	source = urllib.request.urlopen("https://api.telegram.org/bot"+TOKEN+"/getUpdates").read()
	messages = json.loads(source.decode('utf-8'))
	chat_ids = set()
	chat_ids_file = open('chat-ids.txt', 'r') 
	Lines = chat_ids_file.readlines()
	for line in Lines:
		if line != '\n':
			chat_ids.add(int(line))
	for message in messages['result']:
		chat_ids.add(message['message']['from']['id'])
	with open('chat-ids.txt', 'w') as f:
		for item in chat_ids:
			f.write("%s\n" % item)
	for chat_id in chat_ids:
		bot.send_message(chat_id=chat_id, text=text)

def get_news():	
	global last_news
	try:
		source = urllib.request.urlopen('https://www.binance.com/en/support/announcement/c-49?navId=49').read()
	except:
		print("connection to binance failed")
		return
	soup = bs.BeautifulSoup(source,'lxml')

	for item in list(soup.find_all("a", {"class": "css-1ej4hfo"})):
		print(last_news)
		news = item.text
		if last_news != "":
			if news == last_news:
				break
		if "Airdrop" in news:
			if last_news == "":
				last_news = news
				send_notification(news)	
				break
			last_news = news
			send_notification(news)
		if "Hard Fork" in news:
			if last_news == "":
				last_news = news
				send_notification(news)	
				break
			last_news = news
			send_notification(news)


last_news = ""

bot = telegram.Bot(token=TOKEN)

get_news()

schedule.every(10).minutes.do(get_news)

while True:
	schedule.run_pending()
	time.sleep(1)


