# Challenge Answer on the topic Coroutines In Python

file_name_list = ["letter_1.txt","letter_2.txt","letter_3.txt","letter_4.txt","letter_5.txt",
                "letter_6.txt","letter_7.txt","letter_8.txt","letter_9.txt","letter_10.txt"]

try:
    def searchtext():
        mydict = {}
        for item in file_name_list:
            mywords = ""
            with open(item) as file:
                contents = file.readlines()
                for words in contents:
                    mywords = mywords + " " + words.replace("\n", "").lower()
                mydict.update({item:mywords})

        while True:
            text = (yield)
            for key, value in mydict.items():
                if text in value:
                    print("Found in File: ", key)
                    break
            else:
                print("Not Found")

    search = searchtext()
    next(search)
    print("Search Started...")
    keyword = ""
    while keyword is not 'exit':
        keyword = input("Enter Keywords [Type exit to Quit] : ").lower()
        if keyword == 'exit':
            print("Thank you !!!")
            break
        else:    
            search.send(keyword)
    search.close()

except FileNotFoundError as e:
    print("File Not Found !!!")
except Exception as e:
    print("Something wrong. !!! Please Check...")
