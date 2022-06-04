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


from PIL import ImageTk, Image

class Window:
    '''
    '''
    def __init__(self, root):
        '''
        '''
        self.root = root  
        self.root.title("Black-Scholes playground") 
        self.root.geometry("1350x850")
        #        
        self.mainbg = "#E0DFDF"
        self.root.configure(bg=self.mainbg) #"gainsboro")


        # ---------------
        # Left frame
        # ---------------
        self.framel = tk.Frame(master = self.root, 
                            relief = "flat", 
                            bg = self.mainbg, 
                            borderwidth = 1)
        self.framel.place(relx = 0.02, rely = 0.02, relwidth = 0.23, relheight = 0.95)
    
        # Label setup
        self.lab_relief = "flat"
        self.lab_bg     = self.mainbg
        self.lab_height = 1
        self.lab_font   = ("Helvetica Neue", 14, "normal")

        # Entry setup
        self.ent_htick  = 2, 
        self.ent_bordw  = 0
        self.ent_width  = 13
        self.ent_font   = ("Helvetica Neue", 14, "normal")
        self.ent_bg     = "whitesmoke"    

        # Call or Put
        row = 0
        self.label_CP = tk.Label(master = self.framel, 
                            text = "Call or Put (C/P)",
                            relief = self.lab_relief,
                            bg = self.lab_bg,
                            height = self.lab_height,
                            font = self.lab_font)
        self.label_CP.rowconfigure(row, weight = 1, minsize = 15)
        self.label_CP.columnconfigure(0, weight = 1, minsize = 15)
        self.label_CP.grid(row = row, column = 0, padx = 25, pady = (45,10), sticky="w")
        #
        self.entry_CP = tk.Entry(master = self.framel, 
                        width = self.ent_width, 
                        font = self.ent_font,
                        bg = self.ent_bg, 
                        highlightthickness = self.ent_htick, 
                        borderwidth = self.ent_bordw)
        self.entry_CP.rowconfigure(row, weight = 1, minsize = 15)
        self.entry_CP.columnconfigure(0, weight = 1, minsize = 15)
        self.entry_CP.grid(row = row, column = 1, padx = 20, pady = (45,10), sticky="nsew")
        # Default value
        self.entry_CP.insert(0, "C")
        
            
        # Strike Price
        row = row + 1
        self.label_K = tk.Label(master = self.framel, 
                            text = "Strike Price",
                            relief = self.lab_relief,
                            bg = self.lab_bg,
                            height = self.lab_height,
                            font = self.lab_font)
        self.label_K.rowconfigure(row, weight=1, minsize=15)
        self.label_K.columnconfigure(0, weight=1, minsize=15)
        self.label_K.grid(row=row, column=0, padx=25, pady=10, sticky="w")
        #
        self.entry_K = tk.Entry(master = self.framel, 
                        width = self.ent_width, 
                        font = self.ent_font,
                        bg = self.ent_bg, 
                        highlightthickness = self.ent_htick, 
                        borderwidth = self.ent_bordw)
        self.entry_K.rowconfigure(row, weight=1, minsize=6)
        self.entry_K.columnconfigure(0, weight=1, minsize=6)
        self.entry_K.grid(row = row, column = 1, padx=20, pady=10, sticky="nsew")
        # Default value
        self.entry_K.insert(0, 100)
            
        
        # Maturity 
        row = row + 1
        self.label_T = tk.Label(master = self.framel, 
                        text="Maturity (years)",
                        relief = self.lab_relief,
                        bg = self.lab_bg,
                        height = self.lab_height,
                        font = self.lab_font)
        self.label_T.rowconfigure(row, weight=1, minsize=15)
        self.label_T.columnconfigure(0, weight=1, minsize=15)
        self.label_T.grid(row = row, column = 0, padx=25, pady=10, sticky="w")
        #
        self.entry_T = tk.Entry(master = self.framel, 
                        width = self.ent_width, 
                        font = self.ent_font,
                        bg = self.ent_bg, 
                        highlightthickness = self.ent_htick, 
                        borderwidth = self.ent_bordw)
        self.entry_T.rowconfigure(row, weight=1, minsize=6)
        self.entry_T.columnconfigure(0, weight=1, minsize=6)
        self.entry_T.grid(row = row, column = 1, padx=20, pady=10, sticky="nsew")
        # Default value
        self.entry_T.insert(0, 0.25)
        
        
        # Interest Rate 
        row = row + 1
        self.label_r = tk.Label(master = self.framel, 
                            text="Interest rate (%)",
                            relief = self.lab_relief,
                            bg = self.lab_bg,
                            height = self.lab_height,
                            font = self.lab_font)
        self.label_r.rowconfigure(row, weight=1, minsize=15)
        self.label_r.columnconfigure(0, weight=1, minsize=15)
        self.label_r.grid(row = row, column = 0, padx=25, pady=10, sticky="w")
        #
        self.entry_r = tk.Entry(master = self.framel,
                        width = self.ent_width, 
                        font = self.ent_font,
                        bg = self.ent_bg, 
                        highlightthickness = self.ent_htick, 
                        borderwidth = self.ent_bordw)
        self.entry_r.rowconfigure(row, weight=1, minsize=6)
        self.entry_r.columnconfigure(0, weight=1, minsize=6)
        self.entry_r.grid(row = row, column = 1, padx=20, pady=10, sticky="nsew")
        # Default value
        self.entry_r.insert(0, 2)
        

        # Volatility
        row = row + 1
        self.label_v = tk.Label(master = self.framel, 
                            text="Volatility (%)",
                            relief = self.lab_relief,
                            bg = self.lab_bg,
                            height = self.lab_height,
                            font = self.lab_font)
        self.label_v.rowconfigure(row, weight=1, minsize=15)
        self.label_v.columnconfigure(0, weight=1, minsize=15)
        self.label_v.grid(row = row, column = 0, padx=25, pady=10, sticky="w")
        #
        self.entry_v = tk.Entry(master = self.framel, 
                        width = self.ent_width, 
                        font = self.ent_font,
                        bg = self.ent_bg, 
                        highlightthickness = self.ent_htick, 
                        borderwidth = self.ent_bordw)
        self.entry_v.rowconfigure(row, weight=1, minsize=6)
        self.entry_v.columnconfigure(0, weight=1, minsize=6)
        self.entry_v.grid(row = row, column = 1, padx=20, pady=10, sticky="nsew")
        # Default value
        self.entry_v.insert(0, 30)


        # Dividend Yield
        row = row + 1
        self.label_q = tk.Label(master = self.framel, 
                            text="Dividend Yield",
                            relief = self.lab_relief,
                            bg = self.lab_bg,
                            height = self.lab_height,
                            font = self.lab_font)
        self.label_q.rowconfigure(row, weight=1, minsize=15)
        self.label_q.columnconfigure(0, weight=1, minsize=15)
        self.label_q.grid(row = row, column = 0, padx=25, pady=10, sticky="w")
        #
        self.entry_q = tk.Entry(master = self.framel, 
                        width = self.ent_width, 
                        font = self.ent_font,
                        bg = self.ent_bg, 
                        highlightthickness = self.ent_htick, 
                        borderwidth = self.ent_bordw)
        self.entry_q.rowconfigure(row, weight=1, minsize=25)
        self.entry_q.columnconfigure(0, weight=1, minsize=25)
        self.entry_q.grid(row = row, column = 1, padx=20, pady=10, sticky="nsew")
        # Default value
        self.entry_q.insert(0, 0)


        # Button calculate option
        row = row + 1
        self.button = tk.Button(master = self.framel, 
                            text = "Calculate", 
                            highlightthickness = 0, 
                            borderwidth = 0,
                            font = self.lab_font,
                            command = self.computeoption)
        self.button.rowconfigure(row, weight=1, minsize=10)
        self.button.columnconfigure(0, weight=1, minsize=10)
        self.button.grid(columnspan = 2, padx=20, pady=15, sticky="nsew")


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



        # Descriptions
        self.descrelief = "flat" 
        self.descfont   = ("Helvetica Neue", 14, "normal")
        # To see supported font: from tkinter import font; print(font.families())

        # First text
        self.message1 = ''''''
        self.text_box1 = tk.Label(master = self.framel, 
                        text = self.message1,
                        bg = self.mainbg, 
                        relief = self.descrelief)
        self.text_box1.grid(columnspan=2, padx=20, pady = (50,20), sticky="w") 
        self.text_box1.configure(font = self.descfont)

        # First image: the Call or the Put price
        self.img0 = ""
        self.pic0 = tk.Label(master=self.framel, 
                    image = self.img0, 
                    bg = self.mainbg, 
                    relief = self.descrelief,
                    width = 10)
        self.pic0.grid(columnspan=2, padx=20, pady=0, sticky="nsew")
        
        # Second text: "where"
        self.message2 = ''''''
        self.text_box2 = tk.Label(master = self.framel, 
                        text = self.message2,
                        bg = self.mainbg, 
                        relief = self.descrelief)
        self.text_box2.grid(columnspan=2, padx=20, pady=10, sticky="w") 
        self.text_box2.configure(font = self.descfont)

        # Second image: d1
        self.img1 = ""
        self.pic1 = tk.Label(master=self.framel, 
                    image = self.img1, 
                    bg = self.mainbg, 
                    relief = self.descrelief,
                    width = 15)
        self.pic1.grid(columnspan=2, padx=20, pady=2, sticky="nsew")
        
        # Second image: d2
        self.img2 = ""
        self.pic2 = tk.Label(master=self.framel, 
                    image = self.img2, 
                    bg = self.mainbg, 
                    relief = self.descrelief,
                    width = 15)
        self.pic2.grid(columnspan=2, padx=20, pady=(10,0), sticky="nsew")
        


        # ---------------
        # Right frame
        # ---------------

        # Right main box containing the interactive plot
        self.framer = tk.Frame(master = self.root, bg="#80c1ff")
        self.framer.place(relx=0.27, rely=0.02, relwidth=0.71, relheight=0.95)


        # Setup plot Figure 
        self.fig = plt.figure(facecolor = "whitesmoke")
        
        # Subplot spaces
        plt.subplots_adjust(left   = 0.070,
                            right  = 0.95,
                            top    = 0.93,
                            bottom = 0.17,
                            hspace = 0.5,
                            wspace = 0.15)
            
        self.canvas = FigureCanvasTkAgg(self.fig, self.framer)
        self.canvas.get_tk_widget().pack(fill = "both", expand = True)


        # Define sliders
        self.slider_T_ax = plt.axes([0.3, 0.08, 0.50, 0.015])
        self.slider_r_ax = plt.axes([0.3, 0.05, 0.50, 0.015])
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



    def get_CP(self):
        '''
        Get the Call or Put entry
        '''
        CP = str(self.entry_CP.get()) 
        if CP not in ["C", "P"]:
            messagebox.showerror("Option type error", "Enter either 'C' or 'P' in the Call/Put field")
        else:
            return CP


    def get_K(self):
        '''
        Get the Strike price entry
        '''
        try:
            K = float(self.entry_K.get()) 
            if K < 1:
                messagebox.showerror("Strike value error", "Enter at least a strike price equal to 1")
            else:
                return K
        except:
            messagebox.showerror("Strike value error", "Enter a valid strike price")
    

    def get_T(self):
        '''
        Get the Maturity entry 
        '''
        try:
            T = float(self.entry_T.get())
            if T < 0:
                # If a negative maturity is entered, then return 0 (expiration)
                return 0 
            else:
                return T
        except:
            messagebox.showerror("Maturity value error", "Enter a valid maturity value")
    

    def get_r(self):
        '''
        Get the Interest Rate entry 
        '''
        try:
            r = float(self.entry_r.get())
            if r < 0.01:
                # Returns a mininum of 0.01% (1 basis point)
                messagebox.showerror("Interest Rate value error", "Enter at least an interest rate equal to 0.01")
            else:
                return r / 100
        except:
            messagebox.showerror("Interest Rate value error", "Enter a valid interest rate value")


    def get_v(self):
        '''
        Get the Volatility entry 
        '''
        try:
            v = float(self.entry_v.get()) 
            if v < 1:
                # Returns a mininum of 1%
                messagebox.showerror("Volatility value error", "Enter at least a volatility equal 1")
            else:
                return v / 100
        except:
            messagebox.showerror("Volatility value error", "Enter a valid volatility value")


    def get_q(self):
        '''
        Get the Dividend Yield entry 
        '''
        try: 
            q = float(self.entry_q.get())
            if q < 0:
                # If a negative dividend yield is entered, then return 0
                return 0
            else:
                return q
        except:
            messagebox.showerror("Dividend Yield value error", "Enter a valid dividend yield value")


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



    def computeoption(self):
        '''
        Calculate option price and greeks given the input data
        '''        
        # Recover inserted data 
        self.CP   = self.get_CP()
        self.K    = self.get_K() 
        self.T    = self.get_T()
        self.r    = self.get_r()
        self.v    = self.get_v()
        self.q    = self.get_q()
        self.Smin = self.get_Smin(self.K)
        self.Smax = self.get_Smax(self.K)
        self.Sset = self.get_Sset(self.Smin, self.Smax)
    
        # Calculate Option  
        self.option = [ BSOption(self.CP, 
                                 s, 
                                 self.K, 
                                 self.T, 
                                 self.r, 
                                 self.v, 
                                 q = self.q) for s in self.Sset ]

        # Update description
        self.updatedescription()

        # Plot option price and greeks
        self.plotoption()



    def updatedescription(self):
        '''
        '''

        # Message 1: Update Call or Put price according to entry data
        auxoption = "Call" if self.CP == "C" else "Put"
        self.message1 = '''
The Black-Scholes ''' + auxoption + ''' price is given by:
        '''
        self.text_box1.configure(text = self.message1)

        # Image 1: Updating formula for the Call or the Put
        if auxoption == "Call":
            img0 = (Image.open("data/callprice.png")) 
        else:
            img0 = (Image.open("data/putprice.png")) 
        img0 = img0.resize((240,17), Image.ANTIALIAS)
        self.img0 = ImageTk.PhotoImage(img0)
        self.pic0.configure(image=self.img0)

        # Message 2: where
        self.message2 = '''
where 
       '''
        self.text_box2.configure(text = self.message2)


        # Updating formula for d1
        img1 = (Image.open("data/d1.png")) 
        img1 = img1.resize((245,43), Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(img1)
        self.pic1.configure(image=self.img1)


        # Updating formula for d2
        img2 = (Image.open("data/d2.png")) 
        img2 = img2.resize((112,18), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(img2)
        self.pic2.configure(image=self.img2)


        # Plot title
        plt.suptitle("Black-Scholes Option Pricing: {} Option".format("Call" if self.CP == "C" else "Put"),
                    fontsize   = 15, 
                    fontweight = "bold",
                    color      = "k")


    def plotoption(self):
        '''
        Plot 
        '''
        # Clear current axis 
        try:
            for axn in range(len(self.ax)):
                self.ax[axn].clear()

        except:
            self.ax = self.fig.subplots(3,2)
            self.ax = self.ax.flatten()


        # Get prices and greeks for all set of underlyings
        self.prices  = [o.price()     for o in self.option]
        self.lambdas = [o.Lambda()    for o in self.option]
        self.deltas  = [o.delta()     for o in self.option] 
        self.gammas  = [o.gamma()*100 for o in self.option] 
        self.thetas  = [o.theta()     for o in self.option] 
        self.vegas   = [o.vega()      for o in self.option]  
        
        # Plot
        self.p0, = self.ax[0].plot(self.Sset, self.prices,  color="tab:blue")
        self.p1, = self.ax[1].plot(self.Sset, self.lambdas, color="chocolate")
        self.p2, = self.ax[2].plot(self.Sset, self.deltas,  color="tab:red")
        self.p3, = self.ax[3].plot(self.Sset, self.gammas,  color="sandybrown")
        self.p4, = self.ax[4].plot(self.Sset, self.thetas,  color="gray")
        self.p5, = self.ax[5].plot(self.Sset, self.vegas,   color="forestgreen")

        # Set x-labels
        xfontsize = 9
        self.ax[0].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)
        self.ax[1].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)
        self.ax[2].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)
        self.ax[3].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)
        self.ax[4].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)
        self.ax[5].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)

        # Set y-labels    
        yfontsize = 9
        ycol = "k"
        self.ax[0].set_ylabel("Price (USD)", fontsize=yfontsize, color=ycol)
        self.ax[1].set_ylabel("Lambda", fontsize=yfontsize, color=ycol)
        self.ax[2].set_ylabel("Delta (%)", fontsize=yfontsize, color=ycol)
        self.ax[3].set_ylabel("Gamma (%)", fontsize=yfontsize, color=ycol)
        self.ax[4].set_ylabel("Theta", fontsize=yfontsize, color=ycol)
        self.ax[5].set_ylabel("Vega", fontsize=yfontsize, color=ycol)

        # Set grids
        self.ax[0].grid()    
        self.ax[1].grid()      
        self.ax[2].grid()    
        self.ax[3].grid()    
        self.ax[4].grid()    
        self.ax[5].grid()   

        # Tick labels
        xyfontsize = 8 
        plt.setp(self.ax[0].get_xticklabels(), fontsize=xyfontsize)
        plt.setp(self.ax[0].get_yticklabels(), fontsize=xyfontsize)

        plt.setp(self.ax[1].get_xticklabels(), fontsize=xyfontsize)
        plt.setp(self.ax[1].get_yticklabels(), fontsize=xyfontsize)

        plt.setp(self.ax[2].get_xticklabels(), fontsize=xyfontsize)
        plt.setp(self.ax[2].get_yticklabels(), fontsize=xyfontsize)

        plt.setp(self.ax[3].get_xticklabels(), fontsize=xyfontsize)
        plt.setp(self.ax[3].get_yticklabels(), fontsize=xyfontsize)

        plt.setp(self.ax[4].get_xticklabels(), fontsize=xyfontsize)
        plt.setp(self.ax[4].get_yticklabels(), fontsize=xyfontsize)

        plt.setp(self.ax[5].get_xticklabels(), fontsize=xyfontsize)
        plt.setp(self.ax[5].get_yticklabels(), fontsize=xyfontsize)

        # Update plot
        self.update()



    def onslide(self, val):
        '''
        Recompute option data and update plot when slider values changes
        '''
        # Get current sliders' values
        current_T = self.slider_T.val
        current_r = self.slider_r.val
        current_v = self.slider_v.val

        # Update Option given the new values of the sliders
        self.option  = [ BSOption(self.CP, 
                                s, 
                                self.K, 
                                current_T,
                                current_r / 100, 
                                current_v / 100, 
                                q = self.q) for s in self.Sset ]

        # Get prices and greeks for all set of underlyings for new values of the sliders
        self.prices  = [o.price()     for o in self.option]
        self.lambdas = [o.Lambda()    for o in self.option]
        self.deltas  = [o.delta()     for o in self.option]
        self.gammas  = [o.gamma()*100 for o in self.option]    
        self.thetas  = [o.theta()     for o in self.option]    
        self.vegas   = [o.vega()      for o in self.option]
  
        # Update plot 
        self.p0.set_ydata(self.prices)
        self.p1.set_ydata(self.lambdas)
        self.p2.set_ydata(self.deltas)
        self.p3.set_ydata(self.gammas)
        self.p4.set_ydata(self.thetas)
        self.p5.set_ydata(self.vegas)

        # Set new axis 

        # Price
        self.ax[0].set_ylim([min(self.prices) - 0.1*max(self.prices), max(self.prices) + 0.1*max(self.prices)])
        
        # Lambda
        if self.CP == "C":
            if current_T != 0:
                M = self.lambdas[ min(np.where(np.array(self.lambdas) < +np.inf)[0]) ]
                self.ax[1].set_ylim([min(self.lambdas) - 0.1*min(self.lambdas), M + 0.1*M])
            else:
                self.ax[1].set_ylim(bottom = -1)
        else:
            if current_T != 0:
                m = self.lambdas[ max(np.where(np.array(self.lambdas) > - np.inf)[0] ) ]                
                self.ax[1].set_ylim([m + 0.1*m, max(self.lambdas) - 0.1*max(self.lambdas)])
            else:
                self.ax[1].set_ylim(top = +1)

        # Delta
        if self.CP == "C":
            self.ax[2].set_ylim([min(self.deltas) - 0.1*max(self.deltas), max(self.deltas) + 0.1*max(self.deltas)])
        else:
            self.ax[2].set_ylim([min(self.deltas) + 0.1*min(self.deltas), max(self.deltas) - 0.1*min(self.deltas)])            
        
        # Gamma
        if current_T != 0:
            self.ax[3].set_ylim([min(self.gammas) - 0.1*max(self.gammas), max(self.gammas) + 0.1*max(self.gammas)])         

        # Theta
        if current_T != 0:
            self.ax[4].set_ylim(bottom = min(self.thetas) + 0.5*min(self.thetas) if min(self.thetas) < 0 else min(self.thetas) - 0.5*min(self.thetas))
            self.ax[4].set_ylim(top    = max(self.thetas) - 1*max(self.thetas)   if max(self.thetas) < 0 else max(self.thetas) + 1*max(self.thetas))

        else:
            self.ax[4].set_ylim([-5,1])

        # Vega            
        if current_T != 0:
            self.ax[5].set_ylim([min(self.vegas)  - 0.1*max(self.vegas),  max(self.vegas)  + 0.1*max(self.vegas)])




        print(self.Sset)

        satm = np.where(self.Sset >= self.K)[0][0]
        print(self.prices[ satm ])
        print(self.lambdas[ satm ])
        print(self.deltas[ satm ])

        self.ax[0].text(0.1, 0.9, "Price {}".format(self.prices[ satm ]), ha='center', va='center', transform=self.ax[0].transAxes)









        # Update plot
        self.update()


    def update(self):
        '''
        Update plot
        '''
        self.canvas.draw()



if __name__ == "__main__":    
    root = tk.Tk()
    gui = Window(root)
    gui.root.mainloop()