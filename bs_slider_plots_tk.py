'''
Copyright (c) Leonardo Rocchi
'''
# from ast import Return
import numpy as np
import tkinter as tk
from tkinter import messagebox
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from sklearn.metrics import v_measure_score
plt.style.use("seaborn-dark")

from functions.blackscholes import BSOption


class Window:
    '''
    '''
    def __init__(self, root):
        '''
        '''
        self.root = root  
        self.root.title("Black-Scholes playground") 
        self.root.geometry("1250x850")

        # ---------------
        # Left frame
        # ---------------
        self.framel = tk.Frame(master = self.root, relief = tk.RAISED, bg="#E4E4E0", borderwidth = 1)
        self.framel.place(relx = 0.02, rely = 0.02, relwidth = 0.3, relheight = 0.95)
    
    
        # Call or Put
        self.label_CP = tk.Label(master = self.framel, text="Call or Put (C/P)")
        self.label_CP.rowconfigure(0, weight = 1, minsize = 15)
        self.label_CP.columnconfigure(0, weight = 1, minsize = 15)
        self.label_CP.grid(row = 0, column = 0, padx = 25, pady = 10, sticky="nsew")
        #
        self.entry_CP = tk.Entry(master = self.framel, width = 6)
        self.entry_CP.rowconfigure(0, weight = 1, minsize = 15)
        self.entry_CP.columnconfigure(0, weight = 1, minsize = 15)
        self.entry_CP.grid(row = 0, column = 1, padx = 20, pady = 10, sticky="nsew")
        # Default value
        self.entry_CP.insert(0, "C")
        
            
        # Strike Price
        self.label_K = tk.Label(master = self.framel, text="Strike Price")
        self.label_K.rowconfigure(1, weight=1, minsize=15)
        self.label_K.columnconfigure(0, weight=1, minsize=15)
        self.label_K.grid(row=1, column=0, padx=25, pady=10, sticky="nsew")
        #
        self.entry_K = tk.Entry(master = self.framel, width=6)
        self.entry_K.rowconfigure(1, weight=1, minsize=6)
        self.entry_K.columnconfigure(0, weight=1, minsize=6)
        self.entry_K.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        # Default value
        self.entry_K.insert(0, 100)
            
        
        # Maturity 
        self.label_T = tk.Label(master = self.framel, text="Maturity (years)")
        self.label_T.rowconfigure(2, weight=1, minsize=15)
        self.label_T.columnconfigure(0, weight=1, minsize=15)
        self.label_T.grid(row=2, column=0, padx=25, pady=10, sticky="nsew")
        #
        self.entry_T = tk.Entry(master = self.framel, width=6)
        self.entry_T.rowconfigure(2, weight=1, minsize=6)
        self.entry_T.columnconfigure(0, weight=1, minsize=6)
        self.entry_T.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")
        # Default value
        self.entry_T.insert(0, 0.25)
        
        
        # Interest Rate 
        self.label_r = tk.Label(master = self.framel, text="Interest rate (%)")
        self.label_r.rowconfigure(3, weight=1, minsize=15)
        self.label_r.columnconfigure(0, weight=1, minsize=15)
        self.label_r.grid(row=3, column=0, padx=25, pady=10, sticky="nsew")
        #
        self.entry_r = tk.Entry(master = self.framel, width=6)
        self.entry_r.rowconfigure(3, weight=1, minsize=6)
        self.entry_r.columnconfigure(0, weight=1, minsize=6)
        self.entry_r.grid(row=3, column=1, padx=20, pady=10, sticky="nsew")
        # Default value
        self.entry_r.insert(0, 2)
        

        # Volatility
        self.label_v = tk.Label(master = self.framel, text="Volatility (%)")
        self.label_v.rowconfigure(4, weight=1, minsize=15)
        self.label_v.columnconfigure(0, weight=1, minsize=15)
        self.label_v.grid(row=4, column=0, padx=25, pady=10, sticky="nsew")
        #
        self.entry_v = tk.Entry(master = self.framel, width=6)
        self.entry_v.rowconfigure(4, weight=1, minsize=6)
        self.entry_v.columnconfigure(0, weight=1, minsize=6)
        self.entry_v.grid(row=4, column=1, padx=20, pady=10, sticky="nsew")
        # Default value
        self.entry_v.insert(0, 30)


        # Dividend Yield
        self.label_q = tk.Label(master = self.framel, text="Dividend Yield")
        self.label_q.rowconfigure(5, weight=1, minsize=15)
        self.label_q.columnconfigure(0, weight=1, minsize=15)
        self.label_q.grid(row=5, column=0, padx=25, pady=10, sticky="nsew")
        #
        self.entry_q = tk.Entry(master = self.framel, width=6)
        self.entry_q.rowconfigure(5, weight=1, minsize=6)
        self.entry_q.columnconfigure(0, weight=1, minsize=6)
        self.entry_q.grid(row=5, column=1, padx=20, pady=10, sticky="nsew")
        # Default value
        self.entry_q.insert(0, 0)


        # Get inserted data 
        self.CP     = self.get_CP()
        self.K      = self.get_K() 
        self.T      = self.get_T()
        self.r      = self.get_r() 
        self.v      = self.get_v()
        self.q      = self.get_q()
        self.Smin   = self.get_Smin(self.K)
        self.Smax   = self.get_Smax(self.K)
        self.Sset   = self.get_Sset(self.Smin, self.Smax)


        # ---------------
        # Right frame
        # ---------------

        # Right main box containing the interactive plot
        self.framer = tk.Frame(master = self.root, bg="#80c1ff")
        self.framer.place(relx=0.35, rely=0.02, relwidth=0.60, relheight=0.95)


        # Setup plot Figure 
        self.fig = plt.figure(facecolor = "whitesmoke")
        plt.subplots_adjust(left   = 0.075,
                            right  = 0.95,
                            top    = 0.95,
                            bottom = 0.22,
                            hspace = 0.65)

        self.ax = self.fig.subplots(3,2)
        self.ax = self.ax.flatten()
            
        self.canvas = FigureCanvasTkAgg(self.fig, self.framer)
        self.canvas.get_tk_widget().pack(fill = "both", expand = True)


        # Define sliders
        self.slider_T_ax = plt.axes([0.3, 0.12, 0.50, 0.015])
        self.slider_r_ax = plt.axes([0.3, 0.07, 0.50, 0.015])
        self.slider_v_ax = plt.axes([0.3, 0.02, 0.50, 0.015])

        self.slider_T = self.define_slider(self.slider_T_ax,
                                            labl = "Time to Maturity (years)", 
                                            vmin = 0, 
                                            vmax = 5, 
                                            vstp = 0.05, 
                                            vini = self.T)

        self.slider_r = self.define_slider(self.slider_r_ax,
                                            labl = "Risk-free interest rate (%)", 
                                            vmin = 1, 
                                            vmax = 7, 
                                            vstp = 0.1, 
                                            vini = self.r * 100)

        self.slider_v = self.define_slider(self.slider_v_ax,
                                            labl = "Volatility (%)", 
                                            vmin = 1, 
                                            vmax = 100, 
                                            vstp = 1, 
                                            vini = self.v * 100)


        # Calling the interactive plot method as soon as a slider is touched
        self.slider_T.on_changed(self.onslide)
        self.slider_r.on_changed(self.onslide)
        self.slider_v.on_changed(self.onslide)


        # Button calculate option
        self.button = tk.Button(master = self.framel, text="Calculate", command = self.computeoption)
        self.button.rowconfigure(6, weight=1, minsize=6)
        self.button.columnconfigure(0, weight=1, minsize=6)
        self.button.grid(row=6, column=1) #, padx=20, pady=10, sticky="nsew")



    def get_CP(self):
        '''
        Get the Call or Put entry
        '''
        CP = str(self.entry_CP.get()) 
        if CP not in ["C","P"]:
            messagebox.showerror("Option type error", "Enter either 'C' or 'P' in the Call/Put field")
        else:
            return CP


    def get_K(self):
        '''
        Get the Strike price entry
        '''
        K = float(self.entry_K.get()) 
        if K < 1:
            messagebox.showerror("Strike value error", "Enter at least a strike price equal to 1")
        else:
            return K


    def get_T(self):
        '''
        Get the Maturity entry 
        '''
        T = float(self.entry_T.get())
        if T < 0:
            # If a negative maturity is entered, then return 0 (expiration)
            return 0 
        else:
            return T


    def get_r(self):
        '''
        Get the Interest Rate entry 
        '''
        r = float(self.entry_r.get())
        if r < 0.01:
            # Returns a mininum of 0.01% (1 basis point)
            messagebox.showerror("Interest Rate value error", "Enter at least an interest rate equal to 0.01")
        else:
            return r / 100


    def get_v(self):
        '''
        Get the Volatility entry 
        '''
        v = float(self.entry_v.get()) 
        if v < 1:
            # Returns a mininum of 1%
            messagebox.showerror("Volatility value error", "Enter at least a volatility equal 1")
        else:
            return v / 100


    def get_q(self):
        '''
        Get the Dividend Yield entry 
        '''
        q = float(self.entry_q.get())
        if q < 0:
            # If a negative dividend yield is entered, then return 0
            return 0
        else:
            return q


    @staticmethod 
    def get_Smin(K):
        return round(K * (1 - 0.60), 0)


    @staticmethod 
    def get_Smax(K):
        return round(K * (1 + 0.60), 0)


    @staticmethod 
    def get_Sset(Smin, Smax):
        return np.linspace(Smin, Smax, 150)


    def define_slider(self, sliderax, labl="Slider", vmin=0, vmax=1, vstp=0.1, vini=0.5):
        '''
        Define slider for maturitiey values 
        '''
        return Slider(ax = sliderax, 
                    label     = labl, 
                    valmin    = vmin, 
                    valmax    = vmax, 
                    valstep   = vstp, 
                    valinit   = vini,
                    color     = "gray",
                    initcolor = "gray")



    # def define_slider_T(self):
    #     '''
    #     Define slider for maturitiey values 
    #     '''
    #     return Slider(ax = self.slider_T_ax, 
    #                 label     = "Time to Maturity (years)", 
    #                 valmin    = 0, 
    #                 valmax    = 5, 
    #                 valstep   = 0.05, 
    #                 valinit   = self.T,
    #                 color     = "gray",
    #                 initcolor = "gray")

    # def define_slider_r(self):
    #     '''
    #     Define slider for interest rate values 
    #     '''
    #     return Slider(ax      = self.slider_r_ax, 
    #                 label     = "Risk-free interest rate (%)", 
    #                 valmin    = 1,  
    #                 valmax    = 7, 
    #                 valstep   = 0.1, 
    #                 valinit   = self.r * 100,   
    #                 color     = "gray",
    #                 initcolor = "gray")


    # def define_slider_v(self):
    #     '''
    #     Define slider for volatility values 
    #     '''
    #     return Slider(ax      = self.slider_v_ax, 
    #                 label     = "Volatility (%)", 
    #                 valmin    = 1,  
    #                 valmax    = 100, 
    #                 valstep   = 1, 
    #                 valinit   = self.v * 100,   
    #                 color     = "gray",
    #                 initcolor = "gray")


    def computeoption(self):
        '''
        Calculate option price and greeks given the input data
        '''        
        # Recover inserted data 
        self.CP     = self.get_CP()
        self.K      = self.get_K() 
        self.T      = self.get_T()
        self.r      = self.get_r()
        self.v      = self.get_v()
        self.q      = self.get_q()
        self.Smin   = self.get_Smin(self.K)
        self.Smax   = self.get_Smax(self.K)
        self.Sset   = self.get_Sset(self.Smin, self.Smax)
    
        # Calculate Option  
        self.option = [ BSOption(self.CP, 
                                 s, 
                                 self.K, 
                                 self.T, 
                                 self.r, 
                                 self.v, 
                                 q = self.q) for s in self.Sset ]

        # Plot option price and greeks
        self.plotoption()


    def plotoption(self):
        '''
        Plot 
        '''
        
        # Clear current axis 
        for axn in range(len(self.ax)):
            self.ax[axn].clear()

        # Get prices and greeks for all set of underlyings
        self.prices  = [o.price()     for o in self.option]
        self.lambdas = [o.Lambda()    for o in self.option]
        self.deltas  = [o.delta()     for o in self.option] 
        self.gammas  = [o.gamma()*100 for o in self.option] 
        self.thetas  = [o.theta()     for o in self.option] 
        self.vegas   = [o.vega()      for o in self.option]  
        
        self.p0, = self.ax[0].plot(self.Sset, self.prices,  color="tab:blue")
        self.p1, = self.ax[1].plot(self.Sset, self.lambdas, color="chocolate")
        self.p2, = self.ax[2].plot(self.Sset, self.deltas,  color="tab:red")
        self.p3, = self.ax[3].plot(self.Sset, self.gammas,  color="sandybrown")
        self.p4, = self.ax[4].plot(self.Sset, self.thetas,  color="gray")
        self.p5, = self.ax[5].plot(self.Sset, self.vegas,   color="forestgreen")

        self.ax[0].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=9)
        self.ax[1].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=9)
        self.ax[2].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=9)
        self.ax[3].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=9)
        self.ax[4].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=9)
        self.ax[5].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=9)

        self.ax[0].grid()    
        self.ax[1].grid()      
        self.ax[2].grid()    
        self.ax[3].grid()    
        self.ax[4].grid()    
        self.ax[5].grid()    

        # Update plot
        self.update()


    def onslide(self, val):
        '''
        Recompute option data and update plot when slider values changes
        '''

        # Update Option given the new values of the sliders
        self.option  = [ BSOption(self.CP, 
                                s, 
                                self.K, 
                                self.slider_T.val, 
                                self.slider_r.val / 100, 
                                self.slider_v.val / 100, 
                                q = self.q) for s in self.Sset ]

        # Get prices and greeks for all set of underlyings for new values of the sliders
        self.prices  = [o.price()     for o in self.option]
        self.lambdas = [o.Lambda()    for o in self.option]
        self.deltas  = [o.delta()     for o in self.option]
        self.gammas  = [o.gamma()*100 for o in self.option]    
        self.thetas  = [o.theta()     for o in self.option]    
        self.vegas   = [o.vega()      for o in self.option]
  
        self.p0.set_ydata(self.prices)
        self.p1.set_ydata(self.lambdas)
        self.p2.set_ydata(self.deltas)
        self.p3.set_ydata(self.gammas)
        self.p4.set_ydata(self.thetas)
        self.p5.set_ydata(self.vegas)

        # Update plot
        self.update()


    def update(self):
        '''
        Update plot
        '''
        self.canvas.draw()





