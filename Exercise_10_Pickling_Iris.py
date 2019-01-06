import requests
import pickle

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
iris_pkl_file = "iris_data.pkl"

def fetch_data(url):
    mydata = requests.get(url)
    with open("iris_data.txt", "w") as f:
        f.writelines(mydata.text) 
    with open("iris_data.txt") as f:
        iris_contents = f.readlines()
    return iris_contents

iris_list = []
for line in fetch_data(url):
    iris_list.append([line.replace("\n","")])

with open(iris_pkl_file, "wb") as file_obj:
    pickle.dump(iris_list, file_obj)

with open(iris_pkl_file, "rb") as file_obj:
    myStr = pickle.load(file_obj)

print("-----Output: iris Data ---------")
for item in myStr:
    print(item, "\n",end="")
print("Number of items is ", len(myStr))
