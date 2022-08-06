'''
Interactive Option strategy payoff calculator GUI
Options priced with with the Black-Scholes model 
The GUI is built with tkinter and uses matplotlib sliders
Copyright (c) @author: leonardorocchi
'''

import tkinter as tk
from src.guisliderstrategy import PlotGUI


def main_gui():
    root = tk.Tk()
    Gui = PlotGUI(root)
    Gui.root.mainloop()


if __name__ == "__main__":
    main_gui()