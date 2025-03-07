import streamlit as st
from functions import get_key_metrics, get_key_metrics_ttm, get_financial_ratios, get_financial_ratios_ttm, get_pe_ratio, plot_pe_ratio, get_peg_ratio, plot_peg_ratio, \
                    get_pb_ratio, plot_pb_ratio, \
                    get_ps_ratio, plot_ps_ratio, get_ev_ebitda, plot_ev_ebitda, \
                    get_price_to_fcf, plot_price_to_fcf, get_price_to_ocf, plot_price_to_ocf, \
                    get_ev_to_sales, plot_ev_to_sales, get_ev_to_ocf, plot_ev_to_ocf, \
                    get_ev_to_fcf, plot_ev_to_fcf, get_dividend_yield, plot_dividend_yield, \
                    plot_pe_ratios_comparison, plot_peg_ratio_comparison, plot_pb_ratio_comparison, \
                    plot_ps_ratio_comparison, plot_ev_ebitda_comparison, plot_price_to_fcf_comparison, \
                    plot_price_to_ocf_comparison, plot_ev_to_sales_comparison, plot_ev_to_ocf_comparison, \
                    plot_ev_to_fcf_comparison, plot_dividend_yield_comparison
                    

symbol = st.session_state.get('symbol', 'AAPL')

st.title('Valuation Metrics')
st.markdown('''Analyse the valuation metrics of a company by looking at key financial ratios.  
            - **Compare with Competitors**: Compare the valuation trends of a different companies over time. 
            ''')
symbol_input = st.text_input('Enter stock symbol', value=symbol)
if symbol_input:
    st.session_state['symbol'] = symbol_input
    symbol = symbol_input

selected_period = st.selectbox('Select annual or quarter financial data', options=['Annual', 'Quarter'])
period = selected_period.lower()

key_metrics = get_key_metrics(symbol, period)
key_metrics_ttm = get_key_metrics_ttm(symbol)
financial_ratios = get_financial_ratios(symbol, period)
financial_ratios_ttm = get_financial_ratios_ttm(symbol)

# Price to Earnings Ratio (PE Ratio)
pe_ratio_list = get_pe_ratio(key_metrics, key_metrics_ttm)
pe_ratio_plot = plot_pe_ratio(symbol, pe_ratio_list)

pe_ratio_container = st.container()
pe_ratio_expander = pe_ratio_container.expander('PE Ratio', expanded=True)
pe_ratio_expander.plotly_chart(pe_ratio_plot)
# pe_ratios_comparison_expander = pe_ratio_expander.expander('PE Ratios Comparison', expanded=True)
# pe_ratio_symbols = pe_ratios_comparison_expander.text_input('Enter a list of up to 4 stock symbols separated by commas and hit ENTER', value='AAPL,MSFT,GOOGL,AMZN')
# symbol_list = []
# pe_ratios_comparison_list = []
# for symbol in pe_ratio_symbols.split(','):
#     symbol_list.append(symbol)
#     symbol_pe_ratio_list = get_pe_ratio(get_key_metrics(symbol, period), get_key_metrics_ttm(symbol))
#     pe_ratios_comparison_list.append(symbol_pe_ratio_list)
# pe_ratios_comparison_plot = plot_pe_ratios_comparison(symbol_list, pe_ratios_comparison_list)
# pe_ratios_comparison_expander.plotly_chart(pe_ratios_comparison_plot)

# Price to Earnings to Growth Ratio (PEG Ratio)

peg_ratio_list = get_peg_ratio(financial_ratios, financial_ratios_ttm)
peg_ratio_plot = plot_peg_ratio(symbol, peg_ratio_list)

peg_ratio_container = st.container()
peg_ratio_expander = peg_ratio_container.expander('PEG Ratio', expanded=True)
peg_ratio_expander.plotly_chart(peg_ratio_plot)

# Price to Book Ratio (PB Ratio)
pb_ratio_list = get_pb_ratio(key_metrics, key_metrics_ttm)
pb_ratio_plot = plot_pb_ratio(symbol, pb_ratio_list)

