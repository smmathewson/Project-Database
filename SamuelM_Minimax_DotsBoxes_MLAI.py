"""
Dots and Boxes: How does the additional turn mechanic influence game strategy?
##############################################################################
Implementation
Minimax Algorithm with alpha beta pruning
Three unique evaluate functions represent different styles of play

Evaluate Function 1.The snatch_evaluate function adds value to a board when there is a box that can be won.
Other qualifications of the state are ignored.Therefore, this evaluation function is prioritizing finishing boxes.

Evaluate Function 2. The action_evaluate function also is interested in fishing boxes,
but also weighs the number of present moves at each box.
Boxes with 2 lines decreases the state value as adding to them would allow the other player to finish a box.
Boxes with 3 or 4 moves present the function values as safe moves (given more weight).
However, the function values boxes with only one move present the greatest.

Evaluate Function 3. The set_up_evaluate function takes a different approach by favoring boxes
with fewer moves present in order to build up a bord with many boxes to finish.
################################################################################
How is the game played?
Dots and Boxes is a two player game that utilizes a grid board.
The grid is broken up into boxes that can be collected by either player.
Players compete by adding a line to a box in the hopes of eventually completing it.
When a player completes a box they are granted an additional turn.
Once a move is completed it can not be altered.

Two versions of the game are created.
Version 1 - Contains additional turn when box is completed
Version 2 - Does not contain said rule

For either version the player with the most boxes at the end of the game wins.


Game State Representation
The game is represented within a list. Each index symbolizes either a potential move,
a vertex, or an empty gap within the box.

The first, 3rd, 5th, etc. rows contains points * and possible moves are denoted as ?.
When moves are completed they are displayed as either - or |.

The 2nd, 4th, 6th, etc. rows contains a vertical connection denoted as ? and then an empty space and then of course
another vertical connection until we reach the last connection for the row. When printing out no ? are printed as and
empty space looks cleaner/how the game is commonly viewed.

Ex.
1. * ? * ? *                             * - * - *
2. ?   ?   ?    when game is completed   |   |   |
3. * ? * ? *                             * - * - *



"""

"""
INITIAL GAME STATE CREATION
    
    Creates list representation of a game state
    ? symbol filled for all potential actions
    All game states are squares of varying sizes
"""
import math


def make_list_rep(size):

    environment = []
    # every size * 2 index, ex. size * 2 + size * 2 + size * 2 until the
    # end of the point row, so the next row are vertical lines within the box representation
    
    for r in range(0, size * 2 + 1):
        # if the row is even, then we have a star and horizontal connection row
             
        if r % 2 == 0: 
            for c in range(0, size * 2 + 1):
                if c % 2 == 0:  # it's an even space so it's a dot
                    environment.append("*")
                else:
                    # odd index within even row: ?
                    environment.append("?")  # empty spot able to be drawn a line across
        else:
            # odd row so this is vertical and space
            for c in range(0, size * 2 + 1):
                if c % 2 == 0:  # it's an even space so it's a dot
                    environment.append("?")  # possible vertical move, when print, all ? will print as empty strings
                else:
                    environment.append(" ")  # empty space between vertical movements
    
    # return the created initial environment
    return environment


"""
Helper Functions 
"""

# Optimized Action Finder for all individual boxes in game
# Maps a box with their actions indices, actions are placed into sets that can easily be found later


def make_box_mapping(list_rep):
    # Length of row to look through
    line_length = int(math.sqrt(len(list_rep)))
    
    # the number of boxes in the list_representation
    mappin = []
    # once we make mapping, we are able to determine the status of each box to then determine game conditions
    # start = 0

    for start in range(0, len(list_rep) - (2 * line_length), 2 * line_length):
        for index in range(0, line_length - 2, 2):
            new_set = set()
            # Math to grab each action (top left vertex is origin for each box)
            new_set.add(start+index + 1)
            new_set.add(start + line_length + index)
            new_set.add(start + index + 1 + 2 * line_length)
            new_set.add(start + index + line_length + 2)
            mappin.append(new_set)
    return mappin
            

