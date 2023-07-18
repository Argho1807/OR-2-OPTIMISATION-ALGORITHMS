### OR(2) OPTIMISATION ALGORITHMS - COURSERA ASSIGNMENT - WEEK 6 - Q1 ###
# LINEAR PROGRAMMING

import math
import numpy as np
import pandas as pd

from ortools.linear_solver import pywraplp

############################################### SETS AND INDICES ###############################################

num_jobs = 15
num_machines = 3

J = [f'Job {j+1}' for j in range(num_jobs)]
M = [f'Machine {m+1}' for m in range(num_machines)]

############################################### PARAMETERS ###############################################

Processing_times = [7,4,6,9,12,8,10,11,8,7,6,8,15,14,3]

############################################### FORMULATION ###############################################

solver = pywraplp.Solver.CreateSolver('SCIP')

############################################### DECISION VARIABLES ############################################### 

x = {} # 1 if job j assigned to machine m
for j in range(num_jobs):
    for m in range(num_machines):
        x[j,m] = solver.IntVar(0, 1, 'x[j,m]')

makespan = {} # maximum processing time of all three machines
makespan = solver.IntVar(0, math.inf, 'makespan')

############################################### CONSTRAINTS ###############################################

for j in range(num_jobs):
    solver.Add(solver.Sum([x[j,m] for m in range(num_machines)]) == 1)

for m in range(num_machines):
    solver.Add(makespan >= solver.Sum([Processing_times[j]*x[j,m] for j in range(num_jobs)]))

# conflicting
for m in range(num_machines):
    solver.Add(x[1,m] + x[4,m] + x[7,m] <= 1) # 2,5,8
    solver.Add(x[5,m] + x[8,m] <= 1) # 6,9
    solver.Add(x[6,m] + x[4,m] + x[9,m] <= 1) # 7,10
    solver.Add(x[10,m] + x[14,m] <= 1) # 11,15  

############################################### OBJECTIVE ###############################################

z = [] 
z.append(makespan)

############################################### SOLVER ###############################################

solver.Minimize(solver.Sum(z))
status = solver.Solve()

############################################### OUTPUT ###############################################

if status == pywraplp.Solver.OPTIMAL:

    Z = round(solver.Objective().Value(),2)
    print('\nMakespan =',Z,'\n')    
    
    X = [[round(x[j,m].solution_value(),2) for m in range(num_machines)] for j in range(num_jobs)]

    Machine = ['' for m in range(num_machines)]
    for m in range(num_machines):
        for j in range(num_jobs):
            if X[j][m] == 1:
                Machine[m] += f'{j+1} '

    print(pd.DataFrame(Machine, index = M, columns = ['Jobs']),'\n')

else:
    print('The problem does not have an optimal solution.')