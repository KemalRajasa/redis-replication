#!/bin/bash

# Tunggu sebentar untuk memastikan semua container siap
echo "Waiting for Redis nodes to start..."
sleep 5

echo "Initializing Redis Cluster..."
# Menggunakan redis-cli dari dalam container redis-node-1
# Kita menggunakan IP internal docker yang sudah didefinisikan di docker-compose
docker exec -it redis-node-1 redis-cli --cluster create \
  173.18.0.11:6379 \
  173.18.0.12:6379 \
  173.18.0.13:6379 \
  173.18.0.14:6379 \
  173.18.0.15:6379 \
  173.18.0.16:6379 \
  --cluster-replicas 1 --cluster-yes

echo "Cluster Initialization Complete!"
