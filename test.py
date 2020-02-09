#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 18:26:50 2019

@author: mdrahali
"""
from coopr.pyomo import *

TimePeriods = [1,2,3,4,5]
LastTimePeriod = 5
model.StartTime = Var(TimePeriods, initialize=1.0)

def Pred_rule(model, t): 
    if t == LastTimePeriod:
        return Constraint.Skip 
    else:
        return model.StartTime[t] <= model.StartTime[t+1]
    
model.Pred = Constraint(TimePeriods)

instance = model.create()
instance.pprint()
opt = SolverFactory("glpk")
results = opt.solve(instance)
results.write()