# CHECK IF STATE IS FINAL STATE - no moves remaining
# We will do this by searching the list for any '?', these denote possible moves
def check_final(list_rep):
    for slot in range(0, len(list_rep)):
        if list_rep[slot] == "?":
            return False
    return True


# number_of_actions : determine available number of available actions given a state
def number_of_actions(list_rep):
    actions = 0
    for slot in range(0, len(list_rep)):
        if list_rep[slot] == "?":
            actions+=1
    return actions


# actions_in : returns list the indices of possible available actions
# this returns a list of possible actions given a state
# the list of actions are denoted as action indices that still have '?' on them,
# therefore they are moves that have not been used
def actions_in(list_rep):
    actions = []  # list of indices of possible actions
    for moves in range(0,len(list_rep)):
        if list_rep[moves] == "?":
            actions.append(moves)
    return actions


""" 
    Utility: 
    Subscribes a numerical value that determines the results of a final state (win/loss for who)
    Return None if not final state 
    
 Symbol Key: 
 Possible Move = ?  
 Move completed by a player but has not finished a box = + 
 Max wins box = X
 Max wins two boxes with one move = x 
 Min wins box = O 
 Min wins two boxes with one move = o
"""


def utility(list_rep):
    
    # if returns none, we have not gotten to a final state
    if check_final(list_rep):
        score = 0
        for digits in list_rep:
            if digits == 'x':  # rare case - one move finishes two boxes (mx player)
                score += 2
            elif digits == 'X':
                score += 1
            elif digits == 'o':  # same as line 164 expect for min player
                score -= 2
            elif digits == 'O':
                score -= 1

        # Checking score
        if score > 0:  # if X wins return 1 (adding points)
            return 1
        elif score < 0:  # if Y wins return -1 (subtracting points)
            return -1
        else:
            return 0
    else:  # return none if the state is not final
        return None


"""
Min and Max Successor Functions
Min successor: min player will preform an action from an index on given state and then return the new state
Max successor: max player's version.... same functionality 

Symbol Key: 
 Possible Move = ?  
 Move completed by a player but has not finished a box = + 
 
 Max wins box = X
 Max wins two boxes with one move = x 
 
 Min wins box = O 
 Min wins two boxes with one move = o
 
"""


def min_successor(list_rep,ind_number):
    mapping = make_box_mapping(list_rep)
    boxes = []
    successor = list_rep.copy()

    for set_item in mapping:
        if ind_number in set_item:
            # want index of whatever boxes contain this action
            boxes.append(set_item)
          
    # if the length of boxes is greater than 2, then we know the number we sent it is on both boxes
    # boxes contain the sets we need to check
    # box 1, box 2
    # (box 1 ?'s total, box 2 ?'s' total)

    if len(boxes) > 1:  # then 2 is the only possible size
        check_double_win = tuple()
        box1 = 0
        box2 = 0
        set1 = boxes[0]
        set2 = boxes[1]
        
        for number in set1:
            if list_rep[number] == '?':
                box1 += 1
        for numbers in set2:
            if list_rep[numbers] == '?':
                box2 += 1
                    
        if box1 == 1 and box2 == 1:
            # Then the 1 leftover is this possible move, which would trigger both boxes to be owned by this player
            successor[ind_number] = 'o'
        
            return successor
        elif box1 == 1 and box2 != 1:
            successor[ind_number] = 'O'
          
            return successor
        elif box2 == 1 and box1 != 1:
            successor[ind_number] = 'O'
          
            return successor
        else:
            successor[ind_number] = '+'
            return successor
    
    win_if_one = 0
    only_one = boxes[0]
    for num in only_one:
        if list_rep[num] == '?':
            win_if_one += 1
        
    if win_if_one == 1: # I have to check for one box is this is the winning move
        successor[ind_number] = 'O'
          
        return successor
    else:
        successor[ind_number] = '+'
        return successor


