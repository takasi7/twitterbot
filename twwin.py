#! /usr/local/bin/python3
import sys
import os
import time
import os.path
import re
from selenium import webdriver

import mod_twitter
from mod_twitter import fmtext


ID='twitter'
PASSWORD='twitte password'
TWEET='default'
IMAGE=''

if len(sys.argv) >= 3:
	ID = sys.argv[1]
	PASSWORD = sys.argv[2]
	
if len(sys.argv) >= 4:
	TWEET=fmtext(sys.argv[3])
	
if len(sys.argv) >= 5:
	IMAGE = sys.argv[4]
		
options = mod_twitter.firefoxOptions()
options.set_headless(headless=True)
driver = webdriver.Firefox(firefox_options=options)

#options = mod_twitter.chromeOptions()
#options.add_argument('--ignore-certificate-errors')
#driver = webdriver.Chrome(chrome_options=options)

tw = mod_twitter.TwitterDriver(driver)

res=tw.login(ID,PASSWORD)
if res < 0:
	print(res)
	exit()

res=tw.set_text(TWEET)
if res < 0:
	print(res)
	exit()

if len(IMAGE) and os.path.exists(IMAGE):
	res=tw.set_image(IMAGE)
	if res < 0:
		print(res)
		exit()

res=tw.tweet()
print('tweet ',end='')
print(res)

del tw



