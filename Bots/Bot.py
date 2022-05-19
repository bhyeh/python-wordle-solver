# Import packages performing actions on Website
from abc import abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
# Import aux functions
import numpy as np
from numpy import random
from time import sleep

class Bot:

  """Wordle bot parent class.

  Methods
  -------
  open_wordle()
    Navigates Web Driver to NYT Wordle website.

  get_game_tiles(idx)
    Parses gameboard and returns list of 'tile' elements from gameboard and 
    attempt number `idx`.

  update_game_state(game_tiles)
    Updates game state.

  """

  def __init__(self):
    """Constructs necessary attributes for a bot to interact and play Wordle.
    
    Creates instance of Chrome Web Driver and initializes word and game state.

    """
    
    # Initialize Chrome Web Driver
    self.driver = webdriver.Chrome(ChromeDriverManager().install())
    # Intialize word and game states;
    #   -> word_state : begins with complete space of answers + guesses (?)
    #   -> game_state : begins `True`; game is ON
    self.word_state = np.loadtxt('Data\\wordle-answers.txt', dtype = str)
    self.game_state = True

  def open_wordle(self):
      """Navigates Web Driver to NYT Wordle site. 

      """

      # Navigate Web Driver to NYT Wordle site
      #   -> If Wordle ever moves (as it first did when acquired by NYT); code
      #      will likely break (everywhere; not just here)
      self.driver.get('https://www.nytimes.com/games/wordle/index.html')
      sleep(2.5)
      # Click anywhere to minimize intro tab;
      self.actions = ActionChains(self.driver)
      self.actions.click().perform()
      sleep(2.5)

  def get_game_tiles(self, idx):
    """Returns current game state.

    Parameters
    ----------
    idx : int
      Attempt number.
    
    Returns
    -------
    game_tiles : list
      List of 'tile' elements from gameboard and attempt row.

    """

    # Interpret .js gameboard
    game_app = self.driver.find_element(By.TAG_NAME , 'game-app')
    game_rows = self.driver.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app).find_elements(By.TAG_NAME, 'game-row')
    game_tiles = self.driver.execute_script('return arguments[0].shadowRoot', game_rows[idx]).find_elements(By.CSS_SELECTOR , 'game-tile')
    return game_tiles

  def update_game_state(self, game_tiles):
    """Evaluates and updates the current game state.

    Parameters
    ----------
    game_tiles : list
      List of 'tile' elements from gameboard.

    Returns
    -------
    None

    """

    # Interpret attempt:
    #   -> Each 'evaluation' attribute takes on one of three values: 
    #      {'correct', 'present', 'absent'}
    evals = [tile.get_attribute('evaluation') for tile in game_tiles]
    # Game state;
    #   -> Game ends iff all tags are correct
    #      (given six attempts have not been exhausted)
    if all(eval == 'correct' for eval in evals):
      self.game_state = False

  @abstractmethod
  def update_word_state(self):
    pass

  @abstractmethod
  def play_wordle(self):
    pass