def max_successor(list_rep, ind_number):
    mapping = make_box_mapping(list_rep)
    boxes = []
    successor = list_rep.copy()

    # Get boxes that have this move, indicated by a specefic index in the list representation
    for set_item in mapping:
        if ind_number in set_item:
            # want index of whatever boxes contain this action
            boxes.append(set_item)
        
    # if the length of boxes is greater than 2, then we know the number we sent it is on both boxes
    # boxes contain the sets we need to check
    # box 1, box 2
    # (box 1 ?'s total, box 2 ?'s' total)

    if len(boxes) > 1: # if checkng a move that is part of two boxes
        check_double_win = tuple()
        box1 = 0
        box2 = 0
        set1 = boxes[0]
        set2 = boxes[1]
        
        for number in set1:
            if list_rep[number] == '?':
                box1 += 1
        for numbers in set2:
            if list_rep[numbers] == '?':
                box2 += 1
                    
        if box1 == 1 and box2 == 1:
            # Then the 1 leftover is this possible move, which would trigger both boxes to be owned by this player
            successor[ind_number] = 'x'
            
            return successor
        # if box one is still a box win, then we want to lable it as such
        elif box1 == 1 and box2 != 1:
            successor[ind_number] = 'X'
           
            return successor
        # if box two is still a box win, we want to lable it as X
        elif box2 == 1 and box1 != 1:
            successor[ind_number] = 'X'
          
            return successor
        # if no wins are present, we want to lable it as a standard move
        else:
            successor[ind_number] = '+'
            return successor
    
    # checking a move that is part of only one box
    win_if_one = 0
    only_one = boxes[0]
    for num in only_one:
        if list_rep[num] == '?':
            win_if_one += 1
        
    if win_if_one == 1:  # I have to check for one box is this is the winning move
        successor[ind_number] = 'X'
        return successor
    else:
        successor[ind_number] = '+'
        return successor
                    

""" 
Min and Max successor functions that implement a simple turn again mechanic
 
If given a list that contains an 'A' at the end of the list then the other player has recently won a box
The player receiving the list with A recognizes this and send the game state back to the other player while removing 'A'
"""


def min_successor_A(list_rep, ind_number):
    # THIS MEANS THAT THE OTHER PLAYER WON A BOX AND GETS TO GO AGAIN, MAKE SURE TO REMOVE A
    if list_rep[-1] == 'A':
        successor = list_rep.copy()
        successor.remove('A')
        return successor
    
    
    # if final move in box, then put O to show that O won that box
    mapping = make_box_mapping(list_rep)
    boxes = []
    
    successor = list_rep.copy()

    for set_item in mapping:
        if ind_number in set_item:
            # want index of whatever boxes contain this action
            boxes.append(set_item)
          
    # if the length of boxes is greater than 2, then we know the number we sent it is on both boxes
    # boxes contain the sets we need to check
    # box 1, box 2
    # (box 1 ?'s total, box 2 ?'s' total)

    if len(boxes) > 1:  # then 2 is the only possible size
        box1 = 0
        box2 = 0
        set1 = boxes[0]
        set2 = boxes[1]
        
        for number in set1:
            if list_rep[number] == '?':
                box1 += 1
        for numbers in set2:
            if list_rep[numbers] == '?':
                box2 += 1
                    
        if box1 == 1 and box2 == 1:
            # Then the 1 leftover is this possible move, which would trigger both boxes to be owned by this player
            successor[ind_number] = 'o'
            successor.append("A")
            return successor
        elif box1 == 1 and box2 != 1:
            successor[ind_number] = 'O'
            successor.append("A")
            return successor
        elif box2 == 1 and box1 != 1:
            successor[ind_number] = 'O'
            successor.append("A")
            return successor
        else:
            successor[ind_number] = '+'
            return successor
    
    win_if_one = 0
    only_one = boxes[0]
    for num in only_one:
        if list_rep[num] == '?':
            win_if_one += 1
        
    if win_if_one == 1:  # Box winning move
            successor[ind_number] = 'O'
            successor.append("A")  # addded and eventually deleted from list representation, marker for additional turn
            return successor
    else:
        successor[ind_number] = '+'
        return successor


