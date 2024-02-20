import nsepython as np
import math
from scipy.stats import norm
import pandas as pd

def black_scholes_dexter(S0, X, t, σ, r=10, q=0.0, td=365):
    
    
    S0, X, σ, r, q, t = float(S0), float(X), float(σ / 100), float(r / 100), float(q / 100), float(t / td)
      
    d1 = (math.log(S0 / X) + (r - q + 0.5 * σ ** 2) * t) / (σ * math.sqrt(t))
      
    call_delta = math.exp(-q * t) * norm.cdf(d1)
    put_delta = math.exp(-q * t) * (norm.cdf(d1) - 1)
      
    return call_delta, put_delta


σ = np.indiavix()


p = np.quote_derivative('RELIANCE')

# Creating empty lists to store values
identifier_list = []
close_price_list = []
implied_volatility_list = []
call_delta_list = []
put_delta_list = []

for inner_dict in p['stocks']:
    identifier_list.append(inner_dict['metadata']['identifier'])
    close_price_list.append(inner_dict['metadata']['closePrice'])
    implied_volatility_list.append(inner_dict['marketDeptOrderBook']['otherInfo']['impliedVolatility'])
    S0 = inner_dict['metadata']['closePrice']
    X = inner_dict['metadata']['closePrice']
#    call_delta, put_delta = black_scholes_dexter(S0, X, t=3)
#    call_delta_list.append(call_delta)
#    put_delta_list.append(put_delta)

# Constructing DataFrame
data = {
    'Identifier': identifier_list,
    'Close Price': close_price_list,
    'Implied Volatility': implied_volatility_list
#    'Call Delta': call_delta_list,
#    'Put Delta': put_delta_list
}

df = pd.DataFrame(data)

print(df)
