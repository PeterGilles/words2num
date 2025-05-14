from words2num import date_to_num_lb

def test_date_parsing():
    # Test cases for Luxembourgish date expressions
    # Note: Following the n-rule where final -n is dropped when the following word 
    # doesn't start with a vowel or the consonants h, n, d, z, t, r
    test_cases = [
        # Format: (date_text, expected_result)
        
        # Base test cases with years (2000s)
        ("éischte Januar zweedausendvéier", "1.1.2004"),
        ("drëtte Mäerz nonnzénghonnertnénganzwanzeg", "3.3.1929"),
        ("fënneften Abrëll zweedausendeenandrësseg", "5.4.2031"),
        ("zweete Februar nonnzénghonnertaachtasechzeg", "2.2.1968"),
        ("éischte Juli zweedausendzwee", "1.7.2002"),  # Drops -n before J (not a vowel or h,n,d,z,t)
        ("zéngte August nonnzénghonnertsiwenanzwanzeg", "10.8.1927"),
        
        # N-rule tests with vowels (should keep -n)
        ("drëtten Abrëll", "3.4."),  # Keeps -n before A (vowel), note the period
        ("véierten Oktober", "4.10."),  # Keeps -n before O (vowel), note the period
        ("sechsten August", "6.8."),  # Keeps -n before A (vowel)
        ("zéngten Abrëll", "10.4."),  # Keeps -n before A (vowel)
        
        # N-rule tests with specific consonants (should keep -n)
        ("zéngten Dezember", "10.12."),  # Keeps -n before D (consonant in n-rule)
        ("siwenten November", "7.11."),  # Keeps -n before N (consonant in n-rule)
        # These should return None as they're not valid dates
        ("aachten Zuch", None),  # Keeps -n before Z - not a valid date
        ("néngten Dag", None),  # Keeps -n before D - not a valid month
        ("drëtten Hond", None),  # Keeps -n before H - not a valid month
        ("fënneften Tour", None),  # Keeps -n before T - not a valid month
        ("sechsten Rees", None),  # Keeps -n before R - not a valid month
        
        # N-rule tests with other consonants (should drop -n)
        ("éischte Februar", "1.2."),  # Drops -n before F (consonant not in n-rule)
        ("aachte September", "8.9."),  # Drops -n before S (consonant not in n-rule)
        ("zweete Mäerz", "2.3."),  # Drops -n before M (consonant not in n-rule)
        ("véierte Juni", "4.6."),  # Drops -n before J (consonant not in n-rule)
        
        # Written variations (hyphens, alternative spellings)
        ("éischt Januar", "1.1."),  # Base form without ending
        ("éischten-Abrëll", "1.4."),  # With hyphen, vowel follows
        ("zéngt-September", "10.9."),  # With hyphen, consonant follows (drop -n)
        ("drëtt Mäerz", "3.3."),  # Base form without ending
        
        # Month abbreviations
        ("éischte Jan", "1.1."),  # Abbreviated month, drops -n before J (not in n-rule)
        ("zweete Feb", "2.2."),  # Abbreviated month, drops -n before F (not in n-rule)
        ("néngten Dez", "9.12."),  # Abbreviated month, keeps -n before D (in n-rule)
        ("drëtte Sep", "3.9."),  # Abbreviated month, drops -n before S (not in n-rule)
        
        # Year patterns (1900s)
        ("éischten Abrëll nonnzénghonnertaacht", "1.4.1908"),
        # Now should correctly parse "fofzéng" (15)
        ("zéngten Oktober nonnzénghonnertfofzéng", "10.10.1915"),  # Should now parse "fofzéng" correctly
        ("drëtte Mäerz nonnzénghonnertdrësseg", "3.3.1930"),
        
        # Year patterns (2000s)
        ("éischte Februar zweedausenddräizéng", "1.2.2013"),
        ("néngten Abrëll zweedausendnéng", "9.4.2009"),
        ("aachte Mee zweedausendeenandrësseg", "8.5.2031"),
        
        # Complex cases with spaces and compounds
        # Now should correctly parse the hyphenated year
        ("éischten-Abrëll zweedausend-dräizéng", "1.4.2013"),  # Should now handle the hyphenated year
        ("drëtten Abrëll zwee dausend véier", "3.4.2004"),  # Spaced year
        ("éischte Juli nonnzénghonnert véieranachtzeg", "1.7.1984"),  # Special compound year
        ("zéngten August nonnzénghonnert siwenanzwanzeg", "10.8.1927"),  # Spaced year
    ]
    
    results = []
    for date_text, expected in test_cases:
        try:
            result = date_to_num_lb(date_text)
            status = "✅" if result == expected else f"❌ (Got '{result}', expected '{expected}')"
            results.append(f"{date_text.ljust(45)}: {result} {status}")
        except Exception as e:
            results.append(f"{date_text.ljust(45)}: Error: {e} ❌")
    
    # Print results
    print("--- Luxembourgish Date Conversion Test Cases ---")
    for result in results:
        print(result)

def test_edge_cases():
    # Edge cases that should return None
    edge_cases = [
        # Not dates
        "éischten Hond", # Not a month
        "zéngte Kaz", # Not a month
        "drëtte Schoul", # Not a month
        
        # Invalid date components
        "Januar", # Missing day
        "30 Februar", # Invalid day for month
        "2004", # Just year
        
        # Random text
        "Moien, wéi geet et dir?",
        "Dat ass eng Zuel: zweedausenddräizéng",
    ]
    
    # Borderline cases - some now properly rejected
    special_cases = [
        ("fënnef Januar", "5.1."),  # Cardinal used as day (still accepted)
        ("dräizéng September", "13.9."),  # Valid day for September (13)
        ("drësseg Februar", None),  # Invalid day for February (30)
        ("dräianzwanzeg Abrëll", "23.4."),  # Valid day for April (23)
        ("eenandräisseg Juni", None),  # Invalid day for June (31)
    ]
    
    results = []
    for text in edge_cases:
        result = date_to_num_lb(text)
        status = "✅" if result is None else f"❌ (Should return None, got '{result}')"
        results.append(f"{text.ljust(45)}: {result} {status}")
    
    # Print results
    print("\n--- Edge Case Tests (Should Return None) ---")
    for result in results:
        print(result)
        
    print("\n--- Special Cases with Day Validation ---")
    for text, expected in special_cases:
        result = date_to_num_lb(text)
        status = "✅" if result == expected else f"❌ (Expected '{expected}', got '{result}')"
        results.append(f"{text.ljust(45)}: {result} {status}")
        print(f"{text.ljust(45)}: {result} {status}")

if __name__ == "__main__":
    test_date_parsing()
    test_edge_cases()