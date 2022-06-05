import pandas as pd
import numpy as np
from scipy.stats import norm


class BSOption:
    
    def __init__(self, CP, S, K, T, r, v, q = 0):
        '''
        - CP    : either "C" (Call) or "P" (Put)
        - S     : underlying Price 
        - K     : strike Price
        - r     : risk-free interest rate
        - T     : time-to-maturity in years 
        - sigma : implied volatility
        - q     : dividend yield
        '''
        self.CP = BSOption.valid_option(CP)
        self.S  = BSOption.valid_underlying(S)    
        self.K  = BSOption.valid_strike(K)
        self.T  = BSOption.valid_maturity(T)
        self.r  = BSOption.valid_intrate(r)
        self.v  = BSOption.valid_vola(v)
        self.q  = BSOption.valid_yield(q)
    
    @staticmethod 
    def valid_option(CP):
        '''
        Validate input option type
        '''
        if CP in ["C","P"]:
            return CP
        else:
            raise ValueError("First class argument 'CP' must be either 'C' or 'P'")
            
    @staticmethod 
    def valid_underlying(S):
        '''
        Validate input underlying price
        '''
        if S > 0:
            return S
        else:
            raise ValueError("Second class argument 'S' (underlying price) must be greater than 0")
            
    @staticmethod 
    def valid_strike(K):
        '''
        Validate input strike price
        '''
        if K > 0:
            return K
        else:
            raise ValueError("Third argument 'K' (strike price) must be greater than 0")
    
    @staticmethod 
    def valid_maturity(T):
        '''
        Validate input maturity
        '''
        if T >= 0:
            return T
        else:
            raise ValueError("Fourth argument 'T' (maturity) cannot be negative")

    @staticmethod 
    def valid_intrate(r):
        '''
        Validate input interest rate
        '''
        if r >= 0:
            return r
        else:
            raise ValueError("Fifth argument 'r' (interest rate) cannot be negative")

    @staticmethod 
    def valid_vola(sigma):
        '''
        Validate input volatility
        '''
        if sigma > 0:
            return sigma
        else:
            raise ValueError("Sixth argument 'sigma' (volatility) must be greater than 0")
    
    @staticmethod 
    def valid_yield(q):
        '''
        Validate input dividend yield
        '''
        if q >= 0:
            return q
        else:
            raise ValueError("Seventh argument 'q' (dividend yield) cannot be negative")
       
    @property
    def params(self):
        '''
        Returns all input option parameters
        '''
        return {"type"  : self.CP,
                "S"     : self.S, 
                "K"     : self.K, 
                "T"     : self.T,
                "r"     : self.r,
                "sigma" : self.v,
                "q"     : self.q}
     
    @staticmethod
    def N(x, cum=1):
        '''
        Standard Normal CDF or PDF evaluated at the input point x.
        '''  
        if cum:
            # Returns the standard normal CDF
            return norm.cdf(x, loc=0, scale=1)
        else:
            # Returns the standard normal PDF
            return norm.pdf(x, loc=0, scale=1)

    def d1(self):
        '''
        Computte the quantity d1 of Black-Scholes option pricing
        '''
        return ( np.log(self.S / self.K) + (self.r - self.q + 0.5*self.v**2)*self.T ) / (self.v * np.sqrt(self.T))
        
    def d2(self):
        '''
        Computte the quantity d2 of Black-Scholes option pricing
        '''
        return self.d1() - self.v * np.sqrt(self.T)
    
    def price(self):
        '''
        Black-Scholes pricing model - Premium (Price)
        '''
        if self.CP == "C":
            # Call Option
            if self.T > 0:
                # The Call has not expired yet
                return + self.S * np.exp(-self.q*self.T) * self.N(self.d1())  \
                        - self.K * np.exp(-self.r*self.T) * self.N(self.d2())
                       
            else:
                # The Call has expired
                return max(self.S - self.K, 0)
            
        else: 
            # Put Option
            if self.T > 0:
                # The Put has not expired yet
                return - self.S * np.exp(-self.q*self.T) * self.N(-self.d1())  \
                        + self.K * np.exp(-self.r*self.T) * self.N(-self.d2())
                       
            else:
                # The Put has expired
                return max(self.K - self.S, 0)
      
    def delta(self):
        '''
        Black-Scholes pricing model - Delta
        '''    
        if self.CP == "C":
            # Call Option
            if self.T > 0:
                # The Call has not expired yet
                return np.exp(-self.q*self.T) * self.N(self.d1()) 
            
            else:
                # The Call has expired
                if self.price() > 0:
                    return +1
                else: 
                    return 0
                
        else: 
            # Put Option
            if self.T > 0:
                # The Put has not expired yet
                return np.exp(-self.q*self.T) * self.N(self.d1()) - 1
            
            else:
                # The Put has expired
                if self.price() > 0:
                    return -1
                else:             
                    return 0

    def Lambda(self):
        '''
        Black-Scholes pricing model - Lambda
        '''
        if self.CP == "C":
            # Call option
            if self.delta() < 1e-10 or self.price() < 1e-10:
                return +np.inf
            else:
                return self.delta() * self.S / self.price()
        
        else:
            # Put option 
            if self.delta() > -1e-10 or self.price() < 1e-10:
                return -np.inf
            else:
                return self.delta() * self.S / self.price()
                     
    def gamma(self):
        '''
        Black-Scholes pricing model - Gamma 
        '''    
        # Gamma is the same for both Call and Put            
        if self.T > 0:
            # The Option has not expired yet
            return + np.exp(-self.q*self.T) * self.N(self.d1(), cum=0) / (self.S * self.v * np.sqrt(self.T))
            
        else:
            # The Option has expired
            return 0
    
    def theta(self):
        '''
        Black-Scholes pricing model - Theta
        '''
        if self.CP == "C":
            # Call Option
            if self.T > 0:
                # The Call has not expired yet
                return - np.exp(-self.q*self.T) * self.S * self.v * self.N(self.d1(), cum=0) / (2*np.sqrt(self.T)) \
                       + self.q*np.exp(-self.q*self.T) * self.S * self.N(self.d1())   \
                       - self.r*np.exp(-self.r*self.T) * self.K * self.N(self.d2())
            
            else:
                # The Call has expired
                return 0
            
        else: 
            # Put Option
            if self.T > 0:
                # The Put has not expired yet
                return - np.exp(-self.q*self.T) * self.S * self.v * self.N(self.d1(), cum=0) / (2*np.sqrt(self.T)) \
                       - self.q*np.exp(-self.q*self.T) * self.S * (1 - self.N(self.d1()))   \
                       + self.r*np.exp(-self.r*self.T) * self.K * (1 - self.N(self.d2()))
                       
            else:
                # The Put has expired
                return 0

    def vega(self):
        '''
        Black-Scholes pricing model - Vega 
        '''    
        # Vega is the same for both Call and Put            
        if self.T > 0:
            # The Option has not expired yet
            return +np.exp(-self.q*self.T) * self.S * np.sqrt(self.T) * self.N(self.d1(), cum=0) 
            
        else:
            # The Option has expired
            return 0          
            
    def greeks(self):
        '''
        Black-Scholes pricing model - All greeks
        '''   
        return {"Lambda": np.round( BSOption.Lambda(self), 2),
                "Delta" : np.round( BSOption.delta(self),  2),
                "Gamma" : np.round( BSOption.gamma(self),  2),
                "Theta" : np.round( BSOption.theta(self),  2),
                "Vega"  : np.round( BSOption.vega(self) ,  2)}