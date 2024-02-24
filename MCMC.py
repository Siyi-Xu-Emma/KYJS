import pandas as pd
import numpy as np
import random
SIMULATION_RANGE = 168
TOTAL_STEPS_PER_LOT = 5

class Recipe:
    def __str__(self):
        return f"Recipe{self.id}"
    
    def __init__(self, id, time):
        self.remainTime = time
        self.id = id
    
    def getId(self):
        return self.id
    
    def getRemainTime(self):
        return self.remainTime
    
    def cutRemainTime(self):
        self.remainTime -= 1

class Lot:
    def __str__(self):
        return f"Lot{self.id}"
    
    def __init__(self, id, recipe):  
        self.id = id
        self.step = TOTAL_STEPS_PER_LOT
        self.recipe = recipe
        
    def newStep(self, newRecipe):
        self.step -= 1
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
    def __init__(self, lot, recipe):
        super().__init__(1) 
        self.lot = lot
        self.recipe = recipe 
 
class Switching(State):
    def __init__(self, startRecipe, endRecipe):
        super().__init__(2) 
         
class Equipment:
    def __str__(self):
        return f"Equipment{self.id}"
    
    def __init__(self, id):
        self.id = id
        self.state = Idle()##Idle: 0 processing: 1, switching: 2
    
    def getId(self):
        return self.id

    def changeState(self, newState):
        self.state = newState
    
    def getStateId(self):
        return self.state.getId()
        
    
        

 


def simulation(startingEquipmentList):
    profit = 0
    sampleStatusList = []
    currentStatusList = startingEquipmentList
    
    
    ### Start simulation
    for i in range(SIMULATION_RANGE):
        for equipment in currentStatusList:
            if equipment.getStateId() == 0: # is idle
                
            
        
    return (profit, sampleStatusList)
    
    
    



### Initialization
startingEquipmentList = [Equipment(0), Equipment(1), Equipment(2)]

for simulationTime in range(10086):
    maxProfit = 0
    resultPair = simulation(startingEquipmentList)
    statusList = []
    if resultPair[0] > maxProfit:
        maxProfit = resultPair[0]
        statusList = resultPair[1]

print("Maximum Profit:\n", maxProfit, "StatusList:\n", statusList)

