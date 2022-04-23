from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import numpy as np
from numpy import random
from time import sleep

class WordleBot:

    """
    A naive bot that makes random guessed-attempts

    Method
    ------
    play_worlde(self) :
        Opens web browser to NYT Wordle site and makes six random guessess 

    """

    def __init__(self):
        """
        Initializes bot with official list of possible and valid guesses

        """
        self.wordle_guesses = np.loadtxt('wordle-guesses.txt', dtype = str)

    def open_wordle(self):
        """
        Creates instance of Chrome Web Driver and navigates to official NYT Wordle site

        """

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('https://www.nytimes.com/games/wordle/index.html')

        self.actions = ActionChains(self.driver)
        self.actions.click().perform()
        sleep(2.5)

    def make_random_guess(self):
        """
        Generates random guess from list of valid guesses

        """

        guess_idx = np.random.randint(low = 0, high = len(self.wordle_guesses))
        guess = self.wordle_guesses[guess_idx]
        self.actions.send_keys(guess)
        self.actions.send_keys(Keys.RETURN)
        self.actions.perform()

    def evaluate_random_guess(self, idx):
        """
        Evaluates the quality of guess at time step `idx` through simple scoring metric

        Parameters
        ----------
        idx : int
            integer indicating attempt number

        Returns
        -------
        correctness : float
            ratio describing quality of attempt
        
        """

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
        """
        Plays single game of Wordle

        """

        # Open Wordle site
        self.open_wordle()

        # Make guesses
        for i in np.arange(6):
            self.make_random_guess()
            self.evaluate_random_guess(i)
            sleep(2.5)

        # Quit
        sleep(3)
        self.driver.quit()

if __name__ == '__main__':
    bot = WordleBot()
    bot.play_wordle()
