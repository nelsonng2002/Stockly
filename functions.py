import fmpsdk
import yfinance as yf
import os
import requests
import plotly.graph_objects as go
import pandas as pd

api_key = os.environ.get('API_KEY')

def search_company(query):
    url = f"https://financialmodelingprep.com/api/v3/search?query={query}&exchange=NASDAQ&apikey={api_key}"
    response = requests.get(url)
    
    try:
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"An error occurred: {err}")
        return []
    
def get_stock_list():
    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}"
    response = requests.get(url)
    try:
        response.raise_for_status()
        stock_list = response.json()
        symbol_list = []
        for i in range(0, len(stock_list)):
            symbol_list.append(stock_list[i]['symbol'])
        return symbol_list
    except Exception as err:
        print(f"An error occurred: {err}")
        return []

def stock_price_history(symbol, period='1y'):
    stock = yf.Ticker(symbol)
    stock_prices = stock.history(period=period)
    return stock_prices

def calculate_stock_price_change(stock_prices):
    percent_change = round(((stock_prices['Close'][-1] - stock_prices['Close'][0]) / stock_prices['Close'][0] * 100), 2)
    return percent_change

def stock_price_history_line(symbol, stock_prices):
    fig = go.Figure(data=[
        go.Scatter(x=stock_prices.index, y=stock_prices['Close'])
    ])
    
    fig.update_traces(
        fill='tozeroy'
    )

    fig.update_layout(
        title=f'{symbol} Stock Price Over Time',
        xaxis_title='Date',
        yaxis_title='Stock Price'
    )

    return fig

def create_basic_stock_stats(symbol):
    ticker = yf.Ticker(symbol)
    dict = ticker.get_info()
    stats = {
        'Currency': dict.get('currency', 'n/a'),
        'Current Price': round(float(dict.get('currentPrice', 'nan')), 2) if 'currentPrice' in dict else 'n/a',
        'Previous Close': round(float(dict.get('previousClose', 'nan')), 2) if 'previousClose' in dict else 'n/a',
        'Open': round(float(dict.get('open', 'nan')), 2) if 'open' in dict else 'n/a',
        'Day Low': round(float(dict.get('dayLow', 'nan')), 2) if 'dayLow' in dict else 'n/a',
        'Day High': round(float(dict.get('dayHigh', 'nan')), 2) if 'dayHigh' in dict else 'n/a',
        'Volume': round(float(dict.get('volume', 'nan'))) if 'volume' in dict else 'n/a',
        'Market Cap': round(float(dict.get('marketCap', 'nan'))) if 'marketCap' in dict else 'n/a',
        '52 Week High': round(float(dict.get('fiftyTwoWeekHigh', 'nan')), 2) if 'fiftyTwoWeekHigh' in dict else 'n/a',
        '52 Week Low': round(float(dict.get('fiftyTwoWeekLow', 'nan')), 2) if 'fiftyTwoWeekLow' in dict else 'n/a',
        'Profit Margin': round(float(dict.get('profitMargins', 'nan')) * 100, 2) if 'profitMargins' in dict else 'n/a',
        'PE Ratio (TTM)': round(float(dict.get('trailingPE', 'nan')), 2) if 'trailingPE' in dict else 'n/a',
        'Forward PE Ratio': round(float(dict.get('forwardPE', 'nan')), 2) if 'forwardPE' in dict else 'n/a',
        'EPS (TTM)': round(float(dict.get('trailingEps', 'nan')), 2) if 'trailingEps' in dict else 'n/a',
        'Forward EPS': round(float(dict.get('forwardEps', 'nan')), 2) if 'forwardEps' in dict else 'n/a',
        'Price to Book': round(float(dict.get('priceToBook', 'nan')), 2) if 'priceToBook' in dict else 'n/a',
        'Dividend Yield': float(dict.get('dividendYield', 'nan')) if 'dividendYield' in dict else 'n/a',
        'Beta (5Y Monthly)': round(float(dict.get('beta', 'nan')), 2) if 'beta' in dict else 'n/a',
        '5Y Avg Dividend Yield': float(dict.get('fiveYearAvgDividendYield', 'nan')) if 'fiveYearAvgDividendYield' in dict else 'n/a',
        '50 Day Average': round(float(dict.get('fiftyDayAverage', 'nan')), 2) if 'fiftyDayAverage' in dict else 'n/a',
        '200 Day Average': round(float(dict.get('twoHundredDayAverage', 'nan')), 2) if 'twoHundredDayAverage' in dict else 'n/a',
        'Enterprise Value': round(float(dict.get('enterpriseValue', 'nan'))) if 'enterpriseValue' in dict else 'n/a',
        'Shares': round(float(dict.get('floatShares', 'nan'))) if 'floatShares' in dict else 'n/a',
        'Outstanding Shares': round(float(dict.get('sharesOutstanding', 'nan'))) if 'sharesOutstanding' in dict else 'n/a',
        'Book Value': round(float(dict.get('bookValue', 'nan')), 2) if 'bookValue' in dict else 'n/a',
        '52-Week Change': round(float(dict.get('52WeekChange', 'nan')) * 100, 2) if '52WeekChange' in dict else 'n/a',
        'S&P500 52-Week Change': round(float(dict.get('SandP52WeekChange', 'nan')) * 100, 2) if 'SandP52WeekChange' in dict else 'n/a',
        'Total Cash': round(float(dict.get('totalCash', 'nan'))) if 'totalCash' in dict else 'n/a',
        'Total Cash Per Share': round(float(dict.get('totalCashPerShare', 'nan')), 2) if 'totalCashPerShare' in dict else 'n/a',
        'Total Debt': round(float(dict.get('totalDebt', 'nan'))) if 'totalDebt' in dict else 'n/a',
        'EBITDA': round(float(dict.get('ebitda', 'nan'))) if 'ebitda' in dict else 'n/a',
        'Current Ratio': round(float(dict.get('currentRatio', 'nan')), 2) if 'currentRatio' in dict else 'n/a',
        'Revenue Per Share': round(float(dict.get('revenuePerShare', 'nan')), 2) if 'revenuePerShare' in dict else 'n/a',
        'Return on Equity': round(float(dict.get('returnOnEquity', 'nan')) * 100, 2) if 'returnOnEquity' in dict else 'n/a',
        'Gross Margin': round(float(dict.get('grossMargins', 'nan')) * 100, 2) if 'grossMargins' in dict else 'n/a',
        'Operating Margin': round(float(dict.get('operatingMargins', 'nan')) * 100, 2) if 'operatingMargins' in dict else 'n/a',
        'EBITDA Margin': round(float(dict.get('ebitdaMargins', 'nan')) * 100, 2) if 'ebitdaMargins' in dict else 'n/a',
    }

    return stats

def yf_income_statement(symbol, timeframe):
    stock = yf.Ticker(symbol)
    if timeframe == 'Yearly':
        period = 'yearly'
    elif timeframe == 'Quarterly':
        period = 'quarterly'
    dataframe = stock.get_income_stmt(freq=period)
    dataframe.columns = dataframe.columns.strftime('%Y-%m-%d')
    dataframe.rename(index={
    'TaxEffectOfUnusualItems': 'Tax Effect Of Unusual Items',
    'TaxRateForCalcs': 'Tax Rate For Calcs',
    'NormalizedEBITDA': 'Normalized EBITDA',
    'NetIncomeFromContinuingOperationNetMinorityInterest': 'Net Income From Continuing Operation Net Minority Interest',
    'ReconciledDepreciation': 'Reconciled Depreciation',
    'ReconciledCostOfRevenue': 'Reconciled Cost Of Revenue',
    'EBITDA': 'EBITDA',
    'EBIT': 'EBIT',
    'NetInterestIncome': 'Net Interest Income',
    'InterestExpense': 'Interest Expense',
    'InterestIncome': 'Interest Income',
    'NormalizedIncome': 'Normalized Income',
    'NetIncomeFromContinuingAndDiscontinuedOperation': 'Net Income From Continuing And Discontinued Operation',
    'TotalExpenses': 'Total Expenses',
    'TotalOperatingIncomeAsReported': 'Total Operating Income As Reported',
    'DilutedAverageShares': 'Diluted Average Shares',
    'BasicAverageShares': 'Basic Average Shares',
    'DilutedEPS': 'Diluted EPS',
    'BasicEPS': 'Basic EPS',
    'DilutedNIAvailtoComStockholders': 'Diluted NI Avail to Com Stockholders',
    'NetIncomeCommonStockholders': 'Net Income Common Stockholders',
    'NetIncome': 'Net Income',
    'NetIncomeIncludingNoncontrollingInterests': 'Net Income Including Noncontrolling Interests',
    'NetIncomeContinuousOperations': 'Net Income Continuous Operations',
    'TaxProvision': 'Tax Provision',
    'PretaxIncome': 'Pretax Income',
    'OtherIncomeExpense': 'Other Income Expense',
    'OtherNonOperatingIncomeExpenses': 'Other Non Operating Income Expenses',
    'NetNonOperatingInterestIncomeExpense': 'Net Non Operating Interest Income Expense',
    'InterestExpenseNonOperating': 'Interest Expense Non Operating',
    'InterestIncomeNonOperating': 'Interest Income Non Operating',
    'OperatingIncome': 'Operating Income',
    'OperatingExpense': 'Operating Expense',
    'ResearchAndDevelopment': 'Research And Development',
    'SellingGeneralAndAdministration': 'Selling General And Administration',
    'GrossProfit': 'Gross Profit',
    'CostOfRevenue': 'Cost Of Revenue',
    'TotalRevenue': 'Total Revenue',
    'OperatingRevenue': 'Operating Revenue'
}, inplace=True)
    dataframe = dataframe.applymap(lambda x: '{:,.0f}'.format(x) if pd.notnull(x) else x)
    if timeframe == 'Yearly':
        income_statement = dataframe.drop(columns=dataframe.columns[-1], axis=1)
        return income_statement
    elif timeframe == 'Quarterly':
        income_statement = dataframe.drop(columns=dataframe.columns[-2:], axis=1)
        return income_statement
    
