### OR(2) OPTIMISATION ALGORITHMS - COURSERA ASSIGNMENT - WEEK 6 - Q2 ###
# LINEAR PROGRAMMING

import math
import numpy as np
import pandas as pd

from ortools.linear_solver import pywraplp

############################################### SETS AND INDICES ###############################################

num_ambulances = 2
num_districts = 8

A = [f'Ambulance {a+1}' for a in range(num_ambulances)]
D = [f'District {d+1}' for d in range(num_districts)]

############################################### PARAMETERS ###############################################

Populations = [40,30,35,20,15,50,45,60]

Distances = [[0,3,4,6,8,9,8,10],
             [3,0,5,4,8,6,12,9],
             [4,5,0,2,2,3,5,7],
             [6,4,2,0,3,2,5,4],
             [8,8,2,3,0,2,2,4],
             [9,6,3,2,2,0,3,2],
             [8,12,5,5,2,3,0,2],
             [10,9,7,4,4,2,2,0]]

############################################### FORMULATION ###############################################

solver = pywraplp.Solver.CreateSolver('SCIP')

############################################### DECISION VARIABLES ############################################### 

x = {} # 1 if ambulance is assigned to district d
for d in range(num_districts):
    x[d] = solver.IntVar(0, 1, 'x[d]')

y = {} # 1 if for district d ambulance is located in district c
for d in range(num_districts):
    for c in range(num_districts):
        y[d,c] = solver.IntVar(0, 1, 'y[d,c]')

m = {} # maximum population weighted time
m = solver.IntVar(0, math.inf, 'm')

############################################### CONSTRAINTS ###############################################

solver.Add(solver.Sum([x[d] for d in range(num_districts)]) == num_ambulances)

for d in range(num_districts):
    for c in range(num_districts):
        solver.Add(y[d,c] <= x[c])

for d in range(num_districts):
    solver.Add(solver.Sum([y[d,c] for c in range(num_districts)]) == 1)

for d in range(num_districts):
    solver.Add(m >= solver.Sum([Populations[d]*Distances[d][c]*y[d,c] for c in range(num_districts)]))

############################################### OBJECTIVE ###############################################

z = [] 
z.append(m)

############################################### SOLVER ###############################################

solver.Minimize(solver.Sum(z))
status = solver.Solve()

############################################### OUTPUT ###############################################

if status == pywraplp.Solver.OPTIMAL:

    Z = round(solver.Objective().Value(),2)
    print('\nPopulation weighted time =',Z,'\n')    
    
    Y = [[round(y[d,c].solution_value(),2) for c in range(num_districts)] for d in range(num_districts)]

    Districts = ['' for d in range(num_districts)]
    for d in range(num_districts):
        for c in range(num_districts):
            if Y[d][c] == 1:
                Districts[d] += f'{c+1}'

    print(pd.DataFrame(Districts, index = D, columns = ['Nearest district with ambulance']),'\n')

else:
    print('The problem does not have an optimal solution.')