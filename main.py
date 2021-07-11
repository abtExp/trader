# Imports
import sys
import json
import requests
import datetime
import configparser
from utils import *
from selenium import webdriver
from streamlit import cli as stcli
from selenium.webdriver.chrome.options import Options
from kiteconnect import KiteConnect, KiteTicker
from webdriver_manager.chrome import ChromeDriverManager


# GET INFO ABOUT : VWAP, RSI(MA), VOLUME(MA), OPENINTEREST(MA)

class TRADER:
	def __init__(self):
		config = configparser.RawConfigParser()
		config.read('config.cfg')
		self.creds = dict(config.items('creds'))
		self.instruments = dict(config.items('instruments'))
		self.endpoints = dict(config.items('api_endpoints'))
		self.app_vars = dict(config.items('app_vars'))
		self.app = KiteConnect(self.creds['api_key'])
		self.login_url = self.app.login_url()
		self.goto_browser()
		self.access_token = self.app.generate_session(self.request_token, api_secret=self.creds['secret_key'])['access_token']
		self.app.set_access_token(self.access_token)
		self.ticker = TICKER(self.instruments, self.creds['api_key'], self.access_token)
		self.ticker.connect_indices()

	def launch_app(self, driver):
		sys.argv = ["streamlit", "run", self.app_vars['app_file'], '--server.port', self.app_vars['port']]
		stcli.main()
		driver.get(self.endpoints['app_endpoint']+self.app_vars['port'])

	def goto_browser(self):
		try:
			chrome_options = Options()
			chrome_options.add_experimental_option("detach", True)
			driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
			driver.get(self.login_url)
			url = ''
			while 'request_token' not in url:
				url = driver.current_url
			# self.launch_app(driver)
			driver.quit()
			self.request_token = url[url.index('request_token')+len('request_token')+1:url.index('&action')]
		except Exception as e:
			print('Exception Occured. : {}'.format(e))


if __name__ == '__main__':
	trader = TRADER()