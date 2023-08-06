import os
import shutil
import json
import requests
import shelve
import time
import queue
import random
import string
from typing import Optional, Text

def generate_rand_name() -> str:
    """Generate a random name of the form "export_XXXXXX" where XXXXXX are
    6 random characters.

    Returns:
        str: the generated name
    """
    suf = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"exporters_{suf}"

def is_able_to_connect(url: Optional[Text] = None) -> bool:
    """Runs a HTTP GET request to the url.

    Args:
        url (str): an URL (with its schema)

    Returns:
        bool: if a ConnectionError or Timeout are raised, returns `False`.
            `True`, otherwise.
    """
    if url is None:
        url = "https://www.google.com"
    try:
    	request = requests.get(url, timeout=.5)
    	return True
    except (requests.ConnectionError, requests.Timeout):
    	return False

class _DataStore:
    __instantiated = 0
    __used_filenames = []

    def __new__(cls, *args, **kwargs):
        if "shelf_filename" in kwargs.keys():
            if kwargs["shelf_filename"] in cls.__used_filenames:
                raise ValueError(
                        f"File {kwargs['db_filename']} is already being used.")
        return super(_DataStore, cls).__new__(cls)

    def __init__(self,
                 use_memory: bool = True,
                 shelf_filename: Optional[Text] = None,
                 max_size: int = 100 * 100 * 100,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__use_memory = use_memory

        self.__filename = generate_rand_name() if shelf_filename is None \
                                               else shelf_filename
        self.__used_filenames.append(self.__filename)

        self.__size = 0
        self.max_size = max_size

        self.__queue = queue.Queue() if use_memory else None
        self.__shelf = None if use_memory else shelve.open(self.__filename)

    @property
    def size(self):
        return self.__size

    @property
    def use_memory(self) -> bool:
        return self.__use_memory

    @use_memory.setter
    def use_memory(self, new_val: bool) -> bool:
        if self.__use_memory and new_val == False:
            self.export_queue_to_file()
            self.__use_memory = new_val
            self.__queue = None
        elif self.__use_memory == False and new_val:
            self.__queue = self.import_queue_from_file()
            self.__use_memory = new_val
            self.__shelf.close()
            self.__shelf = None
        else:
            print(f"WARNING - use_memory is already set to {new_val}")
        return new_val

    def put(self, data):
        if self.size >= self.max_size:
            print("Cannot save more data.")
            return None
        if self.use_memory:
            self.__put_in_memory(data)
        else:
            self.__put_in_shelf(data)
        self.__size += 1

    def __put_in_memory(self, data):
        self.__queue.put(data)

    def __put_in_shelf(self, data):
        self.__shelf[str(time.time())] = data

    def get(self):
        if self.size <= 0:
            raise Exception("No saved data left.")
        if self.use_memory:
            data = self.__get_from_memory()
        else:
            data = self.__get_from_shelf()
        self.__size -=1
        return data

    def __get_from_memory(self):
        return self.__queue.get()

    def __get_from_shelf(self):
        generator = iter(self.__shelf.keys())
        try:
            key = next(generator)
        except StopIteration:
            return None
        else:
            res = self.__shelf[key].copy()
            del self.__shelf[key]
            return res

    def export_queue_to_shelf(self):
        self.__shelf = shelve.open(self.__filename, "n")
        while not self.__queue.empty():
            data = self.__queue.get()
            self.__shelf[str(time.time())] = data

    def import_queue_from_file(self):
        q = queue.Queue()
        generator = iter(self.__shelf.keys())
        for key in generator:
            q.put(file[key])
        return q

    def __len__(self):
        return self.size

    def __iter__(self):
        return self

    def __next__(self):
        if self.size:
            return self.get()
        raise StopIteration

    def __del__(self):
        if self.__shelf:
            self.__shelf.close()