def yf_balance_sheet(symbol, timeframe):
    stock = yf.Ticker(symbol)
    if timeframe == 'Yearly':
        period = 'yearly'
    elif timeframe == 'Quarterly':
        period = 'quarterly'
    dataframe = stock.get_balance_sheet(freq=period)
    dataframe.columns = dataframe.columns.strftime('%Y-%m-%d')
    dataframe.rename(index={
    'TreasurySharesNumber': 'Treasury Shares Number',
    'OrdinarySharesNumber': 'Ordinary Shares Number',
    'ShareIssued': 'Shares Issued',
    'NetDebt': 'Net Debt',
    'TotalDebt': 'Total Debt',
    'TangibleBookValue': 'Tangible Book Value',
    'InvestedCapital': 'Invested Capital',
    'WorkingCapital': 'Working Capital',
    'NetTangibleAssets': 'Net Tangible Assets',
    'CapitalLeaseObligations': 'Capital Lease Obligations',
    'CommonStockEquity': 'Common Stock Equity',
    'TotalCapitalization': 'Total Capitalization',
    'TotalEquityGrossMinorityInterest': 'Total Equity Gross Minority Interest',
    'StockholdersEquity': 'Stockholders Equity',
    'GainsLossesNotAffectingRetainedEarnings': 'Gains Losses Not Affecting Retained Earnings',
    'OtherEquityAdjustments': 'Other Equity Adjustments',
    'RetainedEarnings': 'Retained Earnings',
    'CapitalStock': 'Capital Stock',
    'CommonStock': 'Common Stock',
    'TotalLiabilitiesNetMinorityInterest': 'Total Liabilities Net Minority Interest',
    'TotalNonCurrentLiabilitiesNetMinorityInterest': 'Total Non-Current Liabilities Net Minority Interest',
    'OtherNonCurrentLiabilities': 'Other Non-Current Liabilities',
    'TradeandOtherPayablesNonCurrent': 'Trade and Other Payables Non-Current',
    'LongTermDebtAndCapitalLeaseObligation': 'Long Term Debt And Capital Lease Obligation',
    'LongTermCapitalLeaseObligation': 'Long Term Capital Lease Obligation',
    'LongTermDebt': 'Long Term Debt',
    'CurrentLiabilities': 'Current Liabilities',
    'OtherCurrentLiabilities': 'Other Current Liabilities',
    'CurrentDeferredLiabilities': 'Current Deferred Liabilities',
    'CurrentDeferredRevenue': 'Current Deferred Revenue',
    'CurrentDebtAndCapitalLeaseObligation': 'Current Debt And Capital Lease Obligation',
    'CurrentCapitalLeaseObligation': 'Current Capital Lease Obligation',
    'CurrentDebt': 'Current Debt',
    'OtherCurrentBorrowings': 'Other Current Borrowings',
    'CommercialPaper': 'Commercial Paper',
    'PayablesAndAccruedExpenses': 'Payables And Accrued Expenses',
    'Payables': 'Payables',
    'TotalTaxPayable': 'Total Tax Payable',
    'IncomeTaxPayable': 'Income Tax Payable',
    'AccountsPayable': 'Accounts Payable',
    'TotalAssets': 'Total Assets',
    'TotalNonCurrentAssets': 'Total Non-Current Assets',
    'OtherNonCurrentAssets': 'Other Non-Current Assets',
    'NonCurrentDeferredAssets': 'Non-Current Deferred Assets',
    'NonCurrentDeferredTaxesAssets': 'Non-Current Deferred Taxes Assets',
    'InvestmentsAndAdvances': 'Investments And Advances',
    'OtherInvestments': 'Other Investments',
    'InvestmentinFinancialAssets': 'Investment in Financial Assets',
    'AvailableForSaleSecurities': 'Available For Sale Securities',
    'NetPPE': 'Net PPE',
    'AccumulatedDepreciation': 'Accumulated Depreciation',
    'GrossPPE': 'Gross PPE',
    'Leases': 'Leases',
    'OtherProperties': 'Other Properties',
    'MachineryFurnitureEquipment': 'Machinery Furniture Equipment',
    'LandAndImprovements': 'Land And Improvements',
    'Properties': 'Properties',
    'CurrentAssets': 'Current Assets',
    'OtherCurrentAssets': 'Other Current Assets',
    'Inventory': 'Inventory',
    'Receivables': 'Receivables',
    'OtherReceivables': 'Other Receivables',
    'AccountsReceivable': 'Accounts Receivable',
    'CashCashEquivalentsAndShortTermInvestments': 'Cash, Cash Equivalents, and Short Term Investments',
    'OtherShortTermInvestments': 'Other Short Term Investments',
    'CashAndCashEquivalents': 'Cash and Cash Equivalents',
    'CashEquivalents': 'Cash Equivalents',
    'CashFinancial': 'Cash Financial'
}, inplace=True)
    dataframe = dataframe.applymap(lambda x: '{:,.0f}'.format(x) if pd.notnull(x) else x)
    if timeframe == 'Yearly':
        balance_sheet = dataframe.drop(columns=dataframe.columns[-1], axis=1)
        return balance_sheet
    elif timeframe == 'Quarterly':
        balance_sheet = dataframe.drop(columns=dataframe.columns[-2:], axis=1)
        return balance_sheet
    
def yf_cashflow(symbol, timeframe):
    stock = yf.Ticker(symbol)
    if timeframe == 'Yearly':
        period = 'yearly'
    elif timeframe == 'Quarterly':
        period = 'quarterly'
    dataframe = stock.get_cashflow(freq=period)
    dataframe.columns = dataframe.columns.strftime('%Y-%m-%d')
    dataframe.rename(index={
    'FreeCashFlow': 'Free Cash Flow',
    'RepurchaseOfCapitalStock': 'Repurchase Of Capital Stock',
    'RepaymentOfDebt': 'Repayment Of Debt',
    'IssuanceOfDebt': 'Issuance Of Debt',
    'IssuanceOfCapitalStock': 'Issuance Of Capital Stock',
    'CapitalExpenditure': 'Capital Expenditure',
    'InterestPaidSupplementalData': 'Interest Paid Supplemental Data',
    'IncomeTaxPaidSupplementalData': 'Income Tax Paid Supplemental Data',
    'EndCashPosition': 'End Cash Position',
    'BeginningCashPosition': 'Beginning Cash Position',
    'ChangesInCash': 'Changes In Cash',
    'FinancingCashFlow': 'Financing Cash Flow',
    'CashFlowFromContinuingFinancingActivities': 'Cash Flow From Continuing Financing Activities',
    'NetOtherFinancingCharges': 'Net Other Financing Charges',
    'CashDividendsPaid': 'Cash Dividends Paid',
    'CommonStockDividendPaid': 'Common Stock Dividend Paid',
    'NetCommonStockIssuance': 'Net Common Stock Issuance',
    'CommonStockPayments': 'Common Stock Payments',
    'CommonStockIssuance': 'Common Stock Issuance',
    'NetIssuancePaymentsOfDebt': 'Net Issuance Payments Of Debt',
    'NetShortTermDebtIssuance': 'Net Short Term Debt Issuance',
    'NetLongTermDebtIssuance': 'Net Long Term Debt Issuance',
    'LongTermDebtPayments': 'Long Term Debt Payments',
    'LongTermDebtIssuance': 'Long Term Debt Issuance',
    'InvestingCashFlow': 'Investing Cash Flow',
    'CashFlowFromContinuingInvestingActivities': 'Cash Flow From Continuing Investing Activities',
    'NetOtherInvestingChanges': 'Net Other Investing Changes',
    'NetInvestmentPurchaseAndSale': 'Net Investment Purchase And Sale',
    'SaleOfInvestment': 'Sale Of Investment',
    'PurchaseOfInvestment': 'Purchase Of Investment',
    'NetBusinessPurchaseAndSale': 'Net Business Purchase And Sale',
    'PurchaseOfBusiness': 'Purchase Of Business',
    'NetPPEPurchaseAndSale': 'Net PPE Purchase And Sale',
    'PurchaseOfPPE': 'Purchase Of PPE',
    'OperatingCashFlow': 'Operating Cash Flow',
    'CashFlowFromContinuingOperatingActivities': 'Cash Flow From Continuing Operating Activities',
    'ChangeInWorkingCapital': 'Change In Working Capital',
    'ChangeInOtherWorkingCapital': 'Change In Other Working Capital',
    'ChangeInOtherCurrentLiabilities': 'Change In Other Current Liabilities',
    'ChangeInOtherCurrentAssets': 'Change In Other Current Assets',
    'ChangeInPayablesAndAccruedExpense': 'Change In Payables And Accrued Expense',
    'ChangeInPayable': 'Change In Payable',
    'ChangeInAccountPayable': 'Change In Account Payable',
    'ChangeInInventory': 'Change In Inventory',
    'ChangeInReceivables': 'Change In Receivables',
    'ChangesInAccountReceivables': 'Changes In Account Receivables',
    'OtherNonCashItems': 'Other Non Cash Items',
    'StockBasedCompensation': 'Stock Based Compensation',
    'DeferredTax': 'Deferred Tax',
    'DeferredIncomeTax': 'Deferred Income Tax',
    'DepreciationAmortizationDepletion': 'Depreciation Amortization Depletion',
    'DepreciationAndAmortization': 'Depreciation And Amortization',
    'NetIncomeFromContinuingOperations': 'Net Income From Continuing Operations'
}, inplace=True)
    dataframe = dataframe.applymap(lambda x: '{:,.0f}'.format(x) if pd.notnull(x) else x)
    if timeframe == 'Yearly':
        cashflow = dataframe.drop(columns=dataframe.columns[-1], axis=1)
        return cashflow
    elif timeframe == 'Quarterly':
        cashflow = dataframe.drop(columns=dataframe.columns[-2:], axis=1)
        return cashflow

