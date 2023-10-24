# Sudoku Report

As the name does not suggest, this projects is focused on the design and implementation of the a boolean satisfiability solver. Of course, the main focus was applying this to `.cnf` files that represent different sudoku problems (or subproblems). 

In this project, a SAT (Boolean Satisfiability Problem) solver is implemented using two algorithms: GSAT and WalkSAT. The program takes as input a CNF (Conjunctive Normal Form) file containing a set of logical clauses and aims to find an assignment of truth values to variables that satisfies all the clauses. The GSAT algorithm makes random moves, flipping variables based on a threshold probability, and attempts to maximize the number of satisfied clauses. On the other hand, the WalkSAT algorithm randomly selects a clause and flips a variable within that clause if it results in more satisfied clauses, otherwise, it flips a variable based on a threshold probability.

## Model and Representation 

As suggested by the assignment, I wrote the `SAT` class to store the problem's variables and apply its methods. 

The constructor is as follows: 
```
def __init__(self, cnf_file_path, solution_path, threshold, max_iterations):
```
It saves and stores the given variables, and then uses the `cnf_file_path` to initialize the other two instance variables: 
- `self.clauses`
- `self.variable_assignments`

A distinctive choice made in the implementation was the representation of variables as keys in a dictionary assigned to `True/False` values for efficient lookup and assignment operations. 

The CNF file is parsed, and clauses are stored as lists of variables in `self.clauses`, each variable represented as a __string__ in the format `x` or `-x`, where `x` is the variable identifier and the negative sign indicates negation. The variables are put into the `self.variable_assignments`, and randomly assigned true false values at the beginning of both algorithms. The representation enables quick access to variables and their assignments because of the dictionary hashing rather than a list lookup, facilitating efficient clause satisfaction checks and variable flipping. Additionally, the program allows flexibility by accepting different CNF files and solution paths, making it versatile for various problem instances. These design choices prioritize computational efficiency and flexibility, enabling the solver to handle a wide range of SAT problems effectively. 

Although the assignment suggested storing assignmnets as indices referring to a list of variables and using positive and negative integer values to represent negation accordingly, I found this method to be much more efficient, simple to implement, and effective at generating solutions for generic problems. I discuss the details on this below. 

## Algorithm Design

### Parsing Clauses from `.cnf` files

In the algorithms for this assignment, the first crucial step is to initialize the list of clauses based on the provided CNF file. The chosen approach here emphasizes simplicity and readability to ensure accurate parsing of the input file. By opening the CNF file, the algorithm reads it line by line. For each line, the elements (representing variables) are extracted and parsed. These elements are then stored as lists within the clauses list, creating a structured representation of the logical constraints. This is done in the function `initialize_clauses`, given below and called in the constructor. 

Although variable initialization and random assignment could've been done in this step as well, I found it easier to separate the logic for design and debugging purposes. As a result, I have to loop through the clauses separately in the `initialize_random_assignment`. In this step, all I do is initialize a list of all of the clauses.

As for the file path of the `.cnf`, I determined that running from the command line would be much more of a logistical pain, so I just pass both the solution path and the `.cnf` path to the `SAT` constructor. 

Pseudo: 
```
def initialize_clauses(self):
    initialize clauses list
    for each line in the file
        Split the line into individual elements (numbers)
        Parse elements and add them to the clauses list
    set instance variable with the updated list
```

### Initializing random values

Random value initialization is done in the initialize_random_assignment function and plays a vital role in the GSAT algorithm.

When encountering negative variables (denoted by the '-' sign), the function converts them into positive variables. This normalization simplifies the assignment process and ensures consistency in variable representation. It also allows us to check if the variable is in the dictionary, regardless of its value. For exmpale, the clause `-112`, represents the variable `112` being stored as `False` in the assignment. Accordingly, we don't store the variable `-112` in the dictionary-- we only store `112`, changing its associated value between `True` and `False`

To maintain a unique assignment for each variable, the function checks if the variable is already present in the assignment dictionary. If not, it randomly assigns a truth value (True or False) to the variable. This step prevents duplicate assignments and ensures a one-time random initialization.

The function utilizes the random.choice method to randomly assign truth values to variables. This approach guarantees a fair and unbiased selection, enhancing the randomness of the initial assignment.

The function's design ensures adaptability to various problem instances. It does not assume any specific variable names or values, allowing it to work seamlessly with different CNF files representing diverse problem scenarios.

Pseudocode: 
```
def initialize_random_assignment(self):
    for each clause line
        for each variable
            if the variable is negative, remove the negative sign
            if the variable isn't in the assignment
                set it to a random value
    update the assignment 
```

### Evaluating how many clauses are satisfied

