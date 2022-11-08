import pandas as pd
import streamlit as st
import yfinance as yf


st.write("""
# Simple Stock Price App

Shown are the stock **closing price** and volume of Google


""")

tickersymbol = 'AAPL'

tickerdata = yf.Ticker(tickersymbol)

tickerDf = tickerdata.history(period='Id', start='2010-5-31', end='2022-5-31')

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)