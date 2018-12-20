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
    value = random.choice(nation_list)
    random.choice(supplier_dict[value])
    value = random.choice(cust_dict[value])
    value = random.choice(order_dict[value])
    random.choice(lineitem_dict[value])

def getMaxFreq(table, col):
    return list(table.iloc[:,col].value_counts().to_dict().values())[0]

def load_dictionary(table, frame):
    d = {}
    for t in table:
        d.setdefault(t[frame[0]], []).append(t[frame[1]])
    return d

def olken(nation_list, supplier_dict ,cust_dict, order_dict, lineitem_dict, max_p):
    """
    Init
    """
    p = 1.0

    output = []

    value = random.choice(nation_list)
    output.append(value)

    if value in supplier_dict:
        p *= len(supplier_dict[value])
        output.append(random.choice(supplier_dict[value]))
    else:
        return False

    if value in cust_dict:
        p *= len(cust_dict[value])
        value = random.choice(cust_dict[value])
        output.append(value)
    else:
        return False

    if value in order_dict:
        p *= len(order_dict[value])
        value = random.choice(order_dict[value])
        output.append(value)
    else:
        return False

    if value in lineitem_dict:
        p *= len(lineitem_dict[value])
        output.append(random.choice(lineitem_dict[value]))
    else:
        return False

    return output if random.uniform(0, max_p) < p else False


def eo_run():
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
    nation_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "nation.tbl"), delimiter='|', usecols=[0], names=["NATIONKEY"])
    supplier_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "supplier.tbl"), delimiter='|', usecols=[0,3], names=["SUPPKEY", "NATIONKEY"])
    cust_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "customer.tbl"), delimiter='|', usecols=[0, 3], names=["CUSTKEY", "NATIONKEY"])
    order_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "orders.tbl"), delimiter='|', usecols=[0, 1], names=["ORDERKEY", "CUSTKEY"])
    lineitem_table = pd.read_table(os.path.join(cur_dir, "data", sf + "x", "lineitem.tbl"), delimiter='|', usecols=[0, 3], names=["ORDERKEY", "LINENUMBER"])


    nation_list = nation_table['NATIONKEY'].values.tolist()
    supplier_list = supplier_table.values.tolist()
    cust_list = cust_table.values.tolist()
    order_list = order_table.values.tolist()
    lineitem_list = lineitem_table.values.tolist()
    
    """
    Prepare to sample
    """
    max_p = 1.0
    frame = [(0,0),(1,0),(1,0),(1,0),(0,1)]

    print('Extended Olken on QX ...')
    print('building dictionary ...')
    supplier_dict = load_dictionary(supplier_list,frame[1])
    cust_dict = load_dictionary(cust_list,frame[2])
    order_dict = load_dictionary(order_list,frame[3])
    lineitem_dict = load_dictionary(lineitem_list,frame[4])


    lst_table = [nation_table, supplier_table, cust_table, order_table, lineitem_table]

    for tbl in range(1,len(frame)):
        max_p *= getMaxFreq(lst_table[tbl],frame[tbl][0])

    print('max_p = {}'.format(max_p))

    """
    Begin sampling
    """
    print('begin sampling ...')
    print('sample size = 1000000')
    tot_size = 1000000
    sample_size = 0
    start_time = time.time()
    trail = 1
    output = []
    while sample_size < tot_size:
        tup = olken(nation_list, supplier_dict ,cust_dict, order_dict, lineitem_dict, max_p)
        if tup:
            sample_size += 1
            output.append(tup)
        trail +=1

    print("sampling time = {}, trail = {}".format((time.time() - start_time), trail))
    print("--"*50)
    return output

if __name__ == '__main__':
    if False:
        eo_output = eo_run()
        with open('data/eo_output.csv', 'w') as f:
            for item in eo_output:
                string = [str(i) for i in item]
                f.write("{}\n".format(','.join(string)))

    else:
        eo_output = pd.read_csv('data/eo_output.csv', sep=',',header=None)
        eo_output = eo_output.values

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
    frame_name = [("", "NATIONKEY"),("SUPPKEY", "NATIONKEY"),("NATIONKEY","CUSTKEY"),("CUSTKEY","ORDERKEY"),("ORDERKEY", "")]

    print('Exact Weight on QX ...')
    print('building dictionary ...')
    lst = [nation_table, supplier_table, cust_table, order_table, lineitem_table]
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

    def position(tup, nation_list, supplier_dict ,cust_dict, order_dict, lineitem_dict):
        s1 = 0
        for nation in range(tup[0]):
            for custkey in cust_dict[nation]:
                for orderkey in order_dict[custkey]:
                    s1 += len(lineitem_dict[orderkey])

            s1 *= len(supplier_dict[nation])

        #sup = len(supplier_dict[tup[0]])
        s2 = 0
        for suppierkey in sorted(supplier_dict[tup[0]]):
            if suppierkey < tup[1]:
                    s2 += 1
        s3 = 0
        for custkey in sorted(cust_dict[tup[0]]):
            if custkey < tup[2]:
                for orderkey in order_dict[custkey]:
                    s3 += len(lineitem_dict[orderkey])
        s4 = 0
        for orderkey in sorted(order_dict[tup[2]]):
            if orderkey < tup[3]:
                s4 += len(lineitem_dict[orderkey])

        return s1+s2*(s3+s4)+1

    print(position([2,125,104863,4714245,1],nation_list, supplier_dict ,cust_dict, order_dict, lineitem_dict))

    # prob = []
    # for tup in eo_output[:10]:
    #     pos = position(tup,nation_list, supplier_dict ,cust_dict, order_dict, lineitem_dict)
    #     prob.append(pos/2400301184)

    # with open('data/eo_ks_output.csv', 'w') as f:
    #     for item in prob:
    #         f.write("{}\n".format(item))

