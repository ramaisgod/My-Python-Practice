import requests
import pickle

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
iris_pkl_file = "iris_data.pkl"
mydata = requests.get(url)

with open("iris.txt", "w") as f:
    f.writelines(mydata.text)
    
with open("iris.txt") as f:
    iris_contents = f.readlines()

iris_list = []
for line in iris_contents:
    iris_list.append([line.replace("\n","")])

with open(iris_pkl_file, "wb") as file_obj:
    pickle.dump(iris_list, file_obj)

with open(iris_pkl_file, "rb") as file_obj:
    myStr = pickle.load(file_obj)

print("-----Output: iris Data ---------")
for item in myStr:
    print(item, "\n",end="")
print("Number of items is ", len(myStr))