def get_income_statement(symbol, period):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period={period}&apikey={api_key}"
    response = requests.get(url)
    income_statement = response.json()

    return income_statement

def get_income_statement_growth(symbol, period):
    url = f"https://financialmodelingprep.com/api/v3/income-statement-growth/{symbol}?period={period}&apikey={api_key}"    
    response = requests.get(url)
    income_growth = response.json()

    return income_growth

def revenue(income_statement):
    revenue_list = []
    for i in range(0, len(income_statement)):
        revenue_list.append({
            'date': income_statement[i]['date'],
            'revenue': income_statement[i]['revenue']
        })

    return revenue_list

def plot_revenue(symbol, revenue_list):
    dates = [entry['date'] for entry in revenue_list][::-1]
    revenues = [entry['revenue'] for entry in revenue_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Revenue', x=dates, y=revenues)
    ])

    fig.update_layout(
        title=f'{symbol} Revenue Over Time',
        xaxis_title='Date',
        yaxis_title='Revenue',
        xaxis=dict(type='category')
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )

    return fig

def plot_revenue_comparison(symbol_list, revenue_comparison_list):
    dates = [entry['date'][:4] if entry['date'] != 'TTM' else 'TTM' for entry in revenue_comparison_list[0][::-1]]
    fig = go.Figure()
    colors = ['rgb(158,202,225)', 'rgb(255,127,80)', 'rgb(34,139,34)', 'rgb(255,215,0)', 'rgb(75,0,130)']
    for i, (symbol, comparison_list) in enumerate(zip(symbol_list, revenue_comparison_list)):
        filtered_comparison_list = [entry for entry in comparison_list if entry['date'][:4] > '2014']
        dates_filtered = [entry['date'][:4] if entry['date'] != 'TTM' else 'TTM' for entry in filtered_comparison_list][::-1]
        revenues = [entry['revenue'] for entry in filtered_comparison_list][::-1]
        fig.add_trace(go.Bar(name=f'{symbol} Revenue', x=dates_filtered, y=revenues, marker_color=colors[i % len(colors)]))
    
    fig.update_layout(
        title='Revenue Comparison Over Time',
        xaxis_title='Date',
        yaxis_title='Revenue',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        width=0.25
    )

    return fig

def gross_profit(income_statement):
    gross_profit_list = []
    for i in range(0, len(income_statement)):
        gross_profit_list.append({
            'date': income_statement[i]['date'],
            'gross_profit': income_statement[i]['grossProfit']
        })

    return gross_profit_list

def plot_gross_profit(symbol, gross_profit_list):
    dates = [entry['date'] for entry in gross_profit_list][::-1]
    gross_profits = [entry['gross_profit'] for entry in gross_profit_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Gross Profit', x=dates, y=gross_profits)
    ])

    fig.update_layout(
        title=f'{symbol} Gross Profit Over Time',
        xaxis_title='Date',
        yaxis_title='Gross Profit',
        xaxis=dict(type='category')
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )

    return fig

def plot_gross_profit_comparison(symbol_list, gross_profit_comparison_list):
    fig = go.Figure()
    colors = ['rgb(158,202,225)', 'rgb(255,127,80)', 'rgb(34,139,34)', 'rgb(255,215,0)', 'rgb(75,0,130)']
    for i, (symbol, comparison_list) in enumerate(zip(symbol_list, gross_profit_comparison_list)):
        filtered_comparison_list = [entry for entry in comparison_list if entry['date'][:4] > '2014']
        dates_filtered = [entry['date'][:4] if entry['date'] != 'TTM' else 'TTM' for entry in filtered_comparison_list][::-1]
        gross_profits = [entry['gross_profit'] for entry in filtered_comparison_list][::-1]
        fig.add_trace(go.Bar(name=f'{symbol} Gross Profit', x=dates_filtered, y=gross_profits, marker_color=colors[i % len(colors)]))
    
    fig.update_layout(
        title='Gross Profit Comparison Over Time',
        xaxis_title='Date',
        yaxis_title='Gross Profit',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        width=0.25
    )

    return fig

def net_income(income_statement):
    net_income_list = []
    for i in range(0, len(income_statement)):
        net_income_list.append({
            'date': income_statement[i]['date'],
            'net_income': income_statement[i]['netIncome']
        })

    return net_income_list

def plot_net_income(symbol, net_income_list):
    dates = [entry['date'] for entry in net_income_list][::-1]
    net_incomes = [entry['net_income'] for entry in net_income_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Net Income', x=dates, y=net_incomes)
    ])

    fig.update_layout(
        title=f'{symbol} Net Income Over Time',
        xaxis_title='Date',
        yaxis_title='Net Income',
        xaxis=dict(type='category')
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )

    return fig

def plot_net_income_comparison(symbol_list, net_income_comparison_list):
    fig = go.Figure()
    colors = ['rgb(158,202,225)', 'rgb(255,127,80)', 'rgb(34,139,34)', 'rgb(255,215,0)', 'rgb(75,0,130)']
    for i, (symbol, comparison_list) in enumerate(zip(symbol_list, net_income_comparison_list)):
        filtered_comparison_list = [entry for entry in comparison_list if entry['date'][:4] > '2014']
        dates_filtered = [entry['date'][:4] if entry['date'] != 'TTM' else 'TTM' for entry in filtered_comparison_list][::-1]
        net_incomes = [entry['net_income'] for entry in filtered_comparison_list][::-1]
        fig.add_trace(go.Bar(name=f'{symbol} Net Income', x=dates_filtered, y=net_incomes, marker_color=colors[i % len(colors)]))
    
    fig.update_layout(
        title='Net Income Comparison Over Time',
        xaxis_title='Date',
        yaxis_title='Net Income',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        width=0.25
    )

    return fig

def operating_income(income_statement):
    operating_income_list = []
    for i in range(0, len(income_statement)):
        operating_income_list.append({
            'date': income_statement[i]['date'],
            'operating_income': income_statement[i]['operatingIncome']
        })
    return operating_income_list

def plot_operating_income(symbol, operating_income_list):
    dates = [entry['date'] for entry in operating_income_list][::-1]
    operating_incomes = [entry['operating_income'] for entry in operating_income_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Operating Income', x=dates, y=operating_incomes)
    ])

    fig.update_layout(
        title=f'{symbol} Operating Income Over Time',
        xaxis_title='Date',
        yaxis_title='Operating Income',
        xaxis=dict(type='category')
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )

    return fig

def plot_operating_income_comparison(symbol_list, operating_income_comparison_list):
    fig = go.Figure()
    colors = ['rgb(158,202,225)', 'rgb(255,127,80)', 'rgb(34,139,34)', 'rgb(255,215,0)', 'rgb(75,0,130)']
    for i, (symbol, comparison_list) in enumerate(zip(symbol_list, operating_income_comparison_list)):
        filtered_comparison_list = [entry for entry in comparison_list if entry['date'][:4] > '2014']
        dates_filtered = [entry['date'][:4] if entry['date'] != 'TTM' else 'TTM' for entry in filtered_comparison_list][::-1]
        operating_incomes = [entry['operating_income'] for entry in filtered_comparison_list][::-1]
        fig.add_trace(go.Bar(name=f'{symbol} Operating Income', x=dates_filtered, y=operating_incomes, marker_color=colors[i % len(colors)]))
    
    fig.update_layout(
        title='Operating Income Comparison Over Time',
        xaxis_title='Date',
        yaxis_title='Operating Income',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        width=0.25
    )

    return fig

def cost_of_revenue(income_statement):
    cost_of_revenue_list = []
    for i in range(0, len(income_statement)):
        cost_of_revenue_list.append({
            'date': income_statement[i]['date'],
            'cost_of_revenue': income_statement[i]['costOfRevenue']
        })

    return cost_of_revenue_list

def plot_cost_of_revenue(symbol, cost_of_revenue_list):
    dates = [entry['date'] for entry in cost_of_revenue_list][::-1]
    cost_of_revenues = [entry['cost_of_revenue'] for entry in cost_of_revenue_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Cost of Revenue', x=dates, y=cost_of_revenues)
    ])

    fig.update_layout(
        title=f'{symbol} Cost of Revenue Over Time',
        xaxis_title='Date',
        yaxis_title='Cost of Revenue',
        xaxis=dict(type='category')
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )

    return fig

def plot_cost_of_revenue_comparison(symbol_list, cost_of_revenue_comparison_list):
    fig = go.Figure()
    colors = ['rgb(158,202,225)', 'rgb(255,127,80)', 'rgb(34,139,34)', 'rgb(255,215,0)', 'rgb(75,0,130)']
    for i, (symbol, comparison_list) in enumerate(zip(symbol_list, cost_of_revenue_comparison_list)):
        filtered_comparison_list = [entry for entry in comparison_list if entry['date'][:4] > '2014']
        dates_filtered = [entry['date'][:4] if entry['date'] != 'TTM' else 'TTM' for entry in filtered_comparison_list][::-1]
        cost_of_revenues = [entry['cost_of_revenue'] for entry in filtered_comparison_list][::-1]
        fig.add_trace(go.Bar(name=f'{symbol} Cost of Revenue', x=dates_filtered, y=cost_of_revenues, marker_color=colors[i % len(colors)]))
    
    fig.update_layout(
        title='Cost of Revenue Comparison Over Time',
        xaxis_title='Date',
        yaxis_title='Cost of Revenue',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        width=0.25
    )

    return fig

