### OR(2) OPTIMISATION ALGORITHMS - COURSERA ASSIGNMENT - WEEK 6 - Q3_1 ###
# HEURISTIC ALGORITHM

import math
import numpy as np
import pandas as pd

from ortools.linear_solver import pywraplp

############################################### SETS AND INDICES ###############################################

num_ambulances = 3
num_districts = 8
 
#num_ambulances = 2
#num_districts = 4

A = [f'Ambulance {a+1}' for a in range(num_ambulances)]
D = [f'District {d+1}' for d in range(num_districts)]

############################################### PARAMETERS ###############################################

Populations = [40,30,35,20,15,50,45,60]

#Populations = [40,30,35,5]

Distances = [[0,3,4,6,8,9,8,10],
             [3,0,5,4,8,6,12,9],
             [4,5,0,2,2,3,5,7],
             [6,4,2,0,3,2,5,4],
             [8,8,2,3,0,2,2,4],
             [9,6,3,2,2,0,3,2],
             [8,12,5,5,2,3,0,2],
             [10,9,7,4,4,2,2,0]]

"""
Distances = [[0,3,4,1],
             [3,0,5,8],
             [4,5,0,1],
             [1,8,1,0]]
"""

############################################### ALGORITHM ###############################################

X = [0 for d in range(num_districts)]

for m in range(num_ambulances):
    max_dist = [max(Populations)*max(max(Distances))*10 for d in range(num_districts)]
    TEMP = X
    for d in range(num_districts):
        if X[d] == 1:
            max_d = max(Populations)*max(max(Distances))*10
        else:
            TEMP[d] = 1
            max_temp = 0
            temp = []
            for c in range(num_districts):
                if TEMP[c] == 1:
                    temp.append(0)
                else:
                    min_temp = Populations[c]*Distances[d][c]
                    for i in range(len(TEMP)):
                        if TEMP[i] == 1:
                            if Populations[c]*Distances[i][c] < min_temp:
                                min_temp = Populations[c]*Distances[i][c]
                    temp.append(min_temp)
            TEMP[d] = 0

            max_dist[d] = max(temp)
    
    min_dist = min(max_dist)
    index = []
    for d in range(num_districts):
        if max_dist[d] == min_dist:
            index.append(d)
    X[index[0]] = 1
    
    print(f'\nIteration {m+1} - Ambulance {m+1} assigned to {D[index[0]]}')

Z = []

Y = [0 for d in range(num_districts)]
for d in range(num_districts):
    if X[d] == 1:
        Y[d] = d+1
    else:
        nearest = max(Populations)*max(max(Distances))*10
        nearest_temp = 0
        for c in range(num_districts):
            if X[c] == 1:
                if Populations[d]*Distances[d][c] < nearest:
                    nearest = Populations[d]*Distances[d][c]
                    nearest_temp = c+1
        Y[d] = nearest_temp
        Z.append(nearest)

print('\nPopulation weighted time =',max(Z))
print('\n',pd.DataFrame(Y, index = D, columns = ['Nearest district with ambulance']),'\n')