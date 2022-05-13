# Import playable bots
from random import Random
from RandomBot import RandomBot
from ReduceBot import ReduceBot
from ZipfBot import ZipfBot
from EntropyBot import EntropyBot

if __name__ == '__main__':
    # Replace bot class with desired bot
    #   -> Check source for constructor arguments (ZipfBot, EntropyBot)
    bot = ZipfBot()
    bot.play_wordle()