if __name__ == "__main__":
    '''
    '''
    
    root = tk.Tk()
    
    gui = Window(root)
    
    gui.root.mainloop()
    
    







# window = tk.Tk()

# window.geometry("1250x800")



# framel = tk.Frame(master=window, relief=tk.RAISED, bg="#E4E4E0", borderwidth=1)
# framel.place(relx=0.02, rely=0.02, relwidth=0.3, relheight=0.95)

# # button_K = tk.Label(master=framel, text="Strike Price")
# # button_K.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.05)


# # Call or Put
# label_K = tk.Label(master=framel, text="Call or Put")
# label_K.rowconfigure(0, weight=1, minsize=15)
# label_K.columnconfigure(0, weight=1, minsize=15)
# label_K.grid(row=0, column=0, padx=25, pady=10, sticky="nsew")

# entry_K = tk.Entry(master=framel, width=6)
# entry_K.rowconfigure(0, weight=1, minsize=15)
# entry_K.columnconfigure(0, weight=1, minsize=15)
# entry_K.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")


# # Strike Price
# label_K = tk.Label(master=framel, text="Strike Price")
# label_K.rowconfigure(1, weight=1, minsize=15)
# label_K.columnconfigure(0, weight=1, minsize=15)
# label_K.grid(row=1, column=0, padx=25, pady=10, sticky="nsew")

