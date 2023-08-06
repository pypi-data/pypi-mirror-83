

# def Conductance(r):
#     # Look at functions as objects
#     # https://medium.com/python-pandemonium/function-as-objects-in-python-d5215e6d1b0d
#     return 1/r

# def __call__(r): #conductance
#     return 1/r 

import sys


def InSeries(g_list):
    sumOfInverse = sum([1/g for g in g_list])
    return 1/sumOfInverse

def InParallel(g_list):
    return sum(g_list)


#callable function for the module
class MyModule(sys.modules[__name__].__class__):
    def __call__(self, r): #conductance
        return 1/r 
sys.modules[__name__].__class__ = MyModule