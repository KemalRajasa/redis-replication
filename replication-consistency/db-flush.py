import redis
import sys
import time

MASTER_HOST = 'localhost'
MASTER_PORT = 6379

REPLICA_HOST = 'localhost'
REPLICA_PORTS = [6380, 6381] # List Port Replica

def clean_database():

    # Koneksi ke Master
    try:
        master = redis.Redis(host=MASTER_HOST, port=MASTER_PORT, decode_responses=True)
        master.ping()
    except redis.ConnectionError:
        print(f"Error: Tidak bisa connect ke Master {MASTER_PORT}")
        sys.exit(1)

    # Setup Koneksi Replica
    replica_conns = []
    for port in REPLICA_PORTS:
        try:
            r = redis.Redis(host=REPLICA_HOST, port=port, decode_responses=True)
            r.ping()
            replica_conns.append({'port': port, 'conn': r})
        except redis.ConnectionError:
            print(f"Replica {port} tidak terjangkau")

    prev_count = master.dbsize()
    print(f"Data sebelum hapus: {prev_count} keys")
    
    master.flushall()
    time.sleep(0.5) 

    print("\nVerifikasi Status Kebersihan:")
    
    # Cek Master
    curr_master = master.dbsize()
    print(f"Master ({MASTER_PORT})  : {curr_master} keys")

    # Cek Semua Replica
    for item in replica_conns:
        port = item['port']
        r = item['conn']
        count = r.dbsize()
        
        status = "BERSIH" if count == 0 else "MASIH ADA DATA"
        print(f"Replica ({port}) : {count} keys [{status}]")

    print("-" * 40)

if __name__ == "__main__":
    clean_database()