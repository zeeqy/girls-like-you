<<<<<<< HEAD
import pandas as pd
import numpy as np
import os
import time
import argparse
import sys
from multiprocessing import Process, Pool, cpu_count, current_process

def computeCountDP(lst, frame):
    level = len(frame) - 1
    lst[level]['W'] = 1
    level -= 1
    while level >= 0:
        lst[level]['W'] = lst[level][frame[level][1]].map(lst[level+1].set_index(frame[level+1][0], append=True)\
                            .sum(level=1)['W']).fillna(0)
        level -= 1

def exactWeight0(lst, frame):
    t = lst[0].sample(n=1)
    w = t['W'].values[0]
    if w == 0:
        return False
    level = 1
    while level < len(lst):
        val = t[frame[level-1][1]].values[0]
        temp_results = lst[level][lst[level][frame[level][0]]==val]
        t = temp_results.sample(n=1)
        level += 1
    return True

def exactWeight(lst, frame):
    idx = np.random.choice(lst[0].index.values)
    w = lst[0].iloc[idx]["W"]
    if w == 0:
        return False
    level = 1
    while level < len(lst):
        val = lst[level-1].iloc[idx][frame[level-1][1]]
        temp_results = lst[level][lst[level][frame[level][0]]==val]
        idx = np.random.choice(temp_results.index.values)
        level += 1
    return True

def sub_processing(lst, frame, sample_size):
    cnt = 0
    while (cnt < sample_size):
        if exactWeight(lst, frame):
            cnt += 1
    print("---- {} sampled {} records...----".format(current_process().name, cnt))
    return

def main():
    """
    Parsing Arguments
    """
    parser = argparse.ArgumentParser(description="take params including scale factors")
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

    """
    Prepare to sample
    """
    # tot_size = 1000
    # sample_size = 0
    frame = [("", "CUSTKEY"),("CUSTKEY", "ORDERKEY"), ("ORDERKEY","")]
    lst = [cust_table,order_table,lineitem_table]

    """
    Begin sampling - Exact Weight
    """

    start_time = time.time()

    computeCountDP(lst, frame)
    cpuNum = cpu_count()
    pool = Pool(cpuNum)
    print("# threads = {}".format(cpuNum))
    for i in range(cpuNum):
        pool.apply_async(sub_processing, args=(lst, frame, tot_size/cpuNum))
    pool.close()
    pool.join()
    # while sample_size <= tot_size:
    #     if exactWeight(lst,frame, sample_size):
    #         sample_size += 1
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
    '''
    data0 = np.array([['','C1','C2'],
                ['Row1',"Peter","kiwi"],
                ['Row2',"John","banana"],
                ['Row3',"Susan","peach"],
                ['Row4',"Joe","apple"]])
    df0 = pd.DataFrame(data=data0[1:,1:],
                  columns=data0[0,1:])
    print df0
    data1 = np.array([['','C3','C4'],
                ['Row1',"apple",4],
                ['Row2',"banana",7],
                ['Row3',"apple",4]])
    df1 = pd.DataFrame(data=data1[1:,1:],
                  columns=data1[0,1:])
    df1['C4'] = pd.to_numeric(df1['C4'])
    print df1
    #df0['W'] = df0['C2'].map(df1.set_index('C3', append=True)\
    #                        .sum(level=1)['C4']).fillna(0)
        #print df0 