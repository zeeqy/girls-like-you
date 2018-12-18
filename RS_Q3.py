import pandas as pd
import numpy as np
import os
import time
import argparse
import sys

def main():
    """
    Parsing Arguments
    """
    parser = argparse.ArgumentParser(description="take params including scale factors")
    parser.add_argument('--sf', nargs=1)
    if (parser.parse_args().sf == None):
        print("Please specify scale factor after --sf\ne.g. \"python RS_Q3.py --sf 0.1\"")
        exit(0)
    else:
        sf = parser.parse_args().sf[0]
    np.random.seed(42)
    ### Load table
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(cur_dir, "data", sf + "x")
    if not os.path.exists(data_path):
        print("\"{}\" doesn't exists... please check again...".format(data_path))
        exit(0)
    cust_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "customer.tbl"), delimiter='|', usecols=[0], names=["CUSTKEY"])
    order_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "orders.tbl"), delimiter='|', usecols=[0, 1], names=["ORDERKEY", "CUSTKEY"])
    lineitem_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "lineitem.tbl"), delimiter='|', usecols=[0, 3], names=["ORDERKEY", "LINENUMBER"])
    ### Sample
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
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()
