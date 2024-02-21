import nsepython as np
import math
from scipy.stats import norm
import pandas as pd

def black_scholes_dexter(S0, X, t, σ, r=7.1, q=0.0, td=365):
    S0, X, σ, r, q, t = float(S0), float(X), float(σ / 100), float(r / 100), float(q / 100), float(t / td)
    
    if t == 0 or σ == 0:
        return None, None  # Return None if time to expiration or volatility is zero
    
    d1 = (math.log(S0 / X) + (r - q + 0.5 * σ ** 2) * t) / (σ * math.sqrt(t))
    
    call_delta = math.exp(-q * t) * norm.cdf(d1)
    put_delta = math.exp(-q * t) * (norm.cdf(d1) - 1)
    
    return call_delta, put_delta

def calculate_deltas(security_name):
    # Retrieve data
    p = np.quote_derivative(security_name)

    # Creating empty lists to store values
    data = {'Identifier': [], 'Close Price': [], 'Implied Volatility': [], 'Strike Price': [], 'Expiry Date': []}
    for inner_dict in p['stocks']:
        data['Identifier'].append(inner_dict['metadata']['identifier'])
        data['Close Price'].append(inner_dict['metadata']['closePrice'])
        data['Implied Volatility'].append(inner_dict['marketDeptOrderBook']['otherInfo']['impliedVolatility'])
        data['Strike Price'].append(inner_dict['metadata']['strikePrice'])
        data['Expiry Date'].append(inner_dict['metadata']['expiryDate'])

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

# Example usage:
security_name = 'RELIANCE'
df = calculate_deltas(security_name)
print(df)
