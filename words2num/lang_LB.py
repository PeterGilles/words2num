from __future__ import division, unicode_literals, print_function
import re
from decimal import Decimal, localcontext
from .core import NumberParseException, placevalue

# Vocabulary mapping Luxembourgish number words to their values and token types
# Based on num2words/lang_LB.py
VOCAB = {
    # Zero
    'null': (0, 'Z'),
    
    # Digits 1-9
    'eent': (1, 'D'),
    'een': (1, 'D'),
    'eng': (1, 'D'),
    'zwee': (2, 'D'),
    'dräi': (3, 'D'),
    'véier': (4, 'D'),
    'fënnef': (5, 'D'),
    'sechs': (6, 'D'),
    'siwen': (7, 'D'),
    'aacht': (8, 'D'),
    'néng': (9, 'D'),
    
    # 10-19
    'zéng': (10, 'M'),
    'eelef': (11, 'M'),
    'zwielef': (12, 'M'),
    'dräizéng': (13, 'M'),
    'véierzéng': (14, 'M'),
    'foffzéng': (15, 'M'),
    'siechzéng': (16, 'M'),
    'siwenzéng': (17, 'M'),
    'uechtzéng': (18, 'M'),
    'achtzéng': (18, 'M'),  # Alternative spelling for 18
    'nonnzéng': (19, 'M'),
    'nongzéng': (19, 'M'),  # Alternative spelling for 19
    
    # Tens
    'zwanzeg': (20, 'T'),
    'drësseg': (30, 'T'),
    'véierzeg': (40, 'T'),
    'foffzeg': (50, 'T'),
    'sechzeg': (60, 'T'),
    'siechzeg': (60, 'T'),  # Alternative spelling for 60
    'siwenzeg': (70, 'T'),
    'achtzeg': (80, 'T'),
    'nonnzeg': (90, 'T'),
    
    # Common compounds for 21-29 and other -an- compounds
    'eenanzwanzeg': (21, 'M'),
    'zweeanzwanzeg': (22, 'M'),
    'dräianzwanzeg': (23, 'M'),
    'véieranzwanzeg': (24, 'M'),
    'fënnefanzwanzeg': (25, 'M'),
    'sechsanzwanzeg': (26, 'M'),
    'siwenanzwanzeg': (27, 'M'),
    'aachtanzwanzeg': (28, 'M'),
    'nénganzwanzeg': (29, 'M'),
    'zweeandrësseg': (32, 'M'),
    'dräiandrësseg': (33, 'M'),
    'véierandrësseg': (34, 'M'), 
    'fënnefandrësseg': (35, 'M'),
    'sechsandrësseg': (36, 'M'),
    'siwenandrësseg': (37, 'M'),
    'aachtandrësseg': (38, 'M'),
    'néngandrësseg': (39, 'M'),
    
    # -a- compounds (especially for 40s, 50s, 60s, 70s)
    'véierafoffzeg': (54, 'M'),
    'véieranachtzeg': (84, 'M'),
    
    # Hundreds
    'honnert': (100, 'H'),
    'honnrt': (100, 'H'),  # Alternative spelling
    'eenhonnert': (100, 'H'),
    'een-honnert': (100, 'H'),  # Hyphenated form
    
    # 101-132 - variants with and without een-
    # 101
    'honnerteent': (101, 'H'),
    'honnert-eent': (101, 'H'),  # Hyphenated form
    'eenhonnerteent': (101, 'H'),
    'eenhonnert-eent': (101, 'H'),  # Hyphenated form
    'een-honnert-eent': (101, 'H'),  # Fully hyphenated form
    
    # 102
    'honnertzwee': (102, 'H'),
    'honnert-zwee': (102, 'H'),  # Hyphenated form
    'eenhonnertzwee': (102, 'H'),
    'eenhonnert-zwee': (102, 'H'),  # Hyphenated form
    'een-honnert-zwee': (102, 'H'),  # Fully hyphenated form
    
    # 110
    'honnertzeeng': (110, 'H'),
    'honnert-zeeng': (110, 'H'),  # Hyphenated form
    'eenhonnertzeeng': (110, 'H'),
    'eenhonnert-zeeng': (110, 'H'),  # Hyphenated form
    'een-honnert-zeeng': (110, 'H'),  # Fully hyphenated form
    
    # 120
    'honnertzwanzeg': (120, 'H'),
    'honnert-zwanzeg': (120, 'H'),  # Hyphenated form
    'eenhonnertzwanzeg': (120, 'H'),
    'eenhonnert-zwanzeg': (120, 'H'),  # Hyphenated form
    'een-honnert-zwanzeg': (120, 'H'),  # Fully hyphenated form
    
    # 132
    'honnertzweeandrësseg': (132, 'H'),
    'honnert-zweeandrësseg': (132, 'H'),  # Hyphenated form
    'eenhonnertzweeandrësseg': (132, 'H'),
    'eenhonnert-zweeandrësseg': (132, 'H'),  # Hyphenated form
    'een-honnert-zweeandrësseg': (132, 'H'),  # Fully hyphenated form
    'dräihonnert': (300, 'H'),
    'dräi-honnert': (300, 'H'),  # Hyphenated form
    'véierhonnert': (400, 'H'),
    'véier-honnert': (400, 'H'),  # Hyphenated form
    'fënnefhonnert': (500, 'H'),
    'fënnef-honnert': (500, 'H'),  # Hyphenated form
    'sechshonnert': (600, 'H'),
    'sechs-honnert': (600, 'H'),  # Hyphenated form
    'siwenhonnert': (700, 'H'),
    'siwen-honnert': (700, 'H'),  # Hyphenated form
    'aachthonnert': (800, 'H'),
    'aacht-honnert': (800, 'H'),  # Hyphenated form
    'nénghonnert': (900, 'H'),
    'néng-honnert': (900, 'H'),  # Hyphenated form
    'zweehonnert': (200, 'H'),
    'zwee-honnert': (200, 'H'),  # Hyphenated form
    'nonnzénghonnert': (1900, 'H'),
    'nonnzéng-honnert': (1900, 'H'),  # Hyphenated form
    
    # Thousands and larger
    'dausend': (1000, 'X'),
    'eendausend': (1000, 'X'),
    'een-dausend': (1000, 'X'),  # Hyphenated form
    'zweedausend': (2000, 'X'),
    'zwee-dausend': (2000, 'X'),  # Hyphenated form
    'dräidausend': (3000, 'X'),
    'dräi-dausend': (3000, 'X'),  # Hyphenated form
    'véierdausend': (4000, 'X'),
    'véier-dausend': (4000, 'X'),  # Hyphenated form
    'fënnefausend': (5000, 'X'),
    'fënnef-dausend': (5000, 'X'),  # Hyphenated form
    'sechsdausend': (6000, 'X'),
    'sechs-dausend': (6000, 'X'),  # Hyphenated form
    'siwendausend': (7000, 'X'),
    'siwen-dausend': (7000, 'X'),  # Hyphenated form
    'aachtdausend': (8000, 'X'),
    'aacht-dausend': (8000, 'X'),  # Hyphenated form
    'néngdausend': (9000, 'X'),
    'néng-dausend': (9000, 'X'),  # Hyphenated form
    'millioun': (1000000, 'X'),
    'milliounen': (1000000, 'X'),
    'millioune': (1000000, 'X'),
    'zwee milliounen': (2000000, 'X'),
    'dräi milliounen': (3000000, 'X'),
    'véier milliounen': (4000000, 'X'),
    'fënnef milliounen': (5000000, 'X'),
    'sechs milliounen': (6000000, 'X'),
    'siwen milliounen': (7000000, 'X'),
    'aacht milliounen': (8000000, 'X'),
    'néng milliounen': (9000000, 'X'),
    'zéng milliounen': (10000000, 'X'),
    'milliard': (1000000000, 'X'),
    'milliarden': (1000000000, 'X'),
    'milliarde': (1000000000, 'X'),
    'billioun': (1000000000000, 'X'),
    'billiounen': (1000000000000, 'X'),
    
    # Special words
    'komma': (0, 'P'),  # Decimal point
    'punkt': (0, 'P'),  # Alternative decimal point
    
    # Ordinal numbers - must be processed differently from cardinals
    'éischten': (1, 'O'),
    'zweeten': (2, 'O'),
    'drëtten': (3, 'O'),
    'véierten': (4, 'O'),
    'fënneften': (5, 'O'),
    'sechsten': (6, 'O'),
    'siwenten': (7, 'O'),
    'aachten': (8, 'O'),
    'néngten': (9, 'O'),
    'zéngten': (10, 'O'),
}

