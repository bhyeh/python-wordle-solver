from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import numpy as np
from numpy import random
from time import sleep
# Parent class
from bot import Bot

class BruteBot(Bot):

  """
  A brute force bot making random guessed attempts and updating search space accordingly

  Methods
  --------
  play_wordle(self)
  """

  def __make_random_guess(self):
    """
    Generates random guess from current word state

    """

    guess_idx = random.randint(low = 0, high = len(self.word_state))
    guess = self.word_state[guess_idx]
    self.actions.send_keys(guess)
    self.actions.send_keys(Keys.RETURN)
    self.actions.perform()

  def update_word_state(self, game_tiles):
    """
    Updates word state based on previous attempt; parses and reduces search space based
    on results from last guess

    Parameters
    ----------
    game_tiles : ndarray
      remaining valid guesses


    Meeting Notes: 4/29/22
    ----------------------
    correct word: boats
    Guess   Result/Information gained
    meeep   we can exclude with those letters
    barts   has mix of all cases; new_state all words w/ letters of b at position 1; 
    ----------------------
    
    """

    # Print current state size
    print('Current word state size: {}'.format(self.word_state.size))
    # Initialize lists for correct, present, absent
    #   -> Contents are sublists
    correct = []
    present = []
    absent = []
    # Intialize running list to track PRESENT and CORRECT letters;
    correct_present = []
    # First pass; append CORRECT and PRESENT letters;
    #   -> This helps with resolving issues with REPEAT letters
    for tile in game_tiles:
      letter = tile.get_attribute('letter')
      eval = tile.get_attribute('evaluation')
      if (eval == 'correct') or (eval == 'present'):
        correct_present.append(letter)
    # Second pass; update search space
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
        correct.append([word for word in self.word_state if word[i] == letter])
      # Letter is present in answer
      elif eval == 'present':
        # Add words to new state WITH LETTER in word
        #   -> This requires further filtering; 
        #      E.g: multiple present letters
        #         ('a') : ['apple', 'tank', 'alone' ] 
        #         ('e') : ['rent', 'prey', ... , 'alone ]
        #   -> correct : ['alone']
        #   -> needs to satsify all 'present' tags
        present.append([word for word in self.word_state if letter in word])
      # Letter is not present in answer
      else:
        # Add words to new state WITHOUT LETTER in word
        #   -> Note: only the first PRESENT letter is marked; the second is marked ABSENT
        #   -> Resolve: maintain list of PRESENT letters; add condition 
        #   -> Issue : if repeat letter is before a CORRECT letter; it is marked ABSENT
        #   -> Resolve: maintain list of CORRECT letters
        if letter not in correct_present:
          absent.append([word for word in self.word_state if letter not in word ])
    # Filter lists;
    #   -> Note: Can not use set.intersection() method on empty list
    #   -> Note: It is possible that set.intersection() itself returns an empty list
    sets = [correct, present, absent]
    # Check for non-emptiness
    for i in np.arange(len(sets)):
      subset = sets[i]
      # Perform intersection if subset is non empty
      if subset:
        # Find intersection of SUB-subsets
        sets[i] = list(set.intersection(*map(set, subset)))
    correct, present, absent = tuple(sets)
    # New word state is the INTERSECTION of three sub lists: (correct ∩ present ∩ absent)
    #   -> Note: if either sets - correct, present, or absent are EMPTY;
    #             the intersection including an EMPTY list is also EMPTY
    #   -> Resolve: check for non-emptiness again and intersect on non-empty subsets
    sets = [subset for subset in [correct, present, absent] if subset]
    new_state = np.array(list(set.intersection(*map(set, sets))))
    print('New word state size: {}'.format(new_state.size))
    print('-'*80)
    self.word_state = new_state

    # 5/1/22 Notes:
    #   -> Issue of REPEAT letters
    # 
    #      Case(1) : Repeated letter is PRESENT;
    #      -> In this case, only the first occurence is marked PRESENT; 
    #         and the second occurence is marked ABSENT 
    #
    #      Case(2) : Repeated letter is CORRECT;
    #      -> Two further possible sub-cases :
    #         (1) First occurence is CORRECT, the second occurence is marked ABSENT
    #         (2) Second occurence is CORRECT, the first occurence is marked ABSENT
    #
    #      -> Second sub-case poses problem; as we enumerate attempt we will mark letter absent
    #         w/o knowing it is actually correct somewhere in the attempt
    # 
    #      E.g.
    #      -> Word: LARVA | Attempt: RURAL | Eval : ['ABSENT', 'ABSENT', 'CORRECT', 'PRESENT', 'PRESENT']
    #      -> 'R' is incorrectly removed from search space; effectively removing the answer as well
    # 
    #      -> When we got to check if 'R' is in CORRECT; it will be FALSE b/c we haven't enumerated the CORRECT
    #         'R' yet
    #
    #   -> Resolve: Perform two passes through `game_tiles`; first pass add to list CORRECT and PRESENT letters
    #               second pass enumerate and update space

  def play_wordle(self):
    """
    \\TODO: Write docstring
    

    """

    # Open Wordle site
    self.open_wordle()
    
    # Play Wordle; until solved or attempts exhausted 
    idx = 0
    while (self.game_state) and (idx != 6):
      self.__make_random_guess()
      # Get game state
      game_tiles = self.get_game_tiles(idx)
      # Update game state
      self.update_game_state(game_tiles)
      if not self.game_state:
        break
      else:
        # Update word state
        self.update_word_state(game_tiles)
        # Update idx
        idx += 1
        # Sleepy
        sleep(2.5)

    sleep(2.5)
    # Click anywhere to minimize intro tab;
    self.actions = ActionChains(self.driver)
    self.actions.click().perform()

    sleep(30)
