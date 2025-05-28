import queue
import numpy as np 
import random
import tkinter as tk
from tkinter import messagebox
import time

class CSP:
    def __init__(self):
        self.variables = []

class Variable:
    def __init__(self, i, j, k, val):
        self.row = i
        self.column = j
        self.block = k
        if val == 0:
            self.domain = [1,2,3,4,5,6,7,8,9]
            self.value = 0
        else:
            self.domain = [val]
            self.value = val

class Arc:
    def __init__(self, a, b):
        self.first = a
        self.second = b

def AC3(csp):
    arcs=queue.Queue()
    for i in csp.variables:
        for j in csp.variables:
            if j.value > 9 or j.value < 0:
                return False #invalid value
            if i != j and (i.row == j.row or i.column == j.column or i.block == j.block): #arc between all elements of a row, col and block
                arcs.put(Arc(i,j))
                
    while not arcs.empty():
        arc = arcs.get()
        if revise(arc.first, arc.second):
            if(len(arc.first.domain) == 0 or len(arc.second.domain)==0): #no possible values, inconsistent
                return False
            for xk in csp.variables:
                if xk != arc.first and xk != arc.second and (xk.row == arc.first.row or xk.column == arc.first.column or xk.block == arc.first.block): #recheck all related arcs
                    arcs.put(Arc(xk,arc.first))
    return True
    
def revise(xi,xj):
    #print("arc:(",xi.row,",",xi.column,") Domain:",xi.domain,"and (",xj.row,",",xj.column,") Domain:",xj.domain)
    revised = False
    for x in xi.domain:
        if (len(xj.domain) == 1 and xj.domain[0] == x) or (xj.value == x): #value in xi domain is the only remaining value in xj domain, using it would make xj inconsistent so we remove it from xi
                xi.domain.remove(x)
                print(x," removed from domain of element at row:",xi.row,"and column:",xi.column,"domain:",xi.domain)
                revised = True
    return revised

def BTS(csp):
    return backtrack({},csp)
    
def backtrack(assignment,csp):
    unassigned = []
    for var in csp.variables:
        if var.value == 0:
            unassigned.append(var)

    if len(unassigned) == 0: #all tiles assigned, solution found
        return True

    smallest_dom = len(min(unassigned, key=lambda x: len(x.domain)).domain) #choose element with smallest domain
    var = random.choice([v for v in unassigned if len(v.domain) == smallest_dom]) #in case of equal length domains, choose randomly (to not always generate the same puzzle) 

    for val in least_constraining_values(csp, var): #iterate a copy of the domain to not ruin it
        if is_valid(csp,var.row,var.column,val):
            var.value = val #assign value since move is valid
            var.domain = [val] #domain becomes solely this value
            assignment[var] = val #append to assignment
            backupdom = {x: x.domain[:] for x in csp.variables} #backup the state in case we backtrack
            if AC3(csp):
                if backtrack(assignment,csp):
                    for vv in csp.variables:
                        if len(vv.domain) == 1:
                            vv.value = vv.domain[0]
                            assignment[vv] = vv.domain[0]
                    return True
            #backtrack
            var.value = 0
            for x in csp.variables:
                x.domain = backupdom[x]
            del assignment[var]

    return False

def is_valid(csp,row,col,num):
    block = row//3 * 3 + col//3 
    for var in csp.variables:
        if not(var.row == row and var.column == col): 
            if var.row == row and var.value == num: #value already in row
                return False
            if var.column == col and var.value == num: #value already in column
                return False
            if var.block == block and var.value == num: #value already in block
                return False
    return True

def least_constraining_values(csp, var):
    value_constraints = []
    for val in var.domain:
        count = 0
        for neighbor in csp.variables:
            if neighbor != var and (neighbor.row == var.row or neighbor.column == var.column or neighbor.block == var.block):
                if val in neighbor.domain:
                    count += 1
        value_constraints.append((val, count))
    # Sort by the number of constraints each value imposes, ascending
    value_constraints.sort(key=lambda x: x[1])
    return [v[0] for v in value_constraints] #least constraints

