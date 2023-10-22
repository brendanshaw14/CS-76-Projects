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

## GSAT 