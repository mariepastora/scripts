"""
This is a python script calculating an estimate of median income, when 
only information available is buckets of income, and the number of people in each bucket 

The main function compute_pareto_median_income, takes a dataframe with only buckets as columns
It returns a dataframe with additional columns 

Credits: 
    - Andre Tartar @ Bloomberg
    - LATimes Datadesk (https://github.com/datadesk/latimes-calculate/blob/pareto/calculate/pareto.py) 
        - Anthony Pesce
        - Steve Doig
        - Bob Hoyer
        - Meghan Hoyer
"""


import pandas as pandas
import itertools
import re


def determine_median_bucket(row):
    """
    Determining which bucket the median household is in
    
    param: a pandas series
    return: a string (name of a bucket aka column of the dataframe)
    """
    bucket = ''
    running_sum = 0
    
    # going through all columns except the last one that has total num of households 
    for i, col in enumerate(row.index.to_list()[:-1]):
        running_sum += row[col]
        if running_sum > row['median_household']:
            bucket = row.index.to_list()[:-1][i]
            return bucket
        
def sum_prev(row):
    """
    Summing all buckets before the one the median household income is in 
    
    param: a pandas series
    return: an int (sum of all cols until median_bucket, median_bucket excluded)
    """
    bucket = row['bucket_median']
    sum_previous = 0
    # list of all columns to sum the values of 
    list_to_loop = list(itertools.takewhile(lambda x: x != bucket, row.index.to_list()))
    for i, col in enumerate(list_to_loop):
        sum_previous += row[col]
    return sum_previous

def calculating_median(row):
    """
    Calculating median estimate (thanks to pareto.py here: https://github.com/datadesk/latimes-calculate/blob/pareto/calculate/pareto.py)
    This function makes the assumption that the median bucket will never be a higher bound bucket (of format "200,000 and over")
    
    param: a pandas series
    return: an int (pareto median for the row)
    """
    bucket_string = row['bucket_median']
    regex = re.compile(r'(\$\d+\,\d+)')
    boundaries = regex.findall(bucket_string)
    try: 
        lower = int(boundaries[0].replace('$', '').replace(',', ''))
        if len(boundaries) == 2:
            width = int(boundaries[1].replace('$', '').replace(',', '')) - lower
        elif len(boundaries) == 1:
            width = lower
        
        return lower + ((row['median_household'] - row['sum_prev']) / row[bucket_string]) * width
    except: 
        raise Exception("Wrong number of boundaries")

def compute_pareto_median_income(df):
    """
    Assume one geography per row, and that income is in column with several buckets, and that there is no other colum
    This is the function you'll want to import 

    param: a dataframe
    return: a copy of original dataframe with additional columns 
    """
    df_copy = df.copy()
    # computing median household for each geography
    df_copy['median_household'] = (df_copy.sum(axis = 1)) / 2
    
    # Determining median bucket
    df_copy['bucket_median'] = df_copy.apply(determine_median_bucket, axis = 1)
    # Computing sum of previous buckets
    df_copy['sum_prev'] = df_copy.apply(sum_prev, axis = 1)
    # Calculating pareto median
    df_copy['pareto_median'] = df_copy.apply(calculating_median, axis = 1)
    
    return df_copy