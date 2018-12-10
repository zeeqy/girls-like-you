import pandas as pd
import numpy as np
import os

"""
Random State 
"""
rd = np.random.RandomState(42)

"""
Load Table
"""
cur_dir = os.path.dirname(os.path.realpath(__file__))
cust_table = pd.read_table(os.path.join(cur_dir, "data", "0.1x", "customer.tbl"), delimiter='|', usecols=[0], names=["CUSTKEY"])
order_table = pd.read_table(os.path.join(cur_dir, "data", "0.1x", "orders.tbl"), delimiter='|', usecols=[0, 1], names=["ORDERKEY", "CUSTKEY"])
lineitem_table = pd.read_table(os.path.join(cur_dir, "data", "0.1x", "lineitem.tbl"), delimiter='|', usecols=[0, 3], names=["ORDERKEY", "LINENUMBER"])

# print(cust_table.head())
# print(order_table.head())
# print(lineitem_table.head())

def getMaxFreq(table, col):
    return list(table[col].value_counts().to_dict().values())[0]

def getFreq(table, col, value):
    return (table.iloc[:,col] == value).sum()

def olken(lst, frame):
    """
    Init
    """
    output = []
    p = 1.0
    level = 1

    """
    First table
    """
    idx = rd.randint(0, lst[0].shape[0])
    value = lst[0].iloc[idx,frame[0][0]]
    output.append(value) #i.e Q3, this is c.custkey

    while level < len(lst):

        degree = getFreq(lst[level],frame[level][0],value)
        idx_offset = rd.randint(0, degree)
        matched = lst[level][lst[level].iloc[:,frame[level][0]] == value].iloc[idx_offset]
        
        """
        Update value
        """

        value = matched[frame[level][1]]

        output.append(value)

        level += 1

        p *= degree

    print(output, p)


olken([cust_table,order_table,lineitem_table],[(0,0),(1,0),(0,1)])
print(getMaxFreq(lineitem_table,'ORDERKEY'))
