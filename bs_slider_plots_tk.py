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
        self.framelcolbg = "#E4E4E0"


        # ---------------
        # Left frame
        # ---------------
        self.framel = tk.Frame(master = self.root, relief = tk.RAISED, bg=self.framelcolbg, borderwidth = 1)
        self.framel.place(relx = 0.02, rely = 0.02, relwidth = 0.23, relheight = 0.95)
    
    
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


        # Button calculate option
        self.button = tk.Button(master = self.framel, text="Calculate", command = self.computeoption)
        self.button.rowconfigure(6, weight=1, minsize=6)
        self.button.columnconfigure(0, weight=1, minsize=6)
        self.button.grid(columnspan=2) #row=6, column=1) #, padx=20, pady=10, sticky="nsew")


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








        self.message1 = ''''''

        self.text_box1 = tk.Label(master = self.framel, 
                        text = self.message1,
                        bg = self.framelcolbg, 
                        relief = "solid")
        self.text_box1.grid(columnspan=2, padx=20, pady=20, sticky="nsew") 
        self.text_box1.configure(font = ("Helvetica Neue", 12, "normal") )




        # self.text_box = tk.Text(master = self.framel, 
        #                     height = 4, 
        #                     width  = 35, 
        #                     relief = "flat", 
        #                     bg="#E4E4E0", 
        #                     borderwidth = 0)
        # self.text_box.grid(columnspan=2, padx=20, pady=20, sticky="nsew") #row=7, column=0, padx=20, pady=10, sticky="nsew")
        # self.text_box.insert('end', self.message)
        # self.text_box.config(state='disabled')
        # self.text_box.configure(font = ("Helvetica Neue", 11, "normal") )

        self.img1 = ""
        # img1 = img1.resize((240,19), Image.ANTIALIAS)
        # self.img1 = ImageTk.PhotoImage(img1)
        self.pic1 = tk.Label(master=self.framel, 
                    image = self.img1, 
                    bg = self.framelcolbg, 
                    relief = "solid",
                    width = 10)
        self.pic1.grid(columnspan=5, padx=8, pady=3, sticky="nsew") #row=7, column=0, padx=20, pady=10, sticky="nsew")
        
        


       








        ##### to see supported font 
        # from tkinter import font
        # print(font.families())


























        # ---------------
        # Right frame
        # ---------------

        # Right main box containing the interactive plot
        self.framer = tk.Frame(master = self.root, bg="#80c1ff")
        self.framer.place(relx=0.27, rely=0.02, relwidth=0.70, relheight=0.95)


        # Setup plot Figure 
        self.fig = plt.figure(facecolor = "whitesmoke")
        
        # Subplot spaces
        plt.subplots_adjust(left   = 0.070,
                            right  = 0.95,
                            top    = 0.93,
                            bottom = 0.17,
                            hspace = 0.5,
                            wspace = 0.15)

        # Plot title
        plt.suptitle("Black-Scholes Option playground: {} Option".format("Call" if self.CP == "C" else "Put"),
                    fontsize   = 15, 
                    fontweight = "bold",
                    color      = "k")

        # self.ax = self.fig.subplots(3,2)
        # self.ax = self.ax.flatten()
            
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


    def updatedescription(self):
        '''
        '''

        auxoption = "Call" if self.CP == "C" else "Put"
        self.message1 = '''
The Black-Scholes ''' + auxoption + ''' price is given by:
        '''

        self.text_box1.configure(text=self.message1)

        if auxoption == "Call":
            img1 = (Image.open("data/callprice.png")) 
        else:
            img1 = (Image.open("data/putprice.png")) 
        img1 = img1.resize((240,19), Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(img1)

        self.pic1.configure(image=self.img1)







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
        xfontsize = 8
        self.ax[0].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)
        self.ax[1].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)
        self.ax[2].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)
        self.ax[3].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)
        self.ax[4].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)
        self.ax[5].set_xlabel("Underlying $S$ (Strike={:.0f})".format(self.K), fontsize=xfontsize)

        # Set y-labels    
        yfontsize = 8
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

        # Set titles 
        # self.ax[0].set_title("Price",  fontsize=11, fontweight="bold")
        # self.ax[1].set_title("Lambda", fontsize=11, fontweight="bold")
        # self.ax[2].set_title("Delta",  fontsize=11, fontweight="bold")
        # self.ax[3].set_title("Gamma",  fontsize=11, fontweight="bold")
        # self.ax[4].set_title("Theta",  fontsize=11, fontweight="bold")
        # self.ax[5].set_title("Vega",   fontsize=11, fontweight="bold") 

        # self.ax[0].set_xticklabels(self.Sset, fontsize=10)
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