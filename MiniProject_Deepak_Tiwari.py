
class library:
    def __init__(self, list1, lib_name):
        self.dict1 = {}
        self.lend_book = {}
        no_of_book = 1
        self.index_of_book = 1
        self.lib_name = lib_name
        for item in list1:
            self.dict1.update({self.index_of_book: {"name": item, "no": no_of_book}})
            self.index_of_book = self.index_of_book + 1

    def display(self):
        print(f"Hello your library name is {self.lib_name}")
        print("######################################")
        print("Index","\t","Name","\t","No of Books")
        s_no=1
        for key, value in self.dict1.items():
            print(f"{s_no}     {value['name']}     {value['no']}")
            s_no=s_no+1

        print("######################################")

    def add_book(self):
        book_name = input("Name of the book: ")
        No_book = int(input("No of the book: "))
        count = 0
        for value in self.dict1.values():
            if value["name"] == book_name:
                value["no"] = value["no"] + No_book
                count = 1
                print("Book Added Successfully")
                print("######################################")
        if (count != 1):
            self.dict1.update({self.index_of_book: {"name": book_name, "no": No_book}})
            self.index_of_book = self.index_of_book + 1
            print("Book Added Successfully")
            print("######################################")

    def lend_bookk(self):
        user_name = input("Enter User name: ")
        book_name = input("Which Book you want to take: ")
        count = 0
        for key,value in list(self.dict1.items()):
            if value["name"] == book_name:
                if(value["no"]>1):
                    value["no"] = value["no"] - 1
                else:
                    del self.dict1[key]
                    count = 1
                self.lend_book.update({book_name: user_name})
                print(" Congrat's,,you tooked the book")
                print("######################################")
        if (count != 1):
            print("Book is not in the library")
    def return_book(self):
        u_name = input("Your name: ")
        book_name = input("Enter book name: ")
        count=0
        if self.lend_book[book_name] == u_name:
            count=1
            for value in list(self.dict1.values()):
                if value["name"] == book_name:
                    value["no"] = value["no"] + 1
                    del self.lend_book[book_name]
                    print("Book returned")
                    print("######################################")
                    count=2
        else:
            print("Sorry you have not taken any book so you can't retrieve any one")
            print("######################################")
        if(count==1):
            self.dict1.update({self.index_of_book: {"name": book_name, "no": 1}})
            self.index_of_book+=1
            del self.lend_book[book_name]
            print("Book returned")
            print("######################################")
    def student_detail(self):
        print("#####student's who have taken book's########")
        for key, value in self.lend_book.items():
            print(f"[book name:{key} student name:{value}]")
        print("######################################")

if __name__ == '__main__':
    try:
        dt = library(["python", "c++", "java"], "CodeWithHarry")
        while (1):
            user_choice = input("1.For Display All Book\n2.For lending book\n3.For Add the book\n4.For return the book\n5.Student who tooked book: ")
            if user_choice == '1':
                dt.display()
            elif user_choice == '2':
                dt.lend_bookk()
            elif user_choice == '3':
                dt.add_book()
            elif user_choice == '4':
                dt.return_book()
            elif user_choice == '5':
                dt.student_detail()
            else:
                print('Wrong Input')
    except:
        print("Something Went Wrong")
