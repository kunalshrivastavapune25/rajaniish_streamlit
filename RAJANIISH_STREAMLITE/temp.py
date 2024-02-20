import nsepython as np
import math
from scipy.stats import norm

def black_scholes_dexter(S0,X,t,σ="",r=10,q=0.0,td=365):
    
    if(σ==""):σ =np.indiavix()  
    
    S0,X,σ,r,q,t = float(S0),float(X),float(σ/100),float(r/100),float(q/100),float(t/td)
    #https://unofficed.com/black-scholes-model-options-calculator-google-sheet/
      
    d1 = (math.log(S0/X)+(r-q+0.5*σ**2)*t)/(σ*math.sqrt(t))
    #stackoverflow.com/questions/34258537/python-typeerror-unsupported-operand-types-for-float-and-int
      
    #stackoverflow.com/questions/809362/how-to-calculate-cumulative-normal-distribution
      
      
    call_delta =math.exp(-q*t)*norm.cdf(d1)
    put_delta =math.exp(-q*t)*(norm.cdf(d1)-1)
      
    return call_delta,put_delta



dir(np)

help(np.quote_derivative)

p = np.quote_derivative('RELIANCE')



for inner_dict in p['stocks']:
    print(inner_dict['metadata']['identifier'], 
          inner_dict['metadata']['closePrice'],
          inner_dict['metadata']['closePrice']
          ) 
    
    
for inner_dict in p['stocks']:
    print(inner_dict['marketDeptOrderBook']['otherInfo']['impliedVolatility']) 


help(np.black_scholes_dexter)

np.fnolist()


S0 = 34950.60
X = 35000.00
σ = ""
t = 3

if(σ==""):
    σ =np.indiavix()  

call_delta,put_delta=black_scholes_dexter(S0,X,t,σ,r=10,q=0.0,td=365)

print(call_delta)
print(put_delta)


# S0 = underlying price
# X = strike price
# σ = volatility
# r = continuously compounded risk-free interest rate
# q = continuously compounded dividend yield
# t = time to expiration
# For,
# σ = Volatility = India VIX has been taken.
# r = 10% (As per NSE Website, it is fixed.)
# q = 0.00% (Assumed No Dividend)
 
