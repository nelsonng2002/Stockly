import streamlit as st
from functions import yf_income_statement, yf_balance_sheet, yf_cashflow

symbol = st.session_state.get('symbol', 'AAPL')
st.title(f'{symbol} Financial Statements')

selected_timeframe = st.selectbox('Select yearly or quarterly financial information', options=['Yearly', 'Quarterly'])

tab1, tab2, tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
with tab1:
    income_statement_df = yf_income_statement(symbol, selected_timeframe)
    st.table(income_statement_df)
with tab2:
    balance_sheet_df = yf_balance_sheet(symbol, selected_timeframe)
    st.table(balance_sheet_df)
with tab3:
    cashflow_df = yf_cashflow(symbol, selected_timeframe)
    st.table(cashflow_df)