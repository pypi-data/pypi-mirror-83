import requests
import zipfile
import os
import random
import logging

import numpy as np
import pandas as pd

URL_MILLION_RANDOM_DIGITS = "https://www.rand.org/content/dam/rand/pubs/monograph_reports/MR1418/MR1418.digits.txt.zip"
N = 1000000
DIGITS_FILENAME = "digits.txt"

def download_digits():
    """Downloads the digits in the original format to a digits.txt file"""
    r = requests.get(url=URL_MILLION_RANDOM_DIGITS)
    open("digits.zip", 'wb').write(r.content)
    zipfile.ZipFile("digits.zip", mode="r").extract(DIGITS_FILENAME)
    os.remove("digits.zip")

def get_digits(format="list"):
    """Returns the digits in the preferred format (list, numpy, pandas)"""
    
    # If the source file is missing, download it
    if not os.path.exists(DIGITS_FILENAME):
        download_digits()
    
    digits = ""
    for line in open(DIGITS_FILENAME, "rt").readlines():
        # Ignore the first group of digits for each line, it is just the row number,
        # then remove any remaining spaces and newline charachters
        digits += list(line.split(" ", maxsplit=1))[1] \
                  .replace(" ", "").replace("\n", "")
    
    list_digits = [int(digit) for digit in digits]
    if format == "list":
        return list_digits
    elif format == "numpy":
        return np.array(list_digits)
    elif format == "pandas":
        return pd.DataFrame(list_digits)


def rand_digit(start_index = None):
    """
        Yield random digits in order from the list. 
        If no start_index is specified, then it is picked (pseudo)-randomly.
    """
    
    if start_index is None:
        start_index = random.randint(0, N)
    logging.debug("Starting index for random digits generator is {}".format(start_index))
    i = start_index
    
    digits = get_digits()
    
    # Yield all digits, then stop
    while i < start_index + N:
        yield digits[i % N]
        i += 1
    
    return


def main():
    
    print("Testing the module randbyrand.")
    
    heading_digits = [1, 0, 0, 9, 7]
    tailing_digits = [4, 1, 9, 8, 8]
    
    # Test download
    if os.path.exists(DIGITS_FILENAME):
        os.remove(DIGITS_FILENAME)
    try:
        digits = get_digits()
    except:
        print("Downloading or reading digits failed.")
        return
    else:
        print("Downloading and reading digits succeded.")
    
    # Test consistency
    n = len(digits) 
    if n != N:
        print("There should be one million digits, but only {} have been loaded.".format(n))
        return
    else:
        print("One million digits have been retrieved correctly.")
    
    if digits[:5] != heading_digits or digits[999995:] != tailing_digits:
        print("Heading and tailing digits do NOT match.")
        return
    else:
        print("Heading and tailing digits match.")
    
    # Test formats other than list
    try:
        digits = get_digits("numpy")
    except:
        print("Digits failed to load as Numpy array.")
        return
    else:
        print("Digits successfully loaded as Numpy array.")
    
    try:
        digits = get_digits("pandas")
    except:
        print("Digits failed to load as Pandas DataFrame.")
        return
    else:
        print("Digits successfully loaded as Pandas DataFrame.")
    
    # Test random digit generator
    x = rand_digit()
    print("Random digit generator loaded successfully.")

    n = len(list(rand_digit()))
    if n != N:
        print("The function rand_digit only generated {} digits instead of one million.".format(n))
        return
    else:
        print("The function rand_digit correctly generated one million digits.")
    
    digits = list(rand_digit(start_index=0))
    if digits[:5] != heading_digits or digits[999995:] != tailing_digits:
        print("Heading and tailing digits of the function rand_digit do NOT match.")
        return
    else:
        print("Heading and tailing digits of the function rand_digit match.")
    
    # Test end
    print("All tests completed  successfully.")
    return
    
    
if __name__ == "__main__":
    main()
