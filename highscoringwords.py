__author__ = 'Oliver Ernster'

# Using Python v3.9.7

from collections import OrderedDict
import random
import string


class HighScoringWords:
    MAX_LEADERBOARD_LENGTH = 100  # the maximum number of items that can appear in the leaderboard
    MIN_WORD_LENGTH = 3  # words must be at least this many characters long
    INITIAL_LETTER_COUNT = 7
    letter_values = {}
    valid_words = []
    top_buildable_words = []
    
    def __init__(self, validwords='wordlist.txt', lettervalues='letterValues.txt'):
        """
        Initialise the class with complete set of valid words and letter values by parsing text files containing the data
        :param validwords: a text file containing the complete set of valid words, one word per line
        :param lettervalues: a text file containing the score for each letter in the format letter:score one per line
        :return:
        """
        with open(validwords) as f:
            self.valid_words = f.read().splitlines()

        with open(lettervalues) as f:
            for line in f:
                (key, val) = line.split(':')
                self.letter_values[str(key).strip().lower()] = int(val)

    def display_results(self):
            print("\nHigh Scoring Words:\n")
            print(self.build_leaderboard_for_word_list())
            starting_letters = self.build_starting_letters()
            print(f"\nStarting_letters: {starting_letters}")
            print("\nTop Buildable Words:\n")
            print(self.build_leaderboard_for_letters(starting_letters))

    def create_all_words_scores(self, valid_words):
        all_words_scores = OrderedDict()
        for word in valid_words:
            total_value = 0
            for letter in word:
                total_value += self.letter_values[letter]
            all_words_scores.update({word:total_value})
        return all_words_scores

    def calculate_leaderboard_for_word_list(self, words_scores):
        max_scores = []
        max_score_words = []
        for cnt, (k, v) in enumerate(words_scores.items()):
            if len(max_scores) < self.MAX_LEADERBOARD_LENGTH:
                max_scores.append(v)
                max_score_words.append(k)
            else:
                if cnt == 100:
                    max_score_words = [x for _, x in sorted(zip(max_scores, max_score_words))]
                else:
                    for idx, ms in enumerate(max_scores):
                        if v > ms:
                            max_scores.insert(idx, v)
                            max_scores.pop()
                            max_score_words.insert(idx, k)
                            max_score_words.pop()
                            break
        max_score_words = [x for _, x in sorted(zip(max_scores, max_score_words))]
        return {msw: ms for msw, ms in zip(max_score_words, max_scores)}

    def build_leaderboard_for_word_list(self):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOAD_LENGTH words from the complete set of valid words.
        :return: The list of top words.
        """
        all_words_scores = self.create_all_words_scores(self.valid_words)
        return self.calculate_leaderboard_for_word_list(all_words_scores).keys()

    def build_starting_letters(self):
        letters = [random.choice(string.ascii_letters) for i in range(0, self.INITIAL_LETTER_COUNT)]
        return ''.join([l.lower() for l in letters])
        
    def build_leaderboard_for_letters(self, starting_letters):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words that can be built using only the letters contained in the starting_letters String.
        The number of occurrences of a letter in the startingLetters String IS significant. If the starting letters are bulx, the word "bull" is NOT valid.
        There is only one l in the starting string but bull contains two l characters.
        Words are ordered in the leaderboard by their score (with the highest score first) and then alphabetically for words which have the same score.
        :param starting_letters: a random string of letters from which to build words that are valid against the contents of the wordlist.txt file
        :return: The list of top buildable words.
        """
        candidate_words = []
        for word in self.valid_words:
            word_incomplete = False
            word_letter_counts = {key: word.count(key) for key in set(word)}
            starting_letters_letter_counts = {key: starting_letters.count(key) for key in set(starting_letters)}
            if all([l in starting_letters for l in word]):
                for cnt, k in enumerate(word_letter_counts.keys()):
                    if k in starting_letters:
                        if starting_letters_letter_counts[k] < word_letter_counts[k]:
                            word_incomplete = True
                            break
                if not word_incomplete and len(word) >= 3:
                    candidate_words.append(''.join(word))
        candidate_words_scores = self.create_all_words_scores(candidate_words)
        self.top_buildable_words = self.calculate_leaderboard_for_word_list(candidate_words_scores)
        return self.top_buildable_words.keys()


if __name__ == '__main__':
    hsw = HighScoringWords()
    hsw.display_results()

