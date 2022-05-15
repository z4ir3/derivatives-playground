'''
Interactive Black-Scholes prices and greeks plot using sliders.
Change the option parameters in the __main__ at the bottom. 
@author: leonardorocchi
'''



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from functions.blackscholes import BSOption
plt.style.use("seaborn-dark")




def interactive_option_plot(IVal):
    '''   
    Interactive plot of Black-Scholes prices and greeks using sliders 
    '''
    
    #### Create the set of Underlying prices 
    IVal["Smin"] = round(IVal["S"] * (1 - 0.50), 0)
    IVal["Smax"] = round(IVal["S"] * (1 + 0.50), 0)
    IVal["Sset"] = np.linspace(IVal["Smin"], IVal["Smax"], IVal["Sres"])
    
    #### Option data
    option  = [ BSOption(IVal["CP"], 
                         s, 
                         IVal["K"], 
                         IVal["T"], 
                         IVal["r"]/100, 
                         IVal["v"]/100, 
                         q = IVal["q"]) for s in IVal["Sset"] ]
    
    # Prices and greeks 
    prices  = [o.price()     for o in option]
    lambdas = [o.Lambda()    for o in option]
    deltas  = [o.delta()     for o in option]
    gammas  = [o.gamma()*100 for o in option]    
    thetas  = [o.theta()     for o in option]    
    vegas   = [o.vega()      for o in option]

    
    #### Set up plot window
    fig = plt.figure(figsize=(10,8), facecolor="whitesmoke")
    #
    plt.subplots_adjust(left   = 0.15,
                        bottom = 0.25,
                        hspace = 0.70)
    #
    ax = fig.subplots(3,2)
    ax = ax.flatten()


    #### Maturity slider (xpos, ypos, width, height)
    slider_T_ax = plt.axes([0.3, 0.15, 0.50, 0.015])
    slider_T    = Slider(ax        = slider_T_ax, 
                         label     = "Time to Maturity (years)", 
                         valmin    = IVal["Tmin"], 
                         valmax    = IVal["Tmax"], 
                         valstep   = IVal["Tstp"], 
                         valinit   = IVal["T"],
                         color     = "gray",
                         initcolor = "gray")
    
    # Maturity slider (xpos, ypos, width, height)
    slider_r_ax = plt.axes([0.3, 0.10, 0.50, 0.015])
    slider_r    = Slider(ax        = slider_r_ax, 
                         label     = "Risk-free interest rate (%)", 
                         valmin    = IVal["rmin"],  
                         valmax    = IVal["rmax"], 
                         valstep   = IVal["Tstp"], 
                         valinit   = IVal["r"],   
                         color     = "gray",
                         initcolor = "gray")
    
    # Maturity slider (xpos, ypos, width, height)
    slider_v_ax = plt.axes([0.3, 0.05, 0.50, 0.015])
    slider_v    = Slider(ax        = slider_v_ax, 
                         label     = "Volatility (%)", 
                         valmin    = IVal["vmin"],  
                         valmax    = IVal["vmax"], 
                         valstep   = IVal["vstp"], 
                         valinit   = IVal["v"],   
                         color     = "gray",
                         initcolor = "gray")
    
    
    # Update plot for slider moves
    def updateplot(val):
        # Current sliders values  
        current_T = slider_T.val
        current_r = slider_r.val
        current_v = slider_v.val

        
        # Update Option
        option = [ BSOption(IVal["CP"], 
                            s,  
                            IVal["K"], 
                            current_T, 
                            current_r / 100, 
                            current_v / 100, 
                            q = IVal["q"]) for s in IVal["Sset"] ]
    
        # Recompute Greeks               
        prices  = [o.price()     for o in option] 
        lambdas = [o.Lambda()    for o in option] 
        deltas  = [o.delta()     for o in option] 
        gammas  = [o.gamma()*100 for o in option] 
        thetas  = [o.theta()     for o in option] 
        vegas   = [o.vega()      for o in option] 
        
        # Set up new values 
        p0.set_ydata( prices  )
        p1.set_ydata( lambdas )
        p2.set_ydata( deltas  )
        p3.set_ydata( gammas  )
        p4.set_ydata( thetas  )
        p5.set_ydata( vegas   )

        # Set new ylims
        
        # Price
        ax[0].set_ylim([min(prices) - 0.1*max(prices), max(prices) + 0.1*max(prices)])
        
        # Lambda
        if IVal["CP"] == "C":
            if current_T != 0:
                M = lambdas[ min(np.where(np.array(lambdas) < +np.inf)[0]) ]
                ax[1].set_ylim([min(lambdas) - 0.1*min(lambdas), M + 0.1*M])
            else:
                ax[1].set_ylim(bottom = -1)
        else:
            if current_T != 0:
                m = lambdas[ max(np.where(np.array(lambdas) > - np.inf)[0] ) ]                
                ax[1].set_ylim([m + 0.1*m, max(lambdas) - 0.1*max(lambdas)])
            else:
                ax[1].set_ylim(top = +1)
        
        # Delta
        if IVal["CP"] == "C":
            ax[2].set_ylim([min(deltas) - 0.1*max(deltas), max(deltas) + 0.1*max(deltas)])
        else:
            ax[2].set_ylim([min(deltas) + 0.1*min(deltas), max(deltas) - 0.1*min(deltas)])            
        
        # Gamma
        if current_T != 0:
            ax[3].set_ylim([min(gammas) - 0.1*max(gammas), max(gammas) + 0.1*max(gammas)])         

        # Theta
        if current_T != 0:
            ax[4].set_ylim(bottom = min(thetas) + 0.5*min(thetas) if min(thetas) < 0 else min(thetas) - 0.5*min(thetas)) #, max(thetas) + 0.1*max(thetas)])
            ax[4].set_ylim(top    = max(thetas) - 1*max(thetas)   if max(thetas) < 0 else max(thetas) + 1*max(thetas)) #, max(thetas) + 0.1*max(thetas)])

        else:
            ax[4].set_ylim([-5,1])

        # Vega            
        if current_T != 0:
            ax[5].set_ylim([min(vegas)  - 0.1*max(vegas),  max(vegas)  + 0.1*max(vegas)])

        # Update figure
        fig.canvas.draw()



    # Calling the updateplot change for slider movements
    slider_T.on_changed(updateplot)
    slider_r.on_changed(updateplot)
    slider_v.on_changed(updateplot)
  
  
    # First plot (the one that will be updated as soon as sliders are touched)  
    p0, = ax[0].plot(IVal["Sset"], prices,  color="tab:blue")
    p1, = ax[1].plot(IVal["Sset"], lambdas, color="chocolate")
    p2, = ax[2].plot(IVal["Sset"], deltas,  color="tab:red")
    p3, = ax[3].plot(IVal["Sset"], gammas,  color="sandybrown")
    p4, = ax[4].plot(IVal["Sset"], thetas,  color="gray")
    p5, = ax[5].plot(IVal["Sset"], vegas,   color="forestgreen")
  
        
    # Set titles
    plt.suptitle("Black-Scholes Option playground: {} Option".format("Call" if IVal["CP"] == "C" else "Put"),
                 fontsize   = 15, 
                 fontweight = "bold",
                 color      = "k")
    ax[0].set_title("Price",  fontsize=11, fontweight="bold")
    ax[1].set_title("Lambda", fontsize=11, fontweight="bold")
    ax[2].set_title("Delta",  fontsize=11, fontweight="bold")
    ax[3].set_title("Gamma",  fontsize=11, fontweight="bold")
    ax[4].set_title("Theta",  fontsize=11, fontweight="bold")
    ax[5].set_title("Vega",   fontsize=11, fontweight="bold")

    # Set x-labels    
    ax[0].set_xlabel("Underlying $S$ (Strike $K=${})".format(IVal["K"]), fontsize=9)
    ax[1].set_xlabel("Underlying $S$ (Strike $K=${})".format(IVal["K"]), fontsize=9)
    ax[2].set_xlabel("Underlying $S$ (Strike $K=${})".format(IVal["K"]), fontsize=9)
    ax[3].set_xlabel("Underlying $S$ (Strike $K=${})".format(IVal["K"]), fontsize=9)
    ax[4].set_xlabel("Underlying $S$ (Strike $K=${})".format(IVal["K"]), fontsize=9)
    ax[5].set_xlabel("Underlying $S$ (Strike $K=${})".format(IVal["K"]), fontsize=9)

    # Set y-labels    
    ax[0].set_ylabel('USD ($)', fontsize=9, color="k")
    ax[2].set_ylabel('Percentage (%)', fontsize=9, color="k")
    ax[3].set_ylabel('Percentage (%)', fontsize=9, color="k")

    # Set grids
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    ax[3].grid()
    ax[4].grid()
    ax[5].grid()

    plt.show()
    
    return option 







