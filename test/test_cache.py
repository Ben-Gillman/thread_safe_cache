from concurrent import futures
import os
import sys
import threading
# Add parent dir to path for importing functions to test
sys.path.insert(1, os.path.join(sys.path[0], ".."))

from threadsafe_cache.cache import Cache

def test_cache_update_then_read():
    cache = Cache()
    update_keys = ["test_key1","test_key2","test_key3"]
    update_values = ["test_value1","test_value2","test_value3"]
    u1 = threading.Thread(target=cache.update, args=(update_keys[0], update_values[0]))
    u2 = threading.Thread(target=cache.update, args=(update_keys[1], update_values[1]))
    u3 = threading.Thread(target=cache.update, args=(update_keys[2], update_values[2]))
    r1 = threading.Thread(target=cache.read, args=[update_keys[0]])
    r2 = threading.Thread(target=cache.read, args=[update_keys[0]])

    u1.start()
    u1.join()

    u2.start()
    r1.start()
    r2.start()
    u3.start()

    r1.join()
    r2.join()
    u2.join()
    u3.join()