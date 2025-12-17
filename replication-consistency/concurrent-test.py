import redis
import time
import threading
import random
import string

MASTER_HOST = 'localhost'
MASTER_PORT = 6379
REPLICA_HOST = 'localhost'
REPLICA_PORT = 6380

TOTAL_KEYS = 5000   
VALUE_SIZE = 51200

# Variable Global (Shared Memory)
latest_key_index = -1
stop_event = threading.Event()
lag_counter = 0
total_reads = 0

def generate_value(size):
    return ''.join(random.choices(string.ascii_letters, k=size))

def writer_job():
    global latest_key_index
    print("[WRITER] start write")
    
    r = redis.Redis(host=MASTER_HOST, port=MASTER_PORT, decode_responses=True)
    payload = generate_value(VALUE_SIZE)
    
    #key dikirim dengan batch, 100 key per batch
    pipe = r.pipeline()
    batch_size = 100
    
    for i in range(TOTAL_KEYS):
        pipe.set(f"key:{i}", payload)
        
        if (i + 1) % batch_size == 0:
            pipe.execute()
            latest_key_index = i
            time.sleep(0.01) 
            
    print("[WRITER] done write")
    stop_event.set()

def reader_job():
    global lag_counter, total_reads
    print("[READER] start read")
    
    r = redis.Redis(host=REPLICA_HOST, port=REPLICA_PORT, decode_responses=True)
    
    while not stop_event.is_set():
        target_index = latest_key_index
        if target_index == -1:
            continue 
        
        key = f"key:{target_index}"
        val = r.get(key)
        total_reads += 1

        #cek data, print jika data tidak ditemukan (lag)
        if val is None:
            lag_counter += 1
            print(f"lag: {key} belum sampai di replica")
        
        time.sleep(0.005)

if __name__ == "__main__":
    master = redis.Redis(host=MASTER_HOST, port=MASTER_PORT)
    master.flushall()
    print("DB Bersih.")

    #buat 2 thread (Pekerja)
    t_writer = threading.Thread(target=writer_job)
    t_reader = threading.Thread(target=reader_job)

    #jalankan serentak
    t_writer.start()
    t_reader.start()

    #tunggu sampai writer selesai
    t_writer.join()
    t_reader.join()

    
    print("\nHASIL CONCURRENT TEST")
    print(f"Total Sampel Cek : {total_reads}")
    print(f"Total Lag (Miss) : {lag_counter}")
    
    if total_reads > 0:
        rate = (lag_counter / total_reads) * 100
        print(f"Stale Read Rate : {rate:.2f}%")