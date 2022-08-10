'''
GUI BS Strategy class
Interactive Option Strategy payoff calculator using Black-Scholes option pricing model 
Copyright (c) @author: leonardorocchi
'''

import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.axis import Axis
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models.blackscholestrategy import BSOptStrat


class PlotGUI:
    '''
    GUI for 
    '''
    def __init__(self, root):
        
        self.root = root  

        # GUI window title
        self.root.title("Option strategy payoff calculator") 
        
        # self.root.geometry( str(self.root.winfo_screenwidth()-5) + "x" + str(self.root.winfo_screenheight()-5) )
        self.root.geometry("1425x825")
        
        # Color palette: "light" or "dark"
        self.definepalette("light")

        # Main font of the GUI
        self.guifont = "Helvetica Neue"
        # self.guifont = "Tahoma"
        # self.guifont = "Adelle Sans Devanagari"
        # self.guifont = "Trebuchet MS"
        # self.guifont = "Verdana"
        # self.guifont = "PT Sans Caption"
        # self.guifont = "Monaco"
        # self.guifont = "Microsoft Sans Serif"
        # self.guifont = "Lucida Grande"
        # self.guifont = "Osaka"
        # self.guifont = "October Tamil"
        # self.guifont = "Al Nile"
        # self.guifont = "Al Tarikh"

        # Left frame 'Text' Title setup
        self.title_relif = "flat"   #"raised"
        self.title_font  = (self.guifont, 20, "bold")

        # Left frame 'Label' setup
        self.lab_relief = "flat"  #"raised"
        self.lab_width  = 13
        self.lab_height = 1
        self.lab_font   = (self.guifont, 14, "normal")

        # Left frame 'Entry' setup
        self.ent_htick  = 2, 
        self.ent_bordw  = 0
        self.ent_width  = 10
        self.ent_font   = ("Helvetica Neue", 14, "normal")

        # Location of the frames for a symmetric frame layout
        
        # Top-left x-coordinate (from left) starting point of the left frame
        self.left_relx = 0.02       
        
        # Top-left y-coordinate (from top) starting point of the left frame
        self.left_rely = 0.02      
        
        # x-lenght of the left frame
        self.left_relwidth = 0.55  

        # x-length space between left frame and right frame
        self.sep_frame_lr = 0.01

        # The equation for x-dimensions must be:
        # > left_relx + left_relwidth + sep_left_right + right_relwidth = 1 - left_relx
        # Fixed parameters are 'left_relx', 'left_relwidth', 'sep_left_right'.
        # Then 'right_relwidth' is given by:
        # > right_relwidth = 1 - 2*left_relx - left_relwidth - sep_left_right    
        self.left_relheight     = 1 - 2 * self.left_rely
        self.right_relx         = self.left_relx + self.left_relwidth + self.sep_frame_lr
        self.right_rely         = self.left_rely
        self.right_relwidth     = 1 - 2 * self.left_relx - self.left_relwidth - self.sep_frame_lr
        self.right_relheight    = self.left_relheight

        # tk Text widget default width (title and descriptions)
        self.deftextwidth = 60

        # Padx and Pady (top pady, bottom pady)
        self.padx               = (25,0)
        self.pady               = (5,0)
        self.first_row_padys    = (25,0)
        self.second_row_padys   = (50,0)
        self.first_addopt_padys = (25,0)    
        self.other_addopt_padys = (5,0)    

        # Title
        self.title_lframe = "Option strategy payoff calculator"

        # Button description
        self.reset_strat_button_name = "Reset Strategy"
        self.add_options_button_name = "Add Option"
        self.calculate_button_name   = "Calculate" 

        # Choose strategy label
        self.choose_strat_label_name = "Choose Strategy"

        # Set of pre-defined option strategies
        self.strat_options = ("Custom strategy",
                            "Long Call",
                            "Short Call",
                            "Long Put",
                            "Short Put",
                            "Bull Call Spread", 
                            "Bull Put Spread", 
                            "Bear Call Spread", 
                            "Bear Put Spread", 
                            "Top Strip",
                            "Bottom Strip",
                            "Top Strap",
                            "Bottom Strap",                            
                            "Top Straddle", 
                            "Bottom Straddle",
                            "Top Strangle",
                            "Bottom Strangle",
                            "Top Butterfly",
                            "Bottom Butterfly",
                            "Top Iron Condor",
                            "Bottom Iron Condor")

        # Chosen strategy (custom or predefined)
        self.chosen_strategy = None

        # Flag: True is the "Add option" button is pushed, False otherwise
        self.flag_add_option = False

        # Flag: True is the "Reset strategy" button is pushed, False otherwise
        self.flag_reset_strategy = False

        # Dictionaries
        
        # Dictionary of options data for the custom strategy
        self.CusOptData = dict()

        # Dictionary of tk.Entries values of the custom strategy
        self.Entries = dict()

        # Dictionary of tk.Labels for option prices of the custom strategy 
        self.LabPrice = dict()

        # Default payoff plot colors for the custom strategy 
        # Max colors = 5 = max number of options
        self.optioncolors = ["tab:blue", 
                            "tab:red", 
                            "forestgreen", 
                            "sandybrown", 
                            "chocolate", 
                            "gray"]

        self.payoffcolplot = "tab:blue"

        # Maximum volatility allowed
        self.maxvola = 70

        # Define the left frame of the GUI
        self.left_frame()

        # Define the right frame of the GUI
        self.right_frame()


    def left_frame(self):
        '''
        Left frame of the GUI containing options data/descriptions  
        '''
    
        # Create the left frame and place it in the GUI
        self.framel = tk.Frame(master = self.root, 
                                relief      = "flat", #raised" 
                                bg          = self.lframebg, 
                                borderwidth = 1)

        self.framel.place(relx = self.left_relx, 
                            rely        = self.left_rely, 
                            relwidth    = self.left_relwidth, 
                            relheight   = self.left_relheight)

        # Set initial row and column numbers    
        self.gridrow = 0
        self.gridcol = 0

        # Label "Title" of the frame
        self.titleframe = self.create_tktext(textheight = 1, textwidth = self.deftextwidth)
        self.config_tktext(self.titleframe, 
                            textmsg  = self.title_lframe, 
                            textrow  = self.gridrow, 
                            textpady = (20,0))

        self.gridrow = 1

        # Label "Initial Data"
        self.label_idata = self.create_tklabel(labeltext = "Initial Data:")
        self.config_tklabel(self.label_idata, labelpady = self.first_row_padys)

        self.gridcol = self.gridcol + 1

        # Label Underlying Price
        self.label_S = self.create_tklabel(labeltext = "Underlying Price")
        self.config_tklabel(self.label_S, labelpady = self.first_row_padys) 

        self.gridcol = self.gridcol + 1

        # Label Strike Price
        self.label_r = self.create_tklabel(labeltext = "Interest Rate(%)")
        self.config_tklabel(self.label_r, labelpady = self.first_row_padys) 

        self.gridcol = self.gridcol + 1

        # Label Dividend Yield
        self.label_q = self.create_tklabel(labelwidth = 13, labeltext = "Dividend Yield")
        self.config_tklabel(self.label_q, labelpady = self.first_row_padys) 

        self.gridcol = self.gridcol + 1

        # Label Maturity
        self.label_T = self.create_tklabel(labelwidth = 22, labeltext = "Strategy Expiration (years)")
        self.config_tklabel(self.label_T, labelpady = self.first_row_padys)


        # ENTRIES

        self.gridrow = 2
        self.gridcol = 0

        # Empty entry "Initial Data"
        self.label_empty = self.create_tklabel(labeltext = "")
        self.config_tklabel(self.label_empty)

        self.gridcol = self.gridcol + 1

        # Entry Underlying Price
        self.entry_S = self.create_tkentry()
        self.config_tkentry(self.entry_S, entrydefval = 100)

        self.gridcol = self.gridcol + 1
     
        # Entry Interest Rate
        self.entry_r = self.create_tkentry()
        self.config_tkentry(self.entry_r, entrydefval = 2)

        self.gridcol = self.gridcol + 1

        # Entry Dividend Yield
        self.entry_q = self.create_tkentry()
        self.config_tkentry(self.entry_q, entrydefval = 0)

        self.gridcol = self.gridcol + 1

        # Entry Maturity
        self.entry_T = self.create_tkentry()
        self.config_tkentry(self.entry_T, entrydefval = 0.25)

        # Choose strategy label

        self.gridrow = 3
        self.gridcol = 0

        # Label "choose strategy"
        self.label_strat = self.create_tklabel(labelfont = (self.lab_font[0], self.lab_font[1], "bold"),
                                                labelwidth = 16, 
                                                labeltext = self.choose_strat_label_name)
        self.config_tklabel(self.label_strat, labelpady = self.second_row_padys) 

        # Reset row and column numbers  
        self.gridrow = 4  
        self.gridcol = 0

        # Set now the default row of the tkinter grid with drop-down menu and buttons
        # This is equal to the current self.gridrow (=4)
        self.defcontrolrow = self.gridrow

        # Strategy drop-down menu 
        # This is the main menu to choose from for computing either pre-defined strategies or custom strategies
        self.strategies_menu = tk.StringVar(self.framel)
        self.stratmenu = tk.OptionMenu(self.framel, 
                                        self.strategies_menu, 
                                        *self.strat_options,
                                        command = self.get_selected_strategy)
        self.stratmenu.grid(row = self.defcontrolrow, columnspan = 2, padx = self.padx, pady = self.pady, sticky = "nsew")


    def right_frame(self): 
        '''
        Right frame of the GUI with plots
        '''
        # Right main box containing the interactive plot
        self.framer = tk.Frame(master = self.root, bg=self.rframeplotbg)
        self.framer.place(relx = self.right_relx, 
                            rely        = self.right_rely, 
                            relwidth    = self.right_relwidth, 
                            relheight   = self.right_relheight)

        # Setup plot Figure 
        self.fig = plt.figure(facecolor = self.rframefigbg)
        
        # Subplot spaces
        plt.subplots_adjust(left   = 0.12,
                            right  = 0.96,
                            top    = 0.96,
                            bottom = 0.16,
                            hspace = 0.27,
                            wspace = 0.3)
            
        # Setup the plot into the GUI
        self.canvas = FigureCanvasTkAgg(self.fig, self.framer)
        self.canvas.get_tk_widget().pack(fill = "both", expand = True)


    def get_S(self):
        '''
        Get the Underlying price entry
        '''
        try:
            S = float(self.entry_S.get()) 
            if S <= 0:
                # Returns error if a negative or zero Underlying price is entered
                tk.messagebox.showerror("Underlying price error", "Enter a positive Underlying price")
            else:
                return S
        except:
            tk.messagebox.showerror("Underlying value error", "Enter a valid Underlying price")


    def get_r(self):
        '''
        Get the Interest Rate entry 
        '''
        try:
            r = float(self.entry_r.get())
            if r < 0.01:
                # Returns a mininum of 0.01% (1 basis point)
                tk.messagebox.showerror("Interest Rate value error", "Enter at least an interest rate equal to 0.01(%)")
            elif r > 10:
                # Returns a maximum interest rate of 10% (1000 basis point)
                tk.messagebox.showerror("Interest Rate value error", "Enter at least an interest rate equal to 10(%)")
            else:
                return r / 100
        except:
            tk.messagebox.showerror("Interest Rate value error", "Enter a valid interest rate value (between 0.01% and 10%)")


    def get_q(self):
        '''
        Get the Dividend Yield entry 
        '''
        try: 
            q = float(self.entry_q.get())
            if q < 0:
                # If a negative dividend yield is entered, then return 0
                tk.messagebox.showerror("Dividend Yield value error", "Enter at least a dividend yield equal 0(%)")
            else:
                return q
        except:
            tk.messagebox.showerror("Dividend Yield value error", "Enter a valid dividend yield value")


    def get_T(self):
        '''
        Get the Maturity entry 
        '''
        try:
            T = float(self.entry_T.get())
            if T < 0:
                # Returns error if a negative maturity is entered
                tk.messagebox.showerror("Maturity value error", "Enter a maturity at least equal to 0 (expiration)")
            elif T > 5:
                # Returns a maximum maturity of 5 years 
                tk.messagebox.showerror("Maturity value error", "Enter a maturity at least equal to 5 (years)")
            else:
                return T
        except:
            tk.messagebox.showerror("Maturity value error", "Enter a valid maturity value (between 0 and 5 years)")
    

    def get_CP(self, CP):
        '''
        Get the Call or Put entry of an Option in the Custom Strategy 
        '''
        # Get the selected option strategy from the drop-down menu 
        CP = self.CPmenu.get()

        # Save the inserted CP value in the CusOptDat dictionary 
        self.CusOptData[self.addoption_times]["CP"] = CP
        # print(self.CusOptData )
        return CP


    def get_K(self):
        '''
        Get the Strike price entry
        '''
        try:
            # Get the inserted Strike Price inserted in the current K-Entry in the "Custom strategy" 
            K = float(self.Entries[self.addoption_times]["K"].get())
            if K < 1:
                # Returns error if a negative strike price is entered
                tk.messagebox.showerror("Strike value error", "Enter at least a strike price equal to 1")
                return -1
            else:
                return K
        except:
            # Returns error if a non-scalar strike price is entered
            tk.messagebox.showerror("Strike value error", "Enter a valid strike price")
        

    def get_v(self):
        '''
        Get the Volatility entry 
        '''
        try:
            # Get the inserted volatility inserted in the current v-Entry in the "Custom strategy" 
            v = float(self.Entries[self.addoption_times]["v"].get())
            if v < 1:
                # Returns a mininum volatility of 1% 
                tk.messagebox.showerror("Volatility value error", "Enter at least a volatility equal 1(%)")
            elif v > self.maxvola:
                # Return a maximum volatility of 100%
                tk.messagebox.showerror("Volatility value error", "Enter at least a volatility equal {}(%)".format(self.maxvola))
            else:
                return v
        except:
            # Returns error if a non-scalar volatility is entered
            tk.messagebox.showerror("Volatility value error", "Enter a valid volatility value (between 1% and {}%)".format(self.maxvola))


    def get_NP(self):
        '''
        Get the Net Position of an option in the "Custom strategy" 
        '''
        try:
            # Get the inserted Net Position inserted in the current NP-Entry in the "Custom strategy" 
            NP = float(self.Entries[self.addoption_times]["NP"].get())
            return NP
        except:
            # Returns error if a non-scalar Net Position is entered
            tk.messagebox.showerror("Net Position value error", "Enter a valid quantity (positive or negative) value")


    def define_slider(self, sliderax, labl="Slider", vmin=0, vmax=1, vstp=0.1, vini=0.5):
        '''
        Define slider for maturity values 
        '''
        return Slider(ax = sliderax, 
                    label     = labl, 
                    valmin    = vmin, 
                    valmax    = vmax, 
                    valstep   = vstp, 
                    valinit   = vini,
                    color     = self.sliderplot,
                    initcolor = self.sliderplot)


    def get_selected_strategy(self, selection):
        '''
        Recover the option strategy selected from the main drop-down menu
        '''
        # As soon as the stragey is changed eliminate all current labels/entries/texts
        try:
            for gridobj in self.framel.grid_slaves():
                if gridobj.grid_info()["row"] > self.defcontrolrow:
                    gridobj.grid_forget()
        except:
            pass

        # Get the selected option strategy from the drop-down menu 
        selection = self.strategies_menu.get()

        # Update selection variable
        self.chosen_strategy = selection
        
        # Calling routine for buttons layout
        self.define_button_layout()


    def define_button_layout(self):
        '''
        Definition of the left frame layout according to the selected option strategy.
        By default, the main "Calculate" button to compute strategies payoff appears as soon as one strategy is selected.
        - If "Custom Strategy" is chosen, two extra button for adding options and for resetting the strategy will appear
        - If a pre-defined strategy is chosen, the user can directly calculate the payoff,
          and eventual extra buttons and options data that may be on the frame are removed 
          (the user may have previously chosen the "Custom Strategy")
        '''
        # Insert the main "Calculate" button to calculate strategies payoffs
        # This button will appear by default and stays fixed        
        self.calculatebutton = self.create_tkbutton(buttoncmd  = self.compute_strategy, 
                                                    buttontext = self.calculate_button_name,
                                                    buttonfont = (self.guifont,13,"bold"))
        self.config_tkbutton(self.calculatebutton, 
                             buttonrow = self.defcontrolrow, 
                             buttoncol = 4, 
                             buttonpady = self.pady)

        # Depending on what strategy is chosen (a pre-defined one or the custom one): 
        # - if "Custom strategy" is chosen, two extra buttons will appear 
        # - if a pre-defined strategy is selected, no extra buttons will appear
    
        if self.chosen_strategy == "Custom strategy":
            # The "Custom strategy" is chosen.
            # There appears a button to add options and a button to reset the strategy 
        
            # Flag variables for button pushed 
            self.flag_add_option     = True
            self.flag_reset_strategy = True

            # Number of times the button is pushed (needed to count options added to the strategy)
            self.addoption_times = 0
        
            # "Add Option" button used to insert options data in the "Custom strategy"            
            self.addoptionbutton = self.create_tkbutton(buttoncmd = self.adding_options, buttontext=self.add_options_button_name)
            self.config_tkbutton(self.addoptionbutton, 
                                buttonrow = self.defcontrolrow, 
                                buttoncol = 2, 
                                buttoncolspan = 1, 
                                buttonpady = self.pady)

            # "Reset Strategy" button used to reset the strategy inserted (remove all options data)            
            self.resetstratbutton = self.create_tkbutton(buttoncmd = self.remove_options, buttontext=self.reset_strat_button_name)
            self.config_tkbutton(self.resetstratbutton, 
                                buttonrow = self.defcontrolrow, #2, 
                                buttoncol = 3, 
                                buttoncolspan = 1, 
                                buttonpady = self.pady)

        else:
            # If "Custom strategy" is not chosen, then the button "Add Option" and the "Reset Strategy" are removed from the frame's grid
            # since we are going to compute a default strategy and no further options need to be added.
            # It is not required to check if the "Add Option" exists in first place.
            # If it not found within the frame's grid objects, then anything is removed and no errors are produced

            if self.flag_add_option is True and self.flag_reset_strategy is True:
                # If enters here, it means that the "Custom Strategy" has been previosuly chosen 
                # and so the "Add Options" and "Reset Strategy" buttons were on the GUI. 
                # We remove them. Also, every label/entry of eventual added options are removed too

                # Remove options labels/entries and reset other variables/flags
                self.remove_options()

                # Remove now the "Add option" and "Reset strategy" buttons
                for gridobj in self.framel.grid_slaves():
                    # Remove according to right position 
                    if gridobj.grid_info()["row"] == self.defcontrolrow and gridobj.grid_info()["column"] in [2,3]:        
                        gridobj.grid_forget()
                
                # Reset flags for the custom strategy
                self.flag_add_option     = False
                self.flag_reset_strategy = False

            # Reset current row position 
            # If "Custom Strategy" was chosen, new rows were added in the grid. Remove them.
            self.gridrow = self.defcontrolrow 


    def adding_options(self):
        '''
        Adds labels/entries data for entering a new option whenever the "Add Options" is pushed in the "Custom Strategy".
        '''
        if self.addoption_times == 5:
            # Maximum number of options in the Custom Strategy
            # The error messagebox will pop up if the "Add Options" is pushed more than 5 times
            tk.messagebox.showerror("Max Options", "Maximum options allowed. Calculate, Reset, o change strategy")

        else:
            # Maximum number of options inserted not reached yet 
            # Labels/Entries for entering data of a new option will appear 
            
            # The "Add Option" button has been pushed (less than the max times).
            # There is a check to do before following through. 
            # Nothing should be below the current self.gridrow level.
            # In fact, the user may have inserted one option and pushed the "Calculate" button.
            # If so, the text with the price to entering the strategy appeared on self.gridrow + 1.
            # However, if now the "Add Option" is pushed again before cleaning, 
            # the new option labels/entries and the text overlap.
            
            # Remove all labels and entries data below current gridrow 
            for gridobj in self.framel.grid_slaves():
                if (gridobj.grid_info()["row"] > self.gridrow):
                    gridobj.grid_forget()

            if self.addoption_times == 0:
                # If enters here, it means it is the first time the "Add options" button is pushed. 
                # Then, the CusOptData dictionary of options is initialized with the first key (no. 0 + 1 = 1)
                self.CusOptData[self.addoption_times + 1] = dict()

            else:
                # If enters here, it means that the "Add options" button has been pushed at least twice.
                # It means that data entries/labeles for a previous options appeared in the GUI and values were inserted. 
                # However, they were not saved yet.
                # Options data just entered will be saved once the "Add options" (or the "Calculate") button is pressed again.
                # This is what this part is needed for.
                # We recover and save the data of the options just inserted (all but the CP data, due to the "OptionMenu")
                # Morevoer, if data were inserted incorrectly, by pushing the "Add options" a error pops up again
                # and no new options can be inserted until correcting wrong values. 

                # Validate options data inserted and save them
                validoptions = self.validate_options()
                # print(validoptions)
                if not validoptions:
                    # If some data is incorrect, exit from the function 
                    return  

                # Once data are correctly saved for previous option (i.e, options data just entered) 
                # the dictionary for the next option is initialized 
                self.CusOptData[self.addoption_times + 1] = dict()

            # Updating number of times the "Add option" button is pushed
            self.addoption_times = self.addoption_times + 1

            self.gridrow = self.gridrow + 1
            self.gridcol = 0

            # LABELS

            # Label Call/Put CP
            self.label_CP = self.create_tklabel(labeltext = "Option {}".format(self.addoption_times))
            self.config_tklabel(self.label_CP, labelpady = self.first_addopt_padys, labelsticky = "nsw")

            self.gridcol = self.gridcol + 1

            # Label Strike Price K
            self.label_K = self.create_tklabel(labeltext = "Strike Price")
            self.config_tklabel(self.label_K, labelpady = self.first_addopt_padys, labelsticky = "nsw")

            self.gridcol = self.gridcol + 1

            # Label volatility v
            self.label_v = self.create_tklabel(labeltext = "Volatility(%)")
            self.config_tklabel(self.label_v, labelpady = self.first_addopt_padys, labelsticky = "nsw")

            self.gridcol = self.gridcol + 1

            # Label Quantity NP
            self.label_NP = self.create_tklabel(labeltext = "Quantity")
            self.config_tklabel(self.label_NP, labelpady = self.first_addopt_padys, labelsticky = "nsw")
            
            self.gridcol = self.gridcol + 1

            # Label of the Option price (text will appear once the "Calculate" button is pushed)
            self.labpricestr = self.create_tklabel(labeltext = '''''')
            self.config_tklabel(self.labpricestr, labelpady = self.first_addopt_padys, labelsticky = "nsw")


            # ENTRIES

            self.gridrow = self.gridrow + 1
            self.gridcol = 0

            # Entry Call/Put CP
            CPs = ("C", "P")
            self.CPmenu = tk.StringVar(self.framel)
            self.entry_CP = tk.OptionMenu(self.framel, 
                                        self.CPmenu,
                                        *CPs, 
                                        command = self.get_CP)
            self.entry_CP.rowconfigure(self.gridrow, weight=1, minsize=15)
            self.entry_CP.columnconfigure(self.gridcol, weight=1, minsize=15)
            self.entry_CP.grid(row = self.gridrow, column = self.gridcol, padx=self.padx, pady=(5,0), sticky="nsew")
    
            self.gridcol = self.gridcol + 1

            # Entry Strike Price K
            self.entry_K = self.create_tkentry()
            self.config_tkentry(self.entry_K, entrypady = self.other_addopt_padys, entrydefval = int(self.get_S()))

            self.gridcol = self.gridcol + 1

            # Entry volatility v
            self.entry_v = self.create_tkentry()
            self.config_tkentry(self.entry_v, entrypady = self.other_addopt_padys, entrydefval = 25)

            self.gridcol = self.gridcol + 1

            # Entry Quantity NP
            self.entry_NP = self.create_tkentry()
            self.config_tkentry(self.entry_NP, entrypady = self.other_addopt_padys)

            self.gridcol = self.gridcol + 1

            # Label (Entry) of the Option price (the price will appear once the "Calculate" button is pushed)
            self.labpriceval = self.create_tklabel(labeltext = '''''')
            self.config_tklabel(self.labpriceval, labelpady = self.other_addopt_padys, labelsticky = "nsw")

            # Save the current entries
            # As soon as the "Add options" button is pushed and new entry data appear, they are saved. 
            # This is required due to the possibility (quite likely) that the user changes some value 
            # in previous options before or after pushing the "Calculate" button.
            # If so, the corresponding value shall be stored correctly in the associated option data dictionary.
            # Therefore, we create a dynamic dictionary of entries whose values are going 
            # to be reviewed every time the "Calculate" button is pushed, so than right inserted values are taken.

            self.Entries[self.addoption_times] = {"K": self.entry_K, 
                                                  "v": self.entry_v,
                                                  "NP": self.entry_NP}
            
            # Save the current labels/prices for the Option prices
            # As soon as the "Calculate" button is pushed, the label and the option price will appear.
            # However, if the user change some data of some of the current options on the GUI 
            # and calculate again the payoff, the new price of the option should replace the older one. 
            # Therefore, we need to track these huys

            self.LabPrice[self.addoption_times] = {"PriceLab": self.labpricestr,
                                                   "PriceVal": self.labpriceval}


    def validate_options(self):
        '''
        Validation of option data inserted in the Custom Strategy when the "Add Options" button is pushed.
        Inserted data are revised abd they are saved if and only if the are not incorrect.
        If some wrong data is entered, the message error will pop up. 
        Then, data will not be saved and no options payoff can be calculated unless entering right values 
        (or until the strategy is reset, if the user want)
        '''
        # Validate the Strike Price
        K = self.get_K() 
        try:
            if K < 0:
                # Negative Strike Price entered
                valid_K = False
            else:
                # A correct Strike Price inserted (positive scalar)
                valid_K = True
                self.CusOptData[self.addoption_times]["K"] = K
        except:
            # Non scalar Strike Price entered
            valid_K = False

        # Validate the volatility
        v = self.get_v() 
        try:
            if v < 1.0 or v > 100.0:
                # Volatility less than 1% or greater than 100% entered
                valid_v = False
            else:
                # A correct volatility inserted (positive scalar between 1% and 100%)
                valid_v = True
                self.CusOptData[self.addoption_times]["v"] = v / 100
        except:
            # Non scalar volatility entered
            valid_v = False

        # Validate the Net Position
        NP = self.get_NP() 
        if isinstance(NP, float) or isinstance(NP, int):
            # A correct Net Position inserted (scalar)
            valid_NP = True
            self.CusOptData[self.addoption_times]["NP"] = NP
        else:
            # Non scalar Net Position entered
            valid_NP = False

        # Validate variable 
        validdata = valid_K and valid_v and valid_NP

        return validdata


    def remove_options(self):
        '''
        If the "Reset strategy" button is pushed, it removes all options that have been 
        added by pushing the "Add options" button in the Custom Strategy.
        In particular:
        - resets the no. times the "Add options" button is pushed 
        - resets the Options data dictionary
        - resets the Entries data dictionary 
        - resets the LabPrice data dictionary
        - removes all labels/entries from 2nd row forward 
        '''
        # Reset number of options that can be added
        self.addoption_times = 0

        # Reset dictionary of Options data of the Custom Strategy
        self.CusOptData = dict()

        # Reset dictionary of Options data of the Custom Strategy
        self.Entries = dict()

        # Reset dictionary of Options Label Prices
        self.LabPrice = dict()

        # Remove all labels and entries data below row 2 
        for gridobj in self.framel.grid_slaves():
            if gridobj.grid_info()["row"] > self.defcontrolrow:
                gridobj.grid_forget()


    def compute_strategy(self):
        '''
        Main function for strategies payoff computation when the "Calculate" button is pushed 
        '''

        if self.chosen_strategy != "Custom strategy":

            # If the chosen strategy is a pre-defined one and the "Calculate" button is pushed
            # it should be checked that no duplicated description/texts appears if the user pushes again 
            # the button without changing any input.
            # Otherwise, any time the button is pushed the same descriptions/texts appear over and over... 

            for gridobj in self.framel.grid_slaves():
                if gridobj.grid_info()["row"] > self.defcontrolrow:
                        gridobj.grid_forget()

        else: #self.chosen_strategy == "Custom strategy":

            # If the Custom Strategy is chosen, one option has been added and the "Calculate" button has been pushed
            # then the labels/entries and strategy cost appeared below self.gridrow.
            # However, suppose some option data is changed by the user the the "Calculate" pushed is pushed again.
            # In this case the new option strategy cost will be overlapped with older one 

            try:
                for gridobj in self.framel.grid_slaves():
                    if (gridobj.grid_info()["row"] >= self.gridrow + 1):
                            gridobj.grid_forget()
            except: 
                pass
            

        # Recover inserted data 
        self.S = self.get_S()
        self.r = self.get_r()
        self.q = self.get_q()
        self.T = self.get_T()

        # Create strategy class with the underlying price, the time-to-maturity, and the dividend yield
        self.Strategy = BSOptStrat(S = self.S, r = self.r, q = self.q)

        # Auxiliary increase/decrese for strike prices in the pre-defined strategies (according to current level of the underlying price)
        dS = 5/100

        if self.chosen_strategy == "Custom strategy":
            # Custom Strategy

            # The inserted data of the last option have not been saved yet. 
            # They will be stored once the "Calculate" button is pushed.
            # Then, validate last options data inserted and save them in the dictionary 

            validoptions = self.validate_options()
            if not validoptions:
                # If some data (of the last option inserted) is incorrect, exit from the function 
                return  
                
            # Revision of all data inserted 
            #
            # It may happen (and it is very likely to happen) that once the "Calculate" button is pushed, 
            # the user changes some values of one the options inserted without resetting the strategy. 
            # Or the user may also push the "Add options" and add a new option.
            #
            # Then, it is requiered a revision of options data everytime that the "Calculate" button is pushed.
            # We do a loop over the CusOptData dictionary and at each iteration the 
            # "self.addoption_times" variable is increased (from 0) so that to enter into each option key.
            # This way, the "validate_options" function is called on the right option data at each iteration.
            #
            # Note that the las inserted option is already validate in the step above 
            # as well as in the last iteration of the loop. 
            # This is because the for loop need to increase "self.addoption_times" up to the number 
            # equal to the number of inserted options.

            for nopt in self.CusOptData.keys(): 
                # Current option data number 
                self.addoption_times = nopt 

                # Validate options data inserted and save them
                validoptions = self.validate_options()
                if not validoptions:
                    # If some data is incorrect, exit from the function
                    # The user may have changed some values and put a wrong value not accepted  
                    return  
            
            # After the revision, all data are correct and the strategy is created 
            for nopt in self.CusOptData.keys():    

                CP = self.CusOptData[nopt]["CP"] 
                K  = self.CusOptData[nopt]["K"] 
                v  = self.CusOptData[nopt]["v"] 
                NP = self.CusOptData[nopt]["NP"] 

                # Inserting the option in the strategy
                if CP == "C":
                    self.Strategy.call(NP=NP, K=K, T=self.T, v=v)
                else:
                    self.Strategy.put(NP=NP, K=K, T=self.T, v=v)


        # Naked

        elif self.chosen_strategy == "Long Call":
            # Long Call (ATM option)
            self.Strategy.call(NP = 1, K = self.S, T = self.T, v = 30/100)
            
        elif self.chosen_strategy == "Short Call":
            # Short Call (ATM option)
            self.Strategy.call(NP = -1, K = self.S, T = self.T, v = 30/100)

        elif self.chosen_strategy == "Long Put":
            # Long Put (ATM option)
            self.Strategy.put(NP = +1, K = self.S, T = self.T, v = 30/100)

        elif self.chosen_strategy == "Short Put":
            # Short Put (ATM option)
            self.Strategy.put(NP = -1, K = self.S, T = self.T, v = 30/100)


        # Bull Spreads

        elif self.chosen_strategy == "Bull Call Spread":
            # Bull Call Spread
            # - 1 long ITM call (K<S)
            # - 1 short OTM call (K>S)
            self.Strategy.call(NP = 1,  K = self.S*(1 - dS), T = self.T, v = 30/100)
            self.Strategy.call(NP = -1, K = self.S*(1 + dS), T = self.T, v = 20/100)

        elif self.chosen_strategy == "Bull Put Spread":
            # Bull Put Spread
            # - 1 long OTM put (K<S)
            # - 1 short ITM put (K>S)
            self.Strategy.put(NP = 1,  K = self.S*(1 - dS), T = self.T, v = 30/100)
            self.Strategy.put(NP = -1, K = self.S*(1 + dS), T = self.T, v = 20/100)


        # Bear Spreads

        elif self.chosen_strategy == "Bear Call Spread":
            # Bear Call Spread
            # - 1 long OTM call (K>S)
            # - 1 short ITM call (K<S)
            self.Strategy.call(NP = 1,  K = self.S*(1 + dS), T = self.T, v = 20/100)
            self.Strategy.call(NP = -1, K = self.S*(1 - dS), T = self.T, v = 30/100)

        elif self.chosen_strategy == "Bear Put Spread":
            # Bear Put Spread
            # - 1 long ITM put (K>S)
            # - 1 short OTM put (K<S)
            self.Strategy.put(NP = 1,  K = self.S*(1 + dS), T = self.T, v = 20/100)
            self.Strategy.put(NP = -1, K = self.S*(1 - dS), T = self.T, v = 30/100)


        # Straps

        elif self.chosen_strategy == "Top Strip":
            # Top Strip (asymmetric straddle)
            # - 1 short call 
            # - 2 short put
            # at the same strike price
            self.Strategy.call(NP = -1, K = self.S, T = self.T, v = 25/100)
            self.Strategy.put(NP  = -2, K = self.S, T = self.T, v = 25/100)

        elif self.chosen_strategy == "Bottom Strip":
            # Bottom Strip (asymmetric straddle)
            # - 1 long call 
            # - 2 long put
            # at the same strike price
            self.Strategy.call(NP = +1, K = self.S, T = self.T, v = 25/100)
            self.Strategy.put(NP  = +2, K = self.S, T = self.T, v = 25/100)
            
        
        # Strips 
        
        elif self.chosen_strategy == "Top Strap":
            # Top Strap (asymmetric straddle)
            # - 2 short call 
            # - 1 short put
            # at the same strike price
            self.Strategy.call(NP = -2, K = self.S, T = self.T, v = 25/100)
            self.Strategy.put(NP  = -1, K = self.S, T = self.T, v = 25/100)

        elif self.chosen_strategy == "Bottom Strap":
            # Bottom Strap (asymmetric straddle)
            # - 2 long call 
            # - 1 long put
            # at the same strike price
            self.Strategy.call(NP = +2, K = self.S, T = self.T, v = 25/100)
            self.Strategy.put(NP  = +1, K = self.S, T = self.T, v = 25/100)
            

        # Straddles 

        elif self.chosen_strategy == "Top Straddle":
            # Top Straddle
            # - 1 short call 
            # - 1 short put
            # at the same strike price
            self.Strategy.call(NP = -1, K = self.S, T = self.T, v = 25/100)
            self.Strategy.put(NP  = -1, K = self.S, T = self.T, v = 25/100)

        elif self.chosen_strategy == "Bottom Straddle":
            # Bottom Straddle
            # - 1 long call 
            # - 1 long put
            # at the same strike price
            self.Strategy.call(NP = +1, K = self.S, T = self.T, v = 25/100)
            self.Strategy.put(NP  = +1, K = self.S, T = self.T, v = 25/100)


        # Strangles 

        elif self.chosen_strategy == "Top Strangle":
            # Top Strangle
            # - 1 short call 
            # - 1 short put
            # at different strike prices
            self.Strategy.call(NP = -1, K = self.S*(1 + dS), T = self.T, v = 20/100)
            self.Strategy.put(NP  = -1, K = self.S*(1 - dS), T = self.T, v = 30/100)

        elif self.chosen_strategy == "Bottom Strangle":
            # Bottom Strangle
            # - 1 long call 
            # - 1 long put
            # at different strike prices
            self.Strategy.call(NP = +1, K = self.S*(1 + dS), T = self.T, v = 20/100)
            self.Strategy.put(NP  = +1, K = self.S*(1 - dS), T = self.T, v = 30/100)


        # Butterflies 

        elif self.chosen_strategy == "Top Butterfly":
            # Top Butterfly
            # - 1 long ITM call 
            # - 1 long OTM call
            # - 2 short ATM call
            self.Strategy.call(NP = +1, K = self.S*(1 - dS*2), T = self.T, v = 30/100)
            self.Strategy.call(NP = +1, K = self.S*(1 + dS*2), T = self.T, v = 20/100)
            self.Strategy.call(NP = -2, K = self.S, T = self.T, v = 25/100)

        elif self.chosen_strategy == "Bottom Butterfly":
            # Bottom Butterfly
            # - 1 short ITM call 
            # - 1 short OTM call
            # - 2 long ATM call
            self.Strategy.call(NP = -1, K = self.S*(1 - dS*2), T = self.T, v = 30/100)
            self.Strategy.call(NP = -1, K = self.S*(1 + dS*2), T = self.T, v = 20/100)
            self.Strategy.call(NP = +2, K = self.S, T = self.T, v = 25/100)


        # Iron Condors

        elif self.chosen_strategy == "Top Iron Condor":
            # Top Iron Condor
            # - Bull Put Spread:
            #   1 long put and 1 short put at different strikes, 
            #   both smaller than the strikes of the Bear Call Spreads 
            self.Strategy.put(NP = +1, K = self.S*(1 - dS*2), T = self.T, v = 30/100)
            self.Strategy.put(NP = -1, K = self.S*(1 - dS),   T = self.T, v = 25/100)
            # - Bear Call Spread:
            #   1 long call and 1 short call at different strikes
            self.Strategy.call(NP = +1, K = self.S*(1 + dS*2), T = self.T, v = 20/100)
            self.Strategy.call(NP = -1, K = self.S*(1 + dS),   T = self.T, v = 15/100)
            
        elif self.chosen_strategy == "Bottom Iron Condor":
            # Bottom Iron Condor
            # - Bear Put Spread:
            #   1 short put and 1 long put at different strikes, 
            #   both smaller than the strikes of the Bear Call Spreads 
            self.Strategy.put(NP = -1, K = self.S*(1 - dS*2), T = self.T, v = 30/100)
            self.Strategy.put(NP = +1, K = self.S*(1 - dS),   T = self.T, v = 25/100)   
            # - Bull Call Spread:
            #   1 short call and 1 long call at different strikes
            self.Strategy.call(NP = -1, K = self.S*(1 + dS*2), T = self.T, v = 20/100)
            self.Strategy.call(NP = +1, K = self.S*(1 + dS),   T = self.T, v = 15/100)
            

        # Create the StratData dictionary with inserted options and the total strategy price 
        self.StratData = self.Strategy.describe_strategy()

        # Once the startegy option has been created 
        # - if the strategy was the custom one, then the prices of single option should be put on the GUI
        # - if the strategy was a pre-defined one, the the descritpion should appear
        # In both cases, also the cost of entering the strategy would appear

        if self.chosen_strategy == "Custom strategy":
            # Custom Strategy

            # When the "Calculate" button is pushed data of each inserted option is reviewed
            # and the current option price is recoved and showed on the GUI

            for o in set(self.StratData.keys()) - set({"Cost"}):
                nopt = int(o.split("_")[1]) 
                
                # Current Option label
                self.LabPrice[nopt]["PriceLab"].configure(text = "Call price" if self.StratData[o]["CP"] == "C" else "Put price")
                
                # Current Option price
                price = self.StratData[o]["Pr"]
                multi = self.StratData[o]["M"]
                posit = self.StratData[o]["NP"]
                nside = "Pay $" if posit >= 0 else "Receive $" 
                self.LabPrice[nopt]["PriceVal"].configure(text = "{:.2f} ({}{:.0f})".format(price, 
                                                                                            nside, 
                                                                                            abs(price * posit * multi)))
          
            # Final text with the cost of the strategy 
            costmsg = "Cost of the entering this strategy: " 
            costmsg = costmsg + "Pay $" if self.StratData["Cost"] > 0 else costmsg + "Receive $"
            costmsg = costmsg + "{:.0f}".format( abs(self.StratData["Cost"]) )

            # Show the cost on the GUI
            self.labcost = self.create_tklabel(labeltext = costmsg)
            self.config_tklabel(self.labcost, 
                                labelrow = self.gridrow + 1,
                                labelcol = 0, 
                                labelcolspan = 5,
                                labelpady = (30,0)) 


        else:
            # Pre-defined strategies

            self.gridrow = self.gridrow + 1

            # Strategy name
            self.stratname = self.create_tklabel(labeltext = self.chosen_strategy,
                                                 labelfont = (self.lab_font[0], self.lab_font[1], "bold"))
            self.config_tklabel(self.stratname, 
                                labelrow = self.gridrow, 
                                labelcol = 0, 
                                labelcolspan = 2,
                                labelpady = (40,0)) 
                                
            self.gridrow = self.gridrow + 1

            # Strategy description text 
            self.stratdesc = self.strategy_description()
            self.predefopt_desc = self.create_tktext(textheight = self.stratdesc["nrows"], 
                                                     textwidth = self.deftextwidth,
                                                     textfont  = self.lab_font)
            self.config_tktext(self.predefopt_desc, 
                                textmsg     = self.stratdesc["msg"], 
                                textrow     = self.gridrow, 
                                textpady    = (20,0))

            # Show all options data of the pre-defined selected strategy 
            optionkeys = [k for k in self.StratData.keys() if k != "Cost"]
            for o in optionkeys: 
                nopt = o.split("_")[1]

                # Print Option info
                stratdesc = "({}) {:.0f} {} {}".format(nopt, 
                                                       abs(self.StratData[o]["NP"]),
                                                       "Long" if self.StratData[o]["NP"] >= 0 else "Short", 
                                                       "Call" if self.StratData[o]["CP"] == "C" else "Put")

                stratdesc = stratdesc + "(K = {:.2f}, T = {:.2f}, v = {:.2f})".format(self.StratData[o]["K"], 
                                                                                      self.StratData[o]["T"], 
                                                                                      self.StratData[o]["v"])

                stratdesc = stratdesc + " | {} Price = {:.2f}".format("Call" if self.StratData[o]["CP"] == "C" else "Put", 
                                                                      self.StratData[o]["Pr"])    

                self.gridrow = self.gridrow + 1

                self.optdescription = self.create_tklabel(labeltext = stratdesc)
                self.config_tklabel(self.optdescription, 
                                    labelrow = self.gridrow,
                                    labelcol = 0, 
                                    labelcolspan = 5,
                                    labelpady = (20,0))

            self.gridrow = self.gridrow + 1

            # Final text with the cost of the strategy 
            costmsg = "Cost of the entering this strategy: " 
            costmsg = costmsg + "Pay $" if self.StratData["Cost"] > 0 else costmsg + "Receive $"
            costmsg = costmsg + "{:.0f}".format( abs(self.StratData["Cost"]) )
        
            # Show the cost on the GUI
            self.labcost = self.create_tklabel(labeltext = costmsg)
            self.config_tklabel(self.labcost, 
                                labelrow        = self.gridrow, 
                                labelcol        = 0, 
                                labelcolspan    = 5,
                                labelpady       = (20,0))


        # Check if sliders are already in the right frame plot window
        try:
            # If enters here, it means the button "Calculate" has been pushed again
            # Then, the current sliders are removed, otherwise the new sliders 
            # corresponding to the last strategy calculation are put on top of them 
            
            # Remove time-to-maturity slider
            Axis.remove(self.slider_T_ax)
            delattr(self, "slider_T_ax")
            delattr(self, "slider_T")

            # Remove delta-volatility slider
            Axis.remove(self.slider_dv_ax)
            delattr(self, "slider_dv_ax")
            delattr(self, "slider_dv")
        except:        
            pass

        # Create current slider axis 
        self.slider_T_ax  = plt.axes([0.35, 0.06, 0.50, 0.015])
        self.slider_dv_ax = plt.axes([0.35, 0.03, 0.50, 0.015])
                
        # Maturity slider
        self.slider_T = self.define_slider(self.slider_T_ax,
                                            labl = "Time to Maturity (years)", 
                                            vmin = 0, 
                                            vmax = self.T, 
                                            vstp = 0.00274, 
                                            vini = self.T)
        self.slider_T.label.set_color(self.sliderlabfg)
        self.slider_T.valtext.set_color(self.sliderlabfg)

        # Recover the volatilities inserted for each option in the strategy
        # They are needed to define the min. and max. delta volatility in 
        # the Delta Volatility slider under the assumption of parallel shifts of the skew
        volas = []
        for opt in set(self.StratData.keys()) - set({"Cost"}):
            volas.append( self.StratData[opt]["v"] * 100 )

        # Delta Volatility slider
        self.slider_dv = self.define_slider(self.slider_dv_ax,
                                            labl = "Delta Vola. (%)", 
                                            vmin = - min(volas) + 1,   
                                            vmax = self.maxvola - max(volas), 
                                            vstp = 1, 
                                            vini = 0)
        self.slider_dv.label.set_color(self.sliderlabfg)
        self.slider_dv.valtext.set_color(self.sliderlabfg)

        # Plot option strategy payoff
        self.plot_strat_payoff()

        # Calling the interactive plot method as soon as a slider is touched
        self.slider_T.on_changed(self.onslide)
        self.slider_dv.on_changed(self.onslide)


    def plot_strat_payoff(self):
        '''
        Plot of option strategies' payoffs
        '''
        # Clear current axis 
        try:
            for axn in range(len(self.ax)):
                self.ax[axn].clear()
            
        except:
            self.ax = self.fig.subplots(2,1)
            self.ax = self.ax.flatten()
                    
        # Top plot
        # All options' payoffs of the strategy at payoffot (T=0)
        for n in range(1,self.Strategy.payoffs_exp_df.shape[1]+1):
            self.ax[0].plot(self.Strategy.payoffs_exp_df.index, 
                            self.Strategy.payoffs_exp_df[n], 
                            color = self.optioncolors[n-1], 
                            label = "Option {}".format(n))
        
        # Bottom plot
        # Current payoff as soon as the strategy is initiated (the plot that changes when slider values are changed)
        self.pff, = self.ax[1].plot(self.Strategy.payoffs.index, 
                                    self.Strategy.payoffs.values, 
                                    color = self.payoffcolplot, 
                                    linestyle = "-", 
                                    label = "Current payoff",
                                    alpha = 0.7)

        # Strategy payoff at maturity (T=0)
        self.pffmat, = self.ax[1].plot(self.Strategy.payoffs_exp.index, 
                                        self.Strategy.payoffs_exp.values, 
                                        color = self.payoffcolplot, 
                                        linestyle = "--", 
                                        label = "Payoff at maturity (T=0)", 
                                        alpha = 1)

        # Get current xlim and ylim
        self.stratxlim = self.ax[1].get_xlim()
        self.stratylim = self.ax[1].get_ylim()

        # Set x-labels
        xfontsize = 9
        self.ax[1].set_xlabel("Underlying $S$", fontsize=xfontsize, color=self.labplotfg)

        # Set y-labels    
        # yfontsize = 9
        # ycol = "k"
        # self.ax[0].set_ylabel("Payoff (USD)", fontsize=yfontsize, color=self.labplotfg)
        # self.ax[1].set_ylabel("Payoff (USD)", fontsize=yfontsize, color=self.labplotfg)
       
        # Set titles
        self.titplotfontsize = 12
        self.ax[0].set_title("Options payoffs at maturity", fontsize=self.titplotfontsize, color=self.labplotfg)
        self.ax[1].set_title("Total strategy payoff", fontsize=self.titplotfontsize, color=self.labplotfg)

        # Set grids
        self.ax[0].grid()    
        self.ax[1].grid()      

        # Legend
        self.ax[0].legend(fontsize=9)
        self.ax[1].legend(fontsize=9)
        
        # Tick labels
        xyfontsize = 8
        plt.setp(self.ax[0].get_xticklabels(), fontsize=xyfontsize, color=self.labplotfg)
        plt.setp(self.ax[0].get_yticklabels(), fontsize=xyfontsize, color=self.labplotfg)

        plt.setp(self.ax[1].get_xticklabels(), fontsize=xyfontsize, color=self.labplotfg)
        plt.setp(self.ax[1].get_yticklabels(), fontsize=xyfontsize, color=self.labplotfg)

        # Update plot
        self.updateplot()


    def onslide(self, val):
        '''
        Recompute option data and update plot when slider values changes
        '''
        # Get current sliders' values
        current_T  = self.slider_T.val
        current_dv = self.slider_dv.val

        # Update Option given the new values of the sliders
        self.StrategySlider = BSOptStrat(S = self.S , r = self.r, q = self.q)

        # If-Else according to the inserted strategy

        if self.chosen_strategy == "Custom strategy":
            # Custom strategy
            # Recover values of the CusOptData dictionary

            # For loop over each option inserted 
            for nopt in self.CusOptData.keys():
                if self.CusOptData[nopt]["CP"] == "C":
                    # Current option is a Call
                    self.StrategySlider.call(NP = self.CusOptData[nopt]["NP"], 
                                            K = self.CusOptData[nopt]["K"], 
                                            T = current_T, 
                                            v = self.CusOptData[nopt]["v"] + current_dv / 100,
                                            optprice = self.StratData[f"Option_{nopt}"]["Pr"])
                else:
                    # Current option is a Put
                    self.StrategySlider.put(NP = self.CusOptData[nopt]["NP"], 
                                            K = self.CusOptData[nopt]["K"], 
                                            T = current_T, 
                                            v = self.CusOptData[nopt]["v"] + current_dv / 100,
                                            optprice = self.StratData[f"Option_{nopt}"]["Pr"])

        else: 
            # Pre-defined strategy 
            # Recover values of the StratData dictionary

            for opt in set(self.StratData.keys()) - set({"Cost"}):
                if self.StratData[opt]["CP"] == "C":
                    # Current option is a Call
                    self.StrategySlider.call(NP = self.StratData[opt]["NP"],  
                                            K = self.StratData[opt]["K"], 
                                            T = current_T, 
                                            v = self.StratData[opt]["v"] + current_dv / 100, 
                                            optprice = self.StratData[opt]["Pr"])
                else:
                    # Current option is a Put
                    self.StrategySlider.put(NP = self.StratData[opt]["NP"],  
                                            K = self.StratData[opt]["K"], 
                                            T = current_T, 
                                            v = self.StratData[opt]["v"] + current_dv / 100, 
                                            optprice = self.StratData[opt]["Pr"])

  
        # Update plot 
        if current_T == 0:
            self.pff.set_ydata(self.Strategy.payoffs_exp.values)    
        else:
            self.pff.set_ydata(self.StrategySlider.payoffs.values)

        self.pffmat.set_ydata(self.Strategy.payoffs_exp.values)

        # Update title 
        self.ax[1].set_title("Total strategy payoff ({:.0f} days left)".format(current_T*365), fontsize=self.titplotfontsize)

        # Set new axis 
        if current_T == 0:
            self.ax[1].set_xlim( self.stratxlim[0], self.stratxlim[1] )
            self.ax[1].set_ylim( self.stratylim[0], self.stratylim[1] )

        # Update plot
        self.updateplot()


    def updateplot(self):
        '''
        Update plot
        '''
        self.canvas.draw()


    def strategy_description(self):
        '''
        Returns the description of the pre-defined strategy
        '''
        Desc = dict()

        if self.chosen_strategy == "Long Call":
            nrows = 2
            desc = '''By buying a Call, \
you hope that the underlying stock price will increase. 
You will pay the option premium to buy the option.''' 

        elif self.chosen_strategy == "Short Call":
            nrows = 2
            desc = '''By writing a Call, \
you hope that the underlying stock price will decrease. 
You will receive the option premium by writing the option.''' 

        elif self.chosen_strategy == "Long Put":
            nrows = 2
            desc = '''By buying a Put, \
you hope that the underlying stock price will decrease. 
You will pay the option premium to buy the option.''' 

        elif self.chosen_strategy == "Short Put":
            nrows = 2
            desc = '''By writing a Put, \
you hope that the underlying stock price will increase. 
You will receive the option premium by writing the option.''' 

        elif self.chosen_strategy == "Bull Call Spread":
            nrows = 3
            desc = '''A Bull Call Spread is made by buying a Call \
with a certain strike price 
and by selling a Call with a higher strike price. \
You hope that the underlying stock price will increase.
Unlike Bull Put Spreads, this strategy requires an initial investment.''' 

        elif self.chosen_strategy == "Bull Put Spread":
            nrows = 3
            desc = '''A Bull Put Spread is made by buying a Put \
with a certain strike price 
and by selling a Put with a higher strike price. \
You hope that the underlying stock price will increase.
Unlike Bull Call Spreads, this strategy provides an initial positive up-front cash inflow.'''

        elif self.chosen_strategy == "Bear Call Spread":
            nrows = 3
            desc = '''A Bear Call Spread is made by buying a Call \
with a certain strike price 
and by selling a Call with a lower strike price. \
You hope that the underlying stock price will decrease.
Unlike Bear Put Spreads, this strategy provides an initial positive up-front cash inflow.'''

        elif self.chosen_strategy == "Bear Put Spread":
            nrows = 3
            desc = '''A Bear Put Spread is made by buying a Put \
with a certain strike price 
and by selling a Put with a lower strike price. \
You hope that the underlying stock price will decrease.
Unlike Bear Call Spreads, this strategy requires an initial investment.'''

        elif self.chosen_strategy == "Top Strip":
            nrows = 4
            desc = '''A Top Strip consists of one short position in one Call \
and two Puts with the same strike price.
You hope there wont' be a big underlying price move and consider a decrease to be more likely than an increase.
It is a kind of an asymmetric Top Straddle.
Unlike Bottom Strips, this strategy provides an initial positive up-front cash inflow.'''

        elif self.chosen_strategy == "Bottom Strip":
            nrows = 4
            desc = '''A Bottom Strip consists of one long position in one Call \
and two Puts with the same strike price.
You hope there will be a big underlying price move and consider a decrease to be more likely than an increase.
It is a kind of an asymmetric Bottom Straddle.
Unlike Top Strips, this strategy requires an initial investment.'''

        elif self.chosen_strategy == "Top Strap":
            nrows = 4
            desc = '''A Top Strap consists of two short positions in one Call \
and one Put with the same strike price.
You hope there wont' be a big underlying price move and consider an increase to be more likely than a decrease.
It is a kind of an asymmetric Top Straddle.
Unlike Bottom Straps, this strategy provides an initial positive up-front cash inflow.'''

        elif self.chosen_strategy == "Bottom Strap":
            nrows = 4
            desc = '''A Bottom Strap consists of two long positions in one Call \
and one Put with the same strike price.
You hope there will be a big underlying price move and consider an increase to be more likely than a decrease.
It is a kind of an asymmetric Bottom Straddle.
Unlike Top Straps, this strategy requires an initial investment.'''

        elif self.chosen_strategy == "Top Straddle":
            nrows = 4
            desc = '''A Top Straddle consists of one short position in one Call \
and one Put with the same strike price.
You hope there wont' be a big underlying price move and you are not sure in which direction the move will be.
It is a kind of a symmetric Top Strip (or Strap).
Unlike Bottom Straddles, this strategy provides an initial positive up-front cash inflow.'''

        elif self.chosen_strategy == "Bottom Straddle":
            nrows = 4
            desc = '''A Bottom Straddle consists of one short position in one Call \
and one Put with the same strike price.
You hope there will be a big underlying price move and you are not sure in which direction the move will be.
It is a kind of a symmetric Bottom Strip (or Strap).
Unlike Top Straddles, this strategy requires an initial investment.'''

        elif self.chosen_strategy == "Top Strangle":
            nrows = 4
            desc = '''A Top Strangle consists of one short Call \
at a certain strike price and one short Put with a lower strike price.
You hope there wont' be a big underlying price move and you are not sure in which direction the move will be.
This is a strategy similar to a Top Straddle.
Unlike Bottom Strangles, this strategy provides an initial positive up-front cash inflow.'''

        elif self.chosen_strategy == "Bottom Strangle":
            nrows = 4
            desc = '''A Bottom Strangle consists of one long Call \
at a certain strike price and one long Put with a lower strike price.
You hope there will be a big underlying price move and you are not sure in which direction the move will be.
This is a strategy similar to a Bottom Straddle.
Unlike Top Strangles, this strategy requires an initial investment.'''

        elif self.chosen_strategy == "Top Butterfly":
            nrows = 5
            desc = '''A Top Butterfly consists of one long Call with relative low strike price, \
a long Call with relative higher strike \
price, and two short Calls with a strike that is halfway between the strikes of the Calls.  
You hope there wont' be a big underlying price move and you are not sure in which direction the move will be.
This is a strategy similar to a Top Straddle but with limited losses.
Unlike Bottom Butterfly, this strategy requires an initial investment.'''

        elif self.chosen_strategy == "Bottom Butterfly":
            nrows = 5
            desc = '''A Bottom Butterfly consists of one short Call with relative low strike price, \
a short Call with relative higher strike \  
price, and two long Calls with a strike that is halfway between the strikes of the Calls.  
You hope there will be a big underlying price move and you are not sure in which direction the move will be.
This is a strategy similar to a Bottom Straddle even though profits are limited.
Unlike Top Butterfly, this strategy provides an initial positive up-front cash inflow.'''

        elif self.chosen_strategy == "Top Iron Condor":
            nrows = 5
            desc = '''A Top Iron Condor consits of a Bull (Call/Put) Spread \
and a Bear (Call/Put) Spread, 
with both strikes of the Bear Spread larger than those of the Bull Spread. 
You hope there wont' be a big underlying price move and you are not sure in which direction the move will be.
This is a strategy similar to a Top Strangle but with limited losses.'''   

        elif self.chosen_strategy == "Bottom Iron Condor":
            nrows = 5
            desc = '''A Bottom Iron Condor consits of a Bear (Call/Put) Spread \
and a Bull (Call/Put) Spread, 
with both strikes of the Bull Spread larger than those of the Bear Spread. 
You hope there will be a big underlying price move and you are not sure in which direction the move will be.
This is a strategy similar to a Bottom Strangle even though profits are limited.'''   

        # Save description and number of rows
        Desc["msg"]   = desc
        Desc["nrows"] = nrows 

        return Desc


    def create_tklabel(self, 
                        labelfont  = None, 
                        labelwidth = None, 
                        labeltext  = ""):
        '''
        Create a tkinter Label
        '''
        return tk.Label(master  = self.framel, 
                        width   = None if labelwidth is None else labelwidth,  
                        text    = labeltext,
                        relief  = self.lab_relief,
                        bg      = self.labelbg,
                        fg      = self.labelfg,
                        height  = self.lab_height,
                        font    = labelfont if labelfont is not None else self.lab_font,
                        anchor  = "w")


    def config_tklabel(self,
                        label,
                        labelrow        = None,
                        labelcol        = None,
                        labelcolspan    = None, 
                        labelroweigth   = 1,
                        labelrowsize    = 15,
                        labelcolweight  = 1,
                        labelcolsize    = 15,
                        labelpadx       = None,
                        labelpady       = None, 
                        labelsticky     = "nsw"):
        '''
        Config a tkinter Label and set it in the grid frame
        '''
        # Label dimensions 
        label.rowconfigure(self.gridrow, 
                            weight  = labelroweigth, 
                            minsize = labelrowsize)

        label.columnconfigure(self.gridcol, 
                            weight  = labelcolweight, 
                            minsize = labelcolsize)

        # Set the label in the grid 
        label.grid(row        = labelrow if labelrow is not None else self.gridrow, 
                   column     = labelcol if labelcol is not None else self.gridcol, 
                   columnspan = labelcolspan if labelcolspan is not None else 1, 
                   padx       = labelpadx if labelpadx is not None else self.padx, 
                   pady       = labelpady if labelpady is not None else self.pady, 
                   sticky     = labelsticky)
 

    def create_tkentry(self):
        '''
        Create a tkinter Entry
        '''
        return tk.Entry(master              = self.framel, 
                        width               = self.ent_width, 
                        font                = self.ent_font,
                        bg                  = self.entrybg, 
                        fg                  = self.entryfg,
                        highlightthickness  = self.ent_htick, 
                        borderwidth         = self.ent_bordw)


    def config_tkentry(self,
                        entry, 
                        entrydefval     = None,
                        entryroweigth   = 1,
                        entryrowsize    = 15,
                        entrycolweight  = 1,
                        entrycolsize    = 15,
                        entrypadx       = None,
                        entrypady       = None, 
                        entrysticky     = "nsw"):
        '''
        Config a tkinter Entry and set it in the grid frame
        '''
        # Label dimensions 
        entry.rowconfigure(self.gridrow, 
                            weight  = entryroweigth, 
                            minsize = entryrowsize)

        entry.columnconfigure(self.gridcol, 
                            weight  = entrycolweight, 
                            minsize = entrycolsize)

        # Set the label in the grid 
        entry.grid(row      = self.gridrow, 
                    column  = self.gridcol, 
                    padx    = entrypadx if entrypadx is not None else self.padx,
                    pady    = entrypady if entrypady is not None else self.pady,
                    sticky  = entrysticky)
 
        # Set default value
        if entrydefval is not None:
            entry.insert(0, entrydefval)


    def create_tkbutton(self, 
                        buttoncmd   = None,
                        buttontext  = None,
                        buttonfont  = None,
                        buttonhlth  = None,
                        buttonbordw = None):
        '''
        Create a tkinter Button
        '''
        return tk.Button(master             = self.framel, 
                        width = 8,  
                        text                = buttontext,
                        font                = buttonfont,
                        bg                  = self.buttonbg,
                        fg                  = self.buttonfg,
                        highlightthickness  = buttonhlth if buttonhlth is not None else 0,
                        borderwidth         = buttonbordw if buttonbordw is not None else 0,
                        command             = buttoncmd)


    def config_tkbutton(self,
                        button, 
                        buttonrow        = None,
                        buttoncol        = None,
                        buttoncolspan    = None,
                        buttonroweigth   = 1,
                        buttonrowsize    = 15,
                        buttoncolweight  = 1,
                        buttoncolsize    = 15,
                        buttonpadx       = None,
                        buttonpady       = None, 
                        entrysticky      = "nswe"):
        '''
        Config a tkinter Button and set it in the grid frame
        '''
        # Label dimensions 
        button.rowconfigure(self.gridrow, 
                            weight  = buttonroweigth, 
                            minsize = buttonrowsize)

        button.columnconfigure(self.gridcol, 
                                weight  = buttoncolweight, 
                                minsize = buttoncolsize)

        # Set the label in the grid 
        button.grid(row         = buttonrow if buttonrow is not None else self.gridrow, 
                    column      = buttoncol if buttoncol is not None else self.gridcol, 
                    columnspan  = buttoncolspan if buttoncolspan is not None else 2,
                    padx        = buttonpadx if buttonpadx is not None else self.padx,
                    pady        = buttonpady if buttonpady is not None else self.pady,
                    sticky      = entrysticky)


    def create_tktext(self, 
                        textfont   = None, 
                        textheight = 2, 
                        textwidth  = 85,
                        texthlth   = None):
        '''
        Create a tkinter Label
        '''
        return tk.Text(master               = self.framel, 
                        height              = textheight,
                        width               = textwidth, 
                        relief              = self.lab_relief,
                        bg                  = self.textbg,
                        fg                  = self.textfg,
                        highlightthickness  = texthlth if texthlth is not None else 0,
                        font                = textfont if textfont is not None else self.title_font)


    def config_tktext(self,
                      text, 
                      textmsg     = None,
                      textrow     = None,
                      textcol     = 0,
                      textcolspan = 5, 
                      textpadx    = None,
                      textpady    = None, 
                      textsticky  = "nswe"):
        '''
        Config a tkinter Text and set it in the grid frame
        '''
        # Set the Text widget in the grid 
        text.grid(row        = textrow if textrow is not None else self.gridrow, 
                  column     = textcol if textcol is not None else self.gridcol, 
                  columnspan = textcolspan,
                  padx       = textpadx if textpadx is not None else self.padx,
                  pady       = textpady if textpady is not None else self.pady,
                  sticky     = textsticky)

        # Insert the text
        text.insert("end",textmsg)


    def definepalette(self, palettetype):
        '''
        Set up GUI color palette
        '''
        if palettetype == "light":
            self.mainbg       = "#E0DFDF"
            self.lframebg     = "whitesmoke"

            self.labelbg      = self.lframebg 
            self.entrybg      = "white"
            self.textbg       = self.lframebg 
            self.buttonbg     = self.mainbg 

            self.labelfg      = "black"
            self.entryfg      = "black"
            self.textfg       = "black"
            self.buttonfg     = "black"

            self.rframeplotbg = "#80c1ff"
            self.rframefigbg  = "whitesmoke"
            self.labplotfg    = "black"
            self.sliderplot   = "gray"
            self.sliderlabfg  = "black"

            plt.style.use("seaborn-dark")
            self.root.configure(bg=self.mainbg)

        elif palettetype == "dark":
            self.mainbg       = "#20222B"
            self.lframebg     = "#10121A"

            self.labelbg      = self.lframebg 
            self.entrybg      = "#646773"
            self.textbg       = self.lframebg 
            self.buttonbg     = self.mainbg 

            self.labelfg      = "white"
            self.entryfg      = "white"
            self.textfg       = "white"
            self.buttonfg     = self.lframebg

            self.rframeplotbg = self.mainbg 
            self.rframefigbg  = self.mainbg 
            self.labplotfg    = "white"
            self.sliderplot   = "gray"
            self.sliderlabfg  = "white"

            plt.style.use("seaborn-dark")
            self.root.configure(bg=self.mainbg)
        else:
            raise ValueError("Wrong color palette type name ('light' or 'dark'")