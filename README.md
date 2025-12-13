# INSTALLATION AND SETUP

```bash
git clone https://github.com/KemalRajasa/redis-replication.git
```

# SKENARIO 1

```bash
cd redis-replication/replication-consistency
docker-compose -f docker-compose.yml up -d
docker ps
```
# SKENARIO 2

```bash
cd redis-replication/failover-sentinel
docker-compose -f docker-compose.yml up -d
docker ps
```
# SKENARIO 3
```bash
cd redis-replication/sharding-cluster
docker-compose -f docker-compose.yml up -d
docker ps
```



