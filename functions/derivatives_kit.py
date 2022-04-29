import pandas as pd
import numpy as np
from scipy.stats import norm


class STKOption:
    
    def __init__(self, S, K, T, r, sigma, q = 0, optype = "C"):
        '''
        - S      : underlying Price 
        - K      : strike Price
        - r      : risk-free interest rate
        - T      : time-to-maturity in years 
        - sigma  : implied volatility
        - q      : 
        - optype : either "C" (Call) or "P" (Put)
        '''
        self.S      = S    
        self.K      = K
        self.T      = T
        self.r      = r 
        self.sigma  = sigma
        self.q      = q
        self.optype = optype
    
    
    @property
    def params(self):
        return {"type"  : self.optype,
                "S"     : self.S, 
                "K"     : self.K, 
                "T"     : self.T,
                "r"     : self.r,
                "sigma" : self.sigma,
                "q"     : self.q}

    
    @staticmethod
    def N(x, mu = 0, sigma = 1):
        '''
        Normal CDF evaluated at the input point x.
        
        inputs:
        - x     : evaluation point 
        - mu    : mean 
        - sigma : standard deviation 
        '''  
        return norm.cdf(x, loc=mu, scale=sigma)

    
    def h(self):
        haux = np.log( (self.S / self.K) * np.exp( (self.r - self.q)*self.T ) )  
        hh   = haux / (self.sigma * np.sqrt(self.T))  +  0.5 * self.sigma * np.sqrt(self.T)        
        return hh

    
    def price(self):
        '''
        Black-Scholes pricing model - Premium (Price)
        '''
        if self.optype == "C":
            
            if self.T > 0:
                # The Call has not expired yet
                return + self.S * np.exp(-self.q*self.T) * self.N(self.h())  \
                       - self.K * np.exp(-self.r*self.T) * self.N(self.h() - self.sigma*np.sqrt(self.T))
            else:
                # The Call has expired
                return max(self.S - self.K, 0)
            
        elif self.optype == "P":

            if self.T > 0:
                # The Put has not expired yet
                return - self.S * np.exp(-self.q*self.T) * self.N(-self.h())  \
                       + self.K * np.exp(-self.r*self.T) * self.N(-self.h() + self.sigma*np.sqrt(self.T))
            else:
                # The Put has expired
                return max(self.K - self.S, 0)
            
        else: 
            raise ValueError('Wrong Option Type')
    
    
    def delta(self):
        '''
        Black-Scholes pricing model - Delta
        '''
        pass
    
        if self.optype == "C":
            
            if self.T > 0:
                # The Call has not expired yet
                return +np.exp(-self.q*self.T) * self.N(self.h()) 
            
            else:
                # The Call has expired
                if self.price() > 0:
                    return +1
                else: 
                    return 0
            
        elif self.optype == "P":
            
            if self.T > 0:
                # The Put has not expired yet
                return -np.exp(-self.q*self.T) * self.N(-self.h())
            
            else:
                # The Put has expired
                if self.price(self) > 0:
                    return -1
                else:             
                    return 0
    
    
    def gamma(self):
        '''
        Black-Scholes pricing model - Gamma 
        '''
        pass
    
        # Gamma is the same for both Call and Put            
        if self.T > 0:
            # The Option has not expired yet
            return +np.exp(-self.q*self.T) * self.N(self.h()) / (self.S * self.sigma * np.sqrt(self.T))
            
        else:
            # The Option has expired
            return 0
    
    def vega(self):
        '''
        Black-Scholes pricing model - Vega 
        '''
        pass
    
        # Vega is the same for both Call and Put            
        if self.T > 0:
            # The Option has not expired yet
            return +np.exp(-self.q*self.T) * self.S * np.sqrt(self.T) * self.N(self.h()) 
            
        else:
            # The Option has expired
            return 0          
        

# end scriptfile