# This is same as min successor but winning moves are intead denoted as X and x (Big X for single win, little x for double)
def max_successor_A(list_rep, ind_number):
    if list_rep[-1] == 'A':
        successor = list_rep.copy()
        successor.remove('A')
        return successor
    
    mapping = make_box_mapping(list_rep)
    boxes = []
    
    successor = list_rep.copy()
    
    # Get boxes that have this move, indicated by a specefic index in the list representation
    for set_item in mapping:
        if ind_number in set_item:
            # want index of whatever boxes contain this action
            boxes.append(set_item)
        
    # if the length of boxes is greater than 2, then we know the action impacts two boxes
    # boxes contain the sets we need to check
    # box 1, box 2
    # (box 1 ?'s total, box 2 ?'s' total)

    if len(boxes) > 1:  # if checking a move that is part of two boxes
        box1 = 0
        box2 = 0
        set1 = boxes[0]  # this can be hardcoded because it's the only option if len > 1
        set2 = boxes[1]
        
        for number in set1:
            if list_rep[number] == '?':
                box1 += 1
        for numbers in set2:
            if list_rep[numbers] == '?':
                box2 += 1
                    
        if box1 == 1 and box2 == 1:
            # Then the 1 leftover is this possible move, which would trigger both boxes to be owned by this player
            successor[ind_number] = 'x'
            successor.append("A")
            return successor
        #if box one is still a box win, then we want to lable it as such
        elif box1 == 1 and box2 != 1:
            successor[ind_number] = 'X'
            successor.append("A")
            return successor
        #if box two is still a box win, we want to lable it as X
        elif box2 == 1 and box1 != 1:
            successor[ind_number] = 'X'
            successor.append("A")
            return successor
        #if no wins are present, we want to lable it as a standard move
        else:
            successor[ind_number] = '+'
            return successor
    
    #checking a move that is part of only one box 
    win_if_one = 0
    only_one = boxes[0]
    for num in only_one:
        if list_rep[num] == '?':
            win_if_one += 1
        
    if win_if_one == 1: #Box winning move
        successor[ind_number] = 'X'
        successor.append("A") #The A added on to the list representation will get deleted after the additional turn is taken, turn marker
        return successor
    else:
        successor[ind_number] = '+'
        return successor
                    


"""
Evaluate Functions
 
The snatch_evaluate function adds value to a board when there is a box that is able to be completed. 
Other qualifications of the state are ignored.Therefore, this evaluation function is prioritizing finishing boxes. 
 
The action_evaluate function also is interested in fishing boxes, but also weighs the number of moves present at each box.
Boxes with 2 moves present decreases the state value as adding to them would allow the other player to finish a box. 
Boxes with 3 or 4 moves present the function values as safe moves (given more weight). 
However, boxes with only one move present the function values the greatest.
 
The set_up_evaluate function takes a different approach by 
favoring boxes with less moves present in order to build up a bord with many boxes to finish.  
 
Min and Max versions are created for each method for the Min and Max algorithm to execute correctly. 
One player valuing +, another -. 
"""



def calculate_winning_boxes(list_rep):
    #figure out which boxes only have one move left
    mappin = make_box_mapping(list_rep)
    number_of_winning_boxes = 0
    for key in mappin:
        total = 0
        stored_box = mappin[key]
        for move in stored_box:
            if list_rep[move] == '?':
                total += 1
        if total == 1:
            number_of_winning_boxes += 1
    return number_of_winning_boxes
            
#greedy evaluate, only a good state when there is one box able to be won, everything else is eh
def snatch_evaluate_max(list_rep):
    #Mapping for each box
    mappin = make_box_mapping(list_rep)
    size = int(math.sqrt(len(list_rep))) // 2
    boxes = size ** 2
    ratio = (size - .1) / boxes #the ratio to add to each box that you could win
    evaluate = 0
    
    for sets in mappin:
        total = 0
        for move in sets:
            if list_rep[move] == '?':
                total += 1
        if total == 1:
            #do something to the value of the state
            evaluate += ratio
        #always be picking states for when we are able to complete a box
            
    return evaluate
#This will priortize finishing boxes, with less priortization on 3 and 4 boxes, while avoiding states that create that set up 3 boxes for the other player
def action_evaluate_max(list_rep):
    #mapping for each box
    mappin = make_box_mapping(list_rep)
    size = int(math.sqrt(len(list_rep))) // 2
    boxes = size ** 2
    ratio = 1 / (boxes - 0.1) 
    evaluate = 0
    
    for sets in mappin:
        total = 0
        for move in sets:
            if list_rep[move] == '?':
                total += 1
        if total == 1:
            evaluate += ratio
        elif total == 2: # if total 2, then it favors the other player, and so we will rate it lower
            evaluate -= ratio / 2
        elif total == 3 or total == 4: #if there is a total of 3 or 4, then it favors us a safe move 
            evaluate += ratio / 2
    
    #-, value for other player
    #+, value for player that called evaluate 
    return evaluate
            