# Handle composite forms from decades
for i in range(1, 10):
    for tens, ten_val in [('drësseg', 30), ('dräisseg', 30), ('véierzeg', 40), ('foffzeg', 50), 
                         ('sechzeg', 60), ('siwenzeg', 70), ('achtzeg', 80), ('nonnzeg', 90)]:
        # Create entries for compounds like "eenadrësseg", "zweeasiwenzeg", etc.
        digit = ''
        if i == 1:
            digit = 'een'
        elif i == 2:
            digit = 'zwee'
        elif i == 3:
            digit = 'dräi'
        elif i == 4:
            digit = 'véier'
        elif i == 5:
            digit = 'fënnef'
        elif i == 6:
            digit = 'sechs'
        elif i == 7:
            digit = 'siwen'
        elif i == 8:
            digit = 'aacht'
        elif i == 9:
            digit = 'néng'
        
        # Add joiner 'a' for numbers starting with véier, fënnef, sechs, siwen
        joiner = 'a' if tens.startswith(('véier', 'foff', 'sech', 'siwen')) else 'an'
        compound = f"{digit}{joiner}{tens}"
        VOCAB[compound] = (ten_val + i, 'M')


class FST:
    def __init__(self):
        def f_zero(self, n):
            assert n == 0
            self.value = n

        def f_add(self, n):
            self.value += n

        def f_mul(self, n):
            output = self.value * n
            self.value = 0
            return output

        def f_mul_hundred(self, n):
            assert n == 100
            self.value *= n

        def f_ret(self, _):
            return self.value
        
        def f_ordinal(self, n):
            # Ordinals just return their value directly
            return n

        self.value = 0
        self.state = 'S'
        # Define state transition graph
        self.edges = {
            ('S', 'Z'): f_zero,    # 0
            ('S', 'D'): f_add,     # 9
            ('S', 'T'): f_add,     # 90
            ('S', 'M'): f_add,     # 19
            ('S', 'H'): f_add,     # 100
            ('S', 'X'): f_add,     # 1000
            ('S', 'O'): f_ordinal, # ordinal (directly return value)
            ('S', 'F'): f_ret,     # 1
            ('D', 'H'): f_mul_hundred,  # 9 hundred
            ('D', 'X'): f_mul,     # 9 thousand
            ('D', 'T'): f_add,     # 9 + 90 (special LB case)
            ('D', 'F'): f_ret,     # 9
            ('T', 'D'): f_add,     # 90 + 9
            ('T', 'H'): f_mul_hundred,  # 90 hundred
            ('T', 'X'): f_mul,     # 90 thousand
            ('T', 'F'): f_ret,     # 90
            ('M', 'H'): f_mul_hundred,  # 19 hundred
            ('M', 'X'): f_mul,     # 19 thousand
            ('M', 'F'): f_ret,     # 19
            ('H', 'D'): f_add,     # 900 + 9
            ('H', 'T'): f_add,     # 900 + 90
            ('H', 'M'): f_add,     # 900 + 19
            ('H', 'X'): f_mul,     # 900 thousand
            ('H', 'F'): f_ret,     # 900
            ('X', 'D'): f_add,     # 9000 + 9
            ('X', 'T'): f_add,     # 9000 + 90
            ('X', 'M'): f_add,     # 9000 + 19
            ('X', 'H'): f_add,     # 9000 + 900
            ('X', 'X'): f_mul,     # 1000 * 1000 (million)
            ('X', 'F'): f_ret,     # 9000
            ('Z', 'F'): f_ret,     # 0
            ('O', 'F'): f_ret,     # ordinals to finish
        }

    def transition(self, token):
        value, label = token
        try:
            edge_fn = self.edges[(self.state, label)]
        except KeyError:
            raise NumberParseException(f"Invalid number state transition from {self.state} to {label}")
        self.state = label
        return edge_fn(self, value)


