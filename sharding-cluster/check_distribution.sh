#!/bin/bash

echo "Checking Key Distribution across nodes..."
echo "----------------------------------------"
echo -e "Node\t\tIP\t\tRole\t\tKeys"
echo "----------------------------------------"

for i in {1..6}; do
  IP="173.18.0.1$i"
  NODE="redis-node-$i"
  
  # Ambil Role (master/slave)
  ROLE=$(docker exec $NODE redis-cli -h $IP role | head -n 1)
  
  # Ambil jumlah Keys (DBSIZE)
  KEYS=$(docker exec $NODE redis-cli -h $IP dbsize)
  
  echo -e "$NODE\t$IP\t$ROLE\t\t$KEYS"
done

echo "----------------------------------------"
echo "Total Keys should be around 10,000 (replicas replicate masters)"
