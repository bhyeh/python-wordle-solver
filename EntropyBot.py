from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import itertools
import numpy as np
# from scipy.stats import entropy
from collections import defaultdict, Counter
from time import sleep
# Parent class
from Bot import Bot

class EntropyBot(Bot):

    """An entropy decision bot that makes guess attempts based on information gain.

    """

    def __init__(self):
        """\\TODO: Write constructor docstrings
        
        """
        
        super(EntropyBot, self).__init__()
        # Initialize all possible permutations a guess can evaluate to
        self.patterns = list(itertools.tools.product(['correct', 'present', 'absent'], repeat = 5))  
        # Precompute dictionary containing all possible word `branches` for an attempt and pattern
        #   -> Read method docstring for more;
        self.pattern_dict = self.__create_pattern_dict()

    def __pattern_match(self, attempt, target):
        """Makes character wise comparison of `attempt` against `target`.

        Following Wordle's mode of evaluation:

            pattern_match('BABES', 'ABBEY')
            >>> ['present', 'present', 'correct', 'correct', 'absent']

            pattern_match('RURAL', 'LARVA')
            >>> ['absent', 'absent', 'correct', 'present', 'present']
            
            pattern_match('STUCK', 'STORY')
            >>> ['correct', 'correct', 'absent', 'absent', 'absent']

            Import note on REPEAT letters attempts:
                Case (1) : Repeated letter is PRESENT only once
                -> First occurence is marked PRESENT, excess is marked ABSENT
                Case (2) : Repeated letter is CORRECT only once
                -> Excess is marked ABSENT
                Case (3) : Repeated letter is both CORRECT and PRESENT
                -> Excess is marked PRESENT
            
            Edge case:
                E.g: 'RURAL' against 'LARVA'
                -> Should evaluate to :     ['ABSENT', 'absent', 'correct', 'present', 'present']
                -> Should NOT evaluate to : ['PRESENT', 'absent', 'correct', 'present', 'present']
        
        Parameters
        ----------
        attempt : str

        target : str
            Word to pattern match against.

        Returns
        -------
        pattern : tuple
            Tuple strings resembling evaluation style of Wordle.

        """

        # First pass; determine letter indices in which `attempt` and `target` do not match
        #   -> Append index at incident
        mismatching_idx = [i for i, a, t in enumerate(zip(attempt, target)) if a != t]
        # Retrieve the letters of `target` that did not match with `attempt`
        mismatching = [target[i] for i in mismatching_idx]
        # Create counter object to count occurence of each mismatching letter in `target`
        counts = Counter(mismatching)
        # Second pass; determine which of two cases wrong letter falls into:
        #   ->  PRESENT or ABSENT
        pattern = ['correct', 'correct', 'correct', 'correct', 'correct']
        for i in mismatching_idx:
            # The letter of `attempt`
            letter = attempt[i]
            # The letter is PRESENT
            if counts[letter] > 0:
                pattern[i] = 'present'
                # Decremenet count;
                #   -> If letter is repeated again, excess needs to be marked ABSENT
                counts[letter] -= 1
            # The letter is ABSENT
            else:
                pattern[i] = 'absent'
        pattern = tuple(pattern)
        return pattern


    def __create_pattern_dict(self):
        """Computes and stores all possible word `branches` from an attempt and pattern.

        The object returned is a double nested dictionary structure with key1 as word and key2
        a pattern and string list as final value. 

        Structure : 

            {'word1' : {'pattern1' : list,
                        'pattern2' : list,
                         ...
                         ...
                        'patternN : list},
                         
             'wordN' : {'pattern1' : list,
                        'pattern2' : list,
                         ...
                         ...
                        'patternN : list}}

            E.g: 
                Consider word state is the following:
                -> ['SHARP', 'CHARD', 'HEARD', 'HAIRY', 'WHARF', 'HARRY', ']
                Then as example if:
                ->  key1  : 'SHARP'
                    key2  : 'absent', 'present', 'present', 'correct', 'absent'
                ->  value : ['CHARD', 'HEARD', 'HAIRY', 'WHARF', 'HARRY']

        Parameters
        ----------

        Returns
        -------
        pattern_dict : dict

        """

        pattern_dict = defaultdict(lambda: defaultdict(set))
        # Iterate through each word in word state
        for word in self.word_state:
            # Iterate again through each word in word state
            #   -> This time to compare agaisnt
            for match in self.word_state:
                # Pattern match word against match
                pattern = self.__pattern_match(word, match)
                # Append pattern matched word
                pattern_dict[word][pattern].add(match)
        return pattern_dict


    def __calculate_entropies(self):
        """\\TODO: Write docstring

        Parameters
        ----------

        Returns
        -------
        entropies : dict
        
        """

        entropies = dict()
        # Iterate over words in word state
        for word in self.word_state:
            # Discrete distribution over pattern
            counts = []
            # Iterate over all 243 possible evaluations
            #   -> Effectively builds a distribution over possible patterns
            for pattern in self.patterns:
                # `matches` is a list of words branching from `word` that satsify `pattern`
                #   -> Can be empty
                matches = self.pattern_dict[word][pattern]
                # Append length of `matches`; this is the frequency for a given pattern 
                counts.append(len(matches))
            # Calculates entropy from discrete distribution
            # entropies[word] = entropy(counts)
        return entropies

    def __make_guess(self, entropies):
        """\\TODO: Write docstring

        Parameters
        ----------
        entropies : dict

        Returns
        -------
        None
        
        """

        # Determine word with highest entropy
        #   -> Retrieve key from dictionary with highest value
        guess = max(entropies.items(), key=lambda x: x[1])[0]   
        # Play guess on gameboard
        self.actions.send_keys(guess)
        self.actions.send_keys(Keys.RETURN)
        self.actions.perform()

    def __update_word_state(self, game_tiles):
        """Filters word state
        
        """

        # \\HARD TODO;
        pass

    def play_wordle(self):
        """Plays game of Wordle.

        Sequence of actions:
            (1) Open Wordle
            (2) Begin playing; while game is ON / attempts left
                -> Calculate entropies from current word state
                -> Guess word w/ maximum entropy
                -> Reduce word state
                -> Repeat
        
        """

        # Open Wordle site
        self.open_wordle()
        # Play Wordle; until solved or attempts are exhausted 
        idx = 0
        while (self.game_state) and (idx != 6):
            # Calculate entropies
            entropies = self.__calculate_entropies()
            # Determine best guess
            self.__make_guess(entropies)
            # Get game state
            game_tiles = self.get_game_tiles(idx)
            # Update game state
            self.update_game_state(game_tiles)
            # Game is won
            if not self.game_state:
                break
            # Continue game
            else:
                # Update word state
                self.__update_word_state(game_tiles)
                # Increment idx
                idx += 1
                # Sleepy
                sleep(2.5)
        # Click anywhere to minimize outro tab;
        self.actions = ActionChains(self.driver)
        self.actions.click()
        self.actions.perform()
        # Close Web Driver after 15 seconds;
        sleep(15)
