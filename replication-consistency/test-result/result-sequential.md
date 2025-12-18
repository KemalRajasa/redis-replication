# Sequential Test Result:

```python
TOTAL_KEYS = 5000   
VALUE_SIZE = 51200
```

## Run 1:

```bash
menulis data
Selesai menulis 5000 keys dalam 1.3339 detik.
membaca replica

----------------------------------------
HASIL AKHIR
Replica Port 6380 : 4708/5000 (94.2%) -> LAGGING
Replica Port 6381 : 4709/5000 (94.2%) -> LAGGING

Terjadi Replication Lag pada salah satu node
```

## Run 2:

```bash
menulis data
Selesai menulis 5000 keys dalam 1.3652 detik.
membaca replica

----------------------------------------
HASIL AKHIR
Replica Port 6380 : 4793/5000 (95.9%) -> LAGGING
Replica Port 6381 : 4793/5000 (95.9%) -> LAGGING

Terjadi Replication Lag pada salah satu node
```

## Run 3:

```bash
menulis data
Selesai menulis 5000 keys dalam 1.3648 detik.
membaca replica

----------------------------------------
HASIL AKHIR
Replica Port 6380 : 4735/5000 (94.7%) -> LAGGING
Replica Port 6381 : 4736/5000 (94.7%) -> LAGGING

Terjadi Replication Lag pada salah satu node

```

## Run 4:

```bash
menulis data
Selesai menulis 5000 keys dalam 1.3761 detik.
membaca replica

----------------------------------------
HASIL AKHIR
Replica Port 6380 : 4704/5000 (94.1%) -> LAGGING
Replica Port 6381 : 4704/5000 (94.1%) -> LAGGING

Terjadi Replication Lag pada salah satu node
```

## Run 5:

```bash
menulis data
Selesai menulis 5000 keys dalam 1.3653 detik.
membaca replica

----------------------------------------
HASIL AKHIR
Replica Port 6380 : 4795/5000 (95.9%) -> LAGGING
Replica Port 6381 : 4796/5000 (95.9%) -> LAGGING

Terjadi Replication Lag pada salah satu node
```


