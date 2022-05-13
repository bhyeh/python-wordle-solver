from random import Random
from RandomBot import RandomBot
from ReduceBot import ReduceBot
from EntropyBot import EntropyBot

if __name__ == '__main__':
    # replace bot class with desired bot
    bot = ReduceBot()
    bot.play_wordle()