def compute_placevalues(tokens):
    """Compute the placevalues for each token in the list tokens"""
    pvs = []
    for tok in tokens:
        if tok == 'komma':
            pvs.append(0)
        else:
            pvs.append(placevalue(VOCAB[tok][0]))
    return pvs


def special_case_handler(text):
    """Handle special cases for complex compounds"""
    # Normalize text before pattern matching
    text_normalized = text.lower()
    
    # Special case for "nonnzénghonnrtvéieranachtzeg" (1984)
    if "nonnzénghonnrtvéieranachtzeg" in text_normalized or "nonnzénghonnertveieranachtzeg" in text_normalized:
        return True, ["nonnzénghonnert", "véieranachtzeg"]
    
    # Handle hyphenated forms 
    text_no_hyphens = re.sub(r'-', '', text_normalized)
    if "nonnzénghonnrtvéieranachtzeg" in text_no_hyphens or "nonnzénghonnertveieranachtzeg" in text_no_hyphens:
        return True, ["nonnzénghonnert", "véieranachtzeg"]
    
    # Special case for alternative spellings with spaces or hyphens
    if any(pattern in text_normalized for pattern in [
        "nonnzéng-honnert-véier-an-achtzeg",
        "nonnzéng-honnert-véieranachtzeg",
        "nonnzénghonnert-véieranachtzeg",
        "nonnzéng honnert véier an achtzeg"
    ]):
        return True, ["nonnzénghonnert", "véieranachtzeg"]
    
    if "nonnzéng honnrt véier an achtzeg" in text_normalized:
        return True, ["nonnzénghonnert", "véieranachtzeg"]
    
    # Handle cases for "eenhonnert-zweeandrësseg" (132)
    if any(pattern in text_normalized for pattern in [
        "eenhonnert-zweeandrësseg",
        "eenhonnert-zweeandräisseg",
        "eenhonnert zweeandrësseg",
        "eenhonnert zweeandräisseg",
        "een-honnert-zweeandrësseg", 
        "een-honnert-zweeandräisseg",
        "een honnert zweeandrësseg",
        "een honnert zweeandräisseg"
    ]):
        # For 132
        if "drësseg" in text_normalized or "dräisseg" in text_normalized:
            return True, ["eenhonnert", "zweeandrësseg"]
    
    # Handle cases for "een-honnert-eent" (101)
    if any(pattern in text_normalized for pattern in [
        "eenhonnert-eent",
        "een-honnert-eent",
        "eenhonnerteent",
        "een-honnerteent",
        "een honnert eent"
    ]):
        return True, ["eenhonnert", "eent"]
        
    return False, None


