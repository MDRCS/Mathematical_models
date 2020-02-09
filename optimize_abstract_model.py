#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 17:34:47 2019

@author: mdrahali
"""

from coopr.opt import SolverFactory
from abstract import model
model.pprint()

instance = model.create('abstract.dat')

instance.pprint()

opt = SolverFactory("glpk")
results = opt.solve(instance)
results.write()