

import numpy as np
import pandas as pd
from functions.blackscholes import BSOption
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
plt.style.use("seaborn-dark")




if __name__ == "__main__":

    
    Smin  = 50
    Smax  = 150
    nres  = 200
    S     = np.linspace(Smin,Smax,nres)
    K     = 100
    r     = 0.01
    sigma = 0.30 
    q     = 0
    
    
    # Initial values
    T0 = 0.3
    
    # Calls and Puts
    call  = [BSOption("C", s, K, T0, r, sigma, q=q) for s in S]
    
    price = [c.price() for c in call]
    delta = [c.delta() for c in call]
    gamma = [c.gamma() for c in call]
    vega  = [c.vega()  for c in call]

    
    fig = plt.figure() #figsize=(15,20))
    plt.subplots_adjust(bottom = 0.25)
    ax  = fig.subplots(2,2)
    ax  = ax.flatten()

 
   
    # Slider button for Maturity (xpos, ypos, width, height)
    slidet_T_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
    slider_T    = Slider(slidet_T_ax, "T", valmin=0, valmax=2, valinit=T0, valstep=0.2)
     
    
    def updateplot(val):
        current_T = slider_T.val
        call  = [BSOption("C", s, K, current_T, r, sigma, q=q) for s in S]
               
        p0.set_ydata([c.price() for c in call])
        p1.set_ydata([c.delta() for c in call])
        p2.set_ydata([c.gamma() for c in call])
        p3.set_ydata([c.vega()  for c in call])

        fig.canvas.draw()
    
    slider_T.on_changed(updateplot)
    
    
    p0, = ax[0].plot(S, price, color="tab:blue")
    p1, = ax[1].plot(S, delta, color="tab:blue")
    p2, = ax[2].plot(S, gamma, color="tab:blue")
    p3, = ax[3].plot(S, vega,  color="tab:blue")

    ax[0].grid()
    
    ax[1].grid()
    ax[1].set_ylim([0,1])
    
    
    ax[2].grid()
    ax[3].grid()

    plt.show()
    
    
    
    
    
    
    
    
    '''
    
    
    
    
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.widgets as mw
    from scipy import stats
    
    
    mu = 1
    sigma = 3
    
    a = 2
    b = 3
    axis_color = 'lightgoldenrodyellow'
    
    
    x = [i for i in range(-100,100,1)]
    
    normal_pdf = stats.norm.pdf(x, mu, sigma)
    a_normal_pdf = [i*a for i in normal_pdf]
    ab_normal_pdf = [i*b*a for i in normal_pdf]
    
    
    fig = plt.figure()
    
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)
    ax4.axis('off')
    #sliders
    a_slider_ax  = fig.add_axes([0.6, 0.25, 0.25, 0.03])
    a_slider = mw.Slider(a_slider_ax, 'a', 1, 100, valinit = a)
    b_slider_ax = fig.add_axes([0.6, 0.4, 0.25, .03])
    b_slider = mw.Slider(b_slider_ax, 'b', 1, 100, valinit = b)
    #function for sliders
    def sliders_on_change(val):
        p1.set_ydata([x*a_slider.val for x in normal_pdf])
        p2.set_ydata([x*a_slider.val*b_slider.val for x in normal_pdf])
        fig.canvas.draw_idle()
    
    a_slider.on_changed(sliders_on_change)
    b_slider.on_changed(sliders_on_change)
    
    
    p1,=ax1.plot(x, normal_pdf, 'r-')
    p2,=ax2.plot(x, a_normal_pdf, 'bo')
    p3,=ax3.plot(x, ab_normal_pdf, 'g*')
    
    plt.show()
    
    '''
