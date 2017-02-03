# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation allows us to apply specific constraints for available solution choices so that we can reduce the number of possibilities. Naked Twins strategy allows us to reduce the number of options further than what we did with only choice and elimination. 

With naked twins we remove the two digits from all the other peer boxes since those two digits will occur in one of those two boxes only. We break the problem into two parts. First, we find the naked twins and second we remove those two digits from other peer boxes. This reduces the number of possibilities and helps us to converge to a solution faster.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Diagonal sudoku problem is solved using constraint propagation including three different parts of our strategy now -- elimination, only choice and naked twins strategy. 

We add new units to the list of units we check for solving sudoku. The two diagonal units increases the units by two additional units added. We solve it by using search for our grid similar to how we solved the original sudoko puzzle without the diagonal sudoku.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.