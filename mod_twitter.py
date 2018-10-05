#! /usr/local/bin/python3

import os
import re

from selenium import webdriver
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
	def __init__(self, driver):
		self.driver = driver
		self.id = None
		self.password = None
		self.timelines = {}
	
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
		#self.driver.get('https://twitter.com/?lang=ja')
		self.driver.get('https://twitter.com/login')
		self.driver.implicitly_wait(5);
		
		#element = self.get_element_tag('a', 'href', 'https://twitter.com/login')		
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
		wait = WebDriverWait(self.driver, 10)
		element = None
		id = 'tweet-box-home-timeline'
		try:
			wait.until(expected_conditions.presence_of_element_located((By.ID,id)))
		except:
			return -6
		
		try:
			element = self.driver.find_element_by_id(id)
		except:
			return -16
		
		#element.click()
		element.send_keys(text)
		return 0
	
	def set_image(self, path):
		wait = WebDriverWait(self.driver, 10)
		element = None
		pos = '//*[@id="timeline"]/div[2]/div/form/div[3]/div[1]/span[1]/div/div/label/input'
		
		try:
			wait.until(expected_conditions.presence_of_element_located((By.XPATH,pos)))
		except:
			return -7
		
		try:
			element = self.driver.find_element_by_xpath(pos)
		except:
			return -17
		
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
		
		try:
			element = self.driver.find_element_by_xpath(pos)
		except:
			return -9
		
		if element.is_enabled() == False:
			return -10
		
		element.click()

		try:
			wait.until(expected_conditions.invisibility_of_element_located((By.XPATH,pos)))
		except:
			return 1
		
		return 0
		
	def get_timeline(self):
		elements = self.driver.find_elements_by_tag_name('li')
		for e in elements:
			idc = e.get_attribute('id')
			if re.match(r'stream-item-tweet-\d+',idc):
				item = {'id':idc}
				try:
					css = '#'+idc+' .js-tweet-text-container'
					element = self.driver.find_element_by_css_selector(css)
					item['text'] = element.text
					
					css = '#'+idc+' a.account-group'
					element = self.driver.find_element_by_css_selector(css)
					user = element.get_attribute('href')
					user = user.replace('https://twitter.com/','')
					item['user'] = user
				except:
					pass
				self.timelines[idc] = item
	

	def __del__(self):
		self.driver.quit()



def fmtext(text):
	text = text.replace('\\n','\n')
	return text
	

def get_firefox_profile():
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


if __name__ == '__main__':
	s='''
	dirver=webdriver.Firefox()
	tw=TwitterDriver(driver)
	r = tw.login('id','password')
	r = tw.set_text('some string')
	r = tw.set_image('image path')
	r = tw.tweet()
	del tw
	'''
	print(s)


