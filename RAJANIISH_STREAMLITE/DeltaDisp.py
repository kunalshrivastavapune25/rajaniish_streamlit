import nsepython as np
import math
from scipy.stats import norm
import pandas as pd
import yfinance as yf
import datetime as dt

def black_scholes_dexter(S0, X, t, σ, r=7.1, q=0.0, td=365):
    
    # S0, 
    # X, 
    # t, 
    # σ, 
    # r=10, 
    # q=0.0 
    # td=365
    
    S0, X, σ, r, q, t = float(S0), float(X), float(σ / 100), float(r / 100), float(q / 100), float(t / td)
    
    if t == 0 or σ == 0:
        return None, None  # Return None if time to expiration or volatility is zero
    
    d1 = (math.log(S0 / X) + (r - q + 0.5 * σ ** 2) * t) / (σ * math.sqrt(t))
    
    call_delta = math.exp(-q * t) * norm.cdf(d1)
    put_delta = math.exp(-q * t) * (norm.cdf(d1) - 1)
    
    return call_delta, put_delta

def calculate_deltas(σ,p):

    
    # Creating empty lists to store values
    identifier_list = []
    close_price_list = []
    implied_volatility_list = []
    strikePrice_list = []
    expiry_list = []
    for inner_dict in p['stocks']:
        identifier_list.append(inner_dict['metadata']['identifier'])
        close_price_list.append(inner_dict['metadata']['closePrice'])
        implied_volatility_list.append(inner_dict['marketDeptOrderBook']['otherInfo']['impliedVolatility'])
        strikePrice_list.append(inner_dict['metadata']['strikePrice'])
        expiry_list.append(inner_dict['metadata']['expiryDate'])    
    
    # Constructing DataFrame
    data = {
        'Identifier': identifier_list,
        'Close Price': close_price_list,
        'Implied Volatility': implied_volatility_list,
        'Strike Price': strikePrice_list,
        'Expiry Date': expiry_list
    }
    
    data['Underlying Value'] = p['underlyingValue']
    df = pd.DataFrame(data)
    
    # Add days to expiry
    df['Expiry Date'] = pd.to_datetime(df['Expiry Date'])
    df['Days to Expiry'] = (df['Expiry Date'] - pd.Timestamp.today()).dt.days
    
    # Calculate call delta and put delta for each row
    call_deltas = []
    put_deltas = []
    for index, row in df.iterrows():
        if row['Identifier'].startswith('OPT'):
            call_delta, put_delta = black_scholes_dexter(row['Underlying Value'], row['Strike Price'], row['Days to Expiry'], σ)
        else:
            call_delta, put_delta = None, None
        
        call_deltas.append(call_delta)
        put_deltas.append(put_delta) if row['Identifier'].startswith('OPT') else put_deltas.append(None)
    
    df['Call Delta'] = call_deltas
    df['Put Delta'] = put_deltas
    df['Call Delta'] = pd.to_numeric(df['Call Delta'], errors='coerce')
    filtered_df = df[df['Call Delta'] <= 0.17]
    filtered_df = filtered_df.sort_values(by=['Call Delta', 'Identifier'], ascending=[False, False])
    call_df_final = filtered_df.groupby('Expiry Date').first().reset_index()[['Identifier', 'Strike Price', 'Call Delta','Expiry Date']]

    df['Put Delta'] = pd.to_numeric(df['Put Delta'], errors='coerce')
    filtered_df = df[df['Put Delta'] >= -0.17]
    filtered_df = filtered_df.sort_values(by=['Put Delta', 'Identifier'], ascending=[True, False])
    put_df_final = filtered_df.groupby('Expiry Date').first().reset_index()[['Identifier', 'Strike Price', 'Put Delta','Expiry Date']]

    merged_df = pd.merge(call_df_final, put_df_final, on='Expiry Date', suffixes=('_call', '_put'))

    merged_df['Spot Price'] = p['underlyingValue'] 
    merged_df['Symbol'] = p['info']['symbol']
    ticker = p['info']['symbol'] + '.NS'
    data = yf.download(ticker , dt.date.today() - pd.to_timedelta('500 days'), dt.datetime.today() , interval="1d")
    std = data["Adj Close"].std()
    merged_df['std'] = std
    merged_df = merged_df[['Symbol','std','Spot Price','Expiry Date','Strike Price_call','Call Delta','Strike Price_put','Put Delta']]

    return merged_df