#This evaluation prioritizes settuping up boxes to be crossed, it prefers placing them o boxes with 3 or 4 moves left, 
#but will finish up boxes before it places on value 2      
def set_up_evaluate_max(list_rep):
    #we want to be able to complete the most number of boxes with a series of box wins
    #lets value 
    mappin = make_box_mapping(list_rep)
    size = int(math.sqrt(len(list_rep))) // 2
    boxes = size ** 2
    ratio = 1 / (boxes - 0.1) #will never total 1 or -1
    evaluate = 0
    
    for sets in mappin:
        total = 0
        for move in sets:
            if list_rep[move] == '?':
                total += 1
        if total == 1:
            evaluate +=ratio / 2
        elif total == 2: # if total 2, then it favors the other player, and so we will rate it lower
            evaluate -= ratio / 2
        elif total == 3 or total == 4: #if there is a total of 3 or 4, then it favors us a safe move 
            evaluate += ratio 
    
    #-, value for other player
    #+, value for player that called evaluate 
    return evaluate


#greedy evaluate, only a good state when there is one box able to be won, everything else is eh
def snatch_evaluate_min(list_rep):
    #Mapping for each box
    mappin = make_box_mapping(list_rep)
    size = int(math.sqrt(len(list_rep))) // 2
    boxes = size ** 2
    ratio = (size - .1) / boxes #the ratio to add to each box that you could win
    evaluate = 0
    
    for sets in mappin:
        total = 0
        for move in sets:
            if list_rep[move] == '?':
                total += 1
        if total == 1:
            evaluate -= ratio
        #always be picking states for when we are able to complete a box
            
    return evaluate

#This will priortize finishing boxes, with less priortization on 3 and 4 boxes,
# while avoiding states that create that set up 3 boxes for the other player
def action_evaluate_min(list_rep):
    #mapping for each box
    mappin = make_box_mapping(list_rep)
    size = int(math.sqrt(len(list_rep))) // 2
    boxes = size ** 2
    ratio = 1 / (boxes - 0.1) #will never total 1 or -1
    evaluate = 0
    
    for sets in mappin:
        total = 0
        for move in sets:
            if list_rep[move] == '?':
                total += 1
        if total == 1:
            evaluate -= ratio
        elif total == 2: # if total 2, then it favors the other player, and so we will rate it lower
            evaluate += ratio / 2
        elif total == 3 or total == 4: #if there is a total of 3 or 4, then it favors us a safe move 
            evaluate -= ratio / 2
    
    #-, value for other player
    #+, value for player that called evaluate 
    return evaluate
            
#This evaluation prioritizes settuping up boxes to be crossed, it prefers placing them o boxes with 3 or 4 moves left, 
#but will finish up boxes before it places on value 2      

def set_up_evaluate_min(list_rep):
    #we want to be able to complete the most number of boxes with a series of box wins
    #lets value 
    mappin = make_box_mapping(list_rep)
    size = int(math.sqrt(len(list_rep))) // 2
    boxes = size ** 2
    ratio = 1 / (boxes - 0.1) #will never total 1 or -1
    evaluate = 0
    
    for sets in mappin:
        total = 0
        for move in sets:
            if list_rep[move] == '?':
                total += 1
        if total == 1:
            evaluate -= ratio / 2
        elif total == 2: # if total 2, then it favors the other player, and so we will rate it lower
            evaluate += ratio / 2
        elif total == 3 or total == 4: #if there is a total of 3 or 4, then it favors us a safe move 
            evaluate -= ratio 
    
    return evaluate
      

"""
Min and Max Alpha Beta with current depth and eventual limit search 

max_value_2/min_value_2 does not implement the additional turn after winning a box for said player

max_value_2A/min_value_2A contains the additional turn after winning a box for said player

Evaluate functions passed to each player 
"""

