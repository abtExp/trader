import requests
import pandas as pd
from .instrument import INSTRUMENT
from kiteconnect import KiteTicker

class TICKER:
	def __init__(self, instruments, api_key, access_token):
		self.api_key = api_key
		self.access_token = access_token
		self.instrument_ticker = KiteTicker(api_key, access_token)
		self.instruments = [int(v) for v in instruments.values()]
		self.active_instruments = []
		self.set_instrument_ticker_callbacks()
		self.instrument_ticker.connect()
		self.show_scores()

	def connect_indices(self):
		def on_connect(ws, response):
			ws.subscribe(self.instruments)
			ws.set_mode(ws.MODE_FULL, self.instruments)
		return on_connect

	def print_instrument_ticks(self, ticks):
		print(ticks)
		curr_prices = [int(float(i['last_price'])) for i in ticks]
		self.subscribe_levels(curr_prices)

	def subscribe_levels(self, curr_prices):
		rounded_currents = [round(i, -2) for i in curr_prices]
		range_vals = [[i for i in range(j-1000, j+1000, 100)] for j in rounded_currents]
		instrument_ids = self.get_instrument_ids(range_vals)
		subscribed_ids = [i.instrument_token for i in self.active_instruments]
		for instrument in instrument_ids:
			if instrument[1] not in subscribed_ids:
				self.active_instruments.append(INSTRUMENT(instrument, self.api_key, self.access_token))

	def get_instrument_ids(self, range_vals):
		try:
			instrument_list = pd.read_csv('instrument_list.csv')
		except Exception as e:
			self.get_instrument_list()
			instrument_list = pd.read_csv('instrument_list.csv')

		instruments = instrument_list[instrument_list['name'] == 'BANKNIFTY']
		instruments = instruments[instruments['strike'].isin(range_vals[0])]
		instrument_strikes = instruments['strike'].tolist()
		instrument_tokens = instruments['instrument_token'].tolist()

		instruments_list = list(zip(instrument_strikes, instrument_tokens))

		return instruments_list

	# Show ROVV Scores For Each Instrument
	def show_scores(self):
		for instrument in self.active_instruments[5:-5]:
			print(instrument.strike)

	def get_instrument_list(self):
		auth_str = 'token {}:{}'.format(self.api_key, self.access_token)
		headers = {
			'X-Kite-Version' : '3',
			'Authorization' : auth_str
		}

		try:
			res = requests.get(
					self.endpoints['instrument_endpoint'],
					headers=headers
				)

			with open('instrument_list.csv', 'w') as f:
				f.write(res.text)

		except Exception as e:
			print(f'Exception Occured : {e}')

	def instrument_ticks(self):
		def on_ticks(ws, ticks):
			self.print_instrument_ticks(ticks)
		return on_ticks

	def instrument_ticker_close(self):
		def on_close(ws, code, reason):
			self.print_instrument_ticks(reason)
			ws.close()
		return on_close


	def set_instrument_ticker_callbacks(self):
		self.instrument_ticker.on_connect = self.connect_indices()
		self.instrument_ticker.on_ticks = self.instrument_ticks()
		self.instrument_ticker.on_close = self.instrument_ticker_close()