# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
# python setup.py sdist

import pandas as pd
pd.set_option('display.max_columns', None) # Displaying all the columns in the dataset
pd.set_option('max_colwidth', None) # Displaying entire contents of columns
pd.set_option("max_rows", 100) # Displaying all rows
pd.set_option('max_seq_item', None) # Displaying everything in the list in the dataframe
pd.set_option('precision', 2) # Displaying precision to just 2 decimal places


def add_numbers(num1, num2):
    return num1 + num2