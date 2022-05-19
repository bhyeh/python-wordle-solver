# Import playable bots
from RandomBot import RandomBot
from ReduceBot import ReduceBot
from ZipfBot import ZipfBot
from EntropyBot import EntropyBot

if __name__ == '__main__':
    # Replace bot class with desired bot
    #   -> Check source code for constructor arguments (ZipfBot, EntropyBot)
    #      where computations are required for first runs
    bot = ZipfBot()
    bot.play_wordle()
