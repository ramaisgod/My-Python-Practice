# Snake Water Gun Game in Python
# The snake drinks the water, the gun shoots the snake, and gun has no effect on water.

import random

player_choice_list = {"s": "Snake","w": "Water","g": "Gun"}
computer_choice_list = ["Snake", "Water", "Gun"]
player_win_chance = [["Snake", "Water"], ["Water", "Gun"], ["Gun", "Snake"]]

player_choice_input = []
player_score_board = []
computer_choice_input = []
computer_score_board = []
tie_count = 0
moves = 1
try:
    player_name = input("Enter Your Name : ").upper()
    while(moves<=10):
        print("\n", end="")
        print(f"Round - {moves} : Please choose :")
        for key, value in player_choice_list.items():
            print("Press", key, "for", value,"\n", end="")
        player_input = input()
        player_choice = player_choice_list[player_input.lower()]
        player_choice_input.append(player_choice)
        # print(f"{player_name} have : ", player_choice)
        computer_choice = random.choice(computer_choice_list)
        computer_choice_input.append(computer_choice)
        # print("Computer has : ", computer_choice)
        if player_choice == computer_choice:
            player_score_board.append(0)
            computer_score_board.append(0)
            tie_count = tie_count + 1
            print("You : ", player_choice)
            print("Computer : ", computer_choice)
            print("Result : Game Tie !!!")
        elif [player_choice, computer_choice] in player_win_chance:
            player_score_board.append(100)
            computer_score_board.append(0)
            print("You : ", player_choice)
            print("Computer : ", computer_choice)            
            print("Result : You Won !!!")
        else:
            player_score_board.append(0)
            computer_score_board.append(100)
            print("You : ", player_choice)
            print("Computer : ", computer_choice)            
            print("Result : Computer Won !!!")                
        moves = moves + 1
        continue

    player_total_score = 0
    for score in player_score_board:
        player_total_score = player_total_score + score

    computer_total_score = 0
    for score in computer_score_board:
        computer_total_score = computer_total_score + score
    
    print("\n")
    if player_total_score > computer_total_score:
        print(f"Congratulations... {player_name} are winner !!!\n")
    elif player_total_score < computer_total_score:
        print("Computer are winner !!!\n")
    else:
        print("Game tie !!!\n")

    print(f"{player_name} - Game Summary:\n", end="")
    print("Won :", player_score_board.count(100), "times.", "\n", end="")
    print("Choices :", player_choice_input, "\n", end="")
    print("Score Board :", player_score_board, "\n", end="")
    print("Total Score :", player_total_score,"\n")

    print("Computer - Game Summary:\n", end="")
    print("Won :", computer_score_board.count(100), "times.", "\n", end="")
    print("Choices :", computer_choice_input, "\n", end="")
    print("Score Board :", computer_score_board, "\n", end="")
    print("Total Score :", computer_total_score,"\n")
   
    print("Game tie", tie_count, "times.\n")
except Exception as e:
    print("Wrong Input. Try Again !!!")