pb_ratio_container = st.container()
pb_ratio_expander = pb_ratio_container.expander('PB Ratio', expanded=True)
pb_ratio_expander.plotly_chart(pb_ratio_plot)

# Price to Sales Ratio (PS Ratio)
ps_ratio_list = get_ps_ratio(key_metrics, key_metrics_ttm)
ps_ratio_plot = plot_ps_ratio(symbol, ps_ratio_list)

ps_ratio_container = st.container()
ps_ratio_expander = ps_ratio_container.expander('PS Ratio', expanded=True)
ps_ratio_expander.plotly_chart(ps_ratio_plot)

# Price to Free Cash Flow

price_to_fcf_list = get_price_to_fcf(key_metrics, key_metrics_ttm)
price_to_fcf_plot = plot_price_to_fcf(symbol, price_to_fcf_list)

price_to_fcf_container = st.container()
price_to_fcf_expander = price_to_fcf_container.expander('Price to Free Cash Flow', expanded=False)
price_to_fcf_expander.plotly_chart(price_to_fcf_plot)

# Price to Operating Cash Flow

price_to_ocf_list = get_price_to_ocf(key_metrics, key_metrics_ttm)
price_to_ocf_plot = plot_price_to_ocf(symbol, price_to_ocf_list)

price_to_ocf_container = st.container()
price_to_ocf_expander = price_to_ocf_container.expander('Price to Operating Cash Flow', expanded=False)
price_to_ocf_expander.plotly_chart(price_to_ocf_plot)

# Enterprise Value to EBITDA
ev_ebitda_list = get_ev_ebitda(key_metrics, key_metrics_ttm)
ev_ebitda_plot = plot_ev_ebitda(symbol, ev_ebitda_list)

ev_ebitda_container = st.container()
ev_ebitda_expander = ev_ebitda_container.expander('EV to EBITDA', expanded=False)
ev_ebitda_expander.plotly_chart(ev_ebitda_plot)

# Enterprise Value to Sales

ev_to_sales_list = get_ev_to_sales(key_metrics, key_metrics_ttm)
ev_to_sales_plot = plot_ev_to_sales(symbol, ev_to_sales_list)

ev_to_sales_container = st.container()
ev_to_sales_expander = ev_to_sales_container.expander('EV to Sales', expanded=False)
ev_to_sales_expander.plotly_chart(ev_to_sales_plot)

# Enterprise Value to Operating Cash Flow

ev_to_ocf_list = get_ev_to_ocf(key_metrics, key_metrics_ttm)
ev_to_ocf_plot = plot_ev_to_ocf(symbol, ev_to_ocf_list)

ev_to_ocf_container = st.container()
ev_to_ocf_expander = ev_to_ocf_container.expander('EV to Operating Cash Flow', expanded=False)
ev_to_ocf_expander.plotly_chart(ev_to_ocf_plot)

# Enterprise Value to Free Cash Flow

ev_to_fcf_list = get_ev_to_fcf(key_metrics, key_metrics_ttm)
ev_to_fcf_plot = plot_ev_to_fcf(symbol, ev_to_fcf_list)

ev_to_fcf_container = st.container()
ev_to_fcf_expander = ev_to_fcf_container.expander('EV to Free Cash Flow', expanded=False)
ev_to_fcf_expander.plotly_chart(ev_to_fcf_plot)

# Dividend Yield

dividend_yield_list = get_dividend_yield(key_metrics, key_metrics_ttm)
dividend_yield_plot = plot_dividend_yield(symbol, dividend_yield_list)

dividend_yield_container = st.container()
dividend_yield_expander = dividend_yield_container.expander('Dividend Yield', expanded=False)
dividend_yield_expander.plotly_chart(dividend_yield_plot)

