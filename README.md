# 645-miniProject

*Maybe it's 645. Maybe I'm barely alive*


### TPC-H Queries

#### Q3
Lineitems joined with the orders they associated with and the customers who placed the orders.
```sql
SELECT c_custkey, o_orderkey, l_linenumber
FROM customer,
     orders,
     lineitem
WHERE c_custkey = o_custkey
  AND l_orderkey = o_orderkey;
```

#### QX
Suppliers and customers in the same nations with the purchase history of the customers.
```sql
SELECT nationkey,
       s_suppkey,
       c_custkey,
       o_orderkey,
       l_linenumber
FROM nation,
     supplier,
     customer,
     orders,
     lineitem
WHERE n_nationkey = s_nationkey
  AND s_nationkey = c_nationkey
  AND c_custkey = o_custkey
  AND o_orderkey = l_orderkey;
```

#### QY
Suppliers that are in the same nation as a pair of customers in the same nation that has once ordered the same items.
```sql
SELECT l1.l_linenumber,
       o1.o_orderkey,
       c1.c_custkey,
       l2.l_linenumber,
       o2.o_orderkey,
       s_suppkey,
       c2.c_custkey
FROM lineitem l1,
     orders o1,
     customer c1,
     lineitem l2,
     orders o2,
     customer c2,
     supplier s
WHERE l1.l_orderkey = o1.o_orderkey
  AND o1.o_custkey = c1.c_custkey
  AND l1.l_partkey = l2.l_partkey
  AND l2.l_orderkey = o2.o_orderkey
  AND o2.o_custkey = c2.c_custkey
  AND c1.c_nationkey = s.s_nationkey
  AND s.s_nationkey = c2.c_nationkey;

```
