import unittest
from words2num import w2n


class TestLuxembourgish(unittest.TestCase):
    """Test Luxembourgish (LB) language implementation."""

    def test_cardinals(self):
        """Test cardinal numbers in Luxembourgish."""
        test_cases = {
            "eent": 1,
            "eenanzwanzeg": 21,
            "zweeavéierzeg": 42,
            "eenhonnert": 100,
            "eenhonnerteent": 101,
            "eendausend": 1000,
            "eng millioun": 1000000,
            "eng millioun eent": 1000001,
        }

        for word, expected in test_cases.items():
            self.assertEqual(w2n(word, lang='lb'), expected)

    def test_decimal_numbers(self):
        """Test decimal numbers in Luxembourgish."""
        test_cases = {
            "dräi komma véier": 3.4,
            "zwee komma néng fënnef": 2.95,
            "eenhonnert komma null eent": 100.01,
        }

        for word, expected in test_cases.items():
            self.assertAlmostEqual(w2n(word, lang='lb'), expected, places=6)

    def test_complex_numbers(self):
        """Test complex number expressions in Luxembourgish."""
        test_cases = {
            "zwee dausend dräihonnert véierafoffzeg": 2354,
            "eng millioun fënnefhonnert dausend": 1500000,
            "dräi milliounen zweehonnert dausend": 3200000,
            "eenhonnert zweeadräisseg": 132,
        }

        for word, expected in test_cases.items():
            self.assertEqual(w2n(word, lang='lb'), expected)

    def test_lux_specific_cases(self):
        """Test Luxembourgish-specific number forms and edge cases."""
        test_cases = {
            # Hyphenated forms
            "zwee-honnert": 200,
            "dräi-honnert": 300,
            "véier-a-foffzeg": 54, 
            
            # Compound forms
            "zweehonnert": 200,
            "dräihonnert": 300,
            "véierafoffzeg": 54,
            "honnertzwee": 102,
            
            # Ordinals
            "éischten": 1,
            "zweeten": 2,
            "drëtten": 3,
            
            # Special combinations
            "véier foffzeg": 54,  # digit followed by tens (no connecting word)
            "Dräi Milliounen": 3000000,  # capitalization
            "véierandrësseg dausend": 34000,
            "zwee punkt dräi fënnef": 2.35,
            "dräi dausend an eenhonnert zwanzeg": 3120,
            "véierdausendvéierafoffzeg": 4254,  # compound with thousands and specific number
            "véier-dausend-véier-a-foffzeg": 4254,  # hyphenated version
        }
        
        for word, expected in test_cases.items():
            try:
                result = w2n(word, lang='lb')
                # Use assertAlmostEqual for floating point numbers
                if isinstance(expected, float):
                    self.assertAlmostEqual(result, expected, places=6)
                else:
                    self.assertEqual(result, expected)
            except Exception as e:
                self.fail(f"Failed to convert '{word}': {str(e)}")

if __name__ == "__main__":
    unittest.main()