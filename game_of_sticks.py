"""
game_of_sticks

Implementation of the Game of Sticks, including an AI that learns the game,
either by playing against a human, or by pre-training against another AI.

The pre-trained AI will remember its winning moves so that it can make the ideal move
at all stages in the game.

Authors:
Nathan Van Kempen - nvankempen@sandiego.edu
"""

import random


def get_player_selection(player_number, sticks_left):
    """
    Parameters:
    player_number (type: int): Either 1 or 2.  Represents Player 1 or Player 2.
    sticks_left (type: int): The number of sticks remaining


    Gets the player's choice for the number of sticks they want to take for their turn.


    Returns: 
    move (type: int): The number of sticks the player chooses to take. 
    """
    valid_input = False 
    while not valid_input:
       if sticks_left < 3:
           question = "Player " + str(player_number) + ": How many sticks do you want to take (1-" + str(sticks_left) + ")?"
           move = input(question)
       else:
            question = "Player " + str(player_number) + ": How many sticks do you want to take (1-3)? "
            move = input(question)

       while move.isdigit() == False:
           print("You must enter a numerical value. Please try again.")
           if sticks_left < 3:
                question = "Player " + str(player_number) + ": How many sticks do you want to take (1-" + str(sticks_left) + ")?"
                move = input(question)
           else:
                question = "Player " + str(player_number) + ": How many sticks do you want to take (1-3)? "
                move = input(question)
           
       move = int(move)
       if move < 1 or move > 3 or move > sticks_left:
            valid_input = False
            if sticks_left < 3:
                print("Please enter a number between 1 and ", sticks_left)
            else: 
                print("Please enter a number between 1 and 3")
       else:
            valid_input = True
    return move

           

def player_vs_player(num_sticks):
    """
    Parameter:
    num_sticks (type: int): The initial number of sticks.


    Allows two players to play against each other.  Once the game is over, players have a chance to rematch.

    """
    initial = num_sticks
    player_number = 1 
    while num_sticks != 0:
        player_move = get_player_selection(player_number, num_sticks)
        print("Player ",player_number," takes ",player_move," sticks.")
        num_sticks -= player_move
        print("There are", num_sticks , " sticks on the board\n")
        if num_sticks != 0:
            if player_number == 1:
                player_number = 2
            else:
                player_number = 1
    print("\nPlayer " + str(player_number) + ", you lose!")

    valid_input = False
    while not valid_input:
        play_again = "\nDo you want to play again? Yes/No\n"
        play_again += "1: Yes\n"
        play_again += "2: No\n"
        yes_or_no = input(play_again)
        if yes_or_no == "1" or yes_or_no.lower() == "yes":
            player_vs_player(initial)
            valid_input = True
        elif yes_or_no == "2" or yes_or_no.lower() == "no":
            print("Thanks for playing!")
            valid_input = True
        else:
            valid_input = False
    
def initialize_hats(num_sticks):

    """
    Parameter:
    num_sticks (type: int): The initial number of sticks.


    Initializes the hat_contents dictionary.  Each hat number represents the number of sticks left and the hat contents represent the choices that the AI can make.
        e.g. Hat 1 will only contain a '1' ball since it can only take 1 stick.
    

    Returns:
    hat_contents (type: dictionary): A dictionary containing hat numbers and its contents (balls)


    """
    hat_contents = {}
    for n in range(1, num_sticks + 1):      #creates a dictionary of hats     
        if n == 1:
            hat_contents[n] = [1]
        elif n == 2:
            hat_contents[n] = [1,2]
        else:
            hat_contents[n] = [1,2,3]
    return hat_contents

def get_ai_selection(num_sticks, hat_contents, hat_besides):

    """
    Parameters:
    num_sticks (type: int): The number of sticks remaining
    hat_contents (type: dictionary): The dictionary containing hat numbers (number of sticks remaining) and their contents (balls/possible moves)
    hat_besides (type: dictionary): The dictionary containing the moves that the AI makes.  When they make a move, the AI will pull a 'ball' out of
                                    the hat (hat_contents) and place the 'ball besides the hat.'


    Gets the AI's move for their turn by randomly picking a 'ball' out of the hat for the number of sticks remaining.  Places each ball
    'besides the hat' and adds it to the hat_besides dictionary.


    Returns:
    choice (type: int): The number of sticks that the AI randomly chooses to take for their turn.

    """
    choice = random.choice(hat_contents.get(num_sticks))
    hat_contents[num_sticks].remove(choice)
    hat_besides[num_sticks] = choice
    return choice

def update_hats(hat_contents, hat_besides, won):

    """
    Parameters:
    hat_contents (type: dictionary): 
    hat_besides (type: dictionary): 
    won (type: boolean): 

    Updates the hats based on whether the AI won or lost.  If the AI won, two balls are added for each move.
    If the AI lost, balls are only added if 
    Clears the hat_besides dictionary.

    Returns:
    Updated contents of the dictionary based on the whether the AI won or lost


    """
    
    if won == True:
        for hat, ball in hat_besides.items():
            hat_contents[hat].extend([ball, ball])
    else:
        for hat, ball in hat_besides.items():
            if ball not in hat_contents[hat]:
                hat_contents[hat].append(ball)
    
    for hat, ball in hat_besides.copy().items():
        del hat_besides[hat]