def revenue_growth(income_statement_growth):
    revenue_growth_list = []
    for i in range(0, len(income_statement_growth)):
        revenue_growth_list.append({
            'date': income_statement_growth[i]['date'],
            'revenue_growth': income_statement_growth[i]['growthRevenue']
        })
    return revenue_growth_list

def net_income_growth(income_statement_growth):
    net_income_growth_list = []
    for i in range(0, len(income_statement_growth)):
        net_income_growth_list.append({
            'date': income_statement_growth[i]['date'],
            'net_income_growth': income_statement_growth[i]['growthNetIncome']
        })
    return net_income_growth_list  

def operating_income_growth(income_statement_growth):
    operating_income_growth_list = []
    for i in range(0, len(income_statement_growth)):
        operating_income_growth_list.append({
            'date': income_statement_growth[i]['date'],
            'operating_income_growth': income_statement_growth[i]['growthOperatingIncome']
        })
    return operating_income_growth_list

def plot_revenue_net_income_operating_income(symbol, income_statement, income_statement_growth):
    revenue_list = revenue(income_statement)
    net_income_list = net_income(income_statement)
    operating_income_list = operating_income(income_statement)
    
    dates = [entry['date'] for entry in revenue_list][::-1]
    revenues = [entry['revenue'] for entry in revenue_list][::-1]
    net_incomes = [entry['net_income'] for entry in net_income_list][::-1]
    operating_incomes = [entry['operating_income'] for entry in operating_income_list][::-1]

    revenue_growth_list = revenue_growth(income_statement_growth)
    net_income_growth_list = net_income_growth(income_statement_growth)
    operating_income_growth_list = operating_income_growth(income_statement_growth)

    revenue_growths = [entry['revenue_growth'] for entry in revenue_growth_list][::-1]
    net_income_growths = [entry['net_income_growth'] for entry in net_income_growth_list][::-1]
    operating_income_growths = [entry['operating_income_growth'] for entry in operating_income_growth_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Revenue', x=dates, y=revenues, marker_color='rgb(158,202,225)',
               hovertemplate='Revenue: %{y}<br>YoY Growth: %{customdata:.2%}', customdata=revenue_growths),
        go.Bar(name='Net Income', x=dates, y=net_incomes, marker_color='rgb(255,127,80)',
               hovertemplate='Net Income: %{y}<br>YoY Growth: %{customdata:.2%}', customdata=net_income_growths),
        go.Bar(name='Operating Income', x=dates, y=operating_incomes, marker_color='rgb(34,139,34)',
               hovertemplate='Operating Income: %{y}<br>YoY Growth: %{customdata:.2%}', customdata=operating_income_growths)
    ])

    fig.update_layout(
        title=f'{symbol} Revenue, Net Income, and Operating Income Over Time',
        xaxis_title='Date',
        yaxis_title='Amount',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        width=0.25
    )

    return fig

def get_gross_profit_margin(financial_ratios, financial_ratios_ttm):
    gross_profit_margin_list = []
    gross_profit_margin_list.append({
        'date': 'TTM',
        'gross_profit_margin': financial_ratios_ttm[0]['grossProfitMarginTTM']
    })
    for i in range(0, len(financial_ratios)):
        gross_profit_margin_list.append({
            'date': financial_ratios[i]['date'],
            'gross_profit_margin': financial_ratios[i]['grossProfitMargin']
        })

    return gross_profit_margin_list

def get_net_income_margin(financial_ratios, financial_ratios_ttm):
    net_income_margin_list = []
    net_income_margin_list.append({
        'date': 'TTM',
        'net_income_margin': financial_ratios_ttm[0]['netProfitMarginTTM']
    })
    for i in range(0, len(financial_ratios)):
        net_income_margin_list.append({
            'date': financial_ratios[i]['date'],
            'net_income_margin': financial_ratios[i]['netProfitMargin']
        })

    return net_income_margin_list

def get_operating_profit_margin(financial_ratios, financial_ratios_ttm):
    operating_profit_margin_list = []
    operating_profit_margin_list.append({
        'date': 'TTM',
        'operating_profit_margin': financial_ratios_ttm[0]['operatingProfitMarginTTM']
    })
    for i in range(0, len(financial_ratios)):
        operating_profit_margin_list.append({
            'date': financial_ratios[i]['date'],
            'operating_profit_margin': financial_ratios[i]['operatingProfitMargin']
        })

    return operating_profit_margin_list

def plot_profit_margins(symbol, gross_profit_margin_list, net_income_margin_list, operating_profit_margin_list):
    filtered_gross_profit_margin_list = [entry for entry in gross_profit_margin_list if entry['date'][:4] > '1999']
    filtered_net_income_margin_list = [entry for entry in net_income_margin_list if entry['date'][:4] > '1999']
    filtered_operating_profit_margin_list = [entry for entry in operating_profit_margin_list if entry['date'][:4] > '1999']

    dates = [entry['date'] for entry in filtered_gross_profit_margin_list][::-1]
    gross_profit_margins = [entry['gross_profit_margin'] for entry in filtered_gross_profit_margin_list][::-1]
    net_income_margins = [entry['net_income_margin'] for entry in filtered_net_income_margin_list][::-1]
    operating_profit_margins = [entry['operating_profit_margin'] for entry in filtered_operating_profit_margin_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Gross Profit Margin', x=dates, y=gross_profit_margins, marker_color='rgb(158,202,225)'),
        go.Bar(name='Net Income Margin', x=dates, y=net_income_margins, marker_color='rgb(255,127,80)'),
        go.Bar(name='Operating Profit Margin', x=dates, y=operating_profit_margins, marker_color='rgb(34,139,34)')
    ])

    fig.update_layout(
        title=f'{symbol} Profit Margins Over Time',
        xaxis_title='Date',
        yaxis_title='Profit Margin',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        width=0.25
    )

    return fig

def earnings_history(symbol):
    stock = yf.Ticker(symbol)
    dataframe = stock.get_earnings_history()
    dataframe['surprisePercent'] = dataframe['surprisePercent'].values * 100
    dataframe.index = dataframe.index.strftime('%Y-%m-%d')
    return dataframe

def get_earnings_history(symbol):
    url = f'https://financialmodelingprep.com/api/v3/historical/earning_calendar/{symbol}?apikey={api_key}'
    response = requests.get(url)
    earnings_history = response.json()
    earnings_history_list = []
    for i in range(0, len(earnings_history)):
        eps = earnings_history[i]['eps']
        eps_estimate = earnings_history[i]['epsEstimated']
        revenue = earnings_history[i]['revenue']
        revenue_estimate = earnings_history[i]['revenueEstimated']
        
        if eps is None and eps_estimate is not None:
            eps = 0
        if revenue is None and revenue_estimate is not None:
            revenue = 0
        
        if eps is not None and eps_estimate is not None and revenue is not None and revenue_estimate is not None:
            earnings_history_list.append({
                'date': earnings_history[i]['fiscalDateEnding'],
                'eps': eps,
                'epsEstimate': eps_estimate,
                'surprisePercent': round((eps - eps_estimate) / eps_estimate * 100, 1),
                'revenue': revenue,
                'revenueEstimate': revenue_estimate
            })

    return earnings_history_list    

def plot_past_year_earnings(symbol, earnings_history_list):
    dates = [entry['date'] for entry in earnings_history_list[:5]][::-1]
    eps_actual = [entry['eps'] for entry in earnings_history_list[:5]][::-1]
    eps_estimate = [entry['epsEstimate'] for entry in earnings_history_list[:5]][::-1]
    surprise_percent = [entry['surprisePercent'] for entry in earnings_history_list[:5]][::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=eps_estimate,
        mode='markers',
        marker=dict(size=12, symbol='circle-open', color='blue', line=dict(width=1, color='gray')),
        name='EPS Estimate'
    ))

    for i, (actual, estimate, surprise) in enumerate(zip(eps_actual, eps_estimate, surprise_percent)):
        if actual != 0:
            color = 'green' if actual > estimate else 'red'
            fig.add_trace(go.Scatter(
                x=[dates[i]],
                y=[actual],
                mode='markers',
                marker=dict(size=12, color=color, line=dict(width=1, color='black')),
                name="Actual EPS" if i == 0 else "",
                hovertemplate=(
                    f"<b>EPS Actual</b>: {actual:.2f}<br>"
                    f"<b>Surprise %</b>: {surprise:.2f}%"
                    "<extra></extra>"
                ),
                showlegend=(i == 0)
            ))

    fig.update_layout(
        title=f"{symbol} Quarterly EPS Actual vs Estimate",
        xaxis_title='Date',
        yaxis_title='EPS',
        font=dict(color='black'),
        legend=dict(x=1, y=1),
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis=dict(type='category')
    )

    return fig

