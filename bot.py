from abc import abstractmethod
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
    Creates instance of Chrome Web Driver and initializes state with official guess list

    """
    
    # Initialize Chrome Web Driver
    self.driver = webdriver.Chrome(ChromeDriverManager().install())
    # Intialize word and game states;
    #   -> word_state : begins with complete space of answers + guesses (?)
    #   -> game_state : begins `True`; game is ON
    self.word_state = np.loadtxt('wordle-answers.txt', dtype = str)
    self.game_state = True

  def __open_wordle(self):
      """
      Navigates to official NYT Wordle site

      """

      # Navigate Web Driver to NYT Wordle site
      self.driver.get('https://www.nytimes.com/games/wordle/index.html')
      # Click anywhere to minimize intro tab;
      self.actions = ActionChains(self.driver)
      self.actions.click().perform()
      sleep(2.5)

  def __get_game_tiles(self, idx):
    """
    Returns current game state

    """

    # Interpret .js gameboard
    game_app = self.driver.find_element(By.TAG_NAME , 'game-app')
    game_rows = self.driver.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app).find_elements(By.TAG_NAME, 'game-row')
    game_tiles = self.driver.execute_script('return arguments[0].shadowRoot', game_rows[idx]).find_elements(By.CSS_SELECTOR , 'game-tile')
    return game_tiles

  def __update_game_state(self, game_tiles):
    """
    Evaluates current game state
    
    """

    # Interpret attempt:
    #   -> Each 'evaluation' attribute takes on one of three values: 
    #      {'correct', 'present', 'absent'}
    evals = [tile.get_attribute('evaluation') for tile in game_tiles]
    # Game state;
    #   -> Game ends iff all tags are correct
    #      (given six attempts have not been exhausted)  
    self.game_state = all(eval != 'correct' for eval in evals)

  @abstractmethod
  def play_wordle():
    pass