# entry_K = tk.Entry(master=framel, width=6)
# entry_K.rowconfigure(1, weight=1, minsize=6)
# entry_K.columnconfigure(0, weight=1, minsize=6)
# entry_K.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")


# # Maturity 
# label_T = tk.Label(master=framel, text="Maturity (years)")
# label_T.rowconfigure(2, weight=1, minsize=15)
# label_T.columnconfigure(0, weight=1, minsize=15)
# label_T.grid(row=2, column=0, padx=25, pady=10, sticky="nsew")

# entry_T = tk.Entry(master=framel, width=6)
# entry_T.rowconfigure(2, weight=1, minsize=6)
# entry_T.columnconfigure(0, weight=1, minsize=6)
# entry_T.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")




# button = Button(framel, text="Calculate", command = self.update_values)














# framer = tk.Frame(master=window, bg="#80c1ff")
# framer.place(relx=0.35, rely=0.02, relwidth=0.60, relheight=0.95)



# # fig = Figure()

# #### Set up plot window
# # fig = plt.figure(figsize=(10,8), facecolor="whitesmoke")
# fig = plt.figure(facecolor="whitesmoke")
# #
# plt.subplots_adjust(left   = 0.075,
#                     right  = 0.95,
#                     top    = 0.95,
#                     bottom = 0.22,
#                     hspace = 0.65)
# #
# ax = fig.subplots(3,2)
# ax = ax.flatten()



