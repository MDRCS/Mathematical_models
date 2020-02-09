#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 17:29:41 2019

@author: mdrahali
"""

from coopr.pyomo import *

model = AbstractModel()
model.N = Set()
model.M = Set()
model.c = Param(model.N)
model.a = Param(model.N, model.M)
model.b = Param(model.M)
model.x = Var(model.N, within=NonNegativeReals)
  
def obj_rule(model):
    return sum(model.c[i]*model.x[i] for i in model.N)
model.obj = Objective(rule=obj_rule)
  
def con_rule(model, m):
    return sum(model.a[i,m]*model.x[i] for i in model.N) \
                 >= model.b[m]
                 
model.con = Constraint(model.M, rule=con_rule)

instance = model.create()
instance.pprint()
opt = SolverFactory("glpk")
results = opt.solve(instance)
results.write()