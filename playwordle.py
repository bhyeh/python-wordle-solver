from random import Random
from RandomBot import RandomBot
from BruteBot import BruteBot
from EntropyBot import EntropyBot

if __name__ == '__main__':
    # replace bot class with desired bot
    bot = BruteBot()
    bot.play_wordle()