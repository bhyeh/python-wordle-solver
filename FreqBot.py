# Import packages performing actions on Website
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# Import aux functions
import numpy as np
from numpy import random
from time import sleep
# Parent class
from Bot import Bot

class FreqBot(Bot):

    """A greedy bot that makes attempts based on current word state and frequency
    of letters. 

    Methods
    -------
    play_wordle()
        \\TODO: Write docstrings. 
    
    """

    def __make_random_guess(self):
        """Generates random guess from current word state and plays guess.

        In FreqBot class, start game by random guess from word state. 

        """

        # Generate random guess
        guess_idx = random.randint(low = 0, high = len(self.word_state))
        guess = self.word_state[guess_idx]
        # Play guess on gameboard
        self.actions.send_keys(guess)
        self.actions.send_keys(Keys.RETURN)
        self.actions.perform()

    def __update_word_state(self, game_tiles):
        """Updates word state based on most recent attempt.
        
        Parses current game state through `game_tiles` and reduces search space 
        based on the tile evaluation results.

        Parameters
        ----------
        game_tiles : list
            List of 'tile' elements from gameboard.

        Returns
        -------
        None
        
        """

        pass

    def __rank_word_state(self):
        """\\TODO: Write docstrings.
        
        """

        pass


    def play_wordle(self):
        """Plays game of Wordle.

        Sequence of actions:
            (1) Open Wordle
            (2) Begin playing; while game is ON / attempts left
                -> Make random guess and play it
                -> Retrieve game state
                -> Update game state
                -> Update word state
                -> Repeat

        """

        # Open Wordle site
        self.open_wordle()
        # Play Wordle; until solved or attempts are exhausted 
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
                self.__update_word_state(game_tiles)
                # Update idx
                idx += 1
                # Sleepy
                sleep(2.5)
        # Click anywhere to minimize outro tab;
        self.actions = ActionChains(self.driver)
        self.actions.click()
        self.actions.perform()
        # Close Web Driver after 15 seconds;
        sleep(15)