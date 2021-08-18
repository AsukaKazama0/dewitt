from selenium import webdriver
import time
import os
from pathlib import Path
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from telegram.utils.request import Request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests
import re
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
# CHROMEDRIVER_PATH = './chromedriver'
def get_list(update: Update, context: CallbackContext):
	update.message.reply_text('Getting File may take more than 10 minutes')
	
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--start-maximized")
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument("--no-sandbox")
	prefs = {"profile.managed_default_content_settings.css": 2}
	chrome_options.add_experimental_option("prefs", prefs)
	driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=chrome_options)
	driver.set_window_size(1920,1080)
	driver.get("https://coinsniper.net/");
	delay=20
	WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'promoted')))
	script = 'promote = document.querySelector(".listings.promoted");promote.remove(); var last = $("table").find("tbody tr:eq(1)").attr("data-listingid");return last;'

	meta = int(driver.execute_script(script))
	for i in range(2,meta):
		driver.get("https://coinsniper.net/coin/{}".format(i));
		script ="""promote = $('a:contains("Join Telegram")').attr("href");return promote;"""
		link = driver.execute_script(script)
		script ="""promote = $('h1');promote.find("span").remove();return promote.text();"""
		name = driver.execute_script(script)
		name = str(name).replace("\n","")
		txt = name.split(' ')
		txt = list(filter(None, txt))
		txt = ' '.join(txt)
		txt = "{} {} : {}\n".format(i,txt,link)
		my_file = Path("readme.txt")
		logfile = open(my_file, 'r')
		loglist = logfile.readlines()


		logfile.close()
		found = False
		for line in loglist:
   			if txt in line:
   				found = True
        		
		
		if my_file.is_file():
			if not found:
				with open('readme.txt', 'a') as file:
					file.write(txt)
					file.close()
    			
		else:
			os.mknod("readme.txt")
	driver.quit()
	chat_id = update.message.chat_id
	# r =  requests.post('https://api.anonymousfiles.io', files={'file': open('./readme.txt', 'rb')})
	# chat_id = update.message.reply_document(document="readme.txt")
	t_bot.send_document(chat_id=chat_id,document=open("readme.txt", 'rb'))

req = Request(connect_timeout=0.5)
t_bot = Bot(
      request=req,
      token='1949733785:AAH4BLvFM_RjAZoheO84MGhxRHT4Q4KwZvc',
)
updater = Updater(bot=t_bot, use_context=True)

dp = updater.dispatcher
dp.add_handler(CommandHandler('get',get_list))
updater.start_polling()
updater.idle()
    
