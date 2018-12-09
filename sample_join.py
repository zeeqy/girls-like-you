import pandas as pd
import random
import os

cur_dir = os.path.dirname(os.path.realpath(__file__))
cust_table = pd.read_table(os.path.join(cur_dir, "data", "0.1x", "customer.tbl"), delimiter='|', usecols=[0], names=["CUSTKEY"])
order_table = pd.read_table(os.path.join(cur_dir, "data", "0.1x", "orders.tbl"), delimiter='|', usecols=[0, 1], names=["ORDERKEY", "CUSTKEY"])
lineitem_table = pd.read_table(os.path.join(cur_dir, "data", "0.1x", "lineitem.tbl"), delimiter='|', usecols=[0, 3], names=["ORDERKEY", "LINENUMBER"])

# print(cust_table.head())
# print(order_table.head())
# print(lineitem_table.head())

def getMaxFreq(table, col):
    return list(table[col].value_counts().to_dict().values())[0]

def olken(lst):
    W = 0.0
    Wp = 0.0
    rej_prob = 0.0
    sample_prob = 0.0
    table1 = lst[0]
    table2 = lst[1]
    table3 = lst[2]
    size1 = table1.shape[0]
    max2 = getMaxFreq(table2, "CUSTKEY")
    max3 = getMaxFreq(table3, "ORDERKEY")
    W = size1 * max2 * max3
    Wp = W
    rej_prob = 1 - W/Wp
    if (random.uniform(0, 1) > rej_prob):
        # sample

    else:
        pass
    
    print(W)



olken([cust_table, order_table, lineitem_table])