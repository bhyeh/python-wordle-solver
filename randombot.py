from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import numpy as np
from numpy import random
from time import sleep
# Import parent class
from Bot import Bot

class RandomBot(Bot):

    """A bot that makes random guessed attempts.

    Method
    ------
    play_worlde()
        Opens web browser, navigates to NYT Wordle site, and proceeds to make six random guessed-attempts.

    """

    def __make_random_guess(self):
        """Generates random guess from current word state and plays guess.

        """

        # Generate random guess
        guess_idx = random.randint(low = 0, high = len(self.word_state))
        guess = self.word_state[guess_idx]
        # Play guess on gameboard
        self.actions.send_keys(guess)
        self.actions.send_keys(Keys.RETURN)
        self.actions.perform()

    def evaluate_guess(self, idx):
        """Evaluates the quality of guess at time step `idx` through simple scoring metric.

        Scoring system:
            (1) Each letter of an attempt can take on three values: 'correct', 'present', 'absent'
                --> 'correct' : letter is in answer and at correct position
                --> 'present' : letter is in answer but at incorrect position
                --> 'absent'  : letter is not in answer
            (2) Assign each label an integer value
                --> 'correct' : 2
                --> 'present' : 1
                --> 'absent'  : 0
            (3) Score an attempt by evaluating each letter, multiply by coresponding label-integer, sum and 
                divide by 10. 
                --> Maximum score is 1.0 (all letters correct)
                --> Minimum score is 0.0 (no letters in answer)

        Parameters
        ----------
        idx : int
            integer indicating attempt number

        Returns
        -------
        None
        
        """

        # Interpret gameboard
        game_app = self.driver.find_element(By.TAG_NAME , 'game-app')
        game_rows = self.driver.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app).find_elements(By.TAG_NAME, 'game-row')
        letters = self.driver.execute_script('return arguments[0].shadowRoot', game_rows[idx]).find_elements(By.CSS_SELECTOR , 'game-tile')

        # Quantize evaluation 
        eval_to_int = {
            'correct' : 2,
            'present' : 1,
            'absent'  : 0
        }

        # Evaluate guess
        correctness = 0
        for letter in letters:
            correctness += eval_to_int[letter.get_attribute('evaluation')]
        correctness /= 10
        print('Correctness: {:.2f}'.format(correctness))

    def play_wordle(self):
        """Plays game of Wordle.

        Sequence of actions:
        (1) Open Wordle
        (2) Begin playing; while game is ON / attempts left
            -> Make random guess and play it
            -> Retrieve game state
            -> Update game state
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
                # Update idx
                idx += 1
                # Sleepy
                sleep(2.5)
        # Click anywhere to minimize intro tab;
        self.actions = ActionChains(self.driver)
        self.actions.click()
        self.actions.perform()
        # Close Web Driver after 15 seconds;
        sleep(15)
