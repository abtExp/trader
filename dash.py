import streamlit as st

import time
import random
import numpy as np
import pandas as pd
import plotly.express as px

st.title('Trader Dashboard')

st.write('Here Goes The Table Of Scores : ')

chart_data = pd.DataFrame(
	np.random.randn(20, 3),
	columns=['a', 'b', 'c'])

st.line_chart(chart_data)


dynamic_area = st.empty()

def update_dashboard(values):
	df = pd.DataFrame(dict(
	r=[random.randint(0,22),
	random.randint(0,22),
	random.randint(0,22),
	random.randint(0,22),
	random.randint(0,22)],
	theta=['processing cost','mechanical properties','chemical stability',
		'thermal stability', 'device integration']))
	fig = px.line_polar(df, r='r', theta='theta', line_close=True)
	dynamic_area.write(fig)

while True:
	update_dashboard(10)
	time.sleep(0.5)