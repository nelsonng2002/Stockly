import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from functions import stock_price_history, stock_price_history_line, calculate_stock_price_change, create_basic_stock_stats, search_company

pd.options.display.float_format = '{:.2f}'.format
st.title('Stockly')
st.markdown('''Welcome to Stockly! This application provides tools to analyse stocks and financial data. To get started, enter a stock symbol. Use the sidebar to navigate through the different pages.  
            **How to interact with charts**    
            - *Chart Frames*: To view a certain frame of the chart, click and drag your cursor over the chart. This is useful if you want to view data within certain dates. Double click on the chart to reset.  
            - *Legend*: Click on the legend items to hide or show data on the chart.
            ''')

stock_price_container = st.container()
st.session_state.symbol = stock_price_container.text_input('Enter a stock symbol:', st.session_state.get('symbol', 'AAPL'))
symbol = st.session_state.symbol
try:
    stats = create_basic_stock_stats(symbol)
    current_price = stats['Current Price']
    open_price = stats['Open']
    percent_change = ((current_price - open_price) / open_price) * 100
    stock_price_container.metric('Current Price', f"{stats['Current Price']}", f"{percent_change:.2f}%")
except TypeError as e:
    st.error(f"Invalid symbol: {symbol}. Please enter a valid stock symbol.")
    stats = None

if stats:

    selected_period = '1y'
    button_clicked = False
    one_week, one_month, three_month, six_month, one_year, two_year, five_year, ten_year, max = stock_price_container.columns(9)

    if one_week.button("1W", use_container_width=True):
        button_clicked = True
        selected_period='1wk'
    if one_month.button("1M", use_container_width=True):
        button_clicked = True
        selected_period='1mo'
    if three_month.button("3M", use_container_width=True):
        button_clicked = True
        selected_period='3mo'
    if six_month.button("6M", use_container_width=True):
        button_clicked = True
        selected_period='6mo'
    if one_year.button("1Y", use_container_width=True):
        button_clicked = True
        selected_period='1y'
    if two_year.button("2Y", use_container_width=True):
        button_clicked = True
        selected_period='2y'
    if five_year.button("5Y", use_container_width=True):
        button_clicked = True
        selected_period='5y'
    if ten_year.button("10Y", use_container_width=True):
        button_clicked = True
        selected_period='10y'
    if max.button("MAX", use_container_width=True):
        button_clicked = True
        selected_period='max'

    # Load the graph based on the selected period or default
    if button_clicked:
        stock_data = stock_price_history(symbol, selected_period)
    else:
        # Default to 1-year graph if no button is clicked
        stock_data = stock_price_history(symbol, '1y')

    stock_price_line = stock_price_history_line(symbol, stock_data)
    stock_price_container.plotly_chart(stock_price_line)
    stock_price_change = calculate_stock_price_change(stock_data)
    if stock_price_change < 0:
        stock_price_container.markdown(f"Change: <span style='color:red'>**{stock_price_change}%**</span>", unsafe_allow_html=True)
    else:
        stock_price_container.markdown(f"Change: <span style='color:green'>**+{stock_price_change}%**</span>", unsafe_allow_html=True)

    # Basic Stock Statistics

    basic_stock_stats_container = st.container()
    basic_stock_stats_container.markdown(f"***Currency: {stats['Currency']}***")
    col1, col2, col3, col4 = basic_stock_stats_container.columns(4)
    col1.markdown(f"""**Previous Close**: {stats["Previous Close"]}  
    **Open**: {stats['Open']}  
    **Day Low**: {stats['Day Low']}  
    **Day High**: {stats['Day High']}  
    **Market Cap**: {stats['Market Cap']}  
    **Volume**: {stats['Volume']}    
    **52 Week Low**: {stats['52 Week Low']}  
    **52 Week High**: {stats['52 Week High']}""")
    col2.markdown(f"""**50 Day Average**: {stats['50 Day Average']}  
    **200 Day Average**: {stats['200 Day Average']}  
    **52-Week Change**: {stats['52-Week Change']}  
    **S&P500 52-Week Change**: {stats['S&P500 52-Week Change']}%    
    **Profit Margin**: {stats['Profit Margin']}%  
    **Gross Margin**: {stats['Gross Margin']}%  
    **Operating Margin**: {stats['Operating Margin']}%  
    **EBITDA Margin**: {stats['EBITDA Margin']}%""")
    col3.markdown(f"""**PE Ratio (TTM)**: {stats['PE Ratio (TTM)']}  
    **Forward PE Ratio**: {stats['Forward PE Ratio']}   
    **EPS (TTM)**: {stats['EPS (TTM)']}  
    **Forward EPS**: {stats['Forward EPS']}    
    **Price to Book**: {stats['Price to Book']}   
    **Book Value**: {stats['Book Value']}  
    **Enterprise Value**: {stats['Enterprise Value']}  
    **EBITDA**: {stats['EBITDA']}""")
    col4.markdown(f"""**Total Cash**: {stats['Total Cash']}  
    **Total Debt**: {stats['Total Debt']}  
    **Total Cash Per Share**: {stats['Total Cash Per Share']}  
    **Current Ratio**: {stats['Current Ratio']}  
    **Return on Equity**: {stats['Return on Equity']}%  
    **Dividend Yield**: {stats['Dividend Yield']}  
    **5Y Avg Dividend Yield**: {stats['5Y Avg Dividend Yield']}  
    **Beta (5Y Monthly)**: {stats['Beta (5Y Monthly)']}  
    **Shares**: {stats['Shares']}  
    **Outstanding Shares**: {stats['Outstanding Shares']}""")