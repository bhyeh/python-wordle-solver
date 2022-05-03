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

    """An entropy decision bot that makes guess attempts based on word information gain.

    """

    # All possible permutations a word attempt can evaluate to
    patterns = list(itertools.tools.product(['correct', 'present', 'absent'], repeat = 5))

    def __init__(self):
        """\\TODO: Write constructor docstrings
        
        """
        super(EntropyBot, self).__init__()

    def __pattern_match(self, attempt, target):
        """Makes character wise comparison of `attempt` against `target`.

        Following Wordle mode of evaluation:

            pattern_match('BABES', 'ABBEY')
            >>> ['present', 'present', 'correct', 'correct', 'absent']

            calculate_pattern('RURAL', 'LARVA')
            >>> ['absent', 'absent', 'correct', 'present', 'present']
            
            calculate_pattern('STUCK', 'STORY')
            >>> ['correct', 'correct', 'absent', 'absent', 'absent']

            Import note on REPEAT letters attempts:
                Case (1) : Repeated letter is PRESENT only once
                -> Only the first occurence is marked PRESENT, the second/excess is marked
                   ABSENT
                Case (2) : Repeated letter is CORRECT only once
                -> Two further sub-cases:
                    (1) First occurence is CORRECT; then the second is marked ABSENT
                    (2) Second occurence is CORRECT; then the first is marked ABSENT
                Case (3) : Repeated letter is both CORRECT and PRESENT
                -> Excess is marked PRESENT
            
            Precarious edge case:
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
        pattern : list

        """

        # Pattern match `attempt` against `target`
        wrong = [i for i, letter in enumerate(attempt) if target[i] != letter]
        counts = Counter(target[i] for i in wrong)
        pattern = ['correct'] * 5
        for i in wrong:
            letter = attempt[i]
            if counts[letter] > 0:
                pattern[i] = 'present'
                counts[letter] -= 1
            else:
                pattern[i] = 'absent'
        return pattern


    def __generate_pattern_dict(self):
        """For each word and possible information returned, store a list
        of candidate words

            >>> pattern_dict = generate_pattern_dict(['weary', 'bears', 'crane'])
            >>> pattern_dict['crane'][(2, 2, 2, 2, 2)]
            {'crane'}

            >>> sorted(pattern_dict['crane'][(0, 1, 2, 0, 1)])
            ['bears', 'weary']

        Parameters
        ----------

        Returns
        -------
        None

        """

        pattern_dict = defaultdict(lambda: defaultdict(set))
        for word in self.word_state:
            for match in self.word_state:
                pattern = self.__pattern_match(word, match)
                pattern_dict[word][pattern].add(match)
        return dict(pattern_dict)


    def __calculate_entropies(self, words, possible_words, pattern_dict):
        """Calculate the entropy for every word in `words`, taking into account
        the remaining `possible_words`

        Parameters
        ----------

        Returns
        -------
        entropies : dict
        
        """

        entropies = {}
        for word in words:
            counts = []
            for pattern in self.patterns:
                matches = pattern_dict[word][pattern]
                matches = matches.intersection(possible_words)
                counts.append(len(matches))
            entropies[word] = entropy(counts)
        return entropies

    def __update_word_state(self):
        """TODO: Write docstring
        
        """

    def play_wordle(self):
        """Plays game of Wordle.

        Sequence of actions:
            (1) Open Wordle
            (2) Begin playing; while game is ON / attempts left
                -> \\TODO
        
        """

        # Open Wordle site
        self.open_wordle()
        # Play Wordle; until solved or attempts are exhausted 
        idx = 0
        while (self.game_state) and (idx != 6):
            # \\TODO
            pass
        # Click anywhere to minimize outro tab;
        self.actions = ActionChains(self.driver)
        self.actions.click()
        self.actions.perform()
        # Close Web Driver after 15 seconds;
        sleep(15)