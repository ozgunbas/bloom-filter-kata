"""
Test for bloom_filter.py module by Erdeniz Bas
"""

import random
import string
import unittest
import urllib.request
from bloom_filter import BloomFilter


class BloomFilterTests(unittest.TestCase):

    @staticmethod
    def _dict(download=False):
        if not download:
            with open('wordlist.txt') as file_p:
                return file_p.read().splitlines()
        words = []
        with urllib.request.urlopen('http://codekata.com/data/wordlist.txt') as resp:
            for i in resp.readlines():
                word = i.decode("windows-1252")[:-1]
                words.append(word)
        return words

    def setUp(self):
        self.bf_ignore_case = BloomFilter()
        self.bf_case = BloomFilter(case_insensitive=False)
        for word in self._dict():
            self.bf_ignore_case.add(word)
            self.bf_case.add(word)

    @staticmethod
    def _gen_str(length=5):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def assert_filter_accuracy(self, filter_obj, words_in_dict, words_not_in_dict):
        for word in words_in_dict:
            self.assertTrue(filter_obj.contains(word))
        for word in words_not_in_dict:
            self.assertFalse(filter_obj.contains(word))

    def test_bloom_filter_simple(self):
        words_in_dict = ['who', 'searching', 'home', 'run', 'segmentalization']
        words_not_in_dict = ['', 'erdeniz', 'jawn', 'aaaaaaaaaaaargh', 'missspell']
        self.assert_filter_accuracy(self.bf_ignore_case, words_in_dict, words_not_in_dict, )

    def test_bloom_filter_case_sensitive(self):
        words_in_dict = ['AA\'s', 'Runyon', 'searching', 'home', 'run', 'segmentalization']
        words_not_in_dict = ['', 'aa\'s', 'runyon', 'Searching', 'Run', 'HOME']
        self.assert_filter_accuracy(self.bf_case, words_in_dict, words_not_in_dict)

    def test_bloom_filter_random(self):
        total_words = 100000
        false_positive = 0
        positives = 0
        word_dict = set(w.lower() for w in self._dict())
        for _ in range(total_words):
            gword = self._gen_str()
            if self.bf_ignore_case.contains(gword):
                positives += 1
                if gword not in word_dict:
                    false_positive += 1
            elif gword in word_dict:
                self.fail("False negatives are unacceptable")
        print(f"Total words    = {total_words}")
        print(f"False positive = {false_positive}")
        print(f"Positives      = {positives}")
        print(f"Negatives      = {total_words - positives}")


if __name__ == '__main__':
    unittest.main()
