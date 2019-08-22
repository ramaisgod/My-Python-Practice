# Os Module 
import os

#print(dir(os)) # print all OS module attributes 

# ---- current working directory (cwd) -----
print(os.getcwd())  
# ---- Change current working directory ----
# os.chdir("D://")
# print(os.getcwd())

# ---- list of all files in cwd --
#print(os.listdir())

# ---- list of all files of any drive --
print(os.listdir("d://"))
print(os.path.splitext("ram.txt")) # split the file and extension return in tuple
print(os.path.splitext("ram.txt")[1])

# --- create folder -----
#os.mkdir("ram")
# --- create folder within folder
#os.makedirs("Ram/Shyam") # this will create two folders, shyam folder inside ram folder

# --- rename files ----
#os.rename("mylog.txt","log.txt")

# ---- get environment variables -------
#print(os.environ.get("Path"))

# ----- join path --------
pth = os.path.join("D://", "/ram.txt") 
print(pth)

# --- check exist path ----
print(os.path.exists("E://ram"))

# --- check file folder ----
# print(os.path.isfile("D:\Python Practice\CODE_WITH_HARRY\Python\log.txt"))
# print(os.path.isdir("D:\Python Practice\CODE_WITH_HARRY\Python"))

# ---
datapath = r"D:\Users\RAM\Desktop\StateName08-02-19_23_09_13\StateName08-02-19_23_09_13"

onlyfiles = []
# for item in myfile:
#     if os.path.isdir(os.path.join(datapath,item)):
#         onlyfiles.append(os.listdir(os.path.join(datapath,item)))
# print(onlyfiles)


for path, subdirs, files in os.walk(datapath):   # -- loop in folder subfolders
    for name in files:
        # onlyfiles.append(name)
        onlyfiles.append(os.path.join(path, name))













