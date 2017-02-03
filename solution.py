# Utils <Start>

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Added diagonal_units
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]


unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# Utils <End>


assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
    # Find twins instance
        twin_units = find_naked_twins(unit, values)
        if(twin_units):
    # Eliminate the naked twins as possibilities for their peers
            eliminate_naked_twins(unit, twin_units, values)
    return values

def find_naked_twins(unit, values):
    """Find naked twins.

      Args:
        unit(array): an array of an axis of elments['A9', 'B8', ... 'I1']
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

      Returns:
         unit_twins(tuple) of matching values ('H4', 'H6')
    """
    unit_twins = {}  # holder for unit values
    for box in unit:
        if len(values[box]) == 2:  # the box has two possible values
            unit_twins[box] = values[box]  # asign the values to a key in the unit twin.
            if len(unit_twins) == 2:  # the unit list has two possible key value pairs
                unit_tuple_value = tuple(unit_twins.values())
                if(unit_tuple_value[0] == unit_tuple_value[1]):
                    return tuple(unit_twins.keys())
                else:
                    return None
    return None

def eliminate_naked_twins(unit, unit_twins, values):
    """
	Eliminate corresponding twin values
    """
    box, twin_box = unit_twins[0], unit_twins[1]
    for target_box in set(peers[box]).intersection(peers[twin_box]):
        for digit in values[box]:
            # Remove the twin values
            assign_value(values, target_box, values[target_box].replace(digit, ''))

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_values = []
    starting_value = '123456789'
    for x in grid:
        if x == '.':
            grid_values.append(starting_value)
        elif x in starting_value:
            grid_values.append(x)
	# Check if the size of grid_values is 81 to cover all the boxes
    assert len(grid_values) == 81
    return dict(zip(boxes, grid_values))

def display(values):
	"""
	Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
	width = 1+max(len(values[s]) for s in boxes)
	line = '+'.join(['-'*(width*3)]*3)
	for r in rows:
	    print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
	                  for c in cols))
	    if r in 'CF': print(line)
	return

# Constraint propagation with Elimination
def eliminate(values):
    final_values = [box for box in values.keys() if len(values[box]) == 1]
    for key in final_values:
        value_character = values[key]
        for pkey in peers[key]:
            values[pkey] = values[pkey].replace(value_character, '')
    return values

# Constraint propagation with only choice
def only_choice(values):
    """Finalize all values that are the only choice for a unit.
    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.
    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    all_digits = '123456789'
    new_values = values.copy()  # note: do not modify original values
    # TODO: Implement only choice strategy here
    for unit in unitlist:
        for digit in all_digits:
            occurrences = [box for box in unit if digit in values[box]]
            if len(occurrences) == 1:
                new_values[occurrences[0]] = digit
            
    return new_values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Apply naked twins strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    # First, reduce the puzzle using the previous function
    temp_values = reduce_puzzle(values)
  
    if temp_values is False:
        return temp_values
    if all(len(temp_values[s]) == 1 for s in boxes):
        return temp_values #solved
        
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(temp_values[s]), s) for s in boxes if len(temp_values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in temp_values[s]:
        new_sudoku = temp_values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    "Using depth-first search and propagation, try all possible values."
    # Applying the already existing function to propagate constraints 
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