def plot_earnings(symbol, earnings_history_list):
    dates = [entry['date'] for entry in earnings_history_list][::-1]
    eps_actual = [entry['eps'] for entry in earnings_history_list][::-1]
    eps_estimate = [entry['epsEstimate'] for entry in earnings_history_list][::-1]
    surprise_percent = [entry['surprisePercent'] for entry in earnings_history_list][::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=eps_estimate,
        mode='markers',
        marker=dict(size=6, symbol='circle-open', color='blue', line=dict(width=1, color='gray')),
        name='EPS Estimate'
    ))

    for i, (actual, estimate, surprise) in enumerate(zip(eps_actual, eps_estimate, surprise_percent)):
        if actual != 0:
            color = 'green' if actual > estimate else 'red'
            fig.add_trace(go.Scatter(
                x=[dates[i]],
                y=[actual],
                mode='markers',
                marker=dict(size=6, color=color, line=dict(width=1, color='black')),
                name="Actual EPS" if i == 0 else "",
                hovertemplate=(
                    f"<b>EPS Actual</b>: {actual:.2f}<br>"
                    f"<b>Surprise %</b>: {surprise:.2f}%"
                    "<extra></extra>"
                ),
                showlegend=(i == 0)
            ))
    
    fig.update_layout(
        title=f"{symbol} Quarterly EPS Actual vs Estimate",
        xaxis_title='Date',
        yaxis_title='EPS',
        font=dict(color='black'),
        legend=dict(x=1, y=1),
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return fig

def plot_gross_profit_margin(symbol, gross_profit_margin_list):
    filtered_gross_profit_margin_list = [entry for entry in gross_profit_margin_list if entry['date'][:4] > '1999']
    dates = [entry['date'] for entry in filtered_gross_profit_margin_list][::-1]
    gross_profit_margins = [entry['gross_profit_margin'] for entry in filtered_gross_profit_margin_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Gross Profit Margin', x=dates, y=gross_profit_margins)
    ])

    fig.update_layout(
        title=f'{symbol} Gross Profit Margin Over Time',
        xaxis_title='Date',
        yaxis_title='Gross Profit Margin',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )

    return fig

def plot_gross_profit_margin_comparison(symbol_list, gross_profit_margin_comparison_list):
    fig = go.Figure()
    colors = ['rgb(158,202,225)', 'rgb(255,127,80)', 'rgb(34,139,34)', 'rgb(255,215,0)', 'rgb(75,0,130)']
    for i, (symbol, comparison_list) in enumerate(zip(symbol_list, gross_profit_margin_comparison_list)):
        filtered_comparison_list = [entry for entry in comparison_list if entry['date'][:4] > '2014']
        dates_filtered = [entry['date'][:4] if entry['date'] != 'TTM' else 'TTM' for entry in filtered_comparison_list][::-1]
        gross_profit_margins = [entry['gross_profit_margin'] for entry in filtered_comparison_list][::-1]
        fig.add_trace(go.Bar(name=f'{symbol} Gross Profit Margin', x=dates_filtered, y=gross_profit_margins, marker_color=colors[i % len(colors)]))
    
    fig.update_layout(
        title='Gross Profit Margin Comparison Over Time',
        xaxis_title='Date',
        yaxis_title='Gross Profit Margin',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        width=0.25
    )

    return fig

def plot_net_income_margin(symbol, net_income_margin_list):
    filtered_net_income_margin_list = [entry for entry in net_income_margin_list if entry['date'][:4] > '1999']
    dates = [entry['date'] for entry in filtered_net_income_margin_list][::-1]
    net_income_margins = [entry['net_income_margin'] for entry in filtered_net_income_margin_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Net Income Margin', x=dates, y=net_income_margins)
    ])

    fig.update_layout(
        title=f'{symbol} Net Income Margin Over Time',
        xaxis_title='Date',
        yaxis_title='Net Income Margin',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(255,127,80)',
        width=0.25
    )

    return fig

def plot_net_income_margin_comparison(symbol_list, net_income_margin_comparison_list):
    fig = go.Figure()
    colors = ['rgb(158,202,225)', 'rgb(255,127,80)', 'rgb(34,139,34)', 'rgb(255,215,0)', 'rgb(75,0,130)']
    for i, (symbol, comparison_list) in enumerate(zip(symbol_list, net_income_margin_comparison_list)):
        filtered_comparison_list = [entry for entry in comparison_list if entry['date'][:4] > '2014']
        dates_filtered = [entry['date'][:4] if entry['date'] != 'TTM' else 'TTM' for entry in filtered_comparison_list][::-1]
        net_income_margins = [entry['net_income_margin'] for entry in filtered_comparison_list][::-1]
        fig.add_trace(go.Bar(name=f'{symbol} Net Income Margin', x=dates_filtered, y=net_income_margins, marker_color=colors[i % len(colors)]))
    
    fig.update_layout(
        title='Net Income Margin Comparison Over Time',
        xaxis_title='Date',
        yaxis_title='Net Income Margin',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        width=0.25
    )

    return fig

def plot_operating_profit_margin(symbol, operating_profit_margin_list):
    filtered_operating_profit_margin_list = [entry for entry in operating_profit_margin_list if entry['date'][:4] > '1999']
    dates = [entry['date'] for entry in filtered_operating_profit_margin_list][::-1]
    operating_profit_margins = [entry['operating_profit_margin'] for entry in filtered_operating_profit_margin_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Operating Profit Margin', x=dates, y=operating_profit_margins)
    ])

    fig.update_layout(
        title=f'{symbol} Operating Profit Margin Over Time',
        xaxis_title='Date',
        yaxis_title='Operating Profit Margin',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(34,139,34)',
        width=0.25
    )

    return fig

def plot_operating_profit_margin_comparison(symbol_list, operating_profit_margin_comparison_list):
    fig = go.Figure()
    colors = ['rgb(158,202,225)', 'rgb(255,127,80)', 'rgb(34,139,34)', 'rgb(255,215,0)', 'rgb(75,0,130)']
    for i, (symbol, comparison_list) in enumerate(zip(symbol_list, operating_profit_margin_comparison_list)):
        filtered_comparison_list = [entry for entry in comparison_list if entry['date'][:4] > '2014']
        dates_filtered = [entry['date'][:4] if entry['date'] != 'TTM' else 'TTM' for entry in filtered_comparison_list][::-1]
        operating_profit_margins = [entry['operating_profit_margin'] for entry in filtered_comparison_list][::-1]
        fig.add_trace(go.Bar(name=f'{symbol} Operating Profit Margin', x=dates_filtered, y=operating_profit_margins, marker_color=colors[i % len(colors)]))
    
    fig.update_layout(
        title='Operating Profit Margin Comparison Over Time',
        xaxis_title='Date',
        yaxis_title='Operating Profit Margin',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        width=0.25
    )

    return fig

def get_roe(financial_ratios, financial_ratios_ttm):
    roe_list = []
    roe_list.append({
        'date': 'TTM',
        'roe': financial_ratios_ttm[0]['returnOnEquityTTM']
    })
    for i in range(0, len(financial_ratios)):
        roe_list.append({
            'date': financial_ratios[i]['date'],
            'roe': financial_ratios[i]['returnOnEquity']
        })

    return roe_list

def plot_roe(symbol, roe_list):
    dates = [entry['date'] for entry in roe_list][::-1]
    roes = [entry['roe'] for entry in roe_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Return on Equity', x=dates, y=roes)
    ])

    fig.update_layout(
        title=f'{symbol} Return on Equity Over Time',
        xaxis_title='Date',
        yaxis_title='Return on Equity',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )

    return fig

def get_roa(financial_ratios, financial_ratios_ttm):
    roa_list = []
    roa_list.append({
        'date': 'TTM',
        'roa': financial_ratios_ttm[0]['returnOnAssetsTTM']
    })
    for i in range(0, len(financial_ratios)):
        roa_list.append({
            'date': financial_ratios[i]['date'],
            'roa': financial_ratios[i]['returnOnAssets']
        })

    return roa_list

def plot_roa(symbol, roa_list):
    dates = [entry['date'] for entry in roa_list][::-1]
    roas = [entry['roa'] for entry in roa_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Return on Assets', x=dates, y=roas)
    ])

    fig.update_layout(
        title=f'{symbol} Return on Assets Over Time',
        xaxis_title='Date',
        yaxis_title='Return on Assets',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )

    return fig

def get_roce(financial_ratios, financial_ratios_ttm):
    roce_list = []
    roce_list.append({
        'date': 'TTM',
        'roce': financial_ratios_ttm[0]['returnOnCapitalEmployedTTM']
    })
    for i in range(0, len(financial_ratios)):
        roce_list.append({
            'date': financial_ratios[i]['date'],
            'roce': financial_ratios[i]['returnOnCapitalEmployed']
        })

    return roce_list

def plot_roce(symbol, roce_list):
    dates = [entry['date'] for entry in roce_list][::-1]
    roces = [entry['roce'] for entry in roce_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Return on Capital Employed', x=dates, y=roces)
    ])

    fig.update_layout(
        title=f'{symbol} Return on Capital Employed Over Time',
        xaxis_title='Date',
        yaxis_title='Return on Capital Employed',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )

    return fig

