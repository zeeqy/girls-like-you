import pandas as pd
import numpy as np
import os
import time




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

def main():
    """
    Random State 
    """
    np.random.seed(42)

    """
    Load Table
    """
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    cust_table = pd.read_table(os.path.join(cur_dir, "data", "0.1x", "customer.tbl"), delimiter='|', usecols=[0], names=["CUSTKEY"])
    order_table = pd.read_table(os.path.join(cur_dir, "data", "0.1x", "orders.tbl"), delimiter='|', usecols=[0, 1], names=["ORDERKEY", "CUSTKEY"])
    lineitem_table = pd.read_table(os.path.join(cur_dir, "data", "0.1x", "lineitem.tbl"), delimiter='|', usecols=[0, 3], names=["ORDERKEY", "LINENUMBER"])

    """
    Prepare to sample
    """
    tot_size = 1000
    sample_size = 0
    max_p = 1.0
    frame = [(0,0),(1,0),(0,1)]
    lst = [cust_table,order_table,lineitem_table]

    for tbl in range(1,len(frame)):
        max_p *= getMaxFreq(lst[tbl],frame[tbl][0])

    """
    Begin sampling
    """
    start_time = time.time()
    
    while sample_size <= tot_size:
        if olken(lst,frame,max_p):
            sample_size += 1

    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
    main()