if __name__ == "__main__":

    # Dictionary of initial values 
    IVal = dict()
    
    # -------------------------------------------------------------------------
    # CHANGE VALUES HERE
    # -------------------------------------------------------------------------
    
    # Option parameters
    IVal["CP"]      = "C"       # option type: either call ("C") or put ("P")
    IVal["S"]       = 100       # underlying price
    IVal["K"]       = 100       # strike price  
    IVal["T"]       = 2         # time-to-maturity (years)
    IVal["r"]       = 2         # risk-free interest rate (percentage)
    IVal["v"]       = 30        # (implied) volatility (percentage)
    IVal["q"]       = 0         # dividend yield
    
    # Resolution 
    IVal["Sres"]    = 200       # underlying resolution (number of prices for x-axis plot)
    
    # Time-to-Maturity slider 
    IVal["Tmin"]    = 0         # time-to-maturity slider min value
    IVal["Tmax"]    = 5         # time-to-maturity slider max value
    IVal["Tstp"]    = 0.05      # time-to-maturity slider step value
    
    # Risk-free rate slider 
    IVal["rmin"]    = 0.1       # risk-free interest rate slider min value (percentage)
    IVal["rmax"]    = 7         # risk-free interest rate slider max value (percentage)
    IVal["rstp"]    = 0.1       # risk-free interest rate slider step value (percentage)
    
    # Volatility slider
    IVal["vmin"]    = 1         # (implied) volatility slider min value (percentage)
    IVal["vmax"]    = 100       # (implied) volatility slider max value (percentage)
    IVal["vstp"]    = 1         # (implied) volatility slider step value (percentage)

    # -------------------------------------------------------------------------


    # Calling the interactive plot routine    
    option = interactive_option_plot(IVal)

    
# end scriptfile
