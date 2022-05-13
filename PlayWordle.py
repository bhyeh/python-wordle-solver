from random import Random
from RandomBot import RandomBot
from ReduceBot import ReduceBot
from ZipfBot import ZipfBot
from EntropyBot import EntropyBot

if __name__ == '__main__':
    # replace bot class with desired bot
    bot = ZipfBot(True)
    bot.play_wordle()
