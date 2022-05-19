# Import playable bots
from Bots.RandomBot import RandomBot
from Bots.ReduceBot import ReduceBot
from Bots.ZipfBot import ZipfBot
from Bots.EntropyBot import EntropyBot

if __name__ == '__main__':
    # Replace bot class with desired bot (default Zipf)
    #   -> Check source code for constructor arguments (ZipfBot, EntropyBot)
    #      where computations are required for first runs
    bot = EntropyBot()
    bot.play_wordle()
