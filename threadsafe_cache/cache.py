from threading import Lock
import time

class Cache:
    def __init__(self):
        self._data = dict()
        self._write_lock = Lock()

    def update(self, key: any, value: any) -> None:
        self._write_lock.acquire()
        print(f"Write lock acquired at {time.strftime('%X')} to update {key},{value}")
        self._data[key] = value

        print(f"Sleeping for 3 seconds")
        time.sleep(3)

        self._write_lock.release()
        print(f"Write lock released at {time.strftime('%X')} for update {key},{value}")

    
    def read(self, key: any) -> any:
        print(f"Start read {key} at {time.strftime('%X')}")
        data = self._data[key]
        print(f"End read {key} at {time.strftime('%X')}")
        return data
