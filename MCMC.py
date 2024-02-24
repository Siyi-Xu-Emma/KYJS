import pandas as pd
import numpy as np
import random
SIMULATION_RANGE = 168
TOTAL_STEPS_PER_LOT = 5
SWITCH_TIME = pd.read_csv("switchTime.csv")
equipmentData = ([0, 1, 3, 4],[1, 2, 4],[0, 2, 3])

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
class Lot: ### Init every lot with a recipe and then can change with every steps completed 
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
    
    def getRemainingStep(self):
        return self.step
    
    def getRecipe(self):
        return self.recipe

class State:
    def __init__(self, id):
        self.id = id
    
    def getId(self):
        return self.id
   
class Idle(State):
    def __init__(self):
        super().__init__(0)

class Processing(State):
    def __init__(self, lot):
        super().__init__(1) 
        self.lot = lot
        self.remainingTime = self.lot.getRecipe().getTime()
        
    def getProcessedLot(self):
        return self.lot
    
    def getRemainingTime(self):
        return self.remainingTime
    
    def cutRemainingTime(self):
        self.remainingTime -= 1
 
class Switching(State):
    def __init__(self, startRecipe, endRecipe):
        super().__init__(2) 
        self.remainingTime = SWITCH_TIME.iloc[startRecipe, endRecipe]
    
    def getRemainingTime(self):
        return self.remainingTime
    
    def cutRemainingTime(self):
        self.remainingTime -= 1
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
    
    def getState(self):
        return self.state
    
        

 


def simulation(startingEquipmentList):
    profit = 0
    sampleStatusList = [startingEquipmentList]
    currentStatusList = startingEquipmentList
    
    ### Start simulation per 'time'
    for i in range(SIMULATION_RANGE):
        for equipment in currentStatusList:
            recipeList = equipmentData[equipment.getId()]
            if equipment.getStateId() == 0: # is idle
            
            elif equipment.getStateId() == 1: # is Processing
            
            else: ## is switching
                
            
                
        sampleStatusList.append(currentStatusList)
            
        
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