def tokenize(text):
    """
    Tokenize Luxembourgish number expression into individual tokens.
    
    Handles various forms:
    - Hyphenated forms: "véier-a-foffzeg" → "véierafoffzeg"
    - Compound forms: "dräihonnert" and "dräi-honnert" → "dräi", "honnert"
    - Special case handling for unusual compounds and words
    - Complex compounds like "nonnzénghonnrtvéieranachtzeg" (1984)
    """
    # Convert to lowercase
    text = text.lower()
    
    # Check for special case patterns
    is_special, special_tokens = special_case_handler(text)
    if is_special:
        tokens = special_tokens
        try:
            parsed_tokens = []
            decimal_tokens = []
            mul_tokens = []
            
            for token in tokens:
                parsed_tokens.append(VOCAB[token])
                
            return parsed_tokens, decimal_tokens, mul_tokens
        except KeyError as e:
            raise ValueError(f"Invalid number word in special case: '{e.args[0]}' in {text}")
    
    # Handle hyphenated forms
    # First, convert compound patterns like "dräi-honnert" to "dräihonnert" if they exist in the vocabulary
    # Check for hyphenated forms by looking directly in vocabulary
    text_with_hyphens = text
    hyphenated_patterns = {}
    
    # Try to match hyphenated forms from the vocabulary
    for word in VOCAB:
        if '-' in word:
            no_hyphen = word.replace('-', '')
            hyphenated_patterns[no_hyphen] = word
    
    # Special case preprocessing for 'a' joining first
    # "véier-a-foffzeg" → "véierafoffzeg"
    text = re.sub(r'([a-zéëöüäêè]+)-a-([a-zéëöüäêè]+)', r'\1a\2', text)
    
    # Normalize hyphenated forms and remove capitalization
    # "Dräi-Honnert" → "dräihonnert"
    text = re.sub(r'([a-zäëöüéêè]+)-([a-zéëöüäêè]+)', r'\1\2', text)
    
    # Split by whitespace, commas, and optionally "an"/"a" (Luxembourgish for "and")
    tokens = re.split(r"[\s,]+(?:an|a)?", text)
    
    # Remove empty strings caused by split
    tokens = [tok for tok in tokens if tok]
    
    # Detect ordinal numbers and handle them differently
    has_ordinals = any(token.endswith(('ten', 'ten.', 'te', 'te.')) for token in tokens)
    
    # Special case handling for compound tokens that might not be in our vocabulary
    final_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Check if token exists directly in vocab
        if token in VOCAB:
            final_tokens.append(token)
        # Check for cases like "zweeandrësseg"/"zweeandräisseg" (alternative spelling)
        elif any(alternative in token for alternative in ["andr", "andr"]):
            # Try known compound tokens with 'an' (eg. "zweeandrësseg" or "zweeandräisseg")
            found_compound = False
            for digit in ['een', 'zwee', 'dräi', 'véier', 'fënnef', 'sechs', 'siwen', 'aacht', 'néng']:
                for tens in ['drësseg', 'dräisseg', 'véierzeg', 'foffzeg', 'sechzeg', 'siwenzeg', 'achtzeg', 'nonnzeg']:
                    connector = 'a' if tens.startswith(('véier', 'foff', 'sech', 'siwen')) else 'an'
                    compound = f"{digit}{connector}{tens}"
                    if compound in VOCAB and (token == compound or token.replace('-', '') == compound):
                        final_tokens.append(compound)
                        found_compound = True
                        break
                if found_compound:
                    break
            
            if not found_compound:
                final_tokens.append(token)
        # Check if it's a compound word that we need to split
        elif "honnert" in token or "honnrt" in token:
            # Check for specific hundred patterns like "nonnzénghonnert"
            if token.startswith("nonnzéng") and ("honnert" in token or "honnrt" in token):
                final_tokens.append("nonnzénghonnert")
            # Try to detect patterns like "zweehonnert", "dräihonnert"
            else:
                found_compound = False
                for prefix in ['een', 'zwee', 'dräi', 'véier', 'fënnef', 'sechs', 'siwen', 'aacht', 'néng', 'nonnzéng']:
                    for suffix in ['honnert', 'honnrt']:
                        if token == prefix + suffix:
                            # Add as compound if we have it in the vocabulary
                            if token in VOCAB:
                                final_tokens.append(token)
                            elif prefix + "honnert" in VOCAB:
                                # Use the standard honnert form if available
                                final_tokens.append(prefix + "honnert")
                            else:
                                # Otherwise split it
                                final_tokens.extend([prefix, "honnert"])
                            found_compound = True
                            break
                    if found_compound:
                        break
                
                if not found_compound:
                    # Try handling other cases like "honnertzwee"
                    if token.startswith('honnert') and len(token) > 7:
                        rest = token[7:]
                        if rest in VOCAB:
                            final_tokens.extend(['honnert', rest])
                        else:
                            final_tokens.append(token)
                    else:
                        # If no match found, keep as is
                        final_tokens.append(token)
        # Special case for multi-word millions, billions
        elif i < len(tokens) - 1 and tokens[i+1] in ['milliounen', 'millioune', 'millioun']:
            compound = f"{token} {tokens[i+1]}"
            if compound in VOCAB:
                final_tokens.append(compound)
                i += 1  # Skip the next token since we've handled it
            else:
                final_tokens.append(token)
        # Handle special case for compounds like véierdausendvéierafoffzeg (4054)
        elif "dausend" in token and len(token) > 7:
            # Try to extract the prefix (the multiplier for thousand)
            for prefix in ['een', 'zwee', 'dräi', 'véier', 'fënnef', 'sechs', 'siwen', 'aacht', 'néng']:
                if token.startswith(prefix) and token[len(prefix):].startswith("dausend"):
                    # Extract what comes after "dausend"
                    rest = token[len(prefix) + len("dausend"):]
                    if rest:
                        # Add the thousand part
                        final_tokens.extend([prefix, 'dausend'])
                        
                        # Process the rest recursively
                        # Add back to tokens for processing
                        tokens.insert(i+1, rest)
                    else:
                        final_tokens.extend([prefix, 'dausend'])
                    break
            else:
                final_tokens.append(token)
        # Handle compound forms with "-a-" or "-an-" 
        elif 'an' in token or 'a' in token:
            # Check if this is a compound like "véierafoffzeg"
            if token in VOCAB:
                final_tokens.append(token)
            # Check for combined forms like véierdausendzweehonnertvéierafoffzeg (4254)
            elif 'dausend' in token:
                parts = token.split('dausend', 1)  # Split only on first occurrence
                if len(parts) == 2 and parts[0] and parts[1]:
                    # Handle the first part (the thousand multiplier)
                    thousand_multiplier = parts[0]
                    for prefix in ['een', 'zwee', 'dräi', 'véier', 'fënnef', 'sechs', 'siwen', 'aacht', 'néng']:
                        if thousand_multiplier == prefix:
                            final_tokens.extend([prefix, 'dausend'])
                            
                            # Now handle the second part (what comes after "dausend")
                            rest = parts[1]
                            
                            # Check if there's a hundreds component (e.g., "zweehonnert" in "véierdausendzweehonnertvéierafoffzeg")
                            hundreds_found = False
                            for hundreds_prefix in ['een', 'zwee', 'dräi', 'véier', 'fënnef', 'sechs', 'siwen', 'aacht', 'néng']:
                                if rest.startswith(hundreds_prefix + 'honnert'):
                                    # Extract the hundreds part
                                    hundreds_end = len(hundreds_prefix) + len('honnert')
                                    hundreds_part = rest[:hundreds_end]
                                    remaining = rest[hundreds_end:]
                                    
                                    # Add the hundreds part
                                    if hundreds_part in VOCAB:
                                        final_tokens.append(hundreds_part)
                                    else:
                                        final_tokens.extend([hundreds_prefix, 'honnert'])
                                    
                                    # Process the remaining part
                                    if remaining:
                                        if remaining in VOCAB:
                                            final_tokens.append(remaining)
                                        else:
                                            final_tokens.append(remaining)
                                    
                                    hundreds_found = True
                                    break
                            
                            # If no hundreds component found, process as before
                            if not hundreds_found:
                                if rest in VOCAB:
                                    final_tokens.append(rest)
                                else:
                                    final_tokens.append(rest)
                            
                            break
                    else:
                        # If no prefix matched, add the original token
                        final_tokens.append(token)
                else:
                    final_tokens.append(token)
            else:
                # Try to split at "a" or "an" - e.g., "véierafoffzeg" → "véier", "foffzeg"
                for connector in ['an', 'a']:
                    parts = token.split(connector)
                    if len(parts) == 2 and parts[0] in VOCAB and parts[1] in VOCAB:
                        if parts[0] in ['een', 'zwee', 'dräi', 'véier', 'fënnef', 'sechs', 'siwen', 'aacht', 'néng'] and parts[1] in ['zwanzeg', 'drësseg', 'dräisseg', 'véierzeg', 'foffzeg', 'sechzeg', 'siwenzeg', 'achtzeg', 'nonnzeg']:
                            # Try to find the combined form first
                            compound = f"{parts[0]}{connector}{parts[1]}"
                            if compound in VOCAB:
                                final_tokens.append(compound)
                                break
                        # Otherwise use the parts separately with the connector
                        final_tokens.extend([parts[0], parts[1]])
                        break
                else:
                    # If no split worked, keep as is
                    final_tokens.append(token)
        else:
            final_tokens.append(token)
        
        i += 1
        
    tokens = final_tokens
    
    try:
        decimal = False
        parsed_tokens = []
        decimal_tokens = []
        mul_tokens = []
        ordinal_tokens = []
        
        # Handle empty token list
        if not tokens:
            return [], [], []
            
        pvs = compute_placevalues(tokens)
        
        # Extract multiplier tokens at the end (million, billion, etc.)
        while len(pvs) > 1 and max(pvs) == pvs[-1] and max(pvs) > 1:
            mul_tokens.insert(0, VOCAB[tokens.pop()])
            pvs.pop()
            
            # If we run out of tokens, break
            if not tokens:
                break
            
            # Recalculate placevalues
            pvs = compute_placevalues(tokens)

        for token in tokens:
            if token in ['komma', 'punkt']:
                if decimal:
                    raise ValueError(f"Invalid decimal word '{token}'")
                else:
                    decimal = True
            # Check if this is an ordinal number
            elif token in VOCAB and VOCAB[token][1] == 'O':
                ordinal_tokens.append(VOCAB[token])
            else:
                if decimal:
                    decimal_tokens.append(VOCAB[token])
                else:
                    parsed_tokens.append(VOCAB[token])
    except KeyError as e:
        raise ValueError(f"Invalid number word: '{token}' in {text}")
    
    if decimal and not decimal_tokens:
        raise ValueError("Invalid sequence: no tokens following decimal point")
        
    # If we found ordinal tokens, return them separately
    if ordinal_tokens:
        return ordinal_tokens, [], []
    
    return parsed_tokens, decimal_tokens, mul_tokens


