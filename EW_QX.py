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

def computeCountDP(lst, frame):
    level = len(frame) - 1
    lst[level]['W'] = 1
    level -= 1
    while level >= 0:
        lst[level]['W'] = lst[level][frame[level][1]].map(lst[level+1].set_index(frame[level+1][0], append=True)\
                            .sum(level=1)['W'])
        level -= 1
    lst[0].dropna(how='any',inplace=True)
    lst[1].dropna(how='any',inplace=True)

def exactWeight(nation_list, supplier_dict ,cust_dict, order_dict, lineitem_dict):
    value = random.choice(nation_list)
    random.choice(supplier_dict[value])
    value = random.choice(cust_dict[value])
    value = random.choice(order_dict[value])
    random.choice(lineitem_dict[value])

def main():
    """
    Parsing Arguments
    """
    parser = argparse.ArgumentParser(description="take params including scale factors")
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
    nation_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "nation.tbl"), delimiter='|', usecols=[0], names=["NATIONKEY"])
    supplier_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "supplier.tbl"), delimiter='|', usecols=[0,3], names=["SUPPKEY", "NATIONKEY"])
    cust_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "customer.tbl"), delimiter='|', usecols=[0, 3], names=["CUSTKEY", "NATIONKEY"])
    order_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "orders.tbl"), delimiter='|', usecols=[0, 1], names=["ORDERKEY", "CUSTKEY"])
    lineitem_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "lineitem.tbl"), delimiter='|', usecols=[0, 3], names=["ORDERKEY", "LINENUMBER"])

    frame = [(0,0),(1,0),(1,0),(1,0),(0,1)]
    frame_name = [("", "NATIONKEY"),("NATIONKEY","CUSTKEY"),("CUSTKEY","ORDERKEY"),("ORDERKEY", "")]

    print('Exact Weight on QX ...')
    print('building dictionary ...')
    lst = [nation_table, cust_table, order_table, lineitem_table]
    computeCountDP(lst, frame_name)
    nation_list = nation_table['NATIONKEY'].values.tolist()
    supplier_list = supplier_table.values.tolist()
    cust_list = cust_table.values.tolist()
    order_list = order_table.values.tolist()
    lineitem_list = lineitem_table.values.tolist()
    supplier_dict = load_dictionary(supplier_list,frame[1])
    cust_dict = load_dictionary(cust_list,frame[2])
    order_dict = load_dictionary(order_list,frame[3])
    lineitem_dict = load_dictionary(lineitem_list,frame[4])

    """
    Begin sampling - Exact Weight
    """
    print('begin sampling ...')
    for tot_size in [1000,10000,100000,1000000]:
        print('sample size = {}'.format(tot_size))
        sample_size = 0
        print('DP ...')
        start_time = time.time()
        computeCountDP(lst, frame_name)
        while sample_size < tot_size:
            exactWeight(nation_list, supplier_dict ,cust_dict, order_dict, lineitem_dict)
            sample_size += 1
        print("sampling time = {}".format((time.time() - start_time)))
        print("--"*50)


if __name__ == '__main__':
    main()