from math import inf

#initalized comparison values for Alpha Beta pruning
neg_infinity = -inf
pos_infinity = inf

def max_value_2(state, max_eval, min_eval, alpha, beta, depth, limit):
    check_value = utility(state)
    check_eval = max_eval(state)
    return_tuple = ()
    if depth == limit or check_value !=None: #we reached furtheast state looking ahead or we got to a final state
        
        if check_value !=None: #final state
            return (check_value,None)
        else:
            return (check_eval,None) #not final, we hit depth limit,return eval
    
    else: #Looking at other game states... we have not hit limit or a final state

        value = neg_infinity #initalized value to compare against
        actions_for_state = actions_in(state)
        new_depth = depth + 1

        for possible_moves in actions_for_state:
            succ = max_successor(state,possible_moves) 
            values, move = min_value_2(succ,max_eval, min_eval, alpha,beta,new_depth,limit) 
            replace_Value = values 
            #gets the state that had that value, able to iterate through both states, and their values

            #Alpha Beta Pruning: Able to ignore state pathways that offer worse options
            if replace_Value > value:
                value = replace_Value
                return_tuple = (value,possible_moves)
            if replace_Value > alpha:
                alpha = replace_Value
            if alpha >= beta:
                break #go to next successor, we can skip

        return return_tuple #value of state, the action taken


def min_value_2(state,max_eval, min_eval, alpha, beta, depth, limit):
    tuple_r = ()
    check_state_value = utility(state)
    check_Eval = min_eval(state)
    
    if depth == limit or check_state_value !=None: 
        
        if check_state_value !=None: #final state
            return (check_state_value,None)
        else:
            return (check_Eval,None) #not final, we hit depth limit,return eval
    
    else:
        value_start = pos_infinity
        actions = actions_in(state)
        new_Depth = depth + 1
        
        for next_moves in actions:
            next_state = min_successor(state,next_moves) 
            values, moves = max_value_2(next_state,max_eval, min_eval, alpha,beta,new_Depth,limit)
            replace_value = values 
            #gets the state that had that value, able to iterate through both states, and their values
            if replace_value < value_start:
                value_start = replace_value
                tuple_r = (value_start, next_moves)
            if replace_value < beta:
                beta = replace_value
            if alpha >= beta:
                break #go to next successor
        
        return tuple_r
    


"""
Max algorithm with additional turn after box completion
A = Again as in turn again 
"""
def max_value_2A(state, max_eval, min_eval, alpha, beta, depth, limit):
    check_value = utility(state)
    check_eval = max_eval(state)
    return_tuple = ()
    if depth == limit or check_value !=None: 
        
        if check_value !=None: #final state
            return (check_value,None)
        else:
            return (check_eval,None) #not final, we hit depth limit,return eval
    
    else:
        value = neg_infinity
        actions_for_state = actions_in(state)
        new_depth = depth + 1

        for possible_moves in actions_for_state:
            succ = max_successor_A(state,possible_moves) 
            values, move = min_value_2A(succ,max_eval, min_eval, alpha,beta,new_depth,limit) 
            replace_Value = values 
                #gets the state that had that value, able to iterate through both states, and their values
            if replace_Value > value:
                value = replace_Value
                return_tuple = (value,possible_moves)
            if replace_Value > alpha:
                alpha = replace_Value
            if alpha >= beta:
                break #go to next successor


        return return_tuple


"""
Min algorithm with additional turn after box completion
A = Again as in turn again
"""
def min_value_2A(state,max_eval, min_eval, alpha, beta, depth, limit):
    tuple_r = ()
    check_state_value = utility(state)
    check_Eval = min_eval(state)
    
    if depth == limit or check_state_value !=None: 
        
        if check_state_value !=None: #final state
            
            return (check_state_value,None)
        else:
            return (check_Eval,None) #not final, we hit depth limit,return eval
    
    else:
        value_start = pos_infinity
        
        actions = actions_in(state)
        new_Depth = depth + 1
        
        for next_moves in actions:
            next_state = min_successor_A(state,next_moves) 
            values, moves = max_value_2A(next_state,max_eval, min_eval, alpha,beta,new_Depth,limit)
            replace_value = values 
            
            #gets the state that had that value, able to iterate through both states, and their values
            if replace_value < value_start:
                value_start = replace_value
                tuple_r = (value_start, next_moves)
            if replace_value < beta:
                beta = replace_value
            if alpha >= beta:
                break #go to next successor
        
        return tuple_r

