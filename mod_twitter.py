#! /usr/local/bin/python3
import sys
import os
from selenium import webdriver
import time
import os.path
import re

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as firefoxOptions
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class TwitterDriver:
	def __init__(self, BROWSER='chrome',DRIVER='',HEADLESS=True,IGNORE_CERT_ERROR=False):
		self.driver = None
		self.id = None
		self.password = None
		self.loginflag = False
		fp = None
		options = None
		if BROWSER=='firefox':
			options = firefoxOptions()
			fp = self.get_firefox_profile()
		elif BROWSER=='chrome':
			options = chromeOptions()
		
		if HEADLESS == True:
			options.set_headless(headless=True)
		
		if IGNORE_CERT_ERROR == True:
			options.add_argument('--ignore-certificate-errors')
		
		if BROWSER == 'firefox':
			self.driver = webdriver.Firefox(firefox_binary='/usr/local/bin/firefox',firefox_options=options,log_path='/dev/null',firefox_profile=fp)
		elif BROWSER == 'chrome':
			self.driver = webdriver.Chrome(DRIVER,chrome_options=options)
	
	def get_firefox_profile(self):
		fp = None
		path = os.path.expanduser('~/.mozilla/firefox')
		if os.path.isdir(path) == False:
			return None
		for f in os.listdir(path):
			if re.search('\.default$',f):
				path = path + '/' + f
				fp = webdriver.FirefoxProfile(path)
				break
		return fp
	
	def get_element_tag(self,tag_name,attribute_name,attribute):
		element = None
		tags = self.driver.find_elements_by_tag_name(tag_name)
		for t in tags:
			if t.get_attribute(attribute_name) == attribute and t.is_displayed() == True:
				element = t
				break
		return element

	def login(self,id,password):
		self.id = id
		self.password = password
		self.driver.get('https://twitter.com/?lang=ja')
		#self.driver.get('http://www.zetecr.net/')
		self.driver.implicitly_wait(5);
		
		element = self.get_element_tag('a', 'href', 'https://twitter.com/login')
		if element == None:
			return -1
		else:
			element.click()
		
		element = self.get_element_tag('input','name','session[username_or_email]')
		if element == None:
			return -2
		else:
			element.send_keys(self.id)
			
		element = self.get_element_tag('input','name','session[password]')
		if element == None:
			return -3
		else:
			element.send_keys(self.password)
		
		element = self.get_element_tag('button','type','submit')
		if element == None:
			element = self.get_element_tag('input', 'type', 'submit')
		
		if element == None:
			return -4
		else:
			element.click()

		element = self.get_element_tag('input','name','session[password]')
		if element != None:
			return -5
		else:
			self.loginflag = True

		pos = '//*[@id="promptbird-modal-prompt-dialog"]/div[2]/div/div/div/div[1]/button'
		try:
			element = self.driver.find_element_by_xpath(pos)
		except:
			element = None
		
		if element != None and element.is_enabled() == True:
			element.click()
		
		return 0
		
		
	def set_text(self, text):
		element = None
		element = self.driver.find_element_by_id('tweet-box-home-timeline')
		if element == None:
			return -6
			
		element.click()
		element.send_keys(text)
		return 0
	
	def set_image(self, path):
		element = None
		pos = '//*[@id="timeline"]/div[2]/div/form/div[3]/div[1]/span[1]/div/div/label/input'
		element = self.driver.find_element_by_xpath(pos)
		if element == None:
			return -7
		element.send_keys(path)
		return 0
		
	def tweet(self):
		element = None
		pos = '//*[@id="timeline"]/div[2]/div/form/div[3]/div[2]/button'
		wait = WebDriverWait(self.driver, 60)
		try:
			wait.until(expected_conditions.element_to_be_clickable((By.XPATH,pos)))
		except:
			return -8
		
		element = self.driver.find_element_by_xpath(pos)
		if element == None:
			return -9
		elif element.is_enabled() == False:
			return -10
		
		element.click()
		return 0
		
	def __del__(self):
		self.driver.quit()



if __name__ == '__main__':
	tw = TwitterDriver(BROWSER='firefox',HEADLESS=True,IGNORE_CERT_ERROR=False)
	res=tw.login('ztecr@ymail.com','iostreamxyz42')
	if res < 0:
		print(res)
		exit()
	
	res=tw.set_text('テスト\nツイート'+'443')
	if res < 0:
		print(res)
		exit()
	
	#res=tw.set_image('D:\\project\\what_you_want\\pic.jpg')
	res=tw.tweet()
	print(res)
	os.system('read "hitenter:"')








