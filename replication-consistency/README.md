# Replication Consistency Test

## Script

`docker-compose.yml` : docker compose file for redis cluster

`concurrent-test.py` : concurrent test script

`sequential-test.py` : sequential test script

## How to run

```bash
python3 concurrent-test.py
python3 sequential-test.py
```

## Result

`test-result` : folder contains the result of the test