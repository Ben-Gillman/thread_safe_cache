from threading import Lock, Semaphore
import time
from typing import Optional


class Cache:
    def __init__(self):
        self._data = dict()
        self._write_lock = Lock()
        self._read_semaphore = Semaphore(value = 3)

    def update(self, key: any, value: any) -> None:
        self._write_lock.acquire()
        print(f"Write lock acquired at {time.strftime('%X')} to update {key},{value}")
        self._data[key] = value

        print(f"Sleeping for 3 seconds")
        time.sleep(3)

        self._write_lock.release()
        print(f"Write lock released at {time.strftime('%X')} for update {key},{value}")

    def read(self, key: any, _=None) -> Optional[any]:
        # _ arg is here for compatability with tests. This is a hack

        print(f"Start read {key} at {time.strftime('%X')}")
        self._read_semaphore.acquire()

        data = self._data.get(key)

        self._read_semaphore.release()
        print(f"End read {key} at {time.strftime('%X')}")
        return data
