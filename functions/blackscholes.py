import pandas as pd
import numpy as np
from scipy.stats import norm


class BSOption:
    
    def __init__(self, CP, S, K, T, r, sigma, q = 0):
        '''
        - CP    : either "C" (Call) or "P" (Put)
        - S     : underlying Price 
        - K     : strike Price
        - r     : risk-free interest rate
        - T     : time-to-maturity in years 
        - sigma : implied volatility
        - q     : dividend yield
        '''
        self.CP    = BSOption.valid_option(CP)
        self.S     = BSOption.valid_underlying(S)    
        self.K     = BSOption.valid_strike(K)
        self.T     = BSOption.valid_maturity(T)
        self.r     = r 
        self.sigma = BSOption.valid_vola(sigma)
        self.q     = BSOption.valid_yield(q)
    
    @staticmethod 
    def valid_option(CP):
        if CP == "C" or CP == "P":
            return CP
        else:
            raise ValueError("First argument 'CP' must be either 'C' or 'P'")
            
    @staticmethod 
    def valid_underlying(S):
        if S > 0:
            return S
        else:
            raise ValueError("Second argument 'S' must be greater than 0")
            
    @staticmethod 
    def valid_strike(K):
        if K > 0:
            return K
        else:
            raise ValueError("Third argument 'K' must be greater than 0")
    
    @staticmethod 
    def valid_maturity(T):
        if T >= 0:
            return T
        else:
            raise ValueError("Fourth argument 'T' cannot be negative")
            
    @staticmethod 
    def valid_vola(sigma):
        if sigma > 0:
            return sigma
        else:
            raise ValueError("Sixth argument 'sigma' must be greater than 0")
    
    @staticmethod 
    def valid_yield(q):
        if q >= 0:
            return q
        else:
            raise ValueError("Seventh argument 'q' cannot be negative")
     
    @property
    def params(self):
        return {"Type"  : self.CP,
                "S"     : self.S, 
                "K"     : self.K, 
                "T"     : self.T,
                "r"     : self.r,
                "sigma" : self.sigma,
                "q"     : self.q}
    
    @staticmethod
    def N(x, cum=1):
        '''
        Standard Normal CDF or PDF evaluated at the input point x.
        '''  
        if cum:
            # Returns the CDF
            return norm.cdf(x, loc=0, scale=1)
        else:
            return norm.pdf(x, loc=0, scale=1)

    

    def d1(self):
        return ( np.log(self.S / self.K) + (self.r - self.q + 0.5*self.sigma**2)*self.T ) / (self.sigma * np.sqrt(self.T))
        
    
    
    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)
    
    
    
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
        Black-Scholes pricing model - Labda
        '''
        if self.T > 0:
            # The Option has not expired yet
            return self.delta() * self.S / self.price()

        else:
            return 0


                
    def gamma(self):
        '''
        Black-Scholes pricing model - Gamma 
        '''    
        # Gamma is the same for both Call and Put            
        if self.T > 0:
            # The Option has not expired yet
            return + np.exp(-self.q*self.T) * self.N(self.d1(), cum=0) / (self.S * self.sigma * np.sqrt(self.T))
            
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
                return - np.exp(-self.q*self.T) * self.S * self.sigma * self.N(self.d1(), cum=0) / (2*np.sqrt(self.T)) \
                       + self.q*np.exp(-self.q*self.T) * self.S * self.N(self.d1())   \
                       - self.r*np.exp(-self.r*self.T) * self.K * self.N(self.d2())
            
            else:
                # The Call has expired
                return 0
            
        else: 
            # Put Option
            if self.T > 0:
                # The Put has not expired yet
                return - np.exp(-self.q*self.T) * self.S * self.sigma * self.N(self.d1(), cum=0) / (2*np.sqrt(self.T)) \
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


# end scriptfile