# Concurrent Test Result:

```python
TOTAL_KEYS = 20000   
VALUE_SIZE = 51200
```

## Run 1:

```bash
[WRITER] start write
[READER] start read
lag: key:10699 belum sampai di replica
lag: key:10799 belum sampai di replica
lag: key:17299 belum sampai di replica
lag: key:17299 belum sampai di replica
[WRITER] done write

HASIL CONCURRENT TEST
Total read       : 651
Total Lag (Miss) : 4
Stale Read Rate : 0.61%
```

## Run 2:

```bash
[WRITER] start write
[READER] start read
lag: key:15999 belum sampai di replica
lag: key:15999 belum sampai di replica
[WRITER] done write

HASIL CONCURRENT TEST
Total read       : 624
Total Lag (Miss) : 2
Stale Read Rate : 0.32%
```

## Run 3:

```bash
DB Bersih.
[WRITER] start write
[READER] start read
lag: key:8999 belum sampai di replica
lag: key:13599 belum sampai di replica
lag: key:13599 belum sampai di replica
lag: key:13599 belum sampai di replica
lag: key:13599 belum sampai di replica
lag: key:13599 belum sampai di replica
lag: key:13599 belum sampai di replica
lag: key:13599 belum sampai di replica
lag: key:13699 belum sampai di replica
lag: key:13899 belum sampai di replica
lag: key:13899 belum sampai di replica
lag: key:13899 belum sampai di replica
lag: key:13899 belum sampai di replica
lag: key:13899 belum sampai di replica
lag: key:13899 belum sampai di replica
lag: key:13999 belum sampai di replica
lag: key:14199 belum sampai di replica
lag: key:14199 belum sampai di replica
lag: key:14199 belum sampai di replica
lag: key:14199 belum sampai di replica
lag: key:14199 belum sampai di replica
lag: key:14199 belum sampai di replica
lag: key:14299 belum sampai di replica
lag: key:14599 belum sampai di replica
lag: key:14599 belum sampai di replica
lag: key:14599 belum sampai di replica
lag: key:14599 belum sampai di replica
lag: key:14599 belum sampai di replica
lag: key:14599 belum sampai di replica
lag: key:14699 belum sampai di replica
lag: key:15199 belum sampai di replica
lag: key:15199 belum sampai di replica
lag: key:15199 belum sampai di replica
lag: key:15199 belum sampai di replica
lag: key:15199 belum sampai di replica
lag: key:15199 belum sampai di replica
lag: key:15299 belum sampai di replica
lag: key:15899 belum sampai di replica
lag: key:15899 belum sampai di replica
lag: key:15899 belum sampai di replica
lag: key:15899 belum sampai di replica
lag: key:15899 belum sampai di replica
lag: key:15899 belum sampai di replica
lag: key:15999 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
[WRITER] done write

HASIL CONCURRENT TEST
Total read       : 645
Total Lag (Miss) : 46
Stale Read Rate : 7.13%
```

## Run 4:

```bash
[WRITER] start write
[READER] start read
lag: key:16899 belum sampai di replica
lag: key:16899 belum sampai di replica
lag: key:16899 belum sampai di replica
lag: key:16899 belum sampai di replica
lag: key:16899 belum sampai di replica
lag: key:16899 belum sampai di replica
lag: key:16999 belum sampai di replica
lag: key:16999 belum sampai di replica
lag: key:17199 belum sampai di replica
lag: key:17199 belum sampai di replica
lag: key:17199 belum sampai di replica
lag: key:17199 belum sampai di replica
lag: key:17199 belum sampai di replica
lag: key:17499 belum sampai di replica
lag: key:17499 belum sampai di replica
lag: key:17499 belum sampai di replica
lag: key:17499 belum sampai di replica
lag: key:17499 belum sampai di replica
lag: key:17499 belum sampai di replica
lag: key:17599 belum sampai di replica
lag: key:17899 belum sampai di replica
lag: key:17899 belum sampai di replica
lag: key:17899 belum sampai di replica
lag: key:17899 belum sampai di replica
lag: key:17899 belum sampai di replica
lag: key:17899 belum sampai di replica
lag: key:17899 belum sampai di replica
lag: key:17899 belum sampai di replica
lag: key:17899 belum sampai di replica
lag: key:18399 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19199 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19799 belum sampai di replica
lag: key:19899 belum sampai di replica
[WRITER] done write

HASIL CONCURRENT TEST
Total read       : 670
Total Lag (Miss) : 65
Stale Read Rate : 9.70%
```

## Run 5:

```bash
[WRITER] start write
[READER] start read
lag: key:6299 belum sampai di replica
lag: key:17099 belum sampai di replica
lag: key:17099 belum sampai di replica
[WRITER] done write

HASIL CONCURRENT TEST
Total read       : 644
Total Lag (Miss) : 3
Stale Read Rate : 0.47%
```
