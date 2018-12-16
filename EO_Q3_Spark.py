import pandas as pd
import numpy as np
import os
import time
import argparse
import sys
from pyspark import SparkContext, SparkConf

def getMaxFreq(table, col):
    return list(table.iloc[:,col].value_counts().to_dict().values())[0]

def freq_table(table, col):
    return table.iloc[:,col].value_counts().to_dict()

def samplejoin(x):
    q = 0
    start_time = time.time()
    while q <= 100:
        if olken(lst_table,lst_freq,frame,max_p):
            q+=1
    return (x, time.time() - start_time)


def olken(lst, lst2, frame, max_p):
    """
    Init
    """
    p = max_p = 1.0
    level = 1

    """
    First table
    """
    idx = np.random.randint(0, lst[0].shape[0])
    value = lst[0].iloc[idx,frame[0][0]]

    while level < len(lst):
        # table dataframe
        df = lst[level]
        # frequency dataframe
        df2 = lst2[level-1]
        # frame in current iteration
        cur_frame = frame[level]

        if value not in df2:
            # zero matching
            return False
        else:
            degree = df2[value]

        idx_offset = np.random.randint(0, degree)
        
        """
        Update value
        """
        attr = list(df.columns.values)[cur_frame[0]]
        value = df[df[attr]==value].iloc[idx_offset,cur_frame[1]]
        level += 1
        p *= degree

    return np.random.uniform(0, max_p) < p



parser = argparse.ArgumentParser(description="take params including scale factors and sample size")
parser.add_argument('--sf', nargs=1)
parser.add_argument('--ss', nargs=1)
if (parser.parse_args().sf == None):
    print("Please specify scale factor after --sf\ne.g. \"python EO_Q3.py --sf 0.1\"")
    exit(0)
else:
    sf = parser.parse_args().sf[0]

if (parser.parse_args().ss == None):
    print("Please specify sample size after --ss\ne.g. \"python EO_Q3.py --ss 10000\"")
    exit(0)
else:
    tot_size = int(parser.parse_args().ss[0])

"""
Random State 
"""
np.random.seed(42)

"""
Load Table
"""
cur_dir = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(cur_dir, "data", sf + "x")
if not os.path.exists(data_path):
    print("\"{}\" doesn't exists... please check again...".format(data_path))
    exit(0)
cust_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "customer.tbl"), delimiter='|', usecols=[0], names=["CUSTKEY"])
order_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "orders.tbl"), delimiter='|', usecols=[0, 1], names=["ORDERKEY", "CUSTKEY"])
lineitem_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "lineitem.tbl"), delimiter='|', usecols=[0, 3], names=["ORDERKEY", "LINENUMBER"])

order_cust_freq = freq_table(order_table, 1)
line_order_freq = freq_table(lineitem_table, 0)

"""
Prepare to sample
"""
sample_size = 0
max_p = 1.0
frame = [(0,0),(1,0),(0,1)]
lst_table = [cust_table,order_table,lineitem_table]
lst_freq = [order_cust_freq, line_order_freq]

for tbl in range(1,len(frame)):
    max_p *= getMaxFreq(lst_table[tbl],frame[tbl][0])


key = [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0)]

rdd = sc.parallelize(key)

rdd.map(samplejoin).collect()


