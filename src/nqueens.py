import random

def manage_input():
    file_handle = open('nqueens.txt', 'r') # open file
    lines_list = file_handle.readlines() # read lines in file
    for line in lines_list:
        numb = int(line) # convert line value to int
        scrambled_list = create_configuration(numb)
        results = run_nqueens(scrambled_list, numb) # calls run_nqueens with numb to determine results
        manage_nqueens(results, numb, 0) # calls manage_nqueens to determine if results are valid

def manage_nqueens(results, numb, count):
    if results != None:
        manage_output(results) # writes successful solution to file
        results.clear() # clears results for next variable
    else: # checks if results are None as this indicates the min_conflicts algorithm was unsuccessful in this case
        if results == None and count < 100:
            count += 1
            scrambled_list = create_configuration(numb) # creates a new initial configuration of queens
            results = run_nqueens(scrambled_list, numb) # call run_nqueens with new configuration of queens
            manage_nqueens(results, numb, count) # re-calls itself to determine if solution has now been found

def manage_output(results):
    with open('nqueens_out.txt', mode='a', encoding='utf-8') as my_file:
        my_file.write(str(results)) # writes result to file
        my_file.write('\n') # add a new line

def create_configuration(numb):
    initial_list = list(range(numb)) # create a list of the size of numb
    scrambled_list = create_scrambled_list(initial_list)
    return scrambled_list

def run_nqueens(scrambled_list, numb):
    solution = min_conflicts(scrambled_list, numb)
    if solution != None:
        result_list = convert_results_list(solution, numb)
        return result_list
    else:
        return None

def create_scrambled_list(initial_list):
    # creates a list where each queen is in it's own row and column as the initial placement of queens
    for i in range(0, len(initial_list) - 1):
        rand_num = random.randint(0, len(initial_list) - 1)
        swap_row = initial_list[i]
        initial_list[i] = initial_list[rand_num]
        initial_list[rand_num] = swap_row
    return initial_list

def convert_results_list(solution, numb):
    # converts results into end solution format
    result_list = []
    for i in range(len(solution)):
        result_list.insert(i, solution[i] + 1)
    return result_list

def determine_min_conflicts(conflicts_list, numb):
    # determines the min conflict positions
    min_conflicts = []
    list_min = min(conflicts_list)
    for i in range(numb):
        if conflicts_list[i] == list_min:
            min_conflicts.append(i)
    return min_conflicts

def determine_max_conflicts(conflicts, numb):
    # determines the max conflict positions
    max_conflicts = []
    for i in range(numb):
        if conflicts[i] > 0:
            max_conflicts.append(i)
    return max_conflicts

def random_position(a_list):
    return random.choice(a_list)

def min_conflicts(solution, numb, max_steps=100):
    for i in range(max_steps):
        conflicts = find_conflicts(solution, numb)
        # if none then the solution has been found return solution
        if sum(conflicts) == 0:
            return solution
        # determines list of conflicts where conflicts are greater than 0
        col_list = determine_max_conflicts(conflicts, numb)
        col = random_position(col_list)
        conflicts_list = [calc_conflicts(solution, numb, col, row) for row in range(numb)]
        # determines list of values which have lower corresponding conflict values
        min_conflicts_list = determine_min_conflicts(conflicts_list, numb)
        # updates solution at position col to a value that minimizes the conflicts
        solution[col] = random_position(min_conflicts_list)
    return None

def find_conflicts(solution, numb):
    return [calc_conflicts(solution, numb, col, solution[col]) for col in range(numb)]

def calc_conflicts(solution, numb, col, row):
    # calculates the conflicts based on col and row position
    conflicts = 0
    for i in range(numb):
        if i == col:
            continue
        if solution[i] == row:
            conflicts += 1
        if (row - i) == (solution[i] - col):
            conflicts += 1
        if (row + i) == (solution[i] + col):
            conflicts += 1
    return conflicts


manage_input()
