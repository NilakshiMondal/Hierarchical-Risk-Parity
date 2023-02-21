import pandas as pd
import numpy as np
import re
from datetime import datetime

# Read in 'original_data.csv', which is the 'data.csv' file that you originally
# sent me over email.
# The cleaned dataset is a lot smaller so we won't have to worry about pushing
# this big file up and down from Git because that analysis part will only use
# 'clean_data.csv' -- the output of this script.
data = pd.read_csv('data/original_data.csv')

# remove the '_returns' from all the column names bc it's awkward
data = data.set_axis(
    [re.sub("([ ]*_.*)$", "", x) for x in list(data.columns)],
    axis=1
)

# round everything to the nearest hour to get an hourly time index
data['timeclose'] = pd.to_datetime(data['timeclose']).dt.round("H")
data.set_index('timeclose', inplace=True)

# I don't think the zeros are meaningful in this data because -- just looking
# at it -- bc it looks like an entire row calculates when just one coin shows a
# return, and the time basis is not evenly spaced. So we want to ignore the
# 0's when we calculate hourly average return.
data[data == 0] = np.nan

# initialize clean_data
clean_data = pd.DataFrame(
    index   = np.unique(data.index),
    columns = data.columns
)

# ASSUMPTION here: For this dataset, what we really want is the average non-zero
# returns observed for that coin during a particular hour.
# This will give us overall hourly returns in 'clean_data', which we can use.
for coin in clean_data.columns:
    for closetime in clean_data.index:
        clean_data.loc[closetime, coin] = np.mean(data.loc[closetime, coin])

# quick function that gives you all the UNIQUE days in a datetime-indexed df
# dates returned as a chr list
def get_unique_days(df):
    return np.unique([
        datetime.strftime(x, "%Y-%m-%d") for x in list(
            pd.to_datetime(clean_data.index).date)
    ])

# use it on clean_data:
clean_data_days_chr = get_unique_days(clean_data)

# remove SHIB, HNT, and SOL, can't use em (bad data)
clean_data.drop(['SHIB', 'HNT', 'SOL'], axis=1, inplace=True)

# The first day and the last two days are also not useful -- just look at the
# dataset to see that they're not complete, so drop them.
clean_data = clean_data.loc[
    (clean_data.index >= str(clean_data_days_chr[1])) & (
            clean_data.index < str(clean_data_days_chr[-2])
    )
]

# update clean_data_days_chr bc why not:
clean_data_days_chr = get_unique_days(clean_data)

# At this point if there's any NaNs in there then I guess they were really 0 (?)
clean_data = clean_data.fillna(0)

# initialize
problem_days = []

# Sanity check: there should be 24 entries (rows) for every day in the dataset.
# Let's see if that's true...
for day in clean_data_days_chr:
    if clean_data.loc[day].shape[0] != 24:
        problem_days.append(day)
        print(str(day) + ": " + str(clean_data.loc[day].shape[0]) + " rows")

# ...and you can see that it's not.

# You need to figure out how to go forward. Options I see are:
# 1. Just delete 01 and 31 Jan every year (WHY are those messed up?) and
#    interpolate for the other 4 days since they're only missing 1 or 3 each
# 2. Do this project using DAILY AVERAGES instead of HOURLY so that you can
#    have a complete set of data
# 3. Figure out how your data.csv was generated to begin with and either fix
#    the problem or find yourself a cleaner dataset from another source

# Let me know what you want to do :)

# You can check out 'clean_data.csv' in Excel if you want bc I write it here:
clean_data.to_csv('clean_data.csv')
