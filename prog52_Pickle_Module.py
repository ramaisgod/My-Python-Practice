# Pickle Module 

import pickle

data = ["RMZ", "ASW", "BAV", "VVM", "GTY", "NIS"]

# --- Pickling python object---------
# file = "mydata.pkl"
# file_obj = open(file, "wb")  # open in binary format
# pickle.dump(data, file_obj)
# file_obj.close()

# ---- Read pickle data ------
file = "mydata.pkl"
file_obj = open(file, "rb")
data2 = pickle.load(file_obj)
print(data2)



