# 645-miniProject

*Maybe it's 645. Maybe I'm barely alive*


### TPC-H Queries

#### Q3

```sql
SELECT *
FROM customer C,
     orders O,
     lineitem L
WHERE C.CUSTKEY = O.CUSTKEY
  AND O.ORDERKEY = L.ORDERKEY
```

#### QX

```sql
SELECT *
FROM nation N,
     supplier S,
     customer C,
     orders O,
     lineitem L
WHERE S.NATIONKEY = N.NATIONKEY
  AND N.NATIONKEY = C.NATIONKEY
  AND C.CUSTKEY = O.CUSTKEY
  AND O.ORDERKEY = L.ORDERKEY
```

#### QY
