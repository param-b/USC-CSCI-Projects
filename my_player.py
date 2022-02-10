import random
import time
import math
from copy import deepcopy
from writing_helper_funcs import readInput, writeOutput
from my_q_player import myQplayer

class OurGO:
    def __init__(self, n):
        self.game_board_size = n
        self.X_move = True
        self.died_stoness = []
        self.no_of_played_moves = 0
        self.max_allowed_moves = n * n - 1
        self.komi = n/2
        self.color_black = 1
        self.color_white = 2
        self.Player1 = 1
        self.Player2 = 2
        self.initial_game_board = []
        self.current_game_board = []

    def set_go_board(self, stone, initial_game_board, current_game_board):
        # Taken from host.py with function name changed
       
        for i in range(self.game_board_size):
            for j in range(self.game_board_size):
                if initial_game_board[i][j] == stone and current_game_board[i][j] != stone:
                    self.died_stoness.append((i, j))

        self.initial_game_board = initial_game_board
        self.current_game_board = current_game_board

    def compare_go_board(self, initial_game_board, current_game_board):
        # Taken from host.py with function name changed
       
        for i in range(self.game_board_size):
            for j in range(self.game_board_size):
                if initial_game_board[i][j] != current_game_board[i][j]:
                    return False
        return True

    def copy_go_board(self):
        # Taken from host.py with function name changed
        return duplicate_state(self)

    def find_neighbour_moves(self, new_go_board, i, j):
        # Taken from host.py with function name changed
        if len(new_go_board) == 0:
            new_go_board = self.current_game_board
        adjacent_nodes = []
        
        if i > 0:
            adjacent_nodes.append((i-1, j))
        if i < len(new_go_board) - 1:
            adjacent_nodes.append((i+1, j))
        if j > 0:
            adjacent_nodes.append((i, j-1))
        if j < len(new_go_board) - 1:
            adjacent_nodes.append((i, j+1))
        return adjacent_nodes

    def find_neighbour_allies(self, new_go_board, i, j):
        # Taken from host.py with function name changed
        if len(new_go_board) == 0:
            new_go_board = self.current_game_board
        allies = self.find_neighbour_moves([], i, j)
        adjacentAllies = []

        for x in allies:
            if new_go_board[x[0]][x[1]] == new_go_board[i][j]:
                adjacentAllies.append(x)
        return adjacentAllies

    def find_neighbour_allies_moves(self, new_go_board, i, j):
        if len(new_go_board) == 0:
            new_go_board = self.current_game_board
        allies = self.find_neighbour_moves(new_go_board, i, j)
        adjacent_allies = []
        for stone in allies:
           
            if new_go_board[stone[0]][stone[1]] == new_go_board[i][j]:
                adjacent_allies.append(stone)
        return allies

    def check_connected_allies(self, new_go_board, i, j):
        if len(new_go_board) == 0:
            new_go_board = self.current_game_board
        queue = [(i, j)]
        member_ally = []
        while queue:
            piece = queue.pop()
            member_ally.append(piece)
            adjacent_allies = self.find_neighbour_allies([], piece[0], piece[1])
            for ally in adjacent_allies:
                if ally not in queue and ally not in member_ally:
                    queue.append(ally)
        return member_ally

    def check_connected_allies_moves(self, new_go_board, i, j):
        # Taken from host.py with function name changed
        if len(new_go_board) == 0:
            new_go_board = self.current_game_board
        queue = [(i, j)]
        member_ally = []
        while queue:
            piece = queue.pop()
            member_ally.append(piece)
            neighbor_allies = self.find_neighbour_allies_moves(
                new_go_board, piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in queue and ally not in member_ally:
                    queue.append(ally)
        return member_ally

    def liberty(self, new_go_board, i, j):
        # Taken from host.py with function name changed
        if len(new_go_board) == 0:
            new_go_board = self.current_game_board
        allies = self.check_connected_allies([], i, j)
        for ally in allies:
            neighbors = self.find_neighbour_moves([], ally[0], ally[1])
            for neighbor in neighbors:
                if new_go_board[neighbor[0]][neighbor[1]] == 0:
                    return True
        return False

    def find_liberty_moves(self, new_go_board, i, j):
        # Taken from host.py with function name changed
        if len(new_go_board) == 0:
            new_go_board = self.current_game_board
        allies = self.check_connected_allies_moves(new_go_board, i, j)
        for ally in allies:
            neighbors = self.find_neighbour_moves(
                new_go_board, ally[0], ally[1])
            for neighbor in neighbors:
                if new_go_board[neighbor[0]][neighbor[1]] == 0:
                    return True
        return False

    def find_dead_stones(self, new_go_board, stone):
        # Taken from host.py with function name changed
        if len(new_go_board) == 0:
            new_go_board = self.current_game_board
        died_stoness = []
        for i in range(len(new_go_board)):
            for j in range(len(new_go_board)):
                # Check if there is a piece at this position:
                if new_go_board[i][j] == stone:
                    # The piece die if it has no liberty
                    if not self.liberty([], i, j):
                        died_stoness.append((i, j))
        return died_stoness

    def find_dead_stones_moves(self, new_go_board, stone):
        # Taken from host.py with function name changed
        if len(new_go_board) == 0:
            new_go_board = self.current_game_board
        died_stoness = []
        for i in range(len(new_go_board)):
            for j in range(len(new_go_board)):
                if new_go_board[i][j] == stone:
                    if not self.find_liberty_moves(new_go_board, i, j):
                        died_stoness.append((i, j))
        return died_stoness

    def  remove_dead_stones(self, stone):
        # Taken from host.py with function name changed
        died_stoness = self.find_dead_stones([], stone)
        if not died_stoness:
            return []
        self.remove_certain_pieces(died_stoness)
        return died_stoness

    def remove_certain_pieces(self, places):
        # Taken from host.py with function name changed
        new_go_board = self.current_game_board
        for stone in places:
            new_go_board[stone[0]][stone[1]] = 0
        self.update_go_board(new_go_board)

    def valid_place_check(self, new_go_board, i, j, stone):
        # Taken from host.py with function name changed
        if len(new_go_board) == 0:
            new_go_board = self.current_game_board
        if not (i >= 0 and i < len(new_go_board)):
            return False
        if not (j >= 0 and j < len(new_go_board)):
            return False

        if new_go_board[i][j] != 0:
            return False

        test_go = self.copy_go_board()
        test_go_board = test_go.current_game_board

        test_go_board[i][j] = stone
        test_go.update_go_board(test_go_board)
        if test_go.liberty([], i, j):
            return True

        test_go. remove_dead_stones(3 - stone)
        if not test_go.liberty([], i, j):
            return False

        else:
            if self.died_stoness and self.compare_go_board(self.initial_game_board, test_go.current_game_board):
                return False
        return True

    def valid_place_check_moves(self, new_go_board, i, j, stone):
        # Taken from host.py with function name changed
        if not (i >= 0 and i < len(new_go_board)):
            return False
        if not (j >= 0 and j < len(new_go_board)):
            return False

        if new_go_board[i][j] != 0:
            return False

        test_go = self.copy_go_board()
        test_go_board = test_go.current_game_board

        test_go_board[i][j] = stone
        test_go.update_go_board(test_go_board)
        if test_go.liberty([], i, j):
            return True

        if not test_go.liberty([], i, j):
            return False

        else:
            if self.died_stoness and self.compare_go_board(self.initial_game_board, test_go.current_game_board):
                return False
        return True

    def update_go_board(self, new_go_board):
        # Taken from host.py with function name changed
        self.current_game_board = new_go_board

    def get_score(self, stone):
        # Taken from host.py with function name changed
        new_go_board = self.current_game_board
        count = 0
        for i in range(self.game_board_size):
            for j in range(self.game_board_size):
                if new_go_board[i][j] == stone:
                    count += 1
        return count


def availaible_posns(new_go_board, stone):
    # Find stones locations on the new_go_board
    locations = []
    for i in range(ini_go.game_board_size):
        for j in range(ini_go.game_board_size):
            if new_go_board[i][j] == stone:
                locations.append((i, j))
    return locations


def eval_func(current_game_board, curr_piece_type):
    #evaluation function: difference of no. of our stones and no. of opponent's stones
    score_white, score_black = find_winner_at_current_stage(current_game_board)
    #endangered_white, endangered_black = groupLibertiesCalculation(current_game_board, 2, find_all_stones_piece_type(current_game_board, 1), find_all_stones_piece_type(current_game_board, 2)), groupLibertiesCalculation(current_game_board, 1, find_all_stones_piece_type(current_game_board, 1), find_all_stones_piece_type(current_game_board, 2))
    endangered_white, endangered_black = 0,0
    if curr_piece_type == 1:
        score = score_black - 0.25*endangered_black - score_white + 0.25*endangered_white
    if curr_piece_type == 2:
        score = score_white - 0.25*endangered_white - score_black + 0.25*endangered_black
    #print('this is the score for this current_game_board')
    #print(score)
    return score

def find_winner_at_current_stage(current_game_board):
    #return count
    count_black = score(current_game_board,1)
    count_white = score(current_game_board,2)
    return count_white + ini_go.komi, count_black

def score(current_game_board, piece_type):
        # Taken from host.py with name of the function changed.
        piece_count = 0
        for i in range(ini_go.game_board_size):
            for j in range(ini_go.game_board_size):
                if current_game_board[i][j] == piece_type:
                    piece_count += 1
        return piece_count

def unocuppied_posn(new_go_board, piece_type):
    # Check valid moves for the current player (ini_go.current_game_board)
    valid_move = []
    for i in range(ini_go.game_board_size):
        for j in range(ini_go.game_board_size):
            if ini_go.valid_place_check(new_go_board, i, j, piece_type):
                valid_move.append((i, j))
    return random.sample(valid_move, len(valid_move))



def unocuppied_posn_moves(new_go_board, piece_type):
    # Check valid moves for the current player (passing new_go_board as parameter)
    valid_move = []
    for i in range(ini_go.game_board_size):
        for j in range(ini_go.game_board_size):
            if ini_go.valid_place_check_moves(new_go_board, i, j, piece_type):
                valid_move.append((i, j))
    return random.sample(valid_move, len(valid_move))

def is_valid_move(x, y, cur_player):
    # check if valid for current player
    if (x, y) in unocuppied_posn(current_game_board, cur_player):
        return True
    else:
        return False


def place_stone(new_go_board, x, y, cur_player):
    # Place the move on the new_go_board
    if is_valid_move(x, y, cur_player):
        ini_go.initial_game_board = duplicate_state(new_go_board)
        new_go_board[x][y] = cur_player
        ini_go.current_game_board = new_go_board
        return new_go_board
    else:
        return new_go_board

def isTerminal():
    return False

def our_min_node(new_go_board, piece_type, depth, alpha, beta, start_time):
    new_go_game_board = duplicate_state(new_go_board)
    #print('in minimax min')
    GLOBAL_min = math.inf
    avail_moves = unocuppied_posn(new_go_game_board, piece_type)

    end = time.time()
    if len(avail_moves) == 0 or  isTerminal() or depth == 0 or end - start_time > 7.5:
        return (-1, -1), eval_func(new_go_game_board, piece_type)
    else:
        for move in avail_moves:
            new_game_board_for_each_iter = duplicate_state(new_go_board)
            new_go_game_board = place_stone(
                new_game_board_for_each_iter, move[0], 
                move[1], piece_type)
            dead_pieces = ini_go. remove_dead_stones(3 - piece_type)
            eatNum = 0
            if len(dead_pieces) > 0:
                eatNum = len(dead_pieces)

            if piece_type == ini_go.color_black:
                next_player = ini_go.Player2
                eatNum = ini_go.Player2 - piece_type
            else:
                next_player = ini_go.Player1
            
            move, new_score = our_max_node(
            new_go_game_board,next_player, 
            depth - 1, alpha, beta, 
            start_time)
            if move is None:
                pass
            if new_score < GLOBAL_min:
                GLOBAL_min = new_score
                best_move = move
            beta = min(new_score, beta)
            if beta <= alpha:
                break
        return best_move, GLOBAL_min

def our_max_node(new_go_board, piece_type, depth, alpha, beta, start_time):
    end = time.time()
    new_go_game_board = duplicate_state(new_go_board)
    cur_max = -math.inf
    # get our valid moves
    moves = unocuppied_posn(new_go_game_board, piece_type)
    # remove moves from valid moves which would be killed by opponent in the next round if they are placed
    stonestoremove = []
    for i in moves:
        ini_go.current_game_board[i[0]][i[1]] = piece_type
        avail_moves = unocuppied_posn(ini_go.current_game_board, 3 - piece_type)
        for j in avail_moves:
            if False:
                return None
            if j[0] and j[1] < 0:
                continue
            ini_go.current_game_board[j[0]][j[1]] = 3 - piece_type
            deadstones = ini_go.find_dead_stones([], piece_type)
            ini_go.current_game_board[j[0]][j[1]] = 0
            if i is not None:
                if i in deadstones:
                    if i not in stonestoremove:
                        stonestoremove.append(i)
                        #print(i)
        ini_go.current_game_board[i[0]][i[1]] = 0

    for a in stonestoremove:
        if a is not None and a in moves:
            moves.remove(a)

    if len(moves) == 0 or isTerminal() or depth == 0 or end - start_time > 7.5:
        return (-1, -1), eval_func(new_go_game_board, piece_type)
    else:
        for i in moves:
            new_game_board_for_each_iter = duplicate_state(new_go_board)
            new_go_game_board = place_stone(
                new_game_board_for_each_iter, i[0], i[1], piece_type)
            ini_go. remove_dead_stones(3 - piece_type)
            if piece_type == ini_go.color_black:
                next_player = ini_go.Player2
            else:
                next_player = ini_go.Player1
            m, new_score = our_min_node(
                new_go_game_board, next_player, 
                depth - 1, alpha, beta, 
                start_time)
            if new_score >= cur_max:
                cur_max = new_score
                best_move = i
            else:
                #print("Not the move")
                worse_move = i
            alpha = max(new_score, alpha)
            if m is None:
                pass
            if beta <= alpha:
                break
        return best_move, cur_max

def place_stone_minmax(new_go_board, piece_type):
    start = time.time()
    final_move, score = our_max_node(
        new_go_board, piece_type, max_depth, -math.inf, math.inf, start)
    i, j = final_move[0], final_move[1]
    x, y =  i, j

    return i, j, score

def find_all_neighbors(curr_move):
    temp = []
    for change in [(1,0), (-1,0), (0,1), (0,-1)]:
        if (0 <= curr_move[0]+change[0] < ini_go.game_board_size) and (0 <= curr_move[1]+change[1] < ini_go.game_board_size):
            temp.append((curr_move[0]+change[0], curr_move[1]+change[1]))
    return temp

def find_empty_neighbor(neighbours):
    empty_x = []
    for neighbor in neighbours:
        if ini_go.current_game_board[neighbor[0]][neighbor[1]]==0:
            empty_x.append(neighbor)
    return empty_x

def find_avail_spaces(ini_go ):
    temp = list()
    for i in range(ini_go.game_board_size):
        for j in range(ini_go.game_board_size):
            if ini_go.current_game_board[i][j] == 0:
                temp.append((i, j))

    return temp

def find_killer_moves_count(ini_go , avail_spaces):
    kill_stones_total = dict()
    for space in avail_spaces:
        ini_go.current_game_board[space[0]][space[1]] = stone
        died_stoness = ini_go.find_dead_stones([], 3-stone)
        ini_go.current_game_board[space[0]][space[1]] = 0
        if len(died_stoness) >= 1:
            kill_stones_total[space] = len(died_stoness)

    sorted_kill_stones_total = sorted(
        kill_stones_total, key=kill_stones_total.get, reverse=True)

    return sorted_kill_stones_total

def find_moves_leading_to_death(ini_go , avail_moves):
    moves_leading_to_death = list()
    for i in avail_moves:
        ini_go.current_game_board[i[0]][i[1]] = stone
        opp_move = unocuppied_posn_moves(ini_go.current_game_board, 3-stone)
        for j in opp_move:
            ini_go.current_game_board[j[0]][j[1]] = 3 - stone
            died_stoness = ini_go.find_dead_stones(ini_go.current_game_board, stone)
            ini_go.current_game_board[j[0]][j[1]] = 0
            if i in died_stoness:
                moves_leading_to_death.append(i)
        ini_go.current_game_board[i[0]][i[1]] = 0

    return moves_leading_to_death

def find_saves_stones(ini_go ):
    saves_stones = dict()
    opp_moves = list()
    for i in range(ini_go.game_board_size):
        for j in range(ini_go.game_board_size):
            if ini_go.current_game_board[i][j] == 0:
                opp_moves.append((i, j))

    for i in opp_moves:
        ini_go.current_game_board[i[0]][i[1]] = 3-stone
        cur_died_stoness = ini_go.find_dead_stones(ini_go.current_game_board, stone)
        ini_go.current_game_board[i[0]][i[1]] = 0
        if len(cur_died_stoness) >= 1:
            saves_stones[i] = len(cur_died_stoness)

    sorted_saves_stones = sorted(saves_stones, key=saves_stones.get, reverse=True)
    return sorted_saves_stones

def get_preferred_move(valid_moves):
    preferred_move= []
    preferred_move.append((2,2))
    preferred_move.append((1,1))
    preferred_move.append((1,3))
    preferred_move.append((3,1))
    preferred_move.append((3,3))
    preferred_move.append((2,0))
    preferred_move.append((2,4))
    preferred_move.append((0,2))
    preferred_move.append((4,2))
    for move in preferred_move:
        if move in valid_moves:
            return move
    return []

def duplicate_state(state):
    return deepcopy(state)

def get_input(ini_go , stone):

    # Find Killer Moves
    avail_spaces = find_avail_spaces(ini_go)

    # Game should be over
    if len(avail_spaces) < 0:
        return (2,2)

    sorted_kill_stones_total = find_killer_moves_count(ini_go, avail_spaces)

    for i in sorted_kill_stones_total:
        # lets start here
        trial_go_game_board = duplicate_state(ini_go.current_game_board)
        trial_go_game_board[i[0]][i[1]] = stone
        died_stone = ini_go.find_dead_stones_moves(trial_go_game_board, 3 - stone)
        eatnum = 0 
        for x in died_stone:
            trial_go_game_board[x[0]][x[1]] = 0
            eatnum += 1

        # print(ini_go.last_game_field)
        # print(trial_go_game_board)
        # print("Killed :" + str(eatnum))
        
        if i != None and ini_go.initial_game_board != trial_go_game_board and eatnum >= 0 :
            return i

    avail_moves = unocuppied_posn(ini_go.current_game_board, stone)

    #BT CODE 
    gameRes = "WIN"
    reward = 0.0
    if gameRes=='WIN':
        reward+=1.0
    elif gameRes=='DRAW':
        reward = 0.5
    elif gameRes=='LOSE':
        reward = 0.0

    moves_leading_to_death = find_moves_leading_to_death(ini_go, avail_moves)

    for x in moves_leading_to_death:
        if x in avail_moves:
            avail_moves.remove(x)

    if len(avail_moves) == 0:
        return "PASS"

    sorted_saves_stones = find_saves_stones(ini_go)

    for poss_move in sorted_saves_stones:
        if poss_move != None and poss_move in avail_moves: 
            return poss_move

    if len(avail_moves) >= 15:
       move = get_preferred_move(avail_moves)
       if len(move) > 0:
           return move
           

    print("Goes to Alpha Beta Now")
    movei, movej, _ = place_stone_minmax(ini_go.current_game_board, stone)
    move_x, move_y = movei, movej
    move_x, move_y = move_x, move_y
    return(move_x, move_y)

def find_all_stones_piece_type(current_game_board, piece_type):
    #find positions of stones on the current_game_board
    placement = []
    for i in range(ini_go.game_board_size):
        for j in range(ini_go.game_board_size):
            if current_game_board[i][j] == piece_type:
                placement.append((i,j))
    return placement

def groupLibertiesCalculation(board, pieceType, blackPieces, whitePieces):
    #print("Enters Group Liberties")
    #print(blackPieces)
    #print(whitePieces)
    #print(pieceType)
    visited = {}
    keys = []
    found_pieces = blackPieces if pieceType == 1 else whitePieces

    while found_pieces:
        #print(found_pieces)
        x_yList = found_pieces[0]
        x = x_yList[0]
        y = x_yList[1]

        #BT CODE
        res = str()
        j = 0
        for i in range(5):
                res += str(board[i][j])

        a, visited = countLiberties(board, x, y, pieceType, visited)

        final_keys = []
        for k, v in visited.items():
            if v == 0 and k not in keys:
                keys.append(k)
            final_keys.append(k)

        found_pieces = list(set(found_pieces) - set(final_keys))
    #print("Exits Group Liberties")
    return len(keys)

def countLiberties(board, i, j, pieceType, visited = {}):
    #print("Inside Count Liberties")
    count = 0
    x_y = (i, j)
    if i < 0 or i >= ini_go.game_board_size or j < 0 or j >= ini_go.game_board_size or board[i][j] == 3 - pieceType or x_y in visited:
        return 0, visited

    if board[i][j] == 0:
        visited[x_y] = 0
        return 1, visited

    visited[x_y] = 1

    count += countLiberties(board, i+1, j, pieceType, visited)[0] +    countLiberties(board, i-1, j, pieceType, visited)[0] + countLiberties(board, i, j+1, pieceType, visited)[0] + countLiberties(board, i, j-1, pieceType, visited)[0]

    return count, visited

def find_initial_white_moves(self, movesMade, validMoves):
    moveCount = len(movesMade)
    if moveCount == 0:
        possible_moves = [(2,2),(1,1),(3,3),(3,1),(1,3)]
        for move in possible_moves:
            if move in validMoves:
                return (self.getMove(move), 0)
            #if self.valid_place_check(board, move[0], move[1], pieceType):
                #return (move, 0) #Or what do you want to do
    elif moveCount == 1:
        if movesMade[0]  == (2,2):
            possible_moves = [(1,1),(3,3),(3,1),(1,3)]
            for move in possible_moves:
                if move in validMoves:
                    return (self.getMove(move), 0)
        elif movesMade[0] == (1,1):
            possible_moves = [(3,1),(1,3),(3,3)]
            for move in possible_moves:
                if move in validMoves:
                    return (self.getMove(move), 0)
        elif movesMade[0] == (1,3):
            possible_moves = [(1,1),(3,3),(3,1)]
            for move in possible_moves:
                    if move in validMoves:
                        return (self.getMove(move), 0)
        elif movesMade[0] == (3,1):
            possible_moves = [(1,1),(3,3),(1,3)]
            for move in possible_moves:
                if move in validMoves:
                    return (self.getMove(move), 0)
    elif moveCount == 2:
        #Find move from orders of move preference
        return ([],0)

def find_initial_black_moves(self, moveCount, opp_moveMade, validMoves):
    if moveCount == 0:
        return (self.getMove((2,2)), 0)
    # We follow the opponent here. When 1 black and 1 white move is played.
    # We can change how we are making valid move check!
    # Create defaultdict and check value
    elif moveCount == 1:
        if opp_moveMade[0][0] == 2 and opp_moveMade[0][0] == 2:
            return (self.getMove((1,2)), 0)

        elif opp_moveMade[0][0] < 2 and opp_moveMade[0][1] < 2:
            possible_moves = [(1,1),(2,1),(1,2)]
            for move in possible_moves:
                if move in validMoves:
                    return (self.getMove(move), 0)
        elif opp_moveMade[0][0] > 2 and opp_moveMade[0][1] < 2:
            possible_moves = [(3,1),(2,1),(3,2)]
            for move in possible_moves:
                if move in validMoves:
                    return (self.getMove(move), 0)
        elif opp_moveMade[0][0] < 2 and opp_moveMade[0][1] > 2:
            possible_moves = [(1,3),(1,2),(2,3)]
            for move in possible_moves:
                if move in validMoves:
                    return (self.getMove(move), 0)
        else:
            possible_moves = [(3,3),(3,2),(2,3)]
            for move in possible_moves:
                if move in validMoves:
                    return (self.getMove(move), 0)
    # Move Count when 2 black and 2 white moves are played. Thrid black move is played.
    elif moveCount == 2:
        if opp_moveMade[0][0] <= 2 and opp_moveMade[0][1] <= 2:
            possible_moves = [(1,1),(2,1),(1,2),(2,2),(0,1),(1,0),(2,0),(0,2)]
            for move in possible_moves:
                if move in validMoves:
                    return (self.getMove(move), 0)
        elif opp_moveMade[0][0] > 2 and opp_moveMade[0][1] < 2:
            possible_moves = [(3,1),(2,1),(3,2),(2,2),(4,2),(3,0),(4,1)]
            for move in possible_moves:
                if move in validMoves:
                    return (self.getMove(move), 0)
        elif opp_moveMade[0][0] < 2 and opp_moveMade[0][1] > 2:
            possible_moves = [(1,3),(1,2),(2,3),(2,2),(2,0),(3,0),(1,4)]
            for move in possible_moves:
                if move in validMoves:
                    return (self.getMove(move), 0)
        else:
            possible_moves = [(3,3),(3,2),(2,3),(2,2),(2,4),(4,2),(3,4),(4,3)+7]
            for move in possible_moves:
                #if self.valid_place_check(board, move[0], move[1], pieceType):
                if move in validMoves:
                    return (self.getMove(move), 0)

def my_initial_move(go, pieceType, whitePieces, blackPieces, validMoves):
     board = []
     previous_board = []
     if pieceType == 1:
            if len(blackPieces) < 3:
                whitePieces = find_og_move_made(previous_board, board, whitePieces)
                print(whitePieces)
                return find_initial_black_moves(len(blackPieces), whitePieces, validMoves)
     else:
        if len(whitePieces) < 3:
            move = find_initial_white_moves(whitePieces, validMoves)
            if len(move[0]) != 0:
                return move
                
def find_og_move_made(self, previous_board, new_board, opp_move_made):
        for i in range(5):
            for j in range(5):
                if previous_board[i][j] != new_board[i][j]:
                    return (i,j)
        for inx in range(len(opp_move_made)):
            if opp_move_made[inx] == (i,j) and inx==0:
                return [opp_move_made[inx+1]]
        return [opp_move_made[0]]

N = 5
max_depth = 4
max_depth_opponent = 1
stone, initial_game_board, current_game_board = readInput(N)
ini_go = OurGO(N)
ini_go.set_go_board(stone, initial_game_board, current_game_board)
action = get_input(ini_go, stone)
if action == None:
    action = "PASS"
writeOutput(action)
