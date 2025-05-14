from words2num import w2n

def test_cases():
    # Test cases for the issues reported
    tests = [
        # 1. For the first error: eenhonnert zweeadräisseg -> 132
        ("eenhonnert zweeadräisseg", 132),
        ("eenhonnert zweeandrësseg", 132),
        ("eenhonnert-zweeandräisseg", 132),
        ("eenhonnert-zweeandrësseg", 132),
        ("een-honnert-zweeandrësseg", 132),
        ("een honnert zweeandrësseg", 132),
        
        # 2. For the second error: een-honnert-eent -> 101
        ("eenhonnert-eent", 101),
        ("een-honnert-eent", 101),
        ("een honnert eent", 101),
        ("eenhonnerteent", 101),
        
        # 3. Already working cases for completeness
        ("zwee-honnert", 200),
        ("dräi-honnert", 300),
        ("véier-a-foffzeg", 54),
    ]
    
    # Test each case
    results = []
    for text, expected in tests:
        try:
            result = w2n(text, lang="lb")
            success = result == expected
            status = "✅" if success else f"❌ (Got {result}, expected {expected})"
            results.append(f"{text.ljust(30)}: {result} {status}")
        except Exception as e:
            results.append(f"{text.ljust(30)}: Error: {e} ❌")
    
    # Print all results
    print("--- Luxembourgish Special Test Cases ---")
    for result in results:
        print(result)

if __name__ == "__main__":
    test_cases()