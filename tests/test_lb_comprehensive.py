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
            "eng millioun fënnefhonnertdausend": 1500000,
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
            "éischten": "1.",
            "zweeten": "2.",
            "drëtten": "3.",
            
            # Special combinations
            "véier fofzeg": 54,  # digit followed by tens (no connecting word)
            "Dräi Milliounen": 3000000,  # capitalization
            "véierandrëssegdausend": 34000
        }
        
        for word, expected in test_cases.items():
            with self.subTest(word=word):
                self.assertEqual(w2n(word, lang='lb'), expected)

    def test_compound_numbers(self):
        """Test compound number parsing."""
        test_cases = [
            ('véieranachtzeg', 84),
            ('fënnefhonnertsechsandrësseg', 536),
            ('nonzénghonnertnénganzwanzeg', 1929),
            ('nonzénghonnertdräianzwanzeg', 1923),
            ('nonzénghonnertsiwenandrësseg', 1937),
            ('nonzéng-honnert-néng-an-zwanzeg', 1929),
            ('nonzéng-honnert-dräi-an-zwanzeg', 1923),
            ('nonzéng-honnert-siwen-an-drësseg', 1937),
            ('véier-an-achtzeg', 84),
            ('fënnef-honnert-sechs-an-drësseg', 536),
        ]
        
        for word, expected in test_cases:
            result = w2n(word, lang='lb')
            assert result == expected, f"Failed to convert '{word}': expected {expected}, got {result}"

    def test_year_numbers(self):
        test_cases = [
            ('nonzénghonnertnénganzwanzeg', 1929),
            ('nonzénghonnertdräianzwanzeg', 1923),
            ('nonzénghonnertzweeanzwanzeg', 1922),
            ('nonzénghonnertvéieranzwanzeg', 1924),
            ('nonzénghonnertfënnefanzwanzeg', 1925),
            ('nonzénghonnertsechsanzwanzeg', 1926),
            ('nonzénghonnertsiwenanzwanzeg', 1927),
            ('nonzénghonnertaachtanzwanzeg', 1928),
            ('nonzénghonnertzéng', 1910),
            ('nonzénghonnerteelef', 1911),
            ('nonzénghonnertzwielef', 1912),
            ('nonzénghonnertdräizéng', 1913),
            ('nonzénghonnertvéierzéng', 1914),
            ('nonzénghonnertfofzéng', 1915),
            ('nonzénghonnertsiechzéng', 1916),
            ('nonzénghonnertsiwenzéng', 1917),
            ('nonzénghonnertuechtzéng', 1918),
            ('nonzénghonnertnonzéng', 1919),
            ('nonzénghonnertzwanzeg', 1920),
            ('nonzénghonnertdrësseg', 1930),
            ('nonzénghonnertvéierzeg', 1940),
            ('nonzénghonnertfofzeg', 1950),
            ('nonzénghonnertsechzeg', 1960),
            ('nonzénghonnertsiwenzeg', 1970),
            ('nonzénghonnertachtzeg', 1980),
            ('nonzénghonnertnonzeg', 1990),
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                self.assertEqual(w2n(word, lang='lb'), expected)

    def test_year_number_generalization(self):
        test_cases = [
            # 1800s
            ('uechtzénghonnertdräizéng', 1813),
            ('uechtzénghonnertzéng', 1810),
            ('uechtzénghonnertnénganzwanzeg', 1829),
            # 1900s
            ('nonzénghonnertdräizéng', 1913),
            ('nonzénghonnertzéng', 1910),
            ('nonzénghonnertnénganzwanzeg', 1929),
            ('nonzénghonnertsiwenandrësseg', 1937),
            # 2000s (should be cardinal)
            ('zweedausend', 2000),
            ('zweedausenddräizéng', 2013),
            ('zweedausendnénganzwanzeg', 2029),
        ]
        for word, expected in test_cases:
            with self.subTest(word=word):
                self.assertEqual(w2n(word, lang='lb'), expected)

if __name__ == '__main__':
    unittest.main() 