def plot_revenue_net_income_changes(symbol, revenue_list, net_income_list):
    dates = [entry['date'] for entry in revenue_list][::-1]
    revenues = [entry['revenue'] for entry in revenue_list][::-1]
    net_incomes = [entry['net_income'] for entry in net_income_list][::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=revenues,
        mode='lines+markers',
        name='Revenue',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))

    fig.add_trace(go.Scatter(
        x=dates,
        y=net_incomes,
        mode='lines+markers',
        name='Net Income',
        line=dict(color='green', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=f'{symbol} Revenue and Net Income Changes Over Time',
        xaxis_title='Date',
        yaxis_title='Amount',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    return fig

def plot_stacked_area_margins(symbol, gross_profit_margin_list, operating_profit_margin_list, net_income_margin_list):
    filtered_gross_profit_margin_list = [entry for entry in gross_profit_margin_list if entry['date'][:4] > '1999']
    filtered_operating_profit_margin_list = [entry for entry in operating_profit_margin_list if entry['date'][:4] > '1999']
    filtered_net_income_margin_list = [entry for entry in net_income_margin_list if entry['date'][:4] > '1999']

    dates = [entry['date'] for entry in filtered_gross_profit_margin_list][::-1]
    gross_profit_margins = [entry['gross_profit_margin'] for entry in filtered_gross_profit_margin_list][::-1]
    operating_profit_margins = [entry['operating_profit_margin'] for entry in filtered_operating_profit_margin_list][::-1]
    net_income_margins = [entry['net_income_margin'] for entry in filtered_net_income_margin_list][::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=gross_profit_margins,
        mode='lines',
        name='Gross Profit Margin',
        stackgroup='one'
    ))

    fig.add_trace(go.Scatter(
        x=dates,
        y=operating_profit_margins,
        mode='lines',
        name='Operating Profit Margin',
        stackgroup='one'
    ))

    fig.add_trace(go.Scatter(
        x=dates,
        y=net_income_margins,
        mode='lines',
        name='Net Income Margin',
        stackgroup='one'
    ))

    fig.update_layout(
        title=f'{symbol} Profit Margins Over Time (Stacked Area)',
        xaxis_title='Date',
        yaxis_title='Margin',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    return fig

def balance_sheet(symbol, period='annual'):
    balance_sheet = fmpsdk.balance_sheet_statement(apikey=api_key, symbol=symbol, period=period)
    # file_path = f'json/{symbol}_balance_sheet.json'
    # os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # with open(file_path, 'w') as f:
    #     json.dump(balance_sheet, f, indent=4)

    return balance_sheet

def cash_flow(symbol, period):
    # cash_flow = fmpsdk.cash_flow_statement(apikey=api_key, symbol=symbol, period=period)
    url = f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?period={period}&apikey={api_key}'
    response = requests.get(url)
    cash_flow = response.json()
    # file_path = f'json/{symbol}_cash_flow.json'
    # os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # with open(file_path, 'w') as f:
    #     json.dump(cash_flow, f, indent=4)

    return cash_flow

def free_cash_flow(cash_flow):
    free_cash_flow_list = []
    for i in range(0, len(cash_flow)):
        free_cash_flow_list.append({
            'date': cash_flow[i]['date'],
            'free_cash_flow': cash_flow[i]['freeCashFlow']
        })

    return free_cash_flow_list

def plot_free_cash_flow(symbol, free_cash_flow_list):
    dates = [entry['date'] for entry in free_cash_flow_list][::-1]
    free_cash_flows = [entry['free_cash_flow'] for entry in free_cash_flow_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Free Cash Flow', x=dates, y=free_cash_flows)
    ])

    fig.update_layout(
        title=f'{symbol} Free Cash Flow Over Time',
        xaxis_title='Date',
        yaxis_title='Free Cash Flow',
        xaxis=dict(type='category')
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )

    return fig

def plot_fcf_net_income(symbol, free_cash_flow_list, net_income_list):
    # Create a dictionary for quick lookup
    fcf_dict = {entry['date']: entry['free_cash_flow'] for entry in free_cash_flow_list}
    ni_dict = {entry['date']: entry['net_income'] for entry in net_income_list}

    # Find common dates
    common_dates = sorted(set(fcf_dict.keys()).intersection(ni_dict.keys()), reverse=False)

    # Extract values for common dates
    dates = common_dates
    free_cash_flows = [fcf_dict[date] for date in dates]
    net_incomes = [ni_dict[date] for date in dates]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dates,
        y=free_cash_flows,
        name='Free Cash Flow',
        marker_color='rgb(158,202,225)'
    ))

    fig.add_trace(go.Bar(
        x=dates,
        y=net_incomes,
        name='Net Income',
        marker_color='rgb(255,127,80)'
    ))

    fig.update_layout(
        title=f'{symbol} Free Cash Flow vs Net Income Over Time',
        xaxis_title='Date',
        yaxis_title='Amount',
        xaxis=dict(type='category')
    )

    return fig


def get_enterprise_values(symbol, period='annual'):
    enterprise_values = fmpsdk.enterprise_values(apikey=api_key, symbol=symbol, period=period)

    return enterprise_values

def get_key_metrics(symbol, period):
    url = f'https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?period={period}&apikey={api_key}'
    response = requests.get(url)
    key_metrics = response.json()
    # key_metrics = fmpsdk.key_metrics(apikey=api_key, symbol=symbol, period=period)

    return key_metrics

def get_key_metrics_ttm(symbol):
    key_metrics_ttm = fmpsdk.key_metrics_ttm(apikey=api_key, symbol=symbol)

    return key_metrics_ttm

def get_financial_ratios(symbol, period):
    url = f'https://financialmodelingprep.com/api/v3/ratios/{symbol}?period={period}&apikey={api_key}'
    response = requests.get(url)
    financial_ratios = response.json()
    # financial_ratios = fmpsdk.financial_ratios(apikey=api_key, symbol=symbol, period=period)

    return financial_ratios

def get_financial_ratios_ttm(symbol):
    financial_ratios_ttm = fmpsdk.financial_ratios_ttm(apikey=api_key, symbol=symbol)

    return financial_ratios_ttm

def get_pe_ratio(key_metrics, key_metrics_ttm):
    pe_ratio_list = []
    pe_ratio_list.append({
        'date': 'TTM',
        'pe_ratio': key_metrics_ttm[0]['peRatioTTM']
    })
    for i in range(0, len(key_metrics)):
        pe_ratio_list.append({ 
            'date': key_metrics[i]['date'],
            'pe_ratio': key_metrics[i]['peRatio']
        })
    
    return pe_ratio_list

