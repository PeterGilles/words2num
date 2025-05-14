# words2num

Inverse text normalization for numbers. Converts number words to their numeric representation.

## Supported Languages

- **English (en-US)**: "forty-two hundred and forty-two" → 4242
- **Spanish (es-US)**: "cuarenta y dos cientos cuarenta y dos" → 4242
- **Luxembourgish (lb/lb-LU)**: "véierdausendvéierafoffzeg" → 4254

## Usage

Basic usage example:

```python
from words2num import w2n

# English
w2n("forty-two") # Returns: 42

# Spanish
w2n("cuarenta y dos", lang="es") # Returns: 42

# Luxembourgish
w2n("véierafoffzeg", lang="lb") # Returns: 54
```

## Features

- Convert cardinal numbers (one, two, three)
- Handle decimal expressions (two point five)
- Support for various number formats and conventions
- Language-specific number parsing rules
- Hyphenated forms and compound words

## Luxembourgish Support

The Luxembourgish (`lb`) implementation includes:

- Cardinal numbers: "eenhonnert zweeanzwanzeg" → 122
- Ordinal numbers: "éischten", "zweeten", "drëtten" → 1, 2, 3
- Decimal numbers with "komma" or "punkt"
- Special handling for compound forms: "dräihonnert" → 300
- Hyphenated forms: "véier-a-foffzeg" → 54
- Various formatting options and number representations

Example usage:

```python
from words2num import w2n

# Cardinal numbers
w2n("eent", lang="lb") # Returns: 1
w2n("zwanzeg", lang="lb") # Returns: 20
w2n("eenhonnert", lang="lb") # Returns: 100

# Complex expressions
w2n("zwee dausend dräihonnert véierafoffzeg", lang="lb") # Returns: 2354
w2n("eng millioun fënnefhonnert dausend", lang="lb") # Returns: 1500000

# Decimals
w2n("dräi komma véier", lang="lb") # Returns: 3.4
w2n("zwee punkt néng fënnef", lang="lb") # Returns: 2.95
```

## Installation

```
pip install words2num
```

## Running Tests

```
python -m unittest discover tests
```

To test a specific language:

```
python -m unittest tests.test_LB  # Test Luxembourgish implementation
```