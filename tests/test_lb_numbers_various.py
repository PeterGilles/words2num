import unittest
from words2num import w2n

class TestLuxembourgishVariousNumbers(unittest.TestCase):
    def test_teens_and_tens(self):
        self.assertEqual(w2n('nonzéng', lang='lb'), 19)
        self.assertEqual(w2n('nonzeg', lang='lb'), 90)
        self.assertEqual(w2n('dräizéng', lang='lb'), 13)
        self.assertEqual(w2n('véierzéng', lang='lb'), 14)
        self.assertEqual(w2n('fofzéng', lang='lb'), 15)
        self.assertEqual(w2n('siechzéng', lang='lb'), 16)
        self.assertEqual(w2n('siwenzéng', lang='lb'), 17)
        self.assertEqual(w2n('uechtzéng', lang='lb'), 18)
        self.assertEqual(w2n('zwanzeg', lang='lb'), 20)
        self.assertEqual(w2n('drësseg', lang='lb'), 30)
        self.assertEqual(w2n('véierzeg', lang='lb'), 40)
        self.assertEqual(w2n('fofzeg', lang='lb'), 50)
        self.assertEqual(w2n('sechzeg', lang='lb'), 60)
        self.assertEqual(w2n('siwenzeg', lang='lb'), 70)
        self.assertEqual(w2n('achtzeg', lang='lb'), 80)

    def test_two_digit_compounds(self):
        self.assertEqual(w2n('eenafofzeg', lang='lb'), 51)
        self.assertEqual(w2n('dräiafofzeg', lang='lb'), 53)
        self.assertEqual(w2n('véierafofzeg', lang='lb'), 54)
        self.assertEqual(w2n('eenasechzeg', lang='lb'), 61)
        self.assertEqual(w2n('dräiasechzeg', lang='lb'), 63)
        self.assertEqual(w2n('véierasechzeg', lang='lb'), 64)
        self.assertEqual(w2n('néngafofzeg', lang='lb'), 59)
        self.assertEqual(w2n('dräiandrësseg', lang='lb'), 33)
        self.assertEqual(w2n('véierandrësseg', lang='lb'), 34)
        self.assertEqual(w2n('néngandrësseg', lang='lb'), 39)

    def test_three_digit_numbers(self):
        self.assertEqual(w2n('eenhonnert', lang='lb'), 100)
        self.assertEqual(w2n('zweehonnert', lang='lb'), 200)
        self.assertEqual(w2n('dräihonnert', lang='lb'), 300)
        self.assertEqual(w2n('véierhonnert', lang='lb'), 400)
        self.assertEqual(w2n('fënnefhonnert', lang='lb'), 500)
        self.assertEqual(w2n('sechshonnert', lang='lb'), 600)
        self.assertEqual(w2n('siwenhonnert', lang='lb'), 700)
        self.assertEqual(w2n('aachthonnert', lang='lb'), 800)
        self.assertEqual(w2n('nénghonnert', lang='lb'), 900)
        self.assertEqual(w2n('eenhonnertnéngafofzeg', lang='lb'), 159)
        self.assertEqual(w2n('dräihonnertdräizéng', lang='lb'), 313)
        self.assertEqual(w2n('dräihonnertvéierafofzeg', lang='lb'), 354)

    def test_four_digit_numbers(self):
        self.assertEqual(w2n('eendausend', lang='lb'), 1000)
        self.assertEqual(w2n('zweedausend', lang='lb'), 2000)
        self.assertEqual(w2n('dräidausend', lang='lb'), 3000)
        self.assertEqual(w2n('véierdausend', lang='lb'), 4000)
        self.assertEqual(w2n('fënnefdausend', lang='lb'), 5000)
        self.assertEqual(w2n('sechsdausend', lang='lb'), 6000)
        self.assertEqual(w2n('siwendausend', lang='lb'), 7000)
        self.assertEqual(w2n('aachtdausend', lang='lb'), 8000)
        self.assertEqual(w2n('néngdausend', lang='lb'), 9000)
        self.assertEqual(w2n('eendausenddräihonnertdräizéng', lang='lb'), 1313)
        self.assertEqual(w2n('zweedausendfofzéng', lang='lb'), 2015)

    def test_five_digit_numbers(self):
        self.assertEqual(w2n('zéngdausend', lang='lb'), 10000)
        self.assertEqual(w2n('eelefdausend', lang='lb'), 11000)
        self.assertEqual(w2n('zwielefdausend', lang='lb'), 12000)
        self.assertEqual(w2n('zéngdausenddräihonnertdräizéng', lang='lb'), 10313)
        self.assertEqual(w2n('eelefdausendfofzéng', lang='lb'), 11015)

    def test_joiner_logic(self):
        """Test the joiner logic for compound numbers."""
        # Test 'a' joiner for specific numbers
        self.assertEqual(w2n('dräiavéierzeg', lang='lb'), 43)
        self.assertEqual(w2n('dräiafofzeg', lang='lb'), 53)
        self.assertEqual(w2n('dräiasechzeg', lang='lb'), 63)
        self.assertEqual(w2n('dräiasiwwenzeg', lang='lb'), 73)

        # Test 'an' joiner for other numbers
        self.assertEqual(w2n('dräianachtzeg', lang='lb'), 83)
        self.assertEqual(w2n('dräiannonzeg', lang='lb'), 93)
        self.assertEqual(w2n('dräianzwanzeg', lang='lb'), 23)

    def test_random_cases(self):
        """Test various random number cases."""
        test_cases = [
            # Simple numbers
            ("eent", 1),
            ("zéng", 10),
            ("honnert", 100),
            ("dausend", 1000),
            
            # Compound numbers
            ("dräiafofzeg", 53),
            ("véierafofzeg", 54),
            ("dräiandrësseg", 33),
            
            # Complex numbers
            ("dräihonnertvéierafofzeg", 354),
            ("véierdausendzweehonnert", 4200),
            ("dräidausenddräihonnertdräizéng", 3313),
            
            # Numbers with joiners
            ("dräi-an-achtzeg", 83),
            ("véier-a-fofzeg", 54),
            ("dräi-a-véierzeg", 43),
            
            # Large numbers
            ("zéngdausenddräihonnert", 10300),
            ("eelefdausendfofzéng", 11015),
            ("zwielefdausend", 12000)
        ]

        for word, expected in test_cases:
            with self.subTest(word=word):
                self.assertEqual(w2n(word, lang='lb'), expected)

if __name__ == '__main__':
    unittest.main() 