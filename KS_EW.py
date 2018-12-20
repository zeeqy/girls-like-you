import pandas as pd
import random
import os
import time
import argparse
import sys

def computeCountDP(lst, frame):
    level = len(frame) - 1
    lst[level]['W'] = 1
    level -= 1
    while level >= 1:
        lst[level]['W'] = lst[level][frame[level][1]].map(lst[level+1].set_index(frame[level+1][0], append=True)\
                            .sum(level=1)['W'])
        level -= 1
    lst[0]['W'] = lst[0][frame[0][1]].map(lst[1].set_index(frame[1][1], append=True)\
                            .sum(level=1)['W'])
    for tbl in range(len(frame)):
        lst[tbl].dropna(how='any',inplace=True)

def exactWeight(nation_list, supplier_dict ,cust_dict, order_dict, lineitem_dict):
    output = []
    value = random.choice(nation_list)
    output.append(value)
    output.append(random.choice(supplier_dict[value]))
    value = random.choice(cust_dict[value])
    output.append(value)
    value = random.choice(order_dict[value])
    output.append(value)
    output.append(random.choice(lineitem_dict[value]))
    return output

def getMaxFreq(table, col):
    return list(table.iloc[:,col].value_counts().to_dict().values())[0]

def load_dictionary(table, frame):
    d = {}
    for t in table:
        d.setdefault(t[frame[0]], []).append(t[frame[1]])
    return d

def position(tup, nation_list, supplier_dict ,cust_dict, order_dict, lineitem_dict):
    s1 = 0
    for nation in range(tup[0]):
        t = 0
        for custkey in cust_dict[nation]:
            for orderkey in order_dict[custkey]:
                t += len(lineitem_dict[orderkey])

        t *= len(supplier_dict[nation])
        s1 += t

    s2 = 0
    for suppierkey in sorted(supplier_dict[tup[0]]):
        if suppierkey < tup[1]:
                s2 += 1

    s6 = 0
    for custkey in sorted(cust_dict[tup[0]]):
        for orderkey in order_dict[custkey]:
            s6 += len(lineitem_dict[orderkey])

    s3 = 0
    for custkey in sorted(cust_dict[tup[0]]):
        if custkey < tup[2]:
            for orderkey in order_dict[custkey]:
                s3 += len(lineitem_dict[orderkey])
    s4 = 0
    s5 = 0
    for orderkey in sorted(order_dict[tup[2]]):
        if orderkey < tup[3]:
            s4 += len(lineitem_dict[orderkey])
        if orderkey == tup[3]:
            while s5 < tup[4]:
                s5 += 1

    return s1 + s2 * s6 + (s3 + s4) + s5

if __name__ == '__main__':
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
    Begin sampling
    """
    if True:
        print('begin sampling ...')
        print('sample size = 10000')
        tot_size = 10000
        sample_size = 0
        start_time = time.time()
        ew_output = []
        while sample_size < tot_size:
            tup = exactWeight(nation_list, supplier_dict ,cust_dict, order_dict, lineitem_dict)
            if tup:
                sample_size += 1
                ew_output.append(tup)

        print("sampling time = {}".format((time.time() - start_time)))
        print("--"*50)
        with open('data/ew_output.csv', 'w') as f:
            for item in ew_output:
                string = [str(i) for i in item]
                f.write("{}\n".format(','.join(string)))
    else:
        ew_output = pd.read_csv('data/ew_output.csv', sep=',',header=None)
        ew_output = ew_output.values


    prob = []
    c = 0
    for tup in ew_output:
        pos = position(tup, nation_list, supplier_dict ,cust_dict, order_dict, lineitem_dict)
        prob.append(pos/2400301184)
        c += 1
        if c % 100 == 0:
            print("currently at {}".format(c))

    with open('data/ew_ks_output.csv', 'w') as f:
        for item in prob:
            f.write("{}\n".format(item))