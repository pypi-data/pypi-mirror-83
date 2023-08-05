This module includes simple functions to retrieve and work with the digits of [_A Million Random Digits with 100,000 Normal Deviates_](https://www.rand.org/pubs/monograph_reports/MR1418.html) by RAND Corporation.

# Usage

## Get all digits
```
import randbyrand

# As a list
digits = randbyrand.get_digits()

# As a numpy array
digits = randbyrand.get_digits("numpy")

# As a Pandas DataFrame
digits = randbyrand.get_digits("pandas")
```

## Random number generator
```
import randbyrand

random_digit = randbyrand.rand_digit().__next__()
```