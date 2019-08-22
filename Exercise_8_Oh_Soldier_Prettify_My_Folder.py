# Oh Soldier Prettify My Folder
# Path, Dictionary File, Format
import os

def soldier(path, file, format):
    os.chdir(path)
    i = 1
    files = os.listdir(path)    
    with open(file) as f:
        file_list = f.read().split("\n")
    
    for file in files:
        if file not in file_list:
            os.rename(file, file.capitalize())
        if os.path.splitext(file)[1] == format:
            os.rename(file, f"{i}.{format}")
            i += 1

soldier(r"D:\Python Practice\CODE_WITH_HARRY\Python\Testing",
r"D:\Python Practice\CODE_WITH_HARRY\Python\Ex_8.txt", "txt")



