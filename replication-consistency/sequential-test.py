import redis
import time
import random
import string

MASTER_HOST = 'localhost'
MASTER_PORT = 6379
REPLICA_HOST = 'localhost'
REPLICA_PORTS = [6380, 6381] 

TOTAL_KEYS = 5000  
VALUE_SIZE = 51200 # dalam bytes   

def generate_value(size):
    return ''.join(random.choices(string.ascii_letters, k=size))

def run_experiment():
    print("menulis data")
    try:
        #master
        master = redis.Redis(host=MASTER_HOST, port=MASTER_PORT, decode_responses=True)

        #replicas
        replica_conns = []
        for port in REPLICA_PORTS:
            r = redis.Redis(host=REPLICA_HOST, port=port, decode_responses=True)
            replica_conns.append({'port': port, 'conn': r})

    except redis.ConnectionError as e:
        print(f"Gagal connect ke Redis: {e}")
        return

    master.flushall()

    # Generate Payload & Set
    payload = generate_value(VALUE_SIZE)
    start_write = time.time()

    pipe = master.pipeline()
    for i in range(TOTAL_KEYS):
        # pattern adalah "key: <number>"
        pipe.set(f"key:{i}", payload)
    pipe.execute()
    
    write_duration = time.time() - start_write
    print(f"Selesai menulis {TOTAL_KEYS} keys dalam {write_duration:.4f} detik.")

    #segera setelah operasi write ke master selesai, operasi read replication dimulai
    print(f"membaca replica")

    # Dictionary untuk menyimpan skor tiap replica
    # Format: {6380: 0, 6381: 0}
    missed_counts = {port: 0 for port in REPLICA_PORTS}
    
    #loop cek data
    for i in range(TOTAL_KEYS):
        key = f"key:{i}"
        for item in replica_conns:
            port = item['port']
            r_conn = item['conn']
            
            #coba ambil data
            val = r_conn.get(key)
            if not val:
                missed_counts[port] += 1
            
    print("\n" + "-"*40)
    print("HASIL AKHIR")
    
    for port in REPLICA_PORTS:
        missed = missed_counts[port]
        success = TOTAL_KEYS - missed
        rate = (success / TOTAL_KEYS) * 100
        
        status = "SYNCED" if missed == 0 else "LAGGING"
        
        print(f"Replica Port {port} : {success}/{TOTAL_KEYS} ({rate:.1f}%) -> {status}")

    total_missed = sum(missed_counts.values())
    if total_missed == 0:
        print("\nno lag, consistent")
    else:
        print("\nTerjadi Replication Lag pada salah satu node")

if __name__ == "__main__":
    run_experiment()