# canvas = FigureCanvasTkAgg(fig, framer)
# canvas.get_tk_widget().pack(fill="both", expand=True)

# # im = np.array(np.random.rand(10,10,10))

# # ax = fig.subplots(1,1)

# # axmax  = fig.add_axes([0.25, 0.01, 0.65, 0.03])
# # smax = Slider(axmax, 'Max', 0, np.max(im), valinit=50)


# # Maturity slider (xpos, ypos, width, height)
# slider_T_ax = plt.axes([0.3, 0.15, 0.50, 0.015])
# slider_T    = Slider(ax        = slider_T_ax, 
#                       label     = "Time to Maturity (years)", 
#                       valmin    = 0, 
#                       valmax    = 4, 
#                       valstep   = 0.02, 
#                       valinit   = 1,
#                       color     = "gray",
#                       initcolor = "gray")


# # # Interest Rate slider (xpos, ypos, width, height)
# # slider_r_ax = plt.axes([0.3, 0.10, 0.50, 0.015])
# # slider_r    = Slider(ax        = slider_r_ax, 
# #                      label     = "Risk-free interest rate (%)", 
# #                      valmin    = IVal["rmin"],  
# #                      valmax    = IVal["rmax"], 
# #                      valstep   = IVal["Tstp"], 
# #                      valinit   = IVal["r"],   
# #                      color     = "gray",
# #                      initcolor = "gray")

    
# # # Volatility slider (xpos, ypos, width, height)
# # slider_v_ax = plt.axes([0.3, 0.05, 0.50, 0.015])
# # slider_v    = Slider(ax        = slider_v_ax, 
# #                      label     = "Volatility (%)", 
# #                      valmin    = IVal["vmin"],  
# #                      valmax    = IVal["vmax"], 
# #                      valstep   = IVal["vstp"], 
# #                      valinit   = IVal["v"],   
# #                      color     = "gray",
# #                      initcolor = "gray")
    


# #### Option data
# option  = [ BSOption("C", 
#                       s, 
#                       100, 
#                       2.5, 
#                       5/100, 
#                       30/100, 
#                       q = 0) for s in np.linspace(50,150,100) ]



# # tracker = IndexTracker(ax, im)
# # canvas.mpl_connect('scroll_event', tracker.onscroll)
# # canvas.mpl_connect('button_release_event', tracker.contrast) #add this for contrast change

# tracker = InteractPlot(ax, option)
# # canvas.mpl_connect('scroll_event', tracker.onslide)
# # canvas.mpl_connect('button_release_event', tracker.contrast) #add this for contrast change

# slider_T.on_changed(tracker.onslide)




# window.mainloop()