def BTSgui(csp):
    return backtrackgui({},csp)

def backtrackgui(assignment,csp):
    unassigned = []
    for var in csp.variables:
        if var.value == 0:
            unassigned.append(var)

    if len(unassigned) == 0: #all tiles assigned, solution found
        return True

    smallest_dom = len(min(unassigned, key=lambda x: len(x.domain)).domain)  #choose element with smallest domain
    var = random.choice([v for v in unassigned if len(v.domain) == smallest_dom]) #in case of equal length domains, choose randomly (to not always generate the same puzzle) 

    for val in least_constraining_values(csp, var):  #iterate a copy of the domain to not ruin it
        if is_valid(csp,var.row,var.column,val):
            var.value = val #assign value since move is valid
            var.domain = [val] #domain becomes solely this value
            assignment[var] = val #append to assignment
            backupdom = {x: x.domain[:] for x in csp.variables} #backup the state in case we backtrack
            entries[var.row][var.column].insert(0, val)
            root.update() #upadte GUI
            time.sleep(0.05) #to see update
            if AC3(csp):
                if backtrackgui(assignment,csp):
                    for vv in csp.variables:
                        if len(vv.domain) == 1:
                            vv.value = vv.domain[0]
                            assignment[vv] = vv.domain[0]
                    return True
            #backtracking
            var.value = 0
            for x in csp.variables:
                x.domain = backupdom[x]
            del assignment[var]
            entries[var.row][var.column].delete(0, tk.END)
            root.update() #upadte GUI
            time.sleep(0.05) #to see update

    return False

def random_generate(difficulty):
    start_time=time.time()
    nosol = True
    while nosol: #try until you get solveable puzzle
        puzzle = np.zeros((9,9), dtype = int)
        csp = CSP()
        for i in range(9):
            for j in range(9):
                k= i//3 *3 + j//3 
                csp.variables.append(Variable(i,j,k,puzzle[i][j]))
        if BTS(csp):
            for var in csp.variables:
                puzzle[var.row][var.column] = var.value
            safe = puzzle.copy() #backup puzzle state
            remove = [(row,col)for row in range(9) for col in range(9)]
            random.shuffle(remove) #remove random places
            if difficulty == 0.1: #easy
                removed = remove[:25]
            elif difficulty == 0.3: #medium
                removed = remove[:45]
            elif difficulty == 0.5: #hard
                removed = remove[:65]

            for i,j in removed:
                puzzle[i][j] = 0
                clone = CSP()
                for i in range(9):
                    for j in range(9):
                        k= i//3 *3 + j//3 
                        clone.variables.append(Variable(i,j,k,puzzle[i][j]))

                if(AC3(clone)) == False or (BTS(clone)) == False: #removing this piece made the puzzle unsolveable, put it back
                    puzzle[i][j] = safe[i][j]

            problem = CSP()
            for i in range(9):
                for j in range(9):
                    k= i//3 *3 + j//3 
                    problem.variables.append(Variable(i,j,k,puzzle[i][j]))
            nosol = False
    end_time=time.time()
    print("Puzzle generated in",(end_time-start_time)*1000,"Milliseconds")
    return problem

def solve_sudoku():
    start_time=time.time()
    global test
    if AC3(test):
        if BTSgui(test):
            for i in range(9):
                for j in range(9):
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, test.variables[i * 9 + j].value)
            messagebox.showinfo("Sudoku Solved", "Sudoku solved successfully!")
            end_time=time.time()
            print("Puzzle solved in",(end_time-start_time)*1000,"Milliseconds")
        else:
            messagebox.showerror("No Solution", "No solution exists for the given Sudoku.")
    else:
        messagebox.showerror("Invalid State", "The initial Sudoku puzzle state is invalid.")

