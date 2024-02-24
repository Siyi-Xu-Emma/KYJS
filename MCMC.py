import pandas as pd
import numpy as np
import random

class Recipe:
    def __str__(self):
        return f"Recipe{self.id}"
    
    def __init__(self, id, time):
        self.time = time
        self.id = id
    
    def getId(self):
        return self.id
    
    def getTime(self):
        return self.time
class Lot:
    def __str__(self):
        return f"Lot{self.id}"
    
    def __init__(self, id, recipe):  
        self.id = id
        self.step = 1
        self.recipe = recipe
        
    def newStep(self, newRecipe):
        self.step += 1
        self.recipe = newRecipe
        
    def getId(self):
        return self.id
    
    def getStep(self):
        return self.step
           
class Equipment:
    def __str__(self):
        return f"Equipment{self.id}"
    
    def __init__(self, id):
        self.id = id
        self.recipe = None
        self.state = 0 ##Idle: 0 processing: 1, switching: 2
    
    def getId(self):
        return self.id
    
        

 
### Initialization
currentState = [Equipment(0), Equipment(1), Equipment(2)]

def simulation(currentState):
    pass
    





print(simulation(currentState))