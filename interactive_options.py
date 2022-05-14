#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 18:46:28 2022

@author: leonardorocchi
"""



import numpy as np
import pandas as pd
from functions.blackscholes import BSOption
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
plt.style.use("seaborn-dark")





def interactive_option_plot(IVal):
    '''    
    '''
    
    # Create the set of Underlying prices 
    IVal["Smin"] = round(IVal["S"] * (1 - 0.50), 0)
    IVal["Smax"] = round(IVal["S"] * (1 + 0.50), 0), 
    IVal["Sset"] = np.linspace(IVal["Smin"], IVal["Smax"], IVal["Sres"])
    
    # Compute Option data
    option  = [ BSOption(IVal["CP"], 
                         s, 
                         IVal["K"], 
                         IVal["T"], 
                         IVal["r"] / 100, 
                         IVal["v"], 
                         q = IVal["q"]) for s in IVal["Sset"] ]
    
    # Compute prices and greeks 
    price = [o.price() for o in option]
    delta = [o.delta() for o in option]
    gamma = [o.gamma() for o in option]    
    vega  = [o.vega()  for o in option]


    
    
    
    # Set up plot window
    fig = plt.figure(figsize=(10,7), facecolor="whitesmoke")
    #
    plt.subplots_adjust(left   = 0.1,
                        bottom = 0.30,
                        hspace = 0.50)
    #
    ax = fig.subplots(2,2)
    ax = ax.flatten()


    # Maturity slider (xpos, ypos, width, height)
    slider_T_ax = plt.axes([0.25, 0.15, 0.55, 0.02])
    slider_T    = Slider(ax        = slider_T_ax, 
                         label     = "Time to Maturity (years)", 
                         valmin    = IVal["Tmin"], 
                         valmax    = IVal["Tmax"], 
                         valstep   = IVal["Tstp"], 
                         valinit   = IVal["T"],
                         color     = "gray",
                         initcolor = "gray")
    
    # Maturity slider (xpos, ypos, width, height)
    slider_r_ax = plt.axes([0.25, 0.10, 0.55, 0.02])
    slider_r    = Slider(ax        = slider_r_ax, 
                         label     = "Risk-free rate (%)", 
                         valmin    = IVal["rmin"],  
                         valmax    = IVal["rmax"], 
                         valstep   = IVal["Tstp"], 
                         valinit   = IVal["r"],   
                         color     = "gray",
                         initcolor = "gray")
    
    # Update plot for slider moves
    def updateplot(val):
        # Current sliders values  
        current_T = slider_T.val
        current_r = slider_r.val
        
        # Update Option
        option = [ BSOption(IVal["CP"], 
                            s,  
                            IVal["K"], 
                            current_T, 
                            current_r / 100, 
                            IVal["v"], 
                            q = IVal["q"]) for s in IVal["Sset"] ]
    
        # Recompute Greeks               
        prices = [o.price() for o in option] 
        deltas = [o.delta() for o in option] 
        gammas = [o.gamma() for o in option] 
        vegas  = [o.vega()  for o in option] 
        
        # Set up new values 
        p0.set_ydata( prices )
        p1.set_ydata( deltas )
        p2.set_ydata( gammas )
        p3.set_ydata( vegas  )
        
        # Set new ylims
        ax[0].set_ylim([min(prices) - 0.1*max(prices), max(prices) + 0.1*max(prices)])
        if IVal["CP"] == "C":
            ax[1].set_ylim([min(deltas) - 0.1*max(deltas), max(deltas) + 0.1*max(deltas)])
        else:
            ax[1].set_ylim([min(deltas) + 0.1*min(deltas), max(deltas) - 0.1*min(deltas)])            
        if current_T != 0:
            ax[2].set_ylim([min(gammas) - 0.1*max(gammas), max(gammas) + 0.1*max(gammas)])            
            ax[3].set_ylim([min(vegas)  - 0.1*max(vegas),  max(vegas)  + 0.1*max(vegas)])

        # Update figure
        fig.canvas.draw()


    # Calling the updateplot change for slider movements
    slider_T.on_changed(updateplot)
    slider_r.on_changed(updateplot)
  
    # First plot (the ne that will be updated as soon as sliders are touched)  
    p0, = ax[0].plot(IVal["Sset"], price, color="tab:blue")
    p1, = ax[1].plot(IVal["Sset"], delta, color="tab:red")
    p2, = ax[2].plot(IVal["Sset"], gamma, color="sandybrown")
    p3, = ax[3].plot(IVal["Sset"], vega,  color="gray")
  
        
    # Set titles
    plt.suptitle("Black-Scholes Option pricing: {} Option".format("Call" if IVal["CP"] == "C" else "Put"),
                 fontsize   = 15, 
                 fontweight = "bold",
                 color      = "k")
    ax[0].set_title("Price", color="k")
    ax[1].set_title("Delta", color="k")
    ax[2].set_title("Gamma", color="k")
    ax[3].set_title("Vega", color="k")
    
    # Set x-labels    
    ax[0].set_xlabel("Underlying $S$ (Strike $K=${})".format(IVal["K"]), color="k")
    ax[1].set_xlabel("Underlying $S$ (Strike $K=${})".format(IVal["K"]), color="k")
    ax[2].set_xlabel("Underlying $S$ (Strike $K=${})".format(IVal["K"]), color="k")
    ax[3].set_xlabel("Underlying $S$ (Strike $K=${})".format(IVal["K"]), color="k")

    # Set y-labels    
    ax[0].set_ylabel('USD ($)', color="k")
    ax[3].set_ylabel('Percentage (%)', color="k")

    # Set grids
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    ax[3].grid()

    # Set color ticks
    ax[0].tick_params(axis="x", colors="k")
    ax[0].tick_params(axis="y", colors="k")
    ax[1].tick_params(axis="x", colors="k")
    ax[1].tick_params(axis="y", colors="k")
    ax[2].tick_params(axis="x", colors="k")
    ax[2].tick_params(axis="y", colors="k")
    ax[3].tick_params(axis="x", colors="k")
    ax[3].tick_params(axis="y", colors="k")

    plt.show()
    
    return option 







if __name__ == "__main__":

    # Dictionary of initial values 
    IVal = dict()
    
    IVal["CP"]      = "C"       # option type: either call ("C") or put ("P")
    IVal["S"]       = 100       # underlying price
    IVal["K"]       = 100       # strike price  
    IVal["T"]       = 2         # time-to-maturity 
    IVal["r"]       = 2         # risk-free interest rate (in percentage)
    IVal["v"]       = 0.3       # (implied) volatility 
    IVal["q"]       = 0         # dividend yield
    # 
    IVal["Sres"]    = 200       # undelying resolution (number of prices for x-axis plot)
    #
    # 
    IVal["Tmin"]    = 0         # time-to-maturity slider min value
    IVal["Tmax"]    = 3.5       # time-to-maturity slider max value
    IVal["Tstp"]    = 0.02      # time-to-maturity slider step value
    #
    IVal["rmin"]    = 0.1       # risk-free interesr rate slider min value (percentage)
    IVal["rmax"]    = 8         # risk-free interesr rate slider max value (percentage)
    IVal["rstp"]    = 0.1       # risk-free interesr rate slider step value (percentage)



    # Calling the interactive plot routine    
    option = interactive_option_plot(IVal)

    
    
# end scriptfile
