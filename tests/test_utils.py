import unittest
from MBlockchain.utils import is_valid_hash

class TestHashValidation(unittest.TestCase):

   def test_is_valid_hash(self):
        # Test with a valid hash
        valid_hash = '0000abcd1234ef5678901234567890abcdef1234567890abcdef1234567890'
        self.assertTrue(is_valid_hash(valid_hash, 4))

        # Test with an invalid hash
        invalid_hash = 'abcd1234ef5678901234567890abcdef1234567890abcdef1234567890'
        self.assertFalse(is_valid_hash(invalid_hash, 4))

        # Test with a hash that has exactly the required leading zeros
        exact_hash = '00001234ef5678901234567890abcdef1234567890abcdef1234567890'
        self.assertTrue(is_valid_hash(exact_hash, 4))

        # Test with a hash that has more than the required leading zeros
        more_zeros_hash = '00000000abcd1234ef5678901234567890abcdef1234567890abcdef12345678'
        self.assertTrue(is_valid_hash(more_zeros_hash, 4))