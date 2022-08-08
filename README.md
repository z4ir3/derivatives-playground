# derivatives-playground

**Black-Scholes** option pricing GUIs 

**First GUI**: plot of option prices and greeks using python **tkinter** library.

<img src="/data/images/gui-screenshot.png" height="500" width="800">

Plain vanilla **Call** and **Put** options. Use the sliders to interactively update plots.  

### Structure

  * Main file *main_gui_bs.py*
  * GUI class in *src/guisliders.py*
  * Black-Scholes option pricing model class in *models/blackscholes.py* 

Please follow the links below for further details about option pricing:
  * A very gentle [introduction to option contracts](http://leonardorocchi.info/topics-pages/qfin/intro-option-contracts/intro-option-contracts.html)
  * General [properties of options prices](http://leonardorocchi.info/topics-pages/qfin/properties-option-pricing/properties-option-pricing.html)
  * Derivation of the [Black-Scholes option pricing model](http://leonardorocchi.info/topics-pages/qfin/black-scholes-option-pricing-model/bs-option-pricing-model.html)




**Second GUI**: option strategy payoff calculator and plot using python **tkinter** library.

<img src="/data/images/gui-strategy-screenshot.png" height="500" width="800">

### Structure

  * Main file *main_gui_bstrategy.py*
  * GUI class in *src/guislidersrtrategy.py*
  * Black-Scholes option pricing model class in *models/blackscholestrategy.py* 