# Compare Metrics with Competitors
comparison_container = st.container()
comparison_container.header('Compare Metrics with Competitors')
metric_to_compare = comparison_container.selectbox('Select a metric to compare with competitors', options=['PE Ratio', 'PEG Ratio', 'PB Ratio', 'PS Ratio', 'Price to FCF', 'Price to OCF', 'EV to EBITDA', 'EV to Sales', 'EV to OCF', 'EV to FCF', 'Dividend Yield'])
comparison_symbols = comparison_container.text_input('Enter a list of up to 4 stock symbols separated by commas and hit ENTER', value='AAPL,MSFT,GOOGL,AMZN')
symbol_list = []
comparison_metric_list = []
for symbol in comparison_symbols.split(','):
    symbol_list.append(symbol)
    if metric_to_compare == 'PE Ratio':
        symbol_metric_list = get_pe_ratio(get_key_metrics(symbol, period), get_key_metrics_ttm(symbol))
    elif metric_to_compare == 'PEG Ratio':
        symbol_metric_list = get_peg_ratio(get_financial_ratios(symbol, period), get_financial_ratios_ttm(symbol))
    elif metric_to_compare == 'PB Ratio':
        symbol_metric_list = get_pb_ratio(get_key_metrics(symbol, period), get_key_metrics_ttm(symbol))
    elif metric_to_compare == 'PS Ratio':
        symbol_metric_list = get_ps_ratio(get_key_metrics(symbol, period), get_key_metrics_ttm(symbol))
    elif metric_to_compare == 'Price to FCF':
        symbol_metric_list = get_price_to_fcf(get_key_metrics(symbol, period), get_key_metrics_ttm(symbol))
    elif metric_to_compare == 'Price to OCF':
        symbol_metric_list = get_price_to_ocf(get_key_metrics(symbol, period), get_key_metrics_ttm(symbol))
    elif metric_to_compare == 'EV to EBITDA':
        symbol_metric_list = get_ev_ebitda(get_key_metrics(symbol, period), get_key_metrics_ttm(symbol))
    elif metric_to_compare == 'EV to Sales':
        symbol_metric_list = get_ev_to_sales(get_key_metrics(symbol, period), get_key_metrics_ttm(symbol))
    elif metric_to_compare == 'EV to OCF':
        symbol_metric_list = get_ev_to_ocf(get_key_metrics(symbol, period), get_key_metrics_ttm(symbol))
    elif metric_to_compare == 'EV to FCF':
        symbol_metric_list = get_ev_to_fcf(get_key_metrics(symbol, period), get_key_metrics_ttm(symbol))
    elif metric_to_compare == 'Dividend Yield':
        symbol_metric_list = get_dividend_yield(get_key_metrics(symbol, period), get_key_metrics_ttm(symbol))
    comparison_metric_list.append(symbol_metric_list)
if metric_to_compare == 'PE Ratio':
    comparison_plot = plot_pe_ratios_comparison(symbol_list, comparison_metric_list)
elif metric_to_compare == 'PEG Ratio':
    comparison_plot = plot_peg_ratio_comparison(symbol_list, comparison_metric_list)
elif metric_to_compare == 'PB Ratio':
    comparison_plot = plot_pb_ratio_comparison(symbol_list, comparison_metric_list)
elif metric_to_compare == 'PS Ratio':
    comparison_plot = plot_ps_ratio_comparison(symbol_list, comparison_metric_list)
elif metric_to_compare == 'Price to FCF':
    comparison_plot = plot_price_to_fcf_comparison(symbol_list, comparison_metric_list)
elif metric_to_compare == 'Price to OCF':
    comparison_plot = plot_price_to_ocf_comparison(symbol_list, comparison_metric_list)
elif metric_to_compare == 'EV to EBITDA':
    comparison_plot = plot_ev_ebitda_comparison(symbol_list, comparison_metric_list)
elif metric_to_compare == 'EV to Sales':    
    comparison_plot = plot_ev_to_sales_comparison(symbol_list, comparison_metric_list)
elif metric_to_compare == 'EV to OCF':
    comparison_plot = plot_ev_to_ocf_comparison(symbol_list, comparison_metric_list)
elif metric_to_compare == 'EV to FCF':
    comparison_plot = plot_ev_to_fcf_comparison(symbol_list, comparison_metric_list)
elif metric_to_compare == 'Dividend Yield':
    comparison_plot = plot_dividend_yield_comparison(symbol_list, comparison_metric_list)
comparison_container.plotly_chart(comparison_plot)