def player_vs_ai(num_sticks, training_rounds):


    """
    Parameter:
    num_sticks (type: int): The number of sticks on the board.
    training_rounds (type: int): The amount of rounds the AI will play against another AI in order to train.

    Allows the player to play the 'game of sticks' against an AI.  At the end of the game, the player can choose to play again.

    """
  
    hat_contents = pretrain_ai(num_sticks, training_rounds)
    write_hat_contents(hat_contents, "hat-contents.txt")   
    hat_besides = {}

    initial = num_sticks 
    turn = 1
    valid_input = False


    while num_sticks > 0:
        if num_sticks == initial:
            print("\nThere are ", num_sticks," sticks on the board.")
        if turn == 1:
            player_choice = get_player_selection(1, num_sticks)
            num_sticks -= player_choice
            print("There are ", num_sticks," sticks on the board.\n")
            turn = 2

        elif turn == 2:
            ai_choice = get_ai_selection(num_sticks, hat_contents, hat_besides)
            print("AI takes ",ai_choice," sticks.")
            num_sticks -= ai_choice
            print("There are ", num_sticks," sticks on the board.\n")
            turn = 1
    if turn == 2:
        won = True
        print("The computer wins")       
    else:
        won = False
        print("Player 1 wins")
    update_hats(hat_contents, hat_besides, won)
    
    
    while not valid_input: 
        play_again = "Do you want to play again? Yes/No\n"
        play_again += "1: Yes\n"
        play_again += "2: No\n"
        yes_or_no = input(play_again)
        if yes_or_no == "1" or yes_or_no.lower() == "yes":
            player_vs_ai(initial, training_rounds)
            valid_input = True
        elif yes_or_no == "2" or yes_or_no.lower() == "no":
            print("Thanks for playing!")
            valid_input = True
        else:
            valid_input = False
            

            
        
        

def pretrain_ai(num_sticks, num_rounds):
    """
    Parameters: 
    The number of sticks to start with and the number of rounds to do during training

    Returns:
    Returns the hat contents dictitonary of player 2 which in this case was AI

    """
    initial = num_sticks
    hat_contents_AI_1 = initialize_hats(num_sticks)
    hat_contents_AI_2 = initialize_hats(num_sticks)
    
    hat_besides_AI_1 = {}
    hat_besides_AI_2 = {}
    
    
    for _ in range(num_rounds):
        num_sticks = initial
        turn = 1
        while num_sticks > 0:
            if turn == 1:
                ai_1_choice = int(get_ai_selection(num_sticks, hat_contents_AI_1, hat_besides_AI_1))
                num_sticks -= ai_1_choice
                turn = 2
            else:
                ai_2_choice = int(get_ai_selection(num_sticks, hat_contents_AI_2, hat_besides_AI_2))
                num_sticks -= ai_2_choice
                turn = 1        
        if turn == 2:
            update_hats(hat_contents_AI_2, hat_besides_AI_2, True)
            update_hats(hat_contents_AI_1, hat_besides_AI_1, False) 
        else:
            update_hats(hat_contents_AI_1, hat_besides_AI_1, True)
            update_hats(hat_contents_AI_2, hat_besides_AI_2, False)
        
    return hat_contents_AI_2

def write_hat_contents(hats, filename):
    """
    Parameters:
    Hats and filename. The hats parameter will be the hat contents dictionary. 
    The filename parameter will be the name of the file where you are going to write the contents of the hats

    Returns:
    None
    """
    
    values = hats.values()
    f = open(filename, 'w')
    f.write("Hat number: (1's, 2's, 3's)\n")
    hat = 1
    for balls in values:
        one_count = str(balls.count(1))
        two_count = str(balls.count(2))
        three_count = str(balls.count(3))
        f.write(str(hat) + ": (" + one_count + "," + two_count + "," + three_count + ")\n")
        hat += 1
    f.close()



def main():
    """
    Parameters:
    user input of number of sticks (10-100) and user input of which gamemode they would like to play. 

    Reurns:
    A game based on the selected gamemode by the user.

    """
    print("Welcome to the Game of Sticks!")
    valid_input = False
    while not valid_input: 
        num_sticks = (input("How many sticks are there on the table initially (10-100)? "))
        while num_sticks.isdigit() == False:
            print("You must enter a numerical value. Please try again.")
            num_sticks = (input("How many sticks are there on the table initially (10-100)? "))
        num_sticks = int(num_sticks)
        if num_sticks < 10 or num_sticks > 100:
            print("Please enter a number between 10 and 100: ")
            continue

        prompt_string = "\nWhat gamemode would you like to play?\n"
        prompt_string += "Enter 1 for Player vs. Player.\n"
        prompt_string += "Enter 2 to play against computer.\n"
        prompt_string += "Enter 3 to play against trained computer\n"
        gamemode = input(prompt_string)
        if gamemode == "1":
            valid_input = True
            player_vs_player(num_sticks)
        elif gamemode == "2":
            player_vs_ai(num_sticks, 0)
            valid_input = True
        elif gamemode == "3":
            player_vs_ai(num_sticks, 1000)
            valid_input = True
        else:
            valid_input = False
        




if __name__ == "__main__":
    main()

