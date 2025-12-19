#!/bin/bash

echo "Populating 10,000 keys (Cluster Mode)..."
echo "This might take 1-2 minutes..."

# Menggunakan loop di dalam container untuk memanggil redis-cli -c (Cluster Mode)
# Mode -c akan otomatis menangani redirect (MOVED errors) ke node yang benar.

docker exec -it redis-node-1 /bin/sh -c '
  i=0
  while [ "$i" -le 10000 ]; do
    # -c enables cluster following (handling redirects)
    redis-cli -c set key$i value$i > /dev/null
    
    # Progress indicator every 1000 keys
    if [ $((i % 1000)) -eq 0 ]; then
      echo "Inserted $i keys..."
    fi
    
    i=$((i + 1))
  done
'

echo "Data population complete!"
