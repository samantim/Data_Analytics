import time
import sys
from io import StringIO

class Logger:
    logged : str 
    def __init__(self):
        self.logged = ""
        self.current_time = time.time()

    def log(self, msg : str):
        self.logged += str(msg) + "\n"

    def save_file(self, file_path : str):
        with open(file_path, "w") as file:
            file.write(self.logged)


def show_elapsed_time(original_func):
    # decorator function to define start and end of function and print elapsed time
    def wrapper_function(*args, **kwargs):
        print(f"\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>function {original_func.__name__} started\n")
        current_time = time.time()
        result = original_func(*args, **kwargs)
        elapsedtime = int(time.time() - current_time)
        print(f"\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>function {original_func.__name__} ended ==> Elapsed time: {elapsedtime} seconds\n")
        if result is not None: 
            return result

    return wrapper_function