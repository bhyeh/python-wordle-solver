from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import numpy as np
from numpy import random
from time import sleep

from bot import Bot

class EntropyBot:

  """
  \\TODO: Write class docstring

  """

  def __init__(self):
      """
      Initializes bot with official list of possible and valid guesses

      """
      self.wordle_guesses = np.loadtxt('wordle-guesses.txt', dtype = str)


  def update_state(self, word, idx):
    """
    \\TODO: Write docstring

    Parameters
    ----------
    idx : int
      integer indicating attempt number

    word: str
      guess at current attempt number

    Returns
    -------
    new_state : ndarray
    
    """

    # Current dictionary state
    old_state = self.wordle_guesses
    new_state = []

    # Interpret gameboard
    game_app = self.driver.find_element(By.TAG_NAME , 'game-app')
    game_rows = self.driver.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app).find_elements(By.TAG_NAME, 'game-row')
    game_tiles = self.driver.execute_script('return arguments[0].shadowRoot', game_rows[idx]).find_elements(By.CSS_SELECTOR , 'game-tile')

    # Parse pattern
    for i, tile in enumerate(game_tiles):
      eval = tile.get_attribute('evaluation')
      letter = word[i]
      if eval == 'correct':
        # Add words from state with letter at position `i` in word
        new_state += [word for word in old_state if word[i] == letter]
      elif eval == 'present':
        # Add words from state with letter in word
        new_state += [word for word in old_state if letter in word]
      else:
        # Add words from state without letter is in word
        new_state += [word for word in old_state if letter not in word ]
    
    return np.array(new_state)

  def calculate_entropy(self, word):
    """"
    \\TODO: Write docstring


    Parameters
    ----------

    Returns
    -------
    
    """

    pass

  def calculate_information_gain(self):
    """
    \\TODO: Write docstring
    
    """

    pass