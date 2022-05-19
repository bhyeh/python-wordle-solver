# Import packages performing actions on Website
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# Import aux libraries
import pickle
import itertools
import numpy as np
import numpy.random as random
from scipy.stats import entropy
from collections import defaultdict, Counter
from time import sleep
# Import parent class
from Bots.Bot import Bot

class EntropyBot(Bot):

    """An entropy decision bot that makes guess attempts based on information 
    gain.
    
    Methods
    -------
    play_wordle()
        Opens web browser, navigates to NYT Wordle site, and proceeds to play a 
        game of Wordle using a greedy entropy based strategy. 
    
    make_guess()
        Generates a greedy guess from current word state and considering 
        highest entropy score. 

    update_word_state()
        Updates word state based on most recent attempt.
        
        Parses current game state through `game_tiles` and reduces search space 
        based on the tile evaluation results 

    """

    def __init__(self, k = 5, compute = False):
        """Constructor with additional attributes for bot to play Wordle using 
        word-ranking from entropy scoring.

        Attributes
        ----------
        k : int
            Indicates top 'k' openers (based on entropy score) to sample from 
            and begin game with.

        compute : bool
            Indicate to compute pattern dictionary at game start.

        """
        super(EntropyBot, self).__init__()
        # Initialize size of top openers to sample from
        self.k = k
        # Initialize all possible permutations a guess can evaluate to
        self.patterns = list(itertools.product(('correct', 'present', 'absent'), repeat = 5))  
        # Precompute dictionary containing all possible word `branches` for an attempt and pattern
        #   -> Read method docstring for more;
        if compute:
            self.pattern_dict = self.__create_pattern_dict()
        else:
            with open('Data\\pattern_dict.pkl', 'rb') as dict:
                self.pattern_dict = pickle.load(dict)

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
        """Computes and stores all possible word `branches` from an attempt and 
        pattern.

        The object returned is a double nested dictionary structure with key1 
        as word and key2 a pattern and string list as final value. 

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
        None

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
        """Calculates the entropy for each word in the current word state.

        Parameters
        ----------
        None 

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
            entropies[word] = entropy(counts)
        return entropies

    def __make_first_guess(self, entropies):
        """Generates an opening guess from initial word state by considering 
        top 'k' words with the highest entropy value. 

        Parameters
        ----------
        entropies : dict

        Returns
        -------
        None
        
        """

        # Determine top 'k' words with highest entropy
        openers = [k for k, _ in sorted(entropies.items(), key = lambda item: item[1], reverse = True)][:self.k]
        guess = random.choice(openers, 1)[0]
        # Define boolean mask to exclude guess in word_state
        bool_mask = self.word_state != guess
        print('Guess: ', guess)
        print('Entropy score: {:.2f}'.format(entropies[guess]))
        # Play guess on gameboard
        self.actions.send_keys(guess)
        self.actions.send_keys(Keys.RETURN)
        self.actions.perform()
        # Remove from word state the just played word
        self.word_state = self.word_state[bool_mask]

    def __make_guess(self, entropies):
        """Generates a greedy guess from current word state by considering 
        highest entropy score. 

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
        # Define boolean mask to exclude guess in word_state
        bool_mask = self.word_state != guess
        print('Guess: ', guess)
        print('Entropy score: {:.2f}'.format(entropies[guess]))
        # Play guess on gameboard
        self.actions.send_keys(guess)
        self.actions.send_keys(Keys.RETURN)
        self.actions.perform()
        # Remove from word state the just played word
        self.word_state = self.word_state[bool_mask]

    def __update_word_state(self, game_tiles):
        """Updates word state based on most recent attempt.
        
        Parses current game state through `game_tiles` and reduces search space 
        based on the tile evaluation results. 

        Parameters
        ----------
        game_tiles : list
            List of 'tile' elements from gameboard.

        Returns
        -------
        None
        
        """

        # Print current state size
        print('Current word state size: {}'.format(self.word_state.size))
        # Initialize lists for correct, present, absent
        #   -> Elements of each are sublists
        correct = []
        present = []
        absent = []
        # First pass; append CORRECT and PRESENT letters;
        #   -> This helps with resolving issues of REPEAT letters
        # Intialize running list to track PRESENT and CORRECT letters;
        correct_present = []
        for tile in game_tiles:
            letter = tile.get_attribute('letter')
            eval = tile.get_attribute('evaluation')
            if (eval == 'correct') or (eval == 'present'):
                correct_present.append(letter)
        # Second pass; update search space;
        #   -> 
        pattern = []
        word = ''
        for i, tile in enumerate(game_tiles):
            letter = tile.get_attribute('letter')
            eval = tile.get_attribute('evaluation')
            # Pattern matching
            pattern.append(eval)
            word += letter
            # Letter is present and at exact position in answer
            if eval == 'correct':
                # Add words to new state with letter at POSITION `i` in word;
                #   -> This requires later filtering; 
                #      E.g: multiple correct letters at multiple positions
                #         ('t' @ idx 0) : ['train', 'tank', ... ] 
                #         ('r' @ idx 1) : ['train', 'brain', ... ]
                #   -> correct : ['train']
                #   -> needs to satsify all 'CORRECT' tags
                correct.append([word for word in self.word_state if word[i] == letter])
            # Letter is present in answer
            elif eval == 'present':
                # Add words to new state WITH LETTER in word
                #   -> This requires further filtering; 
                #      E.g: multiple present letters
                #         ('a') : ['apple', 'tank', 'alone' ] 
                #         ('e') : ['apple', 'prey', 'alone ]
                #   -> present : ['apple', 'alone']
                #   -> needs to satsify all 'PRESENT' tags
                present.append([word for word in self.word_state if letter in word])
            # Letter is not present in answer
            else:
                # Add words to new state WITHOUT LETTER in word
                #   -> Note: only the first PRESENT letter is marked; the second is marked ABSENT
                #   -> Resolve: maintain list of PRESENT letters; add condition 
                #   -> Issue : if repeat letter is before a CORRECT letter; it is marked ABSENT
                #   -> Resolve: maintain list of CORRECT letters
                # Add iff letter is correct/present already (REPEAT case handling)
                if letter not in correct_present:
                    absent.append([word for word in self.word_state if letter not in word ])
        # Retrieve pattern
        pattern = tuple(pattern)
        # Filter lists; each list is sublist satsifying different letter properties
        #   -> For each list, we intersect and find common between each sublist
        #   -> Note: Can not use set.intersection() method on empty list
        #   -> Note: It is possible that set.intersection() itself returns an empty list
        sets = [correct, present, absent]
        for i in np.arange(len(sets)):
            subset = sets[i]
            # Perform intersection method if list is non empty
            if subset:
                # Find intersection of sub list 
                sets[i] = list(set.intersection(*map(set, subset)))
        correct, present, absent = tuple(sets)
        # New word state is the INTERSECTION of three lists: (correct ∩ present ∩ absent)
        #   -> Note: if either sets - correct, present, or absent are EMPTY;
        #            the intersection including an EMPTY list is also EMPTY
        #   -> Resolve: check for non-emptiness again and intersect on non-empty subsets
        sets = [subset for subset in [correct, present, absent] if subset]
        # Add to sets the pattern matched words;
        sets.append(list(self.pattern_dict[word][pattern]))
        # Intersect on all FOUR sets now;
        new_state = np.array(list(set.intersection(*map(set, sets))))
        self.word_state = new_state
        print('New word state size: {}'.format(new_state.size))
        print('-'*80)

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
            # If first guess; begin with opener from the top 'k' ranked openers
            if(idx == 0):
                self.__make_first_guess(entropies)
            # Else; determine best guess from highest ranked entropy 
            # word
            else:
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
        # Close Web Driver after 20 seconds;
        sleep(20)
