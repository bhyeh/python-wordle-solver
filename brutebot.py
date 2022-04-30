from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import numpy as np
from numpy import random
from time import sleep
# Parent class
from bot import Bot

class BruteBot(Bot):

  """
  \\TODO: Write class docstring

  """

  def make_random_guess(self):
    """
    Generates random guess from list of valid guesses

    """

    guess_idx = random.randint(low = 0, high = len(self.state))
    guess = self.state[guess_idx]
    self.actions.send_keys(guess)
    self.actions.send_keys(Keys.RETURN)
    self.actions.perform()

  def update_state(self, idx):
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

    # Print current state size
    print('Current word state size: {}'.format(self.state.size))
    # Interpret .js gameboard
    game_app = self.driver.find_element(By.TAG_NAME , 'game-app')
    game_rows = self.driver.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app).find_elements(By.TAG_NAME, 'game-row')
    game_tiles = self.driver.execute_script('return arguments[0].shadowRoot', game_rows[idx]).find_elements(By.CSS_SELECTOR , 'game-tile')
    # Initialize; correct, present, absent
    correct = []
    present = []
    absent = []
    # Further intialize list to track already present letters
    present_letters = []
    # Parse pattern
    for i, tile in enumerate(game_tiles):
      letter = tile.get_attribute('letter')
      eval = tile.get_attribute('evaluation')
      # Letter is present and at exact position in answer
      if eval == 'correct':
        # Add words to new state with letter at POSITION `i` in word;
        #   -> This requires further filtering; 
        #      E.g: multiple correct letters at multiple positions
        #         ('t' @ idx 0) : ['train', 'tank', ... ] 
        #         ('r' @ idx 1) : ['train', 'brain', ... ]
        #   -> correct : ['train']
        #   -> needs to satsify all 'correct' tags
        correct.append([word for word in self.state if word[i] == letter])
      # Letter is present in answer
      elif eval == 'present':
        # Add words to new state WITH LETTER in word
        #   -> This requires further filtering; 
        #      E.g: multiple present letters
        #         ('a') : ['apple', 'tank', 'alone' ] 
        #         ('e') : ['rent', 'prey', ... , 'alone ]
        #   -> correct : ['alone']
        #   -> needs to satsify all 'present' tags
        present.append([word for word in self.state if letter in word])
      # Letter is not present in answer
      else:
        # Add words to new state WITHOUT LETTER in word
        #   -> Note: only the FIRST present letter is marked; the second 
        #            will appear ABSENT;
        #   -> Resolve: maintain list of present letters; add condition 
        if letter not in present_letters:
          absent.append([word for word in self.state if letter not in word ])
    # Filter lists;
    #   -> Note: Can not use set.intersection() method on empty list
    #   -> Note: It (might) be possible that set.intersection() returns
    #            an empty list
    sets = [correct, present, absent]
    # Check for non-emptiness
    for i in np.arange(len(sets)):
      subset = sets[i]
      # Check if subset is non-empty
      if subset:
        # Find intersection of sub-subsets
        sets[i] = list(set.intersection(*map(set, subset)))
    correct, present, absent = tuple(sets)
    print('-'*80)
    print('Correct subset size: {}'.format(len(correct)))
    print('Present subset size: {}'.format(len(present)))
    print('Absent subset size: {}'.format(len(absent)))
    # New word state is the INTERSECTION of three sub lists: (correct ∩ present ∩ absent)
    #   -> Issue: if either sets - correct, present, or absent are EMPTY;
    #             the intersection including an EMPTY list is also EMPTY
    #   -> Resolve: filter set and include only non-empty subsets
    sets = [subset for subset in [correct, present, absent] if subset]
    new_state = np.array(list(set.intersection(*map(set, sets))))
    print('New word state size: {}'.format(new_state.size))
    print('-'*80)
    if new_state.size < 10:
      print(new_state)
    self.state = new_state

  def play_wordle(self):
    """
    \\TODO: Write docstring
    

    """

    # Open Wordle site
    self.open_wordle()

    # Make guesses
    for idx in np.arange(6):
      # Make random guesses (for now)
      self.make_random_guess()
      # Update word state
      self.update_state(idx)
      sleep(2.5)

    # Quit
    # sleep(3)
    # self.driver.quit()