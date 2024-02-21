import nsepython as np
import math
from scipy.stats import norm
import pandas as pd

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

def calculate_deltas(security_name):
    σ = np.indiavix()
    p = np.quote_derivative(security_name)
    
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
    return df


security_name = 'SBIN'
df = calculate_deltas(security_name)
print(df)