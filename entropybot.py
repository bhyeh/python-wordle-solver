from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import numpy as np
from numpy import random
from time import sleep

from bot import Bot

class EntropyBot(Bot):

  """
  \\TODO: Write class docstring

  """

  def update_state(self, current_state, idx):
    """
    \\TODO: Write docstring

    Parameters
    ----------
    current_state : ndarray
      remaining valid guesses

    idx : int
      integer indicating attempt number

    Returns
    -------
    new_state : ndarray

    Meeting Notes: 4/29/22
    ----------------------
    correct word: boats
    Guess   Result/Information gained
    meeep   we can exclude with those letters
    barts   has mix of all cases; new_state all words w/ letters of b at position 1; 
    ----------------------
    
    """

    # Interpret gameboard
    game_app = self.driver.find_element(By.TAG_NAME , 'game-app')
    game_rows = self.driver.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app).find_elements(By.TAG_NAME, 'game-row')
    game_tiles = self.driver.execute_script('return arguments[0].shadowRoot', game_rows[idx]).find_elements(By.CSS_SELECTOR , 'game-tile')
    # Initialize; correct, present, absent
    correct = []
    present = []
    absent = []
    # Parse pattern
    for i, tile in enumerate(game_tiles):
      letter = tile.get_attribute('letter')
      eval = tile.get_attribute('evaluation')
      # Letter is present and at exact position in answer
      if eval == 'correct':
        # Add words to new state with letter at POSITION `i` in word
        correct += [word for word in current_state if word[i] == letter]
      # Letter is present in answer
      elif eval == 'present':
        # Add words to new state WITH LETTER in word
        present += [word for word in current_state if letter in word]
      # Letter is not present in answer
      else:
        # Add words to new state WITHOUT LETTER in word
        absent += [word for word in current_state if letter not in word ]
    # New worde state is INTERSECTION of three states; (correct x present x absent)
    new_state = list(set.intersection(*map(set, [correct, present, absent])))
    return new_state

  def calculate_information_gain_aux(self, word):
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

  def play_wordle(self):
    """
    \\TODO: Write docstring
    

    """

    # Open Wordle site
    self.open_wordle()

    # Make guesses
    for i in np.arange(6):

      sleep(2.5)

    # Quit
    sleep(3)
    self.driver.quit()