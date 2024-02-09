import concurrent.futures
import os
from random import randrange
import sys
import threading

# Add parent dir to path for importing functions to test
sys.path.insert(1, os.path.join(sys.path[0], ".."))

from threadsafe_cache.cache import Cache


def test_cache_update_then_read():
    cache = Cache()
    update_keys = ["test_key1", "test_key2", "test_key3"]
    update_values = ["test_value1", "test_value2", "test_value3"]
    u1 = threading.Thread(target=cache.update, args=(update_keys[0], update_values[0]))
    u2 = threading.Thread(target=cache.update, args=(update_keys[1], update_values[1]))
    u3 = threading.Thread(target=cache.update, args=(update_keys[2], update_values[2]))
    r1 = threading.Thread(target=cache.read, args=[update_keys[0]])
    r2 = threading.Thread(target=cache.read, args=[update_keys[0]])

    print("Starting: Simple write operation with lock")
    u1.start()
    u1.join()

    print("Starting: Write and read while lock is held by read")
    u2.start()
    r1.start()
    r2.start()
    u3.start()

    r1.join()
    r2.join()
    u2.join()
    u3.join()


def test_cache_many_calls():
    KEY = "test_key_"
    VAL = "test_value_"
    NUM_CALLS = 5
    cache = Cache()
    calls = []
    for n in range(NUM_CALLS):
        calls.append([cache.update, KEY + str(n), VAL + str(n)])
        calls.append([cache.read, KEY + str(randrange(NUM_CALLS)), ""])

    calls.append([cache.read, KEY + "0", ""])

    with concurrent.futures.ThreadPoolExecutor() as ex:
        futures = {
            ex.submit(call[0], call[1], call[2]): str(call[1] + " " + call[2])
            for call in calls
        }

        for future in concurrent.futures.as_completed(futures, timeout=30):
            key = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                print(f"{key} generated an exception: {exc}")
            else:
                print(f"result for {key} is: {result}")

    print(f"Finally: reading from cache. {cache.read(KEY+'0')}")
