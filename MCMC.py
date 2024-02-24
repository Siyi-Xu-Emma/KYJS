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
class State:
    def __init__(self, id):
        self.id = id
    
    def getId(self):
        return self.id
   
class Idle(State):
    def __init__(self):
        super().__init__(0)

class Processing(State):
    def __init__(self):
        super().__init__(1)  
 
class Switching(State):
    def __init__(self):
        super().__init__(2)          
class Equipment:
    def __str__(self):
        return f"Equipment{self.id}"
    
    def __init__(self, id):
        self.id = id
        self.recipe = None
        self.state = Idle()##Idle: 0 processing: 1, switching: 2
    
    def getId(self):
        return self.id
    
    def changeState(self, state):
        self.state = state
    
    def getStateId(self):
        return self.state.getId()
        
    
        

 
### Initialization
startingEquipmentList = [Equipment(0), Equipment(1), Equipment(2)]

def simulation(startingEquipmentList):
    pass
    





print(simulation(startingEquipmentList))