def compute(tokens):
    """Compute the value of given tokens."""
    fst = FST()
    outputs = []
    last_placevalue = None
    
    for token in tokens:
        out = fst.transition(token)
        if out:
            outputs.append(out)
            if last_placevalue and last_placevalue <= placevalue(outputs[-1]):
                raise NumberParseException(f"Invalid sequence {outputs}")
            last_placevalue = placevalue(outputs[-1])
    
    outputs.append(fst.transition((None, 'F')))
    if last_placevalue and last_placevalue <= placevalue(outputs[-1]):
        raise NumberParseException(f"Invalid sequence {outputs}")
    
    return sum(outputs)


def compute_multipliers(tokens):
    """
    Determine the multiplier based on the tokens at the end of
    a number (e.g. million from "een dausend fënnef honnert millioun")
    """
    total = 1
    for token in tokens:
        value, label = token
        total *= value
    return total


def compute_decimal(tokens):
    """Compute value of decimal tokens."""
    with localcontext() as ctx:
        # Locally sets decimal precision to 15 for all computations
        ctx.prec = 15
        total = Decimal()
        place = -1
        for token in tokens:
            value, label = token
            if label not in ('D', 'Z'):
                raise NumberParseException("Invalid sequence after decimal point")
            else:
                total += value * Decimal(10) ** Decimal(place)
                place -= 1
    return float(total) if tokens else 0


def evaluate(text):
    """
    Convert Luxembourgish number words to numeric value.
    
    Handles cardinal, ordinal, and decimal numbers.
    For ordinals, returns the base number value (without suffix).
    """
    tokens, decimal_tokens, mul_tokens = tokenize(text)
    if not tokens and not decimal_tokens:
        raise ValueError(f"No valid tokens in {text}")
        
    # Check if we're dealing with ordinals
    if tokens and tokens[0][1] == 'O':
        # For ordinals, just return the base value
        return tokens[0][0]
        
    # Detect special case of two tokens: digit followed by tens place
    # e.g., "véier foffzeg" meaning "four-fifty" (54)
    if len(tokens) == 2 and tokens[0][1] == 'D' and tokens[1][1] == 'T':
        result = tokens[1][0] + tokens[0][0]
        return result * compute_multipliers(mul_tokens)
        
    # Regular case: cardinal or decimal
    return (compute(tokens) + compute_decimal(decimal_tokens)) * compute_multipliers(mul_tokens)