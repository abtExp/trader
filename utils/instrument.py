from utils.functions import *
from kiteconnect import KiteTicker


class INSTRUMENT:
    def __init__(self, instrument, api_key, access_token):
        self.strike = instrument[0]
        self.instrument_token = instrument[1]
        self.ticker = KiteTicker(api_key, access_token)
        self.entries = []
        self.period = 14
        self.ma_period = 20
        self.rsi = None
        self.vw = None
        self.vol = None
        self.oi = None
        self.set_callbacks()
        self.ticker.connect()

    def connect_callback(self):
        def on_connect(ws, response):
            ws.subscribe([self.instrument_token])
            ws.set_mode(ws.MODE_FULL, [self.instrument_token])

        return on_connect

    def update_entries(self):
        if len(self.entries) >= self.period:
            self.entries = self.entries[1:]

    def tick_callback(self):
        def on_tick(ws, ticks):
            print(ticks)
            self.entries.append(ticks)
            self.calc_indicators()
            self.update_entries()

        return on_tick

    def calc_indicators(self):
        print(self.entries)
        if len(self.entries) >= self.period:
            # Perform Calculations
            self.vol, self.rsi, self.vw, self.oi = calc_vals(self.entries)

    def close_callback(self):
        def on_close(ws, code, reason):
            ws.close()
            # Perform Some Other Stuff
        return on_close

    def set_callbacks(self):
        self.ticker.on_connect = self.connect_callback()
        self.ticker.on_ticks = self.tick_callback()
        self.ticker.on_close = self.close_callback()