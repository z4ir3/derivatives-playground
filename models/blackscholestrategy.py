'''
Black-Scholes option pricing class
Copyright (c) @author: leonardorocchi
'''

import pandas as pd
import numpy as np
from scipy.stats import norm
# from models.blackscholes_new import BSOption


class BSOption:
    
    def __init__(self, CP, S, K, T, r, v, q = 0):
        '''
        - CP    : either "C" (Call) or "P" (Put)
        - S     : underlying Price 
        - K     : strike Price
        - r     : risk-free interest rate
        - T     : time-to-maturity in years 
        - v     : implied volatility
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
            raise ValueError("Argument 'CP' must be either 'C' or 'P'")
            
    @staticmethod 
    def valid_underlying(S):
        '''
        Validate input underlying price
        '''
        if S > 0:
            return S
        else:
            raise ValueError("Argument 'S' (underlying price) must be greater than 0")
            
    @staticmethod 
    def valid_strike(K):
        '''
        Validate input strike price
        '''
        if K > 0:
            return K
        else:
            raise ValueError("Argument 'K' (strike price) must be greater than 0")
    
    @staticmethod 
    def valid_maturity(T):
        '''
        Validate input maturity
        '''
        if T >= 0:
            return T
        else:
            raise ValueError("Argument 'T' (maturity) cannot be negative")

    @staticmethod 
    def valid_intrate(r):
        '''
        Validate input interest rate
        '''
        if r >= 0:
            return r
        else:
            raise ValueError("Argument 'r' (interest rate) cannot be negative")

    @staticmethod 
    def valid_vola(v):
        '''
        Validate input volatility
        '''
        if v > 0:
            return v
        else:
            raise ValueError("Argument 'v' (volatility) must be greater than 0")
    
    @staticmethod 
    def valid_yield(q):
        '''
        Validate input dividend yield
        '''
        if q >= 0:
            return q
        else:
            raise ValueError("Argument 'q' (dividend yield) cannot be negative")
       
    @property
    def params(self):
        '''
        Returns all input option parameters
        '''
        return {"type": self.CP,
                "S"   : self.S, 
                "K"   : self.K, 
                "T"   : self.T,
                "r"   : self.r,
                "v"   : self.v,
                "q"   : self.q}
     
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

    def d1(self, S):
        '''
        Compute the quantity d1 of Black-Scholes option pricing
        '''
        return ( np.log(S / self.K) + (self.r - self.q + 0.5*self.v**2)*self.T ) / (self.v * np.sqrt(self.T))
        
    def d2(self, S):
        '''
        Compute the quantity d2 of Black-Scholes option pricing
        '''
        return self.d1(S) - self.v * np.sqrt(self.T)
    
    def price(self, *argv):
        '''
        Black-Scholes pricing model - Premium (Price)
        '''
        try:
            S = argv[0]
        except:
            S = self.S
        
        if self.CP == "C":
            # Call Option
            if self.T > 0:
                # The Call has not expired yet
                return + S * np.exp(-self.q*self.T) * self.N(self.d1(S))  \
                       - self.K * np.exp(-self.r*self.T) * self.N(self.d2(S))
                       
            else:
                # The Call has expired
                return max(S - self.K, 0)
            
        else: 
            # Put Option
            if self.T > 0:
                # The Put has not expired yet
                return - S * np.exp(-self.q*self.T) * self.N(-self.d1(S))  \
                       + self.K * np.exp(-self.r*self.T) * self.N(-self.d2(S))
                       
            else:
                # The Put has expired
                return max(self.K - S, 0)
      
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
    
    def underlying_set(self, *argv):
        '''
        Generate a set of underlying prices lower and higher than the current input underlying price
        The limit is currently (-40%,+40%) of the input underlying price
        '''
        try:
            S = argv[0]
        except:
            S = self.S
        Smin = S * (1 - 0.40)
        Smax = S * (1 + 0.40)
        return list(np.linspace(Smin,S,100)[:-1]) + list(np.linspace(S,Smax,100))
        
    def setprices(self):
        '''
        Generate a pd.Series of option prices using the set of the generated underlying prices 
        '''
        oprices = [self.price(p) for p in self.underlying_set()]
        oprices = pd.Series(oprices, index=self.underlying_set())
        return oprices 




class BSOptStrat:
    '''
    Class for generating option strategies. Pricing done with Black-Scholes model
    '''
    def __init__(self, S=100, r=0.02, q=0):
        '''
        - S : Underlying Price 
        - r : risk-free interest rate
        - q : dividend yield
        '''
        self.S              = S
        self.r              = r
        self.q              = q
        self.instruments    = [] 
        self.payoffs        = BSOptStrat.init_payoffs(S)
        self.payoffs_exp    = BSOptStrat.init_payoffs(S)
        self.payoffs_exp_df = pd.DataFrame()
    

    def init_payoffs(S):
        '''
        Generating a set of underlying prices from the given input current underlying price S
        '''
        ss = pd.Series([0] * len(BSOption.underlying_set(0,S)), index = BSOption.underlying_set(0,S))
        return ss
 
        
    def call(self, NP=+1, K=100, T=0.25, v=0.30, M=100, optprice=None):
        '''
        Creating a Call Option 
        - NP : Net Position, >0 for long positions, <0 for short positions 
        - K  : Strike price
        - T  : Time-to-Maturity in years 
        - v  : Volatility
        - M  : Multiplier of the Option (number of stocks allowed to buy/sell)
        '''
        # Create Call Option with current data
        option = BSOption("C", self.S, K, T, self.r, v, q=self.q)
        
        # Call payoff before expiration (T>0)
        if optprice is not None:
            call_price = optprice
        else:
            call_price = option.price()
        
        # Generating the set of payoff for at different underlying prices 
        # Here, option.setprices() are the prices of the call (i.e., as if it were long)
        # - If NP > 0, the price must be paid, then:
        #   payoffs = option.setprices() * NP * M  - Call price * NP * M
        # - If NP < 0, the price is to be received, then:
        #   payoffs = Call price * abs(NP) * M - option.setprices() * abs(NP) * M 
        #           = option.setprices() * NP * M  - Call price * NP * M
        # Summary: ( option.setprices() - call_price ) * NP * M
        payoffs = ( option.setprices() - call_price ) * NP * M

        # Update strategy instruments with current instrument data
        self.update_strategy("C", call_price, NP, K, T, v, M, payoffs)
        
        # Update strategy with current instrument data at maturity 
        self.option_at_exp("C", call_price, NP, K, v, M)
            

    def put(self, NP=+1, K=100, T=0.25, v=0.30, M=100, optprice=None):
        '''
        Creating a Put Option 
        - NP : Net Position, >0 for long positions, <0 for short positions 
        - K  : Strike price
        - T  : Time-to-Maturity in years 
        - v  : Volatility
        - M  : Multiplier of the Option (number of stocks allowed to buy/sell)
        '''
        # Create Put Option with current data
        option = BSOption("P", self.S, K, T, self.r, v, q=self.q)
        
        # Call payoff before expiration (T>0)
        if optprice is not None:
            put_price = optprice
        else:
            put_price = option.price()
        
        # Generating the set of payoff for at different underlying prices 
        payoffs = ( option.setprices() - put_price) * NP * M
            
        # Update strategy instruments with current instrument data
        self.update_strategy("P", put_price, NP, K, T, v, M, payoffs)
        
        # Update strategy with current instrument data at maturity 
        self.option_at_exp("P", put_price, NP, K, v, M)


    def update_strategy(self, CP, price, NP, K, T, v, M, payoffs):
        '''
        Updates the current payoffs of the option strategy as soon as that a new option is inserted. 
        The current list of instruments composing the strategy is also updated        
        
        New input(s): 
        - price   : price of the input option 
        - payoffs : Payoff of the input option (for a set of given underlying prices)
        '''
        # Update current payoff strategy with new instrument payoff 
        self.update_payoffs(payoffs, T=T)

        # Create a dictionary with the data of the given option  
        inst = {"CP": CP,
                "NP": NP,
                "K" : K,
                "T" : T,
                "v" : v,
                "M" : M,
                "Pr": round(price,2)}
        
        # Concat new instrument to total strategy instrument list
        self.instruments.append(inst)


    def update_payoffs(self, payoffs, T=0):
        '''
        Update current payoff strategy with new instrument payoff.
        It updates either the payoff for T>0 or at maturity for T=0
        '''
        if T > 0:
            self.payoffs     = payoffs + self.payoffs
        else:
            self.payoffs_exp = payoffs + self.payoffs_exp
        
 
    def option_at_exp(self, CP, price, NP, K, v, M):
        '''
        Calculates the payoff of the option at maturity (T=0)
        '''
        # Create Option at maturity (calling class with T = 0) 
        option = BSOption(CP, self.S, K, 0, self.r, v, q=self.q)

        # Option payoff at maturity: 
        # - Call: (max(S - K;0) - C) * NP * M
        # - Put:  (P - max(S - K;0)) * NP * M
        payoffs_exp = ( option.setprices() - price ) * NP * M        

        # Update the dataframe of payoff at maturity of single options with the new current inserted option 
        self.update_payoffs_exp_df(payoffs_exp)

        # Update the strategy payoff at maturity with the one of the new current inserted option 
        self.update_payoffs(payoffs_exp, T=0)


    def update_payoffs_exp_df(self, payoffs_exp):
        '''
        Update the dataframe of payoff at maturity of single options with the new current inserted option 
        '''
        # Concat new option payoff with current dataframe
        self.payoffs_exp_df = pd.concat([self.payoffs_exp_df, pd.DataFrame(payoffs_exp)], axis=1)

        # Update columns 
        self.payoffs_exp_df.columns = [n for n in range(1,self.payoffs_exp_df.shape[1]+1)]
                
        
    def describe_strategy(self): #, stratname=None):
        '''
        This method can be called once the option has been set.
        Here, all option data saved so far in the list of instrument are now saved 
        in a dictionary and the cost of entering the strategy is also computed 
        '''       
        # Create dictionary of options inserted in the strategy 
        StratData = dict()
        
        stratcost = 0
        for n, o in enumerate(self.instruments):
        
            # Key of the dictionay (Option number) 
            StratData["Option_{}".format(n+1)] = o
            
            # Compute total strategy cost: sum of NLVs (Net Liquidation Value) of the option
            # NLV = price * net position * multiplier
            stratcost = stratcost + o["Pr"] * o["NP"] * o["M"]
            
        # Save the strategy cost
        StratData["Cost"] = stratcost

        return StratData
        
        
    def get_payoffs_exp_df(self):
        '''
        Returns a dataframe with the payoff at maturity of the strategy's option
        '''
        return self.payoffs_exp_df


    def get_payoffs(self):
        '''
        Returns the current strategy payoff
        '''
        return self.payoffs

    
    def get_payoffs_exp(self):
        '''
        Returns the strategy payoff at maturity 
        '''
        return self.payoffs_exp