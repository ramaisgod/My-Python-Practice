# Function Caching In Python 
# It is use to save the execution time of program if need to repeat same task . 
# it store some variale in system cache and 
from functools import lru_cache
import time

@lru_cache(maxsize=3)    # maxsize will store latest 3 call in cache memory
def some_task(n):
    # do some stuff here
    time.sleep(n) # here is some work which take lot of time
    return n


if __name__ == "__main__":
    print("Doing some task.")
    some_task(3)
    print("Calling again ... Doing some task.")
    some_task(3)
    print("Calling once again ... Doing some task.")
    
