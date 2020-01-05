"""
Implementation of a simple BloomFilter by Erdeniz Bas
This is inspired by http://codekata.com/kata/kata05-bloom-filters/
"""
import math
import hashlib
from bitstring import BitArray


class BloomFilter:
    """
    BloomFilter class for space-efficent set membership test
    """
    def __init__(self, population_count=500000, arr_len=4000000, case_insensitive=True):
        # TODO: In case the user cares more about false positive rate than memory usage,
        #       it might be possible to calculate arr_len based on population_count and acceptable
        #       false positive probability based on the table
        #       http://pages.cs.wisc.edu/~cao/papers/summary-cache/node8.html
        #       However, I don't have the time to figure out the formula that generated that table

        # Both arguments must be positive
        assert arr_len > 0
        assert population_count > 0
        # Use the formulate given at http://pages.cs.wisc.edu/~cao/papers/summary-cache/node8.html
        hash_count = int((arr_len / population_count) * math.log(2))
        # No point going forward if arr_len is already too small
        if hash_count < 1:
            raise Exception("Array size is to small for given population count."
                            " Please consider increasing the arr_len or decreasing population_count"
                            " such that: (arr_len / population_count) * math.log(2) >= 1")
        self.hash_count = hash_count
        self.bit_vector = BitArray(length=arr_len)
        # Support for case insensitive search should be defined before the bits are set accordingly
        self.case_insensitive = case_insensitive
        self.arr_len = arr_len

    def _digests_for_word_iterator(self, word: str) -> int:
        """
        Iterator method that yields all the md5 digests modulus arr_len. Each digest is salted by a
        monotically increasing int value [0,1,2...hash_count-1]
        :param word: A string that needs to be hashed
        :return: Iterator object of all hashes of param word
        """
        if self.case_insensitive:
            word = word.lower()
        for i in range(self.hash_count):
            # Add salt value
            sword = word + str(i)
            # Encode and hash
            hash_md5 = hashlib.md5(sword.encode('utf-8'))
            digest = int(hash_md5.hexdigest(), 16) % self.arr_len
            yield digest

    def add(self, word: str):
        """
        Sets the bits of word salted hashes in the BitArray
        :param word: A sting that needs to be added to the Bloom Filter
        :return: None
        """
        for digest in self._digests_for_word_iterator(word):
            self.bit_vector.set(True, digest)

    def contains(self, word: str) -> bool:
        """
        Checks if word's salted hashes are set in the BitArray. False positives are possible
        but false negatives are not.
        :param word: A string that needs to be verified
        :return: True if word exists in the Bloom Filter, False otherwise
        """
        for digest in self._digests_for_word_iterator(word):
            if not self.bit_vector[digest]:
                return False
        return True
