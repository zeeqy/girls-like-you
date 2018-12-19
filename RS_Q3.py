import pandas as pd
import random
import os
import time
import argparse
import sys

def load_dictionary(table, frame):
    d = {}
    for t in table:
        d.setdefault(t[frame[0]], []).append(t[frame[1]])
    return d

def rev_sample(cust_list, order_dict, lineitem_dict):
    """
    Init
    """
    value = random.choice(cust_list)

    if value in order_dict:
        value = random.choice(order_dict[value])
    else:
        return False

    if value in lineitem_dict:
        return True
    else:
        return False

def main():
    """
    Parsing Arguments
    """
    parser = argparse.ArgumentParser(description="take params including scale factors and sample size")
    parser.add_argument('--sf', nargs=1)
    if (parser.parse_args().sf == None):
        print("Please specify scale factor after --sf\ne.g. \"python EO_Q3.py --sf 0.1\"")
        exit(0)
    else:
        sf = parser.parse_args().sf[0]
    
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

    cust_list = cust_table['CUSTKEY'].values.tolist()
    order_list = order_table.values.tolist()
    lineitem_list = lineitem_table.values.tolist()
    
    """
    Prepare to sample
    """
    sample_size = 0
    frame = [(0,0),(1,0),(0,1)]
    print('Reverse Sample on Q3 ...')
    print('building dictionary ...')
    order_dict = load_dictionary(order_list,frame[1])
    lineitem_dict = load_dictionary(lineitem_list,frame[2])

    """
    Begin sampling
    """
    print('begin sampling ...')
    for tot_size in [1000,10000,100000,1000000]:
        print('sample size = {}'.format(tot_size))
        start_time = time.time()
        while sample_size < tot_size:
            if rev_sample(cust_list,order_dict,lineitem_dict):
                sample_size += 1

        print("sampling time = {}".format((time.time() - start_time)))
        print("--"*50)

if __name__ == '__main__':
    main()