"""
For Testing Purposes 
THIS IS A RANDOM PLAYER, HE WILL BE CONSIDERED A MIN PLAYER 
"""
from random import randint

def Randy_Random(state):
    
    randy_moves = actions_in(state)
    randy_state = state.copy()
    ranGe = len(randy_moves)
    randy_choice = randint(0, ranGe-1) #top end it can be equal to, we need to subtract by 1 for the correct range of possible indices
    
    #This is the index of the random action Randy will manipulate in the state
    his_move = randy_moves[randy_choice]
    
    #This is the new state after randy has acted upon it
    final_state = min_successor(randy_state, his_move)
    
    return final_state

"""
Print Representation
"""

def draw_DBQ(list_rep):
    line_number = 0
    for get_line in range(0, len(list_rep), int(math.sqrt(len(list_rep)))):

        #Either printing - or | two cases to sift through

        if line_number % 2 != 0:#odd line number, |, " ", or box winning identifiers
            print("\n")
            for index_v in range(0, int(math.sqrt(len(list_rep)))): # size_l *2 + 1, math to cycle through said line
            
                if list_rep[index_v + get_line] == '+': 
                    print("|", end = " ")
                elif list_rep[index_v + get_line] == 'X': 
                    print("X", end = " ")
                elif list_rep[index_v + get_line] == 'x': 
                    print("x", end = " ")
                elif list_rep[index_v + get_line] == 'o': 
                    print("o", end = " ")
                elif list_rep[index_v + get_line] == 'O':
                    print("O", end = " ")
                elif list_rep[index_v + get_line] == '?':
                    print("?", end = " ")
                else:
                    print(" ", end = " ")
        else: #its even *, -, or box winning identifiers
            print("\n")
            for index in range(0, int(math.sqrt(len(list_rep)))): 
                if list_rep[index + get_line] == '*':
                    print("*", end  = " ")
                elif list_rep[index + get_line] == '?':
                    print("?", end = " ")
                elif list_rep[index + get_line] == '+':
                    print("-", end = " ")
                elif list_rep[index + get_line] == 'X': 
                    print("X", end = " ")
                elif list_rep[index + get_line] == 'O': 
                    print("O", end = " ")
                elif list_rep[index + get_line] == 'x': 
                    print("x", end = " ")
                elif list_rep[index + get_line] == 'o': 
                    print("o", end = " ")
                else:
                    print(" ", end = " ")

        line_number += 1



""" 
Game Simulations
Game Simulation 2 will run an evaluate pairing for a number of different sized games, 
starting at 2 X 2 up to whatever max size is declared. 
This simulation is not used for testing but is available to determine if the size of the game impacts the matchup. 
To reduce runtime of implementing this I opted for comparing matchups against game mechanics.  
 
Game Simulation 3 and 3A run any number of games at any given size. 
Both min and max evaluate algorthims are passed. 
 
Game simulation 3 does not have the turn again mechanic.
 
Game simulation 3A does have the turn again mechanic. 
"""

def game_simulation_2(games_played,max_size_of_game, max_eval,min_eval):
    record_maps = dict()
    for size_of_game in range(2, max_size_of_game):
        record = [0, 0, 0]
        
        for games in range(games_played):
            env = make_list_rep(size_of_game)
            actions = number_of_actions(env)
            for turn in range(1,actions + 1):
                if turn % 2 == 0:
                    value, action = max_value_2(env, max_eval, min_eval, alpha=- 1, beta=+ 1, depth=0, limit=3)
                    env = max_successor(env, action)
                else:
                    value, action = min_value_2(env, max_eval, min_eval, alpha=- 1, beta=+ 1, depth=0, limit=3)
                    env = min_successor(env, action)
            
                u = utility(env)
                if u is not None: #-1, min win, 0 = tie, 1 = max win
                    record[u] += 1
                    break
        record_maps[size_of_game] = record
    return record_maps #returns the record

