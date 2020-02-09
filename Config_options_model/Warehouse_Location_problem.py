#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 07:53:19 2019

@author: mdrahali
"""

# wl_concrete.py: ConcreteModel version of warehouse location determination problem
import csv
from pyomo.environ import *

model = ConcreteModel(name="(WL)")

N = ['Harlingen', 'Memphis', 'Ashland']
M = ['NYC', 'LA', 'Chicago', 'Houston']
d = {('Harlingen', 'NYC'): 1956, \
     ('Harlingen', 'LA'): 1606, \
     ('Harlingen', 'Chicago'): 1410, \
     ('Harlingen', 'Houston'): 330, \
     ('Memphis', 'NYC'): 1096, \
     ('Memphis', 'LA'): 1792, \
     ('Memphis', 'Chicago'): 531, \
     ('Memphis', 'Houston'): 567, \
     ('Ashland', 'NYC'): 485, \
     ('Ashland', 'LA'): 2322, \
     ('Ashland', 'Chicago'): 324, \
     ('Ashland', 'Houston'): 1236 }
P = 2

model.x = Var(N, M, bounds=(0,1))
model.y = Var(N, within=Binary)

#model.x.pprint()

def obj_rule(model):
    return sum(d[n,m]*model.x[n,m] for n in N for m in M)

model.obj = Objective(rule=obj_rule)

# @deliver:
def one_per_cust_rule(model, m):
    return sum(model.x[n,m] for n in N) == 1
model.one_per_cust = Constraint(M, rule=one_per_cust_rule)
# @:deliver

def warehouse_active_rule(model, n, m):
    return model.x[n,m] <= model.y[n]
model.warehouse_active = Constraint(N, M, rule=warehouse_active_rule)

def num_warehouses_rule(model):
    return sum(model.y[n] for n in N) <= P


model.num_warehouses = Constraint(rule=num_warehouses_rule)

#solver = SolverFactory('glpk') # create the glpk solver 
#solver.solve(model) # solve
#
#status = solver.solve(model) # solve
##model.y.pprint() # print the optimal warehouse locations
#
#status.write(filename='results.json', format='json')



"Postprocess function that allows us to store the results in csv file"

def pyomo_postprocess(options=None, instance=None,\
                      results=None):
    #
    # Collect the data
    #
    vars = set()
    data = {}
    f = {}
    for i in range(len(results.solution)):
        data[i] = {}
        for var in results.solution[i].variable:
            vars.add(var)
            data[i][var] = \
                results.solution[i].variable[var]['Value']
        for obj in results.solution[i].objective:
            f[i] = results.solution[i].objective[obj]['Value']
            break
        
    print(f,data)
    #
    # Write a CSV file, with one row per solution.
    # The first column is the function value, the remaining
    # columns are the values of nonzero variables.
    #
    rows = []
    vars = list(vars)
    vars.sort()
    rows.append(['obj']+vars)
    for i in range(len(results.solution)):
        row = [f[i]]
        for var in vars:
            row.append( data[i].get(var,None) )
        rows.append(row)
    print("Creating results file results.csv")
    OUTPUT = open('results.csv', 'w')
    writer = csv.writer(OUTPUT)
    writer.writerows(rows)
    OUTPUT.close()
    
    
# produce nicely formatted output
#for wl in N:
#    if value(model.y[wl]) > 0.5:
#        customers = [str(cl) for cl in M if \
#                     value(model.x[wl, cl] > 0.5)]
#        print(str(wl)+' serves customers: '+str(customers))
#    else:
#        print(str(wl)+": do not build")

#pyomo solve --solver=glpk wl_concrete.py