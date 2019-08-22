# --- Coroutines In Python ------ 
# It is used when function take too much time to initialize

def searcher():
    import time
    # some work which takes too much time
    time.sleep(3) 
    names = ["AWJ", "ASW", "RMZ", "VVM", "PBI", "SWO", "GTY", "NIS", "SII", "BAV", "DEE"]

    while True:
        text = (yield)
        if text in names:
            print("Found !!!")
        else:
            print("Not Found !!!")

search = searcher()
print("Search Started...")
next(search) # start searching
search.send("RMZ")
input("Press any key...")
search.send("awj")
input("Press any key...")
search.send("VVM")
search.close() # stop coroutines 