def submit():
    global test
    solution = np.zeros((9,9),dtype = int)
    if AC3(test):
        if BTS(test):
            for i in range(9):
                for j in range(9):
                    solution[i][j] = test.variables[i * 9 + j].value #solve puzzle

    puzzle = np.zeros((9, 9), dtype=int) #user solution
    for i in range(9):
        for j in range(9):
            value = entries[i][j].get()
            if value.isdigit():
                puzzle[i, j] = int(value)
            else:
                puzzle[i, j] = 0
    for i in range(9):
        for j in range(9):
            entries[i][j].config(bg="white") #reset colour in case of continuously submitting 
    incorrect = False #assume correcy
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != solution[i][j]: #wrong answer
                entries[i][j].config(bg="red")
                incorrect = True
            else: # all correct
                entries[i][j].config(bg="green")

    if incorrect:
        messagebox.showerror("Incorrect Solution", "The solution entered is incorrect.")
    else:
        messagebox.showinfo("Correct Solution", "The solution entered is correct.")

def generate_puzzle(difficulty):
    global test
    test = random_generate(difficulty)
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            val = test.variables[i * 9 + j].value
            if val != 0:
                entries[i][j].insert(0, val)
                entries[i][j].config(state="disabled")
            else:
                entries[i][j].config(state="normal")

def set_initial_puzzle():
    global test
    puzzle = np.zeros((9, 9), dtype=int)
    for i in range(9):
        for j in range(9):
            value = entries[i][j].get() #get input
            if value.isdigit():
                puzzle[i, j] = int(value)
            else:
                puzzle[i, j] = 0

    test = CSP()
    for i in range(9):
        for j in range(9):
            k = i // 3 * 3 + j // 3 #block number
            test.variables.append(Variable(i, j, k, puzzle[i, j]))
    
    if AC3(test):
        messagebox.showinfo("Initial Puzzle Set", "Initial puzzle has been set successfully.")
    else:
        messagebox.showerror("Invalid State", "The initial Sudoku puzzle state is invalid.")

def reset_board():
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state="normal") #can be written on
            entries[i][j].config(bg="white") #in care we submitted a previous answer and it marked red/green
            entries[i][j].delete(0, tk.END) #delete number in cell

# Initialize the main window
root = tk.Tk()
root.title("Sudoku Solver")
canvas = tk.Canvas(root, width=400, height=400)
canvas.grid(row=0,column=0,rowspan=9,columnspan=9)
canvas.create_line(135, 0, 135, 400, fill="grey", width=10) #Vertical 1
canvas.create_line(0, 135, 400, 135, fill="grey", width=10) #Horizontal 1
canvas.create_line(270, 0, 270, 400, fill="grey", width=10) #Vertical 2
canvas.create_line(0, 270, 400, 270, fill="grey", width=10) #Horizontal 2

# Create a grid of entry widgets
entries = [[tk.Entry(root, width=2, font=("Arial", 18), justify="center") for _ in range(9)] for _ in range(9)]

for i in range(9):
    for j in range(9):
        entries[i][j].grid(row=i, column=j, padx=5, pady=5)

# Difficulty selection buttons "auto generate"
button_frame = tk.Frame(root)
button_frame.grid(row=9, column=0, columnspan=9, pady=10)

easy_button = tk.Button(button_frame, text="Easy", command=lambda: generate_puzzle(0.1))
easy_button.pack(side="left", padx=10)

medium_button = tk.Button(button_frame, text="Medium", command=lambda: generate_puzzle(0.3))
medium_button.pack(side="left", padx=10)

hard_button = tk.Button(button_frame, text="Hard", command=lambda: generate_puzzle(0.5))
hard_button.pack(side="left", padx=10)

# Entering initial state button
set_initial_button = tk.Button(button_frame, text="Set Initial Puzzle", command=set_initial_puzzle)
set_initial_button.pack(side="left", padx=10)

# Solve, submit and reset buttons
solve_button = tk.Button(root, text="Solve", command=solve_sudoku)
solve_button.grid(row=10, column=0, columnspan=4, pady=10)

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=10, column=2, columnspan=4, pady=10)

reset_button = tk.Button(root, text="Reset", command=reset_board)
reset_button.grid(row=10, column=4, columnspan=4, pady=10)

# Run the GUI
root.mainloop()