Counting the number of clauses satisfied by a current variable assignment is crucial for the GSAT and WalkSAT algorithms because it ultimately serves an evaluation function for the effectiveness of an assignment. For GSAT, it is instrumental in evaluating the progress made during each iteration. For WalkSAT, it helps in deciding whether a newly flipped variable leads to more satisfied clauses, guiding the algorithm's exploration.

The function systematically iterates through the list of clauses, examining the variables within each clause. If a variable is satisfied (either positively or negatively based on its assignment), the entire clause is considered satisfied. The function utilizes a straightforward approach, incrementing the satisfied_clauses counter for every satisfied clause encountered.

In terms of implementation, the function is designed to efficiently handle large sets of clauses, contributing to the overall performance of the SAT solver. It relies just on the `SAT` class's instance variables (specifically, `self.variable_assignments). 

Originally, I used an all integer implementation to solve the problem-- storing integers with true false values in the assignments dictionary. This was the easiest approach, becuase it allows easy changing of true false values and quick lookups, while allowing the code to discard the sign of the variable easily using the `abs()` function. 

However, I realized that this could likely impact the goal of writing a generic solver, since it would only allow for `.cnf` files with integer values-- not like the Map Coloring Problem. Accordingly, I restructured the whole program to model after the example mentioned in the assignment that relies on storing indices of variables. This solved the issue of applicability to non-integeer `.cnf` files, but absolutely destroyed the efficiency of the program. This was becuase it had to search for whether or not the index was positive or negative in the list, as opposed to just using the dictionary to hash the key. This made the algorithm only a fraction of the previous speed. 

Accordingly, I switched it back to the previous storage method with a dictionary storing true or false values, but this time I store the variables as strings rather than ints. This is discussed above in the report as well-- it ensures that the variable name or type doesn't matter, but still allows us to assign it a true false value and look it up quickly. 

As for the logic behind the function, the algorithm loops through each clause. Since a clause is satisfied if at least one of the conditions is true, we loop through each variable in the constraint until we find one that is true. If so, we break the loop and incrememnt the number of clauses satisfied, continuing if not. Below is the pseudocode-- notice how I handle negative values. 

Pseudocode: 
```
def count_satisfied_clauses(self):
    remember the number of satisfied clauses
    loop through clauses
        set is_clause_satisfied to false
        for each variable in the clause
            if the variable is negative and that variable's value is false
                increment and break
            if the variable is positive that variable's value is true
                increment and break
        if the entire clause is satisfied, increment the count
    return the number of satisfied clauses
```

### Printing solution outputs: 

I checked out the solution printing mechanism given to us in `Sudoku.py`, and saw that it takes an input file with a list of true variables. So, I wrote the function `write_solution` within the SAT class, and call it every time the gsat or walksat functions terminate.

This function is very simple- it just loops through each of the variables in the assignmnet dictionary, printing them to the file on a line. This works well, and is used for output of test results. 
## GSAT 

The GSAT (greedy SAT) algorithm operates on the principle of local search, starting from an initial assignment of truth values to variables and iteratively refining it. In each iteration, GSAT assesses the current assignment's quality, measured by the number of satisfied clauses. If the assignment satisfies all clauses, the problem is solved. Otherwise, GSAT makes probabilistic decisions: it either flips a randomly chosen variable with a certain probability or identifies the variable whose flip maximizes the number of satisfied clauses. The algorithm's randomized nature allows it to escape local optima and explore diverse configurations, enhancing the chances of converging to a satisfying assignment.

The algorithm operates within a loop controlled by the maximum number of iterations defined by the user. During each iteration, the algorithm evaluates the current assignment, aiming to maximize the number of satisfied clauses. It employs a threshold probability to make stochastic decisions, balancing exploration and exploitation. If the threshold is not met, the algorithm identifies variables whose flips yield the highest satisfaction gains. This local search behavior enables the algorithm to systematically refine the assignment, gradually approaching a satisfying solution.

Keep in mind: this algorithm is pretty terrible at solving the sudoku problem. It's extremely inefficient, relies a lot on random chace for success, and takes absolutely forever. Since it has too loop through every variable seemingly endless times (if the threshold is not met, each iteration will search each constraint for every single variable), this algorithm takes eons. 

Regardless, is the pseudocode representing the GSAT algorithm. 

```
def gsat(self):
    # while under max iterations
        # get new num_satisfied and print it for observation
        # Check if the current assignment satisfies all clauses, return solution if so
        # Random number between 0 and 1
        if the number is greater than the threshold
            Random Move: Flip a random variable
        else:
            # Flip the variable that maximizes the number of satisfied clauses
    return No solution found within max_iterations
```