#Different simulatoed games that are then later graphed
def game_simulation_3(games_played,size_of_game,max_eval,min_eval):
    record = [0, 0, 0]
        
    for games in range(games_played):
        env = make_list_rep(size_of_game)
        actions = number_of_actions(env)
        for turn in range(1, actions + 1):
            if turn % 2 == 0:
                value, action = max_value_2(env, max_eval, min_eval, alpha=-1, beta=+1, depth=0, limit=3)
                env = max_successor(env, action)
                
            else:
                value, action = min_value_2(env, max_eval, min_eval, alpha=-1, beta=+1, depth=0, limit=3)
                env = min_successor(env, action)
            
            u = utility(env)
            if u is not None:
                record[u] += 1
                break
    return record #returns the record

#Different simulatoed games that are then later graphed
def game_simulation_3A(games_played,size_of_game,max_eval,min_eval):
    record = [0, 0, 0]
    for games in range(games_played):
        env = make_list_rep(size_of_game)
        #actions = number_of_actions(env)
        turn = 0
        while utility(env) == None:
            if turn % 2 == 0:
                value, action = max_value_2A(env,max_eval,min_eval, alpha=-1, beta=+1, depth=0, limit=3)
                env = max_successor_A(env, action)
            else:
                value, action = min_value_2A(env,max_eval,min_eval, alpha=-1, beta=+1, depth=0, limit=3)
                env = min_successor_A(env,action)
            
            u = utility(env)
            if u is not None:
                record[u] += 1
                break
            turn += 1
    return record #returns the record

""" 
After running experiment we have found that turn again mechanic does not influence the evaluate matchup outcome.
The better evaluate function dominates whether the mathcup whether the mechanic is present or not.
"""



#My System: 1 minute and 30 seconds to run.

import matplotlib.pyplot as plt
#snatch_evaluate_min/max
#action_evaluate_min/max
#set_up_evaluate_min/max

#This helper function will graph using the metplotlib.pyplot
def make_graph(plot,string_title,x_label, y_label, bar_0, bar_1):
    plot.bar(bar_0,bar_1)
    plot.title(string_title)
    plot.xlabel(x_label)
    plot.ylabel(y_label)
    plot.show()

if __name__ == "__main__":
    #these will become the x-labels of each of the graphs, depedning on the pairings
    s_a = ["Ties", "Snatch Wins", "Action Wins "]
    se_a = ["Ties", "Set up Wins", "Action Wins"]
    s_se = ["Ties", "Snatch Evaluate", "Set up Evaluate"]


    #NO TURN AGAIN
    game_s_a = game_simulation_3(50,3, snatch_evaluate_max, action_evaluate_min)
    game_se_a = game_simulation_3(50,3,set_up_evaluate_max, action_evaluate_min)
    game_s_se = game_simulation_3(50,3,snatch_evaluate_max, set_up_evaluate_min)

    #Turn Again after box win
    game_s_a_T = game_simulation_3A(50,3, snatch_evaluate_max, action_evaluate_min)
    game_se_a_T = game_simulation_3A(50,3,set_up_evaluate_max, action_evaluate_min)
    game_s_se_T = game_simulation_3A(50,3,snatch_evaluate_max, set_up_evaluate_min)



    make_graph(plt,"No Turn Again: Action vs. Snatch", "Evaluate Function","Total Wins",s_a,game_s_a)
    make_graph(plt,"No Turn Again: Set Up vs. Action", "Evaluate Function", "Total Wins", se_a, game_se_a)
    make_graph(plt,"No Turn Again: Snatch vs. Set Up", "Evaluate Function","Total Wins",s_se,game_s_se)

    make_graph(plt,"Turn Again: Action vs. Snatch", "Evaluate Function", "Total Wins", s_a, game_s_a_T)
    make_graph(plt,"Turn Again: Set Up vs. Action", "Evaluate Function","Total Wins",se_a,game_se_a_T)
    make_graph(plt,"Turn Again: Snatch vs. Set Up", "Evaluate Function", "Total Wins", s_se, game_s_se_T)



