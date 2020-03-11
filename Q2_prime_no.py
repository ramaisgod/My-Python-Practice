# Print prime numbers between two numbers
# Prime number is whom can divide only with 1 and itself

from_no = 100
to_no = 150

for number in range(from_no, to_no+1):
    if number > 2:
        for i in range(2, number):
            if number % i == 0:
                break
        else:
            print(number)


