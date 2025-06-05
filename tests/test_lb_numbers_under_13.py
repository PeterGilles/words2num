import unittest
from words2num import w2n

class TestLuxembourgishNumbersUnder13(unittest.TestCase):
    def test_numbers_under_13_not_converted(self):
        """Test that single numbers under 13 are not converted."""
        numbers_under_13 = [
            'eent', 'een', 'eng',  # 1
            'zwee',                 # 2
            'dräi',                # 3
            'véier',               # 4
            'fënnef',              # 5
            'sechs',               # 6
            'siwen',               # 7
            'aacht',               # 8
            'néng',                # 9
            'zéng',                # 10
            'eelef',               # 11
            'zwielef'              # 12
        ]
        
        for number in numbers_under_13:
            with self.subTest(number=number):
                with self.assertRaises(ValueError) as context:
                    w2n(number, lang='lb')
                self.assertIn(f"Numbers under 13 ('{number}') should not be converted", str(context.exception))
    
    def test_compound_numbers_with_under_13(self):
        """Test that compound numbers containing numbers under 13 are converted correctly."""
        test_cases = [
            ('eenhonnert', 100),        # 1 hundred
            ('zweehonnert', 200),       # 2 hundred
            ('dräihonnert', 300),       # 3 hundred
            ('véierhonnert', 400),      # 4 hundred
            ('fënnefhonnert', 500),     # 5 hundred
            ('sechshonnert', 600),      # 6 hundred
            ('siwenhonnert', 700),      # 7 hundred
            ('aachthonnert', 800),      # 8 hundred
            ('nénghonnert', 900),       # 9 hundred
            ('zéng honnert', 1000),     # 10 hundred
            ('eelefhonnert', 1100),     # 11 hundred
            ('zwielefhonnert', 1200),   # 12 hundred
            ('eendausend', 1000),       # 1 thousand
            ('zweedausend', 2000),      # 2 thousand
            ('dräidausend', 3000),      # 3 thousand
            ('véierdausend', 4000),     # 4 thousand
            ('fënnefdausend', 5000),    # 5 thousand
            ('sechsdausend', 6000),     # 6 thousand
            ('siwendausend', 7000),     # 7 thousand
            ('aachtdausend', 8000),     # 8 thousand
            ('néngdausend', 9000),      # 9 thousand
            ('zéngdausend', 10000),     # 10 thousand
            ('eelefdausend', 11000),    # 11 thousand
            ('zwielefdausend', 12000)   # 12 thousand
        ]
        
        for number, expected in test_cases:
            with self.subTest(number=number):
                result = w2n(number, lang='lb')
                self.assertEqual(result, expected)
    
    def test_larger_numbers_still_work(self):
        """Test that numbers 13 and above still work correctly."""
        test_cases = [
            ('dräizéng', 13),
            ('véierzéng', 14),
            ('fofzéng', 15),
            ('siechzéng', 16),
            ('siwenzéng', 17),
            ('uechtzéng', 18),
            ('nonnzéng', 19),
            ('zwanzeg', 20)
        ]
        
        for number, expected in test_cases:
            with self.subTest(number=number):
                result = w2n(number, lang='lb')
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main() 