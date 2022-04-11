from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import numpy as np
from numpy import random
from time import sleep

class WordleBot():

    """
    

    """

    def __init__(self):
        """
        

        """

        self.wordle_guesses = np.loadtxt('wordle-guesses.txt', dtype = str)

    def open_wordle(self):
        """
        

        """

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('https://www.nytimes.com/games/wordle/index.html')

        self.actions = ActionChains(self.driver)
        self.actions.click().perform()
        sleep(2.5)

    def make_random_guess(self):
        """
        
        
        """

        guess_idx = np.random.randint(low = 0, high = len(self.wordle_guesses))
        guess = self.wordle_guesses[guess_idx]
        self.actions.send_keys(guess)
        self.actions.send_keys(Keys.RETURN)
        self.actions.perform()

    def play_wordle(self):
        """
        

        """

        # Open Wordle site
        self.open_wordle()

        # Make guesses
        for i in np.arange(6):
            self.make_random_guess()
            sleep(2.5)

        # Quit
        sleep(3)
        self.driver.quit()

if __name__ == '__main__':
    bot = WordleBot()
    bot.play_wordle()
