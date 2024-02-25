import pandas as pd
import numpy as np
import random
SIMULATION_RANGE = 168
TOTAL_STEPS_PER_LOT = 5
SWITCH_TIME = pd.read_csv("switchTime.csv")
RECIPE_COST = pd.read_csv("recipeCost.csv")
equipmentData = ([0, 1, 3, 4],[1, 2, 4],[0, 2, 3])
stepData = ([], [], [], [],[])
MINIMUM_POSSIBILITY = 0.01
NORMAL_POSSIBILITY = 0.5
MAXIMUM_POSSIBILITY = 0.9

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
        self.remainingTime = 1
    
    def cutRemainingTime(self):
        self.remainingTime -1
    
    def targetLot(self):
        return -1
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
    
    def targetLot(self):
        return self.lot.getId()
class Switching(State):
    def __init__(self, startLot, endLot):
        super().__init__(2) 
        self.startLot = startLot
        self.endLot = endLot
        startRecipe = startRecipe.getRecipe().getId()
        endRecipe = endRecipe.getRecipe().getId()
        self.remainingTime = SWITCH_TIME.iloc[startRecipe, endRecipe]
    
    def getRemainingTime(self):
        return self.remainingTime
    
    def cutRemainingTime(self):
        self.remainingTime -= 1
        
    def getEndLot(self):
        return self.endLot  
    
    def targetLot(self):
        return self.endLot.getId()
      
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
    
def convert(currentEquipmentList):
    result = []
    for equipment in currentEquipmentList:
        if equipment.getStateId() == 0:
            result.append(['idle'] * 3)
        if equipment.getStateId() == 1:
            result.append([equipment.getState().getProcessedLot().getId(), equipment.getState().getRecipe().getId(), equipment.getState().getProcessedLot().getStep()])
        if equipment.getStateId() == 2:
            result.append(['switch'] * 3)

def choose_with_probability(choices, probabilities): ### Choose one of the choices according to their probabilities.
    if not choices:
        return None
    if len(choices) != len(probabilities):
        raise ValueError("Length of choices and probabilities should be the same.")
    # Normalize probabilities to sum up to 1
    total_probability = sum(probabilities)
    normalized_probabilities = [p / total_probability for p in probabilities]
    # Choose one item based on probabilities
    choice = random.choices(choices, weights=normalized_probabilities, k=1)[0]
    return choice 

def isConflicting(chosenEvents):
    count = 0
    eventIdList = []
    for id in len(chosenEvents):
        if chosenEvents[id]:
            count += 1
            eventIdList.append(id)
    if count == 3: ### three new events chosen
        for state in chosenEvents:
            for otherState in chosenEvents:
                if (not state == otherState) and (state.targetLot() == otherState.targetLot()):
                    return True
        return False
    elif count == 2:
        x = chosenEvents[eventIdList[0]]
        y = chosenEvents[eventIdList[1]]
        if x.targetLot() == y.targetLot():
            return True
        return False
            
    else:
        return False
        
def simulation(startingEquipmentList):
    profit = 0
    x = 0
    y = 0
    z = 0

    sample = []
    currentEquipmentList = startingEquipmentList
    lotsAvailable = []
    lotsUncompleted = []
    MlotId = -1
    eventsDict = {}
    
    ### Start simulation per 'time'
    for i in range(SIMULATION_RANGE):
        eventsDict = {}
        for i in range(len(startingEquipmentList)):
            eventsDict[i] = []
        
        for equipment in currentEquipmentList:
            equipment.getState().cutRemainingTime()
            recipeList = equipmentData[equipment.getId()]
            if equipment.getState().getRemainingTime() > 0:
                #### Need not change state
                if equipment.getStateId() == 1: # is Processing
                    pass
                else: ## is switching
                    pass
                
            else: ### Need to change state
                if equipment.getStateId() == 0: ## is Idle
                    # from available lots choose the one with less steps left to do newstep
                        # equally choose recipe
                    
                    
                    # if no available then create a new lot 
                    if not lotsAvailable:
                        MLotId += 1
                        chosenRecipe = choose_with_probability(recipeList, len(recipeList) * [NORMAL_POSSIBILITY])
                        lotsAvailable.append(Lot(MLotId, chosenRecipe))
                    
                        
                        
                elif equipment.getStateId() == 1: # is Processing
                    # choice: 
                    pass
                    
                else: ## is switching
                    # has to change state
                    newState = Processing(equipment.getState().getEndLot()) 
                    equipment.changeState(newState)
        # update
        events = list(eventsDict.values()) 
        # a list of 3 lists, each list containing two lists: new states and occuring weightages
        ## eg: [[[Processing@0000000F, Switching@0000000A], [2, 1]], [], []]
        chosenEvents = list(map(lambda x: choose_with_probability(x[0], x[1])))
        while(isConflicting(chosenEvents)):
            chosenEvents = list(map(lambda x: choose_with_probability(x[0], x[1])))
        
        for id in range(len(chosenEvents)):
            if chosenEvents[id]:
                currentEquipmentList[id].changeState(chosenEvents[id])   
        
        sample.append(convert(currentEquipmentList))
        
    return (profit, x, y, z, sample)
    
    
    



### Initialization
startingEquipmentList = [Equipment(0), Equipment(1), Equipment(2)]

for simulationTime in range(1008600):
    maxProfit = 0
    resultPair = simulation(startingEquipmentList)
    statusList = []
    if resultPair[0] > maxProfit:
        maxProfit = resultPair[0]
        statusList = resultPair[1]

print("Maximum Profit:\n", maxProfit, "StatusList:\n", statusList)

