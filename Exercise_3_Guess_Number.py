# Exercise-3 
n = 18
g = 0
while(g<=9):
    g = g + 1
    if g > 9:
        print("Game Over !!!.")
        break
    else:   
        print("Guess and Enter Any Number : ")
        num = int(input())
        if num == n:
            print("Congratulations !!! You won the game.")
            print("You have taken total ", 9 - g, " guesses.")
            break         
        elif num >= 100:
            print("Your number is too much greater than my Number. Please try bellow 100")
            print("Number of guesses left = ", 9 - g)
        elif num >=10 and num <=20:
            print("Your are near to my Number.")
            print("Number of guesses left = ", 9 - g)
        elif num > n and num < 100:
            print("Your number is greater than my Number.")
            print("Number of guesses left = ", 9 - g)
        elif num < n:
            print("Your number is less than my Number.")
            print("Number of guesses left = ", 9 - g)           
    continue 