def plot_pe_ratio(symbol, pe_ratio_list):
    dates = [entry['date'] for entry in pe_ratio_list][::-1]
    pe_ratios = [entry['pe_ratio'] for entry in pe_ratio_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='PE Ratio', x=dates, y=pe_ratios)
    ])

    fig.update_layout(
        title=f'{symbol} Price to Earnings (PE) Ratio Over Time',
        xaxis_title='Date',
        yaxis_title='PE Ratio',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def plot_pe_ratios_comparison(symbol_list, pe_ratio_comparison_list):
    fig = go.Figure()
    colors = ['rgb(158,202,225)', 'rgb(255,127,80)', 'rgb(34,139,34)', 'rgb(255,215,0)', 'rgb(75,0,130)']
    for i, (symbol, comparison_list) in enumerate(zip(symbol_list, pe_ratio_comparison_list)):
        filtered_comparison_list = [entry for entry in comparison_list if entry['date'][:4] > '2014']
        dates_filtered = [entry['date'][:4] if entry['date'] != 'TTM' else 'TTM' for entry in filtered_comparison_list][::-1]
        pe_ratios = [entry['pe_ratio'] for entry in filtered_comparison_list][::-1]
        fig.add_trace(go.Bar(name=f'{symbol} PE Ratio', x=dates_filtered, y=pe_ratios, marker_color=colors[i % len(colors)]))
    
    fig.update_layout(
        title='Price to Earnings (PE) Ratio Comparison Over Time',
        xaxis_title='Date',
        yaxis_title='PE Ratio',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        width=0.25
    )

    return fig

def get_peg_ratio(financial_ratios, financial_ratios_ttm):
    peg_ratio_list = []
    peg_ratio_list.append({
        'date': 'TTM',
        'peg_ratio': financial_ratios_ttm[0]['priceEarningsToGrowthRatioTTM']
    })
    for i in range(0, len(financial_ratios)):
        peg_ratio_list.append({ 
            'date': financial_ratios[i]['date'],
            'peg_ratio': financial_ratios[i]['priceEarningsToGrowthRatio']
        })

    return peg_ratio_list

def plot_peg_ratio(symbol, peg_ratio_list):
    dates = [entry['date'] for entry in peg_ratio_list][::-1]
    peg_ratios = [entry['peg_ratio'] for entry in peg_ratio_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='PEG Ratio', x=dates, y=peg_ratios)
    ])

    fig.update_layout(
        title=f'{symbol} Price to Earnings to Growth (PEG) Ratio Over Time',
        xaxis_title='Date',
        yaxis_title='PEG Ratio',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def get_pb_ratio(key_metrics, key_metrics_ttm):
    pb_ratio_list = []
    pb_ratio_list.append({
        'date': 'TTM',
        'pb_ratio': key_metrics_ttm[0]['pbRatioTTM']
    })
    for i in range(0, len(key_metrics)):
        pb_ratio_list.append({ 
            'date': key_metrics[i]['date'],
            'pb_ratio': key_metrics[i]['pbRatio']
        })
    
    return pb_ratio_list

def plot_pb_ratio(symbol, pb_ratio_list):
    dates = [entry['date'] for entry in pb_ratio_list][::-1]
    pb_ratios = [entry['pb_ratio'] for entry in pb_ratio_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='PB Ratio', x=dates, y=pb_ratios)
    ])

    fig.update_layout(
        title=f'{symbol} Price to Book (PB) Ratio Over Time',
        xaxis_title='Date',
        yaxis_title='PB Ratio',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def get_ps_ratio(key_metrics, key_metrics_ttm):
    ps_ratio_list = []
    ps_ratio_list.append({
        'date': 'TTM',
        'ps_ratio': key_metrics_ttm[0]['priceToSalesRatioTTM']
    })
    for i in range(0, len(key_metrics)):
        ps_ratio_list.append({ 
            'date': key_metrics[i]['date'],
            'ps_ratio': key_metrics[i]['priceToSalesRatio']
        })
    
    return ps_ratio_list

def plot_ps_ratio(symbol, ps_ratio_list):
    dates = [entry['date'] for entry in ps_ratio_list][::-1]
    ps_ratios = [entry['ps_ratio'] for entry in ps_ratio_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='PS Ratio', x=dates, y=ps_ratios)
    ])

    fig.update_layout(
        title=f'{symbol} Price to Sales (PS) Ratio Over Time',
        xaxis_title='Date',
        yaxis_title='PS Ratio',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def get_ev_ebitda(key_metrics, key_metrics_ttm):
    ev_ebitda_list = []
    ev_ebitda_list.append({
        'date': 'TTM',
        'ev_ebitda': key_metrics_ttm[0]['enterpriseValueOverEBITDATTM']
    })
    for i in range(0, len(key_metrics)):
        ev_ebitda_list.append({ 
            'date': key_metrics[i]['date'],
            'ev_ebitda': key_metrics[i]['enterpriseValueOverEBITDA']
        })

    return ev_ebitda_list

def plot_ev_ebitda(symbol, ev_ebitda_list):
    dates = [entry['date'] for entry in ev_ebitda_list][::-1]
    ev_ebitdas = [entry['ev_ebitda'] for entry in ev_ebitda_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='EV/EBITDA', x=dates, y=ev_ebitdas)
    ])

    fig.update_layout(
        title=f'{symbol} Enterprise Value to EBITDA (EV/EBITDA) Over Time',
        xaxis_title='Date',
        yaxis_title='EV/EBITDA',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def get_price_to_fcf(key_metrics, key_metrics_ttm):
    price_to_fcf_list = []
    price_to_fcf_list.append({
        'date': 'TTM',
        'price_to_fcf': key_metrics_ttm[0]['pfcfRatioTTM']
    })
    for i in range(0, len(key_metrics)):
        price_to_fcf_list.append({ 
            'date': key_metrics[i]['date'],
            'price_to_fcf': key_metrics[i]['pfcfRatio']
        })

    return price_to_fcf_list

def plot_price_to_fcf(symbol, price_to_fcf_list):
    dates = [entry['date'] for entry in price_to_fcf_list][::-1]
    price_to_fcfs = [entry['price_to_fcf'] for entry in price_to_fcf_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Price to FCF', x=dates, y=price_to_fcfs)
    ])

    fig.update_layout(
        title=f'{symbol} Price to Free Cash Flow (P/FCF) Over Time',
        xaxis_title='Date',
        yaxis_title='P/FCF',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def get_price_to_ocf(key_metrics, key_metrics_ttm):
    price_to_ocf_list = []
    price_to_ocf_list.append({
        'date': 'TTM',
        'price_to_ocf': key_metrics_ttm[0]['pocfratioTTM']
    })
    for i in range(0, len(key_metrics)):
        price_to_ocf_list.append({ 
            'date': key_metrics[i]['date'],
            'price_to_ocf': key_metrics[i]['pocfratio']
        })

    return price_to_ocf_list

def plot_price_to_ocf(symbol, price_to_ocf_list):
    dates = [entry['date'] for entry in price_to_ocf_list][::-1]
    price_to_ocfs = [entry['price_to_ocf'] for entry in price_to_ocf_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Price to Operating Cash Flow', x=dates, y=price_to_ocfs)
    ])

    fig.update_layout(
        title=f'{symbol} Price to Operating Cash Flow (P/OCF) Over Time',
        xaxis_title='Date',
        yaxis_title='P/OCF',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def get_ev_to_sales(key_metrics, key_metrics_ttm):
    ev_to_sales_list = []
    ev_to_sales_list.append({
        'date': 'TTM',
        'ev_to_sales': key_metrics_ttm[0]['evToSalesTTM']
    })
    for i in range(0, len(key_metrics)):
        ev_to_sales_list.append({ 
            'date': key_metrics[i]['date'],
            'ev_to_sales': key_metrics[i]['evToSales']
        })
    
    return ev_to_sales_list

def plot_ev_to_sales(symbol, ev_to_sales_list):
    dates = [entry['date'] for entry in ev_to_sales_list][::-1]
    ev_to_sales = [entry['ev_to_sales'] for entry in ev_to_sales_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='EV to Sales', x=dates, y=ev_to_sales)
    ])

    fig.update_layout(
        title=f'{symbol} Enterprise Value to Sales (EV/Sales) Over Time',
        xaxis_title='Date',
        yaxis_title='EV/Sales',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def get_ev_to_ocf(key_metrics, key_metrics_ttm):
    ev_to_ocf_list = []
    ev_to_ocf_list.append({
        'date': 'TTM',
        'ev_to_ocf': key_metrics_ttm[0]['evToOperatingCashFlowTTM']
    })
    for i in range(0, len(key_metrics)):
        ev_to_ocf_list.append({ 
            'date': key_metrics[i]['date'],
            'ev_to_ocf': key_metrics[i]['evToOperatingCashFlow']
        })
    
    return ev_to_ocf_list

def plot_ev_to_ocf(symbol, ev_to_ocf_list):
    dates = [entry['date'] for entry in ev_to_ocf_list][::-1]
    ev_to_ocf = [entry['ev_to_ocf'] for entry in ev_to_ocf_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='EV to Operating Cash Flow', x=dates, y=ev_to_ocf)
    ])

    fig.update_layout(
        title=f'{symbol} Enterprise Value to Operating Cash Flow (EV/OCF) Over Time',
        xaxis_title='Date',
        yaxis_title='EV/OCF',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def get_ev_to_fcf(key_metrics, key_metrics_ttm):
    ev_to_fcf_list = []
    ev_to_fcf_list.append({
        'date': 'TTM',
        'ev_to_fcf': key_metrics_ttm[0]['evToFreeCashFlowTTM']
    })
    for i in range(0, len(key_metrics)):
        ev_to_fcf_list.append({ 
            'date': key_metrics[i]['date'],
            'ev_to_fcf': key_metrics[i]['evToFreeCashFlow']
        })
    
    return ev_to_fcf_list

def plot_ev_to_fcf(symbol, ev_to_fcf_list):
    dates = [entry['date'] for entry in ev_to_fcf_list][::-1]
    ev_to_fcf = [entry['ev_to_fcf'] for entry in ev_to_fcf_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='EV to Free Cash Flow', x=dates, y=ev_to_fcf)
    ])

    fig.update_layout(
        title=f'{symbol} Enterprise Value to Free Cash Flow (EV/FCF) Over Time',
        xaxis_title='Date',
        yaxis_title='EV/FCF',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def get_dividend_yield(key_metrics, key_metrics_ttm):
    dividend_yield_list = []
    dividend_yield_list.append({
        'date': 'TTM',
        'dividend_yield': key_metrics_ttm[0]['dividendYieldTTM']
    })
    for i in range(0, len(key_metrics)):
        dividend_yield_list.append({ 
            'date': key_metrics[i]['date'],
            'dividend_yield': key_metrics[i]['dividendYield']
        })
    
    return dividend_yield_list

def plot_dividend_yield(symbol, dividend_yield_list):
    dates = [entry['date'] for entry in dividend_yield_list][::-1]
    dividend_yields = [entry['dividend_yield'] for entry in dividend_yield_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Dividend Yield', x=dates, y=dividend_yields)
    ])

    fig.update_layout(
        title=f'{symbol} Dividend Yield Over Time',
        xaxis_title='Date',
        yaxis_title='Dividend Yield',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def get_debt_to_equity_ratio(financial_ratios, financial_ratios_ttm):
    debt_to_equity_ratio_list = []
    debt_to_equity_ratio_list.append({
        'date': 'TTM',
        'debt_to_equity_ratio': financial_ratios_ttm[0]['debtEquityRatioTTM']
    })
    for i in range(0, len(financial_ratios)):
        debt_to_equity_ratio_list.append({ 
            'date': financial_ratios[i]['date'],
            'debt_to_equity_ratio': financial_ratios[i]['debtEquityRatio']
        })

    return debt_to_equity_ratio_list

def plot_debt_to_equity_ratio(symbol, debt_to_equity_ratio_list):
    dates = [entry['date'] for entry in debt_to_equity_ratio_list][::-1]
    debt_to_equity_ratios = [entry['debt_to_equity_ratio'] for entry in debt_to_equity_ratio_list][::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=debt_to_equity_ratios,
        mode='lines+markers',
        name='Debt to Equity Ratio',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=f'{symbol} Debt to Equity Ratio Over Time',
        xaxis_title='Date',
        yaxis_title='Debt to Equity Ratio',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    return fig

def get_total_debt_to_cap(financial_ratios, financial_ratios_ttm):
    total_debt_to_cap_list = []
    total_debt_to_cap_list.append({
        'date': 'TTM',
        'total_debt_to_cap': financial_ratios_ttm[0]['totalDebtToCapitalizationTTM']
    })
    for i in range(0, len(financial_ratios)):
        total_debt_to_cap_list.append({ 
            'date': financial_ratios[i]['date'],
            'total_debt_to_cap': financial_ratios[i]['totalDebtToCapitalization']
        })

    return total_debt_to_cap_list

def plot_total_debt_to_cap(symbol, total_debt_to_cap_list):
    dates = [entry['date'] for entry in total_debt_to_cap_list][::-1]
    total_debt_to_caps = [entry['total_debt_to_cap'] for entry in total_debt_to_cap_list][::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=total_debt_to_caps,
        mode='lines+markers',
        name='Total Debt to Capitalization',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=f'{symbol} Total Debt to Capitalization Over Time',
        xaxis_title='Date',
        yaxis_title='Total Debt to Capitalization',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    return fig

def get_current_ratio(financial_ratios, financial_ratios_ttm):
    current_ratio_list = []
    current_ratio_list.append({
        'date': 'TTM',
        'current_ratio': financial_ratios_ttm[0]['currentRatioTTM']
    })
    for i in range(0, len(financial_ratios)):
        current_ratio_list.append({ 
            'date': financial_ratios[i]['date'],
            'current_ratio': financial_ratios[i]['currentRatio']
        })

    return current_ratio_list

def get_quick_ratio(financial_ratios, financial_ratios_ttm):
    quick_ratio_list = []
    quick_ratio_list.append({
        'date': 'TTM',
        'quick_ratio': financial_ratios_ttm[0]['quickRatioTTM']
    })
    for i in range(0, len(financial_ratios)):
        quick_ratio_list.append({ 
            'date': financial_ratios[i]['date'],
            'quick_ratio': financial_ratios[i]['quickRatio']
        })

    return quick_ratio_list

def plot_current_quick_ratio(symbol, current_ratio_list, quick_ratio_list):
    dates = [entry['date'] for entry in current_ratio_list][::-1]
    current_ratios = [entry['current_ratio'] for entry in current_ratio_list][::-1]
    quick_ratios = [entry['quick_ratio'] for entry in quick_ratio_list][::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=current_ratios,
        mode='lines+markers',
        name='Current Ratio',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))

    fig.add_trace(go.Scatter(
        x=dates,
        y=quick_ratios,
        mode='lines+markers',
        name='Quick Ratio',
        line=dict(color='green', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=f'{symbol} Current and Quick Ratios Over Time',
        xaxis_title='Date',
        yaxis_title='Ratio',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    return fig

def plot_current_ratio(symbol, current_ratio_list):
    dates = [entry['date'] for entry in current_ratio_list][::-1]
    current_ratios = [entry['current_ratio'] for entry in current_ratio_list][::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=current_ratios,
        mode='lines+markers',
        name='Current Ratio',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=f'{symbol} Current Ratio Over Time',
        xaxis_title='Date',
        yaxis_title='Current Ratio',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    return fig

def get_working_capital(key_metrics, key_metrics_ttm):
    working_capital_list = []
    working_capital_list.append({
        'date': 'TTM',
        'working_capital': key_metrics_ttm[0]['workingCapitalTTM']
    })
    for i in range(0, len(key_metrics)):
        working_capital_list.append({ 
            'date': key_metrics[i]['date'],
            'working_capital': key_metrics[i]['workingCapital']
        })

    return working_capital_list

def plot_working_capital(symbol, working_capital_list):
    dates = [entry['date'] for entry in working_capital_list][::-1]
    working_capitals = [entry['working_capital'] for entry in working_capital_list][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Working Capital', x=dates, y=working_capitals)
    ])

    fig.update_layout(
        title=f'{symbol} Working Capital Over Time',
        xaxis_title='Date',
        yaxis_title='Working Capital',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

def get_capex_operating_cashflow(key_metrics, key_metrics_ttm):
    capex_operating_cashflow_list = []
    capex_operating_cashflow_list.append({
        'date': 'TTM',
        'capex_operating_cashflow': key_metrics_ttm[0]['capexToOperatingCashFlowTTM']
    })
    for i in range(0, len(key_metrics)):
        capex_operating_cashflow_list.append({ 
            'date': key_metrics[i]['date'],
            'capex_operating_cashflow': key_metrics[i]['capexToOperatingCashFlow']
        })

    return capex_operating_cashflow_list

def plot_capex_operating_cashflow(symbol, capex_operating_cashflow_list):
    dates = [entry['date'] for entry in capex_operating_cashflow_list][::-1]
    capex_operating_cashflows = [entry['capex_operating_cashflow'] for entry in capex_operating_cashflow_list][::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=capex_operating_cashflows,
        mode='lines+markers',
        name='Capex to Operating Cash Flow',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=f'{symbol} Capex to Operating Cash Flow Over Time',
        xaxis_title='Date',
        yaxis_title='Capex to Operating Cash Flow',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    return fig

def get_capex_per_share(key_metrics, key_metrics_ttm):
    capex_per_share_list = []
    capex_per_share_list.append({
        'date': 'TTM',
        'capex_per_share': key_metrics_ttm[0]['capexPerShareTTM']
    })
    for i in range(0, len(key_metrics)):
        capex_per_share_list.append({ 
            'date': key_metrics[i]['date'],
            'capex_per_share': key_metrics[i]['capexPerShare']
        })

    return capex_per_share_list

def plot_capex_per_share(symbol, capex_per_share_list):
    dates = [entry['date'] for entry in capex_per_share_list][::-1]
    capex_per_shares = [entry['capex_per_share'] for entry in capex_per_share_list][::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=capex_per_shares,
        mode='lines+markers',
        name='Capex to Operating Cash Flow',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=f'{symbol} Capex to Operating Cash Flow Over Time',
        xaxis_title='Date',
        yaxis_title='Capex to Operating Cash Flow',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    return fig

def get_product_revenue_segment(symbol, period):
    url = f"https://financialmodelingprep.com/api/v4/revenue-product-segmentation?symbol={symbol}&structure=flat&period={period}&apikey={api_key}"
    response = requests.get(url)
    revenue_segments = response.json()

    return revenue_segments

def plot_revenue_segments(symbol, revenue_segments):

    # Extract dates and segment names
    dates = [list(segment.keys())[0] for segment in revenue_segments if list(segment.keys())[0][:4] >= '2012']
    all_segments = set()
    for segment in revenue_segments:
        date = list(segment.keys())[0]
        if date[:4] >= '2012':
            all_segments.update(segment[date].keys())
    
    # Initialize data dictionary
    data = {segment: [] for segment in all_segments}
    for segment in revenue_segments:
        date = list(segment.keys())[0]
        if date[:4] >= '2012':
            for seg in all_segments:
                data[seg].append(segment[date].get(seg, 0))
    
    # Reverse the dates and data
    dates = dates[::-1]
    for seg in data:
        data[seg] = data[seg][::-1]
    
    # Create the plot
    fig = go.Figure()
    colors = ['rgb(158,202,225)', 'rgb(255,127,80)', 'rgb(34,139,34)', 'rgb(255,215,0)', 'rgb(75,0,130)', 'rgb(255,69,0)', 'rgb(0,191,255)', 'rgb(255,20,147)', 'rgb(0,128,0)', 'rgb(128,0,128)']
    
    for i, (segment, values) in enumerate(data.items()):
        fig.add_trace(go.Bar(
            name=segment,
            x=dates,
            y=values,
            marker_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        title=f'{symbol} Revenue Segments Over Time',
        xaxis_title='Date',
        yaxis_title='Revenue',
        barmode='stack',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )
    
    return fig

def get_revenue_geo_segment(symbol, period):
    url = f"https://financialmodelingprep.com/api/v4/revenue-geographic-segmentation?symbol={symbol}&structure=flat&period={period}&apikey={api_key}"
    response = requests.get(url)
    revenue_geo_segments = response.json()

    return revenue_geo_segments

def plot_revenue_geo_segments(symbol, revenue_geo_segments):
    # Extract dates and segment names
    dates = [list(segment.keys())[0] for segment in revenue_geo_segments if list(segment.keys())[0][:4] >= '2012']
    all_segments = set()
    for segment in revenue_geo_segments:
        date = list(segment.keys())[0]
        if date[:4] >= '2012':
            all_segments.update(segment[date].keys())
    
    # Initialize data dictionary
    data = {segment: [] for segment in all_segments}
    for segment in revenue_geo_segments:
        date = list(segment.keys())[0]
        if date[:4] >= '2012':
            for seg in all_segments:
                data[seg].append(segment[date].get(seg, 0))
    
    # Reverse the dates and data
    dates = dates[::-1]
    for seg in data:
        data[seg] = data[seg][::-1]
    
    # Create the plot
    fig = go.Figure()
    colors = ['rgb(158,202,225)', 'rgb(255,127,80)', 'rgb(34,139,34)', 'rgb(255,215,0)', 'rgb(75,0,130)', 'rgb(255,69,0)', 'rgb(0,191,255)', 'rgb(255,20,147)', 'rgb(0,128,0)', 'rgb(128,0,128)']
    
    for i, (segment, values) in enumerate(data.items()):
        fig.add_trace(go.Bar(
            name=segment,
            x=dates,
            y=values,
            marker_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        title=f'{symbol} Revenue Geographical Segments Over Time',
        xaxis_title='Date',
        yaxis_title='Revenue',
        barmode='stack',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )
    
    return fig

def get_employee_count(symbol):
    url = f'https://financialmodelingprep.com/api/v4/historical/employee_count?symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    employee_count = response.json()

    return employee_count

def plot_employee_count(symbol, employee_count):
    dates = [entry['filingDate'] for entry in employee_count][::-1]
    employee_counts = [entry['employeeCount'] for entry in employee_count][::-1]

    fig = go.Figure(data=[
        go.Bar(name='Employee Count', x=dates, y=employee_counts)
    ])

    fig.update_layout(
        title=f'{symbol} Annual Employee Count Over Time',
        xaxis_title='Date',
        yaxis_title='Employee Count',
        xaxis=dict(type='category', title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title_font=dict(size=14, color='black'), tickfont=dict(size=14, color='black'))
    )

    fig.update_traces(
        marker_color='rgb(158,202,225)',
        width=0.25
    )
    return fig

