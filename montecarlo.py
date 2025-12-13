

# Change the method in board class to return the action space
def MonteCarloSim(board, depth, width):
    board = copy.deepcopy(board)
    best_score = -9999999
    for i in range(width):
        current_score = 0
        for j in range(depth):
            current_action_space = board.action_space()
            current_row, current_column, next_row, next_column = current_action_space[np.random.randint(0, len(current_action_space))]

            board.move(current_row, current_column, next_row, next_column)
            
            