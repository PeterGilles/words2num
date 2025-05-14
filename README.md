# words2num - Luxembourgish Implementation

Inverse text normalization for Luxembourgish numbers and dates. Converts word forms to their numeric representation.

## Overview

This library provides comprehensive support for Luxembourgish (Lëtzebuergesch) language, including:

- Conversion of number words to digits
- Date expression parsing with support for the Luxembourgish n-rule

## Usage

Basic usage examples:

```python
from words2num import w2n, date_to_num_lb

# Number conversion
w2n("véierafoffzeg", lang="lb")  # Returns: 54
w2n("eenhonnert zweeanzwanzeg", lang="lb")  # Returns: 122
w2n("dräi komma véier", lang="lb")  # Returns: 3.4

# Date parsing
date_to_num_lb("éischten Abrëll")  # Returns: "1.4."
date_to_num_lb("fënneften August")  # Returns: "5.8."
date_to_num_lb("éischte Januar zweedausendvéier")  # Returns: "1.1.2004"
```

## Features

- Cardinal numbers ("eent", "zwee", "dräi", etc.)
- Ordinal numbers ("éischten", "zweeten", "drëtten", etc.)
- Decimal numbers with "komma" or "punkt"
- Complex compound forms ("zweehonnert", "dräihonnert", etc.)
- Hyphenated forms ("véier-a-foffzeg")
- Date expressions with n-rule implementation
- Month names and abbreviations

## Number Conversion Details

The Luxembourgish number parser handles:

```python
from words2num import w2n

# Cardinal numbers
w2n("eent", lang="lb")  # Returns: 1
w2n("zwanzeg", lang="lb")  # Returns: 20
w2n("eenhonnert", lang="lb")  # Returns: 100

# Complex expressions
w2n("zwee dausend dräihonnert véierafoffzeg", lang="lb")  # Returns: 2354
w2n("eng millioun fënnefhonnert dausend", lang="lb")  # Returns: 1500000

# Decimals
w2n("dräi komma véier", lang="lb")  # Returns: "3,4" (comma as decimal separator)
w2n("zwee punkt néng fënnef", lang="lb")  # Returns: 2.95 (period as decimal separator)

# Special forms
w2n("zwee-honnert", lang="lb")  # Returns: 200 (hyphenated)
w2n("dräihonnert", lang="lb")  # Returns: 300 (compound)
w2n("een-honnert-eent", lang="lb")  # Returns: 101 (hyphenated)
w2n("éischten", lang="lb")  # Returns: 1 (ordinal)
```

## Date Parsing Details

The Luxembourgish date parser handles expressions with proper n-rule implementation:

```python
from words2num import date_to_num_lb

# Full dates (day.month.year)
date_to_num_lb("éischte Januar zweedausendvéier")  # Returns: "1.1.2004"
date_to_num_lb("drëtte Mäerz nonnzénghonnertnénganzwanzeg")  # Returns: "3.3.1929"
date_to_num_lb("fënneften August zweedausendeenandrësseg")  # Returns: "5.8.2031"

# Partial dates (day.month.)
date_to_num_lb("fënneften August")  # Returns: "5.8."
date_to_num_lb("véierten Oktober")  # Returns: "4.10."
date_to_num_lb("zéngten Abrëll")  # Returns: "10.4."

# N-rule implementation
date_to_num_lb("éischten Abrëll")  # Returns: "1.4." (keeps -n before vowel A)
date_to_num_lb("zweeten Oktober")  # Returns: "2.10." (keeps -n before vowel O)
date_to_num_lb("drëtten Dezember")  # Returns: "3.12." (keeps -n before D)
date_to_num_lb("véierten November")  # Returns: "4.11." (keeps -n before N)

date_to_num_lb("éischte Februar")  # Returns: "1.2." (drops -n before F)
date_to_num_lb("zweete Juli")  # Returns: "2.7." (drops -n before J)
date_to_num_lb("drëtte Mäerz")  # Returns: "3.3." (drops -n before M)
date_to_num_lb("véierte September")  # Returns: "4.9." (drops -n before S)

# Abbreviations
date_to_num_lb("éischten Jan")  # Returns: "1.1."
date_to_num_lb("zweete Feb")  # Returns: "2.2."
date_to_num_lb("drëtten Dez")  # Returns: "3.12."

# Hyphenated forms
date_to_num_lb("éischten-Abrëll")  # Returns: "1.4."
date_to_num_lb("zweete-Mäerz")  # Returns: "2.3."
```

### The Luxembourgish N-Rule

The n-rule in Luxembourgish states that final -n is:
- Kept before vowels and the consonants h, n, d, z, t, r
- Dropped before other consonants

This rule is correctly implemented in the date parser for ordinal forms.

## Installation

```
pip install words2num
```

## Running Tests

To test the Luxembourgish implementation:

```python
# Run the validation script that tests all functionality
python validate_words2num_LB.py

# Run specific test suite for date parsing
python test_lb_dates.py
```