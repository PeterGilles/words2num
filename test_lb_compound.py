from words2num import w2n

def test_word(word):
    try:
        result = w2n(word, lang="lb")
        print(f"'{word}' => {result}")
        return result
    except Exception as e:
        print(f"Error processing '{word}': {e}")
        return None

# Test our main case
test_word("nonnzénghonnrtvéieranachtzeg")

# Test with different spellings and variations
variations = [
    "nonnzéng honnrt véier an achtzeg",
    "nonnzénghonnert véieranachtzeg",
    "nonnzénghonnert-véieranachtzeg",
    "nonnzéng-honnert-véier-an-achtzeg",
    "nonnzéng honnert véier an achtzeg"
]

for var in variations:
    test_word(var)