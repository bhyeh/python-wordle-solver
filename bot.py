from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import numpy as np
from numpy import random
from time import sleep

class Bot:

  """
  \\TODO: Write class docstring
  
  
  """

  def __init__(self):
    """
    \\TODO: Write docstring
    
    """
    
    self.wordle_guesses = np.loadtxt('wordle-guesses.txt', dtype = str)
