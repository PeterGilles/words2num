import unittest
from words2num import w2n

class TestLuxembourgishComprehensive(unittest.TestCase):
    """Comprehensive test suite for Luxembourgish number parsing.
    
    This test suite covers:
    - Basic numbers (1-19)
    - Tens (20-90)
    - Compound numbers with 'a' and 'an' joiners
    - Hundreds and thousands
    - Complex compound numbers
    - Decimal numbers
    - Special cases and edge cases
    """

    def test_teens_and_tens(self):
        """Test numbers from 13-19 and multiples of 10."""
        test_cases = {
            'nonzéng': 19,
            'nonzeg': 90,
            'dräizéng': 13,
            'véierzéng': 14,
            'fofzéng': 15,
            'siechzéng': 16,
            'siwenzéng': 17,
            'uechtzéng': 18,
            'zwanzeg': 20,
            'drësseg': 30,
            'véierzeg': 40,
            'fofzeg': 50,
            'sechzeg': 60,
            'siwenzeg': 70,
            'achtzeg': 80
        }
        
        for word, expected in test_cases.items():
            with self.subTest(word=word):
                self.assertEqual(w2n(word, lang='lb'), expected)

    def test_two_digit_compounds(self):
        """Test compound numbers in the tens range."""
        test_cases = {
            'eenafofzeg': 51,
            'dräiafofzeg': 53,
            'véierafofzeg': 54,
            'eenasechzeg': 61,
            'dräiasechzeg': 63,
            'véierasechzeg': 64,
            'néngafofzeg': 59,
            'dräiandrësseg': 33,
            'véierandrësseg': 34,
            'néngandrësseg': 39
        }
        
        for word, expected in test_cases.items():
            with self.subTest(word=word):
                self.assertEqual(w2n(word, lang='lb'), expected)

    def test_three_digit_numbers(self):
        """Test hundreds and compound hundreds."""
        test_cases = {
            'eenhonnert': 100,
            'zweehonnert': 200,
            'dräihonnert': 300,
            'véierhonnert': 400,
            'fënnefhonnert': 500,
            'sechshonnert': 600,
            'siwenhonnert': 700,
            'aachthonnert': 800,
            'nénghonnert': 900,
            'eenhonnertnéngafofzeg': 159,
            'dräihonnertdräizéng': 313,
            'dräihonnertvéierafofzeg': 354
        }
        
        for word, expected in test_cases.items():
            with self.subTest(word=word):
                self.assertEqual(w2n(word, lang='lb'), expected)

    def test_four_digit_numbers(self):
        """Test thousands and compound thousands."""
        test_cases = {
            'eendausend': 1000,
            'zweedausend': 2000,
            'dräidausend': 3000,
            'véierdausend': 4000,
            'fënnefdausend': 5000,
            'sechsdausend': 6000,
            'siwendausend': 7000,
            'aachtdausend': 8000,
            'néngdausend': 9000,
            'eendausenddräihonnertdräizéng': 1313,
            'zweedausendfofzéng': 2015
        }
        
        for word, expected in test_cases.items():
            with self.subTest(word=word):
                self.assertEqual(w2n(word, lang='lb'), expected)

    def test_five_digit_numbers(self):
        """Test numbers in the ten thousands range."""
        test_cases = {
            'zéngdausend': 10000,
            'eelefdausend': 11000,
            'zwielefdausend': 12000,
            'zéngdausenddräihonnertdräizéng': 10313,
            'eelefdausendfofzéng': 11015
        }
        
        for word, expected in test_cases.items():
            with self.subTest(word=word):
                self.assertEqual(w2n(word, lang='lb'), expected)

    def test_decimal_numbers(self):
        """Test decimal numbers with both comma and point."""
        test_cases = {
            "dräi komma véier": 3.4,
            "zwee komma néng fënnef": 2.95,
            "eenhonnert komma null eent": 100.01,
            "zwee punkt dräi fënnef": 2.35
        }
        
        for word, expected in test_cases.items():
            with self.subTest(word=word):
                self.assertAlmostEqual(w2n(word, lang='lb'), expected, places=6)

    def test_complex_numbers(self):
        """Test complex number expressions."""
        test_cases = {
            "zweedausenddräihonnertvéierafofzeg": 2354,
            "eng millioun fënnefhonnert dausend": 1500000,
            "dräi milliounen zweehonnertdausend": 3200000,
            "eenhonnertzweeadräisseg": 132,
            "dräi dausend an eenhonnert zwanzeg": 3120,
            "véierdausendzweehonnertvéierafofzeg": 4254
        }
        
        for word, expected in test_cases.items():
            with self.subTest(word=word):
                self.assertEqual(w2n(word, lang='lb'), expected)

    def test_special_cases(self):
        """Test Luxembourgish-specific number forms and edge cases."""
        test_cases = {
            # Hyphenated forms
            "zwee-honnert": 200,
            "dräi-honnert": 300,
            "véier-a-fofzeg": 54,
            "véier-dausend-zweehonnert-véier-a-fofzeg": 4254,
            
            # Compound forms
            "zweehonnert": 200,
            "dräihonnert": 300,
            "véierafofzeg": 54,
            "honnertzwee": 102,
            
            # Ordinals
            "éischten": 1,
            "zweeten": 2,
            "drëtten": 3,
            
            # Special combinations
            "véier fofzeg": 54,  # digit followed by tens (no connecting word)
            "Dräi Milliounen": 3000000,  # capitalization
            "véierandrëssegdausend": 34000
        }
        
        for word, expected in test_cases.items():
            with self.subTest(word=word):
                self.assertEqual(w2n(word, lang='lb'), expected)

if __name__ == '__main__':
    unittest.main() 