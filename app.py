import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title='Stockly', page_icon=':bar_chart:', layout='wide')

pages = {
    "Stock Data": [
        st.Page("stock.py", title="Stock"),
    ],
    "Fundamental Analysis": [
        st.Page("financial_statements.py", title="Financial Statements"),
        st.Page("profitability.py", title="Profitability Metrics"),
        st.Page("valuation.py", title="Valuation Metrics"),
        st.Page("financial_health.py", title="Financial Health Metrics"),
    ],
}

pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()

# symbol = st.text_input('Enter a stock symbol:', 'AAPL')

# price_container = st.container()

