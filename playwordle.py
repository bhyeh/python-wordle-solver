from random import Random
from randombot import RandomBot
from brutebot import BruteBot
from entropybot import EntropyBot

if __name__ == '__main__':
    # replace bot class with desired bot
    bot = BruteBot()
    bot.play_wordle()