This algorithmic integration not only enhances the solver's performance but also showcases the dynamic nature of SAT problem-solving, where the balance between exploration and exploitation plays a crucial role in finding optimal solutions.

## Walksat

In the WalkSAT algorithm, I employed a different strategy for local search, emphasizing a balance between random exploration and greedy exploitation. The algorithm operates within a loop of a specified maximum number of iterations, aiming to find a satisfying assignment for the given SAT problem. The algorithm starts by randomly selecting an unsatisfied clause from the list of unsatisfied clauses. This choice reflects a deliberate focus on unsatisfied portions of the problem, allowing the algorithm to concentrate its efforts on problematic areas of the solution space.

This was the only part of the problem that called for a stuctural change to my representation, becuase I needed a way to quickly and easily access a list of unsatisfied clauses to choose from. I decided to store this as a separate list within an instance variable. Although this causes a memory hit, it is insignificant (these will only be a fraction of the size of the clauses lists). This made since becuase I already have to test whether or not a clause is satisfied in each iteration of the main loop, so each time it isn't satisfied, I just add it to the unsatisfied set. I pull a random clause from this set and use it for exploration.

During each iteration, the algorithm evaluates two options: it either flips a random variable from the chosen unsatisfied clause with a certain probability, introducing stochastic exploration, or it evaluates potential flips within the clause and selects the variable whose flip maximizes the number of satisfied clauses. This approach blends random exploration with local greedy search, ensuring the algorithm can escape local optima while capitalizing on promising solutions when found. By limiting our search space for the next variable to flip to only the variables within the unsatisfied, we gain massive performance improvements. 

The integration of WalkSAT into the SAT solver framework enhances the solver's adaptability to different problem instances. The algorithm's focus on unsatisfied clauses aligns with the common heuristic that addressing problematic parts of the problem often leads to massive improvements. 

Pseudocode: 
```
def walksat(self):
    while under max iterations
    get new num_satisfied and print it for observation
    if the assignment is complete:
        return the assignments as current
    choose a random unsatisfied clause
    Random number between 0 and 1
    if random_threshold > self.threshold:
        Random Move: Flip a random variable from the unsatisfied clause
    otherwise, loop through candidates and flip the best value
    for variable in random_clause:
        # flip the variable
        # count num clauses satisfied with the new one
        # flip it back
        # if it's the new highest, reset the list
            # empty the list and add it to the list
        # otherwise, if flipping that variable results in an equal score: 
            # add it to the list
    # flip a random variable from the maximizing list
# No solution found within max_iterations
return None  
```

## Testing 

As I developed this project, I first focused mainly on testing the helped methods used for the gsat and walksat algorithms (`initialize_clauses, initializie_random_assignment, and count_satisfied_clauses`). These do a lot of the important work, and since the algorithm is pretty simple, the main work was making sure that these methods worked correctly. I worked mainly with the `one_cell.cnf` constraints, since this was a small enough problem for me to verify manually that every single component was working correctly. 

Initialize clauses was easy: I just had to ensure that every single clause was getting written into the list correctly. I made sure that the files could be read correctly, and then printed the values of the instance variables after initialization to make sure everything was there correctly. 

I did the same for `initialize_random_assignment`: I just had to make sure that every variable was being assigned, and that the values were random each time. I printed the value of the assignment instance variables a few times, making sure that they were about evenly split true and false and that it was a different assignment each time. 

As for count satisfied clauses, I modified the function to print the value of each clause it was evaluated by the counter, as well as its evaluation. This was easy to check with one cell, and I got everything working. 

Then, I wrote both the gsat and walksat algorithms and used them on the simpler puzzles, testing to make sure that the found solutions. I had these print out the number of constraints satisfied out of the total number at each iteration of the loop, so I could observe the progression of the solver. This was helpful. 

Once I got to the larger problems that filled the whole board, I also used the `write_solution` method to print these to a file that could display the outputs using the `Sudoku` method that we were given. This made things easy to check for validity, and allowed me to verify that both algorithms were printing correct solutions and finding them as efficiently as they were supposed to. Then, I just ran them on each of the files until they couldn't find the solution within 100,000 iterations. This was a very long time on the gsat-- and it also depended somewhat on the threshold, the problem, and the random seed. 

The Walksat was a lot better- it finds solutions pretty quickly, except for sometimes when it gets stuck at local optima that are very close to the solutions-- again this is more dependent on the random seed. I found that varying the seed could make a big difference, but generally the walksat was able to solve all of the problems (except bonus). 


See `README.md` for a tutorial on how to navigate the testing in `sudoku_solver.py`: this is pretty simple. I've printed all the results of my tests to the solutions folder in the directory, so you can just run the second block of code that just prints the outputs of these files (or run the actual tests, I guess). 
