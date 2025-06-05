# words2num - Luxembourgish Implementation

Inverse text normalization for Luxembourgish numbers and dates. Converts word forms to their numeric representation.

## Overview

This library provides comprehensive support for Luxembourgish (Lëtzebuergesch) language, including:

- Conversion of number words to digits
- Date expression parsing with support for the Luxembourgish n-rule
- Support for compound numbers and complex expressions
- Proper handling of Luxembourgish-specific number forms

## Installation

The package is available directly from GitHub:

```bash
pip install git+https://github.com/petergilles/words2num.git
```

## Quick Start

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

### Number Conversion

The library supports:

- Cardinal numbers ("eent", "zwee", "dräi", etc.)
- Ordinal numbers ("éischten", "zweeten", "drëtten", etc.)
- Decimal numbers with "komma" or "punkt"
- Complex compound forms ("zweehonnert", "dräihonnert", etc.)
- Hyphenated forms ("véier-a-foffzeg")
- Numbers up to billions

### Date Parsing

- Full dates (day.month.year)
- Partial dates (day.month.)
- Proper n-rule implementation
- Month names and abbreviations
- Hyphenated forms

## Examples

### Number Conversion

```python
from words2num import w2n

# Basic numbers
w2n("eent", lang="lb")  # Returns: 1
w2n("zwanzeg", lang="lb")  # Returns: 20
w2n("eenhonnert", lang="lb")  # Returns: 100

# Complex expressions
w2n("zwee dausend dräihonnert véierafofzeg", lang="lb")  # Returns: 2354
w2n("eng millioun fënnefhonnert dausend", lang="lb")  # Returns: 1500000

# Decimals
w2n("dräi komma véier", lang="lb")  # Returns: 3.4
w2n("zwee punkt néng fënnef", lang="lb")  # Returns: 2.95

# Special forms
w2n("zwee-honnert", lang="lb")  # Returns: 200 (hyphenated)
w2n("dräihonnert", lang="lb")  # Returns: 300 (compound)
w2n("een-honnert-eent", lang="lb")  # Returns: 101 (hyphenated)
w2n("éischten", lang="lb")  # Returns: 1 (ordinal)
```

### Date Parsing

```python
from words2num import date_to_num_lb

# Full dates
date_to_num_lb("éischte Januar zweedausendvéier")  # Returns: "1.1.2004"
date_to_num_lb("drëtte Mäerz nonnzénghonnertnénganzwanzeg")  # Returns: "3.3.1929"

# Partial dates
date_to_num_lb("fënneften August")  # Returns: "5.8."
date_to_num_lb("véierten Oktober")  # Returns: "4.10."

# N-rule examples
date_to_num_lb("éischten Abrëll")  # Returns: "1.4." (keeps -n before vowel A)
date_to_num_lb("éischte Februar")  # Returns: "1.2." (drops -n before F)
```

### The Luxembourgish N-Rule

The n-rule in Luxembourgish states that final -n is:
- Kept before vowels and the consonants h, n, d, z, t, r
- Dropped before other consonants

This rule is correctly implemented in the date parser for ordinal forms.

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test suite
python -m pytest tests/test_lb_numbers_various.py
python -m pytest tests/test_lb_dates.py
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.