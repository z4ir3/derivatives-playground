# from ast import Return
import numpy as np
import tkinter as tk
from tkinter import messagebox
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.style.use("seaborn-dark")

from blackscholes import BSOption


class Window:
    '''
    '''
    def __init__(self, root):
        '''
        '''
        self.root = root  
        self.root.title("Black-Scholes playground") 
        self.root.geometry("1250x850")

        # Left main box 
        self.framel = tk.Frame(master = self.root, relief = tk.RAISED, bg="#E4E4E0", borderwidth = 1)
        self.framel.place(relx = 0.02, rely = 0.02, relwidth = 0.3, relheight = 0.95)
    
    
        # Call or Put
        self.label_CP = tk.Label(master = self.framel, text="Call or Put (C/P)")
        self.label_CP.rowconfigure(0, weight = 1, minsize = 15)
        self.label_CP.columnconfigure(0, weight = 1, minsize = 15)
        self.label_CP.grid(row = 0, column = 0, padx = 25, pady = 10, sticky="nsew")
        #
        # cp = tk.StringVar()
        # self.entry_CP = tk.Entry(master = self.framel, width = 6, textvariable = cp)
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
        self.entry_r.insert(0, 1)
        
    

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
        self.Smin   = self.get_Smin()
        self.Smax   = self.get_Smax()
        self.Sset   = self.get_Sset()


        # ---------------
        # Right frame
        # ---------------

        # Right main box containing the interactive plot
        self.framer = tk.Frame(master = self.root, bg="#80c1ff")
        self.framer.place(relx=0.35, rely=0.02, relwidth=0.60, relheight=0.95)


        # Setup plot Figure 
        self.fig = plt.figure(facecolor = "whitesmoke")
        #
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
        self.slider_T_ax = plt.axes([0.3, 0.15, 0.50, 0.015])
        self.slider_r_ax = plt.axes([0.3, 0.10, 0.50, 0.015])
        self.slider_v_ax = plt.axes([0.3, 0.05, 0.50, 0.015])

        self.slider_T = self.define_slider_T()
        self.slider_r = self.define_slider_r()
        self.slider_v = self.define_slider_v()



        # Calling the interactive plot method as soon as a slider is touched
        self.slider_T.on_changed(self.interactiveplot)


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
            messagebox.showerror("Option type error", "Enter either 'C' or 'P'")
        else:
            return CP


    
    # @staticmethod 
    # def get_CP(self.entry_CP.get()):
    #     return str(self.entry_CP.get()) 
    

    # @staticmethod 
    def get_K(self):
        return float(self.entry_K.get()) 

    # @staticmethod 
    def get_T(self):
        return float(self.entry_T.get())
    
    # @staticmethod 
    def get_r(self):
        return float(self.entry_r.get()) / 100 
    
    # @staticmethod 
    def get_v(self):
        return float(self.entry_v.get()) / 100
        
    # @staticmethod 
    def get_q(self):
        return float(self.entry_q.get())

    # @staticmethod 
    def get_Smin(self):
        return round(self.K * (1 - 0.60), 0)

    # @staticmethod 
    def get_Smax(self):
        return round(self.K * (1 + 0.60), 0)
        
    # @staticmethod 
    def get_Sset(self):
        return np.linspace(self.Smin, self.Smax, 150)

    # def axslider_T_ax(self):
    #     return plt.axes([0.3, 0.15, 0.50, 0.015])
        
    def define_slider_T(self):
        '''
        '''
        return Slider(ax = self.slider_T_ax, 
                    label     = "Time to Maturity (years)", 
                    valmin    = 0, 
                    valmax    = 5, 
                    valstep   = 0.05, 
                    valinit   = self.T,
                    color     = "gray",
                    initcolor = "gray")


    # def axslider_r_ax(self):
    #     '''
    #     '''
    #     return plt.axes([0.3, 0.05, 0.50, 0.015])
    
    def define_slider_r(self):
        '''
        '''
        return Slider(ax      = self.slider_r_ax, 
                    label     = "Risk-free interest rate (%)", 
                    valmin    = 0.1,  
                    valmax    = 7, 
                    valstep   = 0.1, 
                    valinit   = self.r,   
                    color     = "gray",
                    initcolor = "gray")


    # def axslider_v_ax(self):
    #     '''
    #     '''
    #     return plt.axes([0.3, 0.05, 0.50, 0.015])
    
    def define_slider_v(self):
        '''
        '''
        return Slider(ax      = self.slider_v_ax, 
                    label     = "Volatility (%)", 
                    valmin    = 1,  
                    valmax    = 100, 
                    valstep   = 1, 
                    valinit   = self.v,   
                    color     = "gray",
                    initcolor = "gray")



    def computeoption(self):
        '''
        '''        
        # # Get inserted data 
        # self.CP = str(self.entry_CP.get()) 
        # self.K  = float(self.entry_K.get()) 
        # self.T  = float(self.entry_T.get())
        # self.r  = float(self.entry_r.get()) / 100 
        # self.v  = float(self.entry_v.get()) / 100
        # self.q  = float(self.entry_q.get())

        # Get inserted data 
        self.CP     = self.get_CP()
        self.K      = self.get_K() 
        self.T      = self.get_T()
        self.r      = self.get_r() 
        self.v      = self.get_v()
        self.q      = self.get_q()
        self.Smin   = self.get_Smin()
        self.Smax   = self.get_Smax()
        self.Sset   = self.get_Sset()



        # # Create the set of Underlying prices 
        # self.Smin = round(self.K * (1 - 0.60), 0)
        # self.Smax = round(self.K * (1 + 0.60), 0)
        # self.Sset = np.linspace(self.Smin, self.Smax, 150)
    
        # Calculate Option  
        self.option = [ BSOption(self.CP, 
                                 s, 
                                 self.K, 
                                 self.T, 
                                 self.r, 
                                 self.v, 
                                 q = self.q) for s in self.Sset ]




        self.firstplot()




    def firstplot(self):
        # self.setupfigure()
        print("button pushed")
        
        for axn in range(len(self.ax)):
            self.ax[axn].clear()


        self.prices  = [o.price()     for o in self.option]
        self.lambdas = [o.Lambda()    for o in self.option]
        
        # print(self.prices[30:40])
        # print(self.ax[0])
        
        self.p0, = self.ax[0].plot(self.Sset, self.prices,  color="tab:blue")
        self.p1, = self.ax[1].plot(self.Sset, self.lambdas, color="chocolate")

        self.ax[0].set_xlabel("Underlying $S$", fontsize=9)

        self.ax[0].grid()    
        self.ax[1].grid()      



        # # Maturity slider (xpos, ypos, width, height)
        # self.slider_T_ax = plt.axes([0.3, 0.15, 0.50, 0.015])
        # self.slider_T    = Slider(ax        = self.slider_T_ax, 
        #                           label     = "Time to Maturity (years)", 
        #                           valmin    = 0, 
        #                           valmax    = 5, 
        #                           valstep   = 0.05, 
        #                           valinit   = self.T,
        #                           color     = "gray",
        #                           initcolor = "gray")


        # self.slider_T.on_changed(self.interactiveplot())
        # self.slider_T.on_changed(self.interactiveplot())







        self.update()







    # def setupfigure(self):
    
    #     # # Setup Figure 
    #     # self.fig = plt.figure(facecolor = "whitesmoke")
    #     # #
    #     # plt.subplots_adjust(left   = 0.075,
    #     #                     right  = 0.95,
    #     #                     top    = 0.95,
    #     #                     bottom = 0.22,
    #     #                     hspace = 0.65)

    #     # self.ax = self.fig.subplots(3,2)
    #     # self.ax = self.ax.flatten()
            
    #     # self.canvas = FigureCanvasTkAgg(self.fig, self.framer)
    #     # self.canvas.get_tk_widget().pack(fill = "both", expand = True)


    #     # Maturity slider (xpos, ypos, width, height)
    #     self.slider_T_ax = plt.axes([0.3, 0.15, 0.50, 0.015])
    #     self.slider_T    = Slider(ax        = self.slider_T_ax, 
    #                               label     = "Time to Maturity (years)", 
    #                               valmin    = 0, 
    #                               valmax    = 5, 
    #                               valstep   = 0.05, 
    #                               valinit   = self.T,
    #                               color     = "gray",
    #                               initcolor = "gray")


    #     self.slider_T.on_changed(self.interactiveplot())











    def interactiveplot(self, val):



        print("slider moved")
 


        print(self.slider_T.val)

        # Update Option
        self.option  = [ BSOption(self.CP, 
                                s, 
                                self.K, 
                                self.slider_T.val, 
                                self.r, 
                                self.v, 
                                q = self.q) for s in self.Sset ]



        self.prices  = [o.price()     for o in self.option]
        self.lambdas = [o.Lambda()    for o in self.option]
        # self.deltas  = [o.delta()     for o in option]
        # self.gammas  = [o.gamma()*100 for o in option]    
        # self.thetas  = [o.theta()     for o in option]    
        # # self.vegas   = [o.vega()      for o in option]
  
  
        # print(self.prices[40:50])
        # print(self.ax[0])
        

        self.p0.set_ydata(self.prices)
        self.p1.set_ydata(self.lambdas)

        # self.p0, = self.ax[0].plot(self.Sset, self.prices,  color="tab:blue")
        # self.p1, = self.ax[1].plot(self.Sset, self.lambdas, color="chocolate")


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



    # gui.slider_T.on_changed(gui.interactiveplot())

    
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