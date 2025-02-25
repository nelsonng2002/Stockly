import streamlit as st
from functions import get_financial_ratios, get_financial_ratios_ttm, get_key_metrics, get_key_metrics_ttm, \
                    get_debt_to_equity_ratio, plot_debt_to_equity_ratio, get_total_debt_to_cap, plot_total_debt_to_cap, \
                    get_current_ratio, get_quick_ratio, plot_current_quick_ratio, plot_current_ratio, get_working_capital, \
                    plot_working_capital, get_capex_operating_cashflow, plot_capex_operating_cashflow, get_capex_per_share, \
                    plot_capex_per_share, get_employee_count, plot_employee_count

st.title('Financial Health')
st.markdown('''Analyse the financial health of a company by looking at key financial ratios.''')

symbol = st.session_state.get('symbol', 'AAPL')
symbol_input = st.text_input('Enter stock symbol', value=symbol)
if symbol_input:
    st.session_state['symbol'] = symbol_input
    symbol = symbol_input

selected_period = st.selectbox('Select annual or quarter financial data', options=['Annual', 'Quarter'])
period = selected_period.lower()

financial_ratios = get_financial_ratios(symbol, period)
financial_ratios_ttm = get_financial_ratios_ttm(symbol)
key_metrics = get_key_metrics(symbol, period)
key_metrics_ttm = get_key_metrics_ttm(symbol)

# Current + Quick Ratio
current_ratio_container = st.container()
current_ratio = get_current_ratio(financial_ratios, financial_ratios_ttm)
current_ratio_plot = plot_current_ratio(symbol, current_ratio)
current_ratio_container.plotly_chart(current_ratio_plot)
quick_ratio = get_quick_ratio(financial_ratios, financial_ratios_ttm)
current_quick_ratio_plot = plot_current_quick_ratio(symbol, current_ratio, quick_ratio)
current_ratio_container.plotly_chart(current_quick_ratio_plot)

# Debt to Equity Ratio
debt_to_equity_container = st.container()
debt_to_equity_ratio = get_debt_to_equity_ratio(financial_ratios, financial_ratios_ttm)
debt_to_equity_ratio_plot = plot_debt_to_equity_ratio(symbol, debt_to_equity_ratio)
debt_to_equity_container.plotly_chart(debt_to_equity_ratio_plot)

# Total Debt to Capital
total_debt_to_cap_container = st.container()
total_debt_to_cap = get_total_debt_to_cap(financial_ratios, financial_ratios_ttm)
total_debt_to_cap_plot = plot_total_debt_to_cap(symbol, total_debt_to_cap)
total_debt_to_cap_container.plotly_chart(total_debt_to_cap_plot)

# Working Capital
working_capital_container = st.container()
working_capital = get_working_capital(key_metrics, key_metrics_ttm)
working_capital_plot = plot_working_capital(symbol, working_capital)
working_capital_container.plotly_chart(working_capital_plot)

# Capital Expenditure to Operating Cash Flow
capex_operating_cashflow_container = st.container()
capex_operating_cashflow = get_capex_operating_cashflow(key_metrics, key_metrics_ttm)
capex_operating_cashflow_plot = plot_capex_operating_cashflow(symbol, capex_operating_cashflow)
capex_operating_cashflow_container.plotly_chart(capex_operating_cashflow_plot)

# Capital Expenditure per Share
capex_per_share_container = st.container()
capex_per_share = get_capex_per_share(key_metrics, key_metrics_ttm)
capex_per_share_plot = plot_capex_per_share(symbol, capex_per_share)
capex_per_share_container.plotly_chart(capex_per_share_plot)

# Employee Growth
employee_growth_container = st.container()
employee_count = get_employee_count(symbol)
employee_count_plot = plot_employee_count(symbol, employee_count)
employee_growth_container.plotly_chart(employee_count_plot)