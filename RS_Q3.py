import pandas as pd
import numpy as np
import os
import time
import argparse
import sys

<<<<<<< HEAD
=======
def getMaxFreq(table, col):
    return list(table.iloc[:,col].value_counts().to_dict().values())[0]

def getFreq(table, col, value):
    return (table.iloc[:,col] == value).sum()

def olken(lst, frame, max_p):
    """
    Init
    """
    output = []
    p = max_p = 1.0
    level = 1

    """
    First table
    """
    idx = np.random.randint(0, lst[0].shape[0])
    value = lst[0].iloc[idx,frame[0][0]]
    output.append(value) #i.e Q3, this is c.custkey

    while level < len(lst):

        degree = getFreq(lst[level],frame[level][0],value)
        
        # zero matching
        if not degree:

            return False

        idx_offset = np.random.randint(0, degree)
        matched = lst[level][lst[level].iloc[:,frame[level][0]] == value].iloc[idx_offset]
        
        """
        Update value
        """
        value = matched[frame[level][1]]
        output.append(value)
        level += 1
        p *= degree

    return np.random.uniform(0, max_p) < p

>>>>>>> 1d371c502e99d2995371eec1a46c822c0ae028cb
def main():
    """
    Parsing Arguments
    """
<<<<<<< HEAD
    parser = argparse.ArgumentParser(description="take params including scale factors")
    parser.add_argument('--sf', nargs=1)
=======
    parser = argparse.ArgumentParser(description="take params including scale factors and sample size")
    parser.add_argument('--sf', nargs=1)
    parser.add_argument('--ss', nargs=1)
>>>>>>> 1d371c502e99d2995371eec1a46c822c0ae028cb
    if (parser.parse_args().sf == None):
        print("Please specify scale factor after --sf\ne.g. \"python RS_Q3.py --sf 0.1\"")
        exit(0)
    else:
        sf = parser.parse_args().sf[0]
<<<<<<< HEAD
=======

    if (parser.parse_args().ss == None):
        print("Please specify sample size after --ss\ne.g. \"python RS_Q3.py --ss 10000\"")
        exit(0)
    else:
        tot_size = parser.parse_args().ss[0]
>>>>>>> 1d371c502e99d2995371eec1a46c822c0ae028cb
    
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

    """
    Prepare to sample
    """
<<<<<<< HEAD
    tot_size = 1000
    sample_size = 0
    start_time = time.time()
    while sample_size < tot_size:
        output = []
        t = lineitem_table.iloc[np.random.randint(0, lineitem_table.shape[0])]
        output.append(t)
        t2 = order_table[order_table['ORDERKEY'] == t["ORDERKEY"]]
        idx = np.random.randint(0, t2.shape[0])
        t2 = t2.iloc[idx]
        output.append(t2)
        t3 = cust_table[cust_table['CUSTKEY'] == t2["CUSTKEY"]]
        idx = np.random.randint(0, t3.shape[0])
        t3 = t3.iloc[idx]
        output.append(t3)
        #print output
        sample_size += 1
=======
    sample_size = 0

    max_p = 1.0   # <-------- special for reverse sample

    frame = [(0,0),(1,0),(0,1)]
    lst = [cust_table,order_table,lineitem_table]

    """
    Begin sampling
    """
    start_time = time.time()
    
    while sample_size <= tot_size:
        if olken(lst,frame,max_p):
            sample_size += 1

>>>>>>> 1d371c502e99d2995371eec1a46c822c0ae028cb
    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
<<<<<<< HEAD
    main()
=======
    main()




>>>>>>> 1d371c502e99d2995371eec1a46c822c0ae028cb