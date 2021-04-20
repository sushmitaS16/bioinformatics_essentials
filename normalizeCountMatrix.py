#!/usr/bin/python
'''
@sushmitaS16
'''

import os
import sys
import argparse
import pandas as pd
import numpy as np


desc = "Script to normalize a count matrix (based on 'DESeq2' normalization algorithm)"

# initialize parser
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("-i", "--infile", help="Input count matrix")
parser.add_argument("-o", "--outfile", help="Output normalized count matrix")

# read arguments from command line
args = parser.parse_args()

# define input and output files
countfile = args.infile
normalized_countfile = args.outfile

df = pd.DataFrame(pd.read_table(countfile, header=0, sep='\t', index_col=0))
data = df.copy()
#print(df.dtypes)

samples = df.columns


# NOTE: The scaling factor has to take read depth and library composition into account

# 1. Take log (log base e) of all read count values
df = df.apply(np.log)
slength = len(df.iloc[:,0])

# 2. Averaging each row (NOTE: avg values are not easily swayed by outliers)
df = df.assign(avg=df.mean(axis=1))

# check if any average value is not infinity
print(np.array(df['avg'] == -np.Inf).all())

# 3. Filter out the genes with with infinity (NOTE: this will filter out sample specific genes/transcripts)
df = df.loc[df['avg'] != -np.Inf]
avg = df['avg']

# 4. Subtract avg log value from log counts
df = df.subtract(avg, axis=0)
df = df.drop('avg', axis=1)

# 5. Calculate median of the ratios for each sample(column wise median)
median = df.median(axis=0)

# 6. Convert medians to "normal" numbers to obtain the final sample-specific scaling factors
median = np.exp(median)

# 7. Divide the original read counts by the scaling factors
data = data.divide(median, axis=1)


data.to_csv(normalized_countfile, sep='\t', index_label="ID")