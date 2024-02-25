import pandas as pd
import numpy as np
import random
SIMULATION_RANGE = 10
TOTAL_STEPS_ID = 4
SWITCH_TIME = pd.read_csv("switchTime.csv")
RECIPE_COST = pd.read_csv("recipeCost.csv")
recipeTime = [4, 3, 5, 2, 6]
equipmentData = ([0, 1, 3, 4],[1, 2, 4],[0, 2, 3])
stepData = ([0,1,3], [2,4], [1,3,4], [1,2],[0,2,3])
MINIMUM_POSSIBILITY = 0.01
NORMAL_POSSIBILITY = 0.5
MAXIMUM_POSSIBILITY = 0.9
recipeTimePrio = [4, 3, 5, 2, 6]
recipeCostPrio = [3, 2, 5, 1,4]
stepPrio = [2, 4, 6, 8]


class Lot: ### Init every lot with a recipe and then can change with every steps completed 
    def __str__(self):
        return f"Lot{self.id}"
    
    def __init__(self, id, step, recipe):  
        self.id = id
        self.step = step
        self.recipe = recipe
        
    def getId(self):
        return self.id
    
    def getStep(self):
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
        
    def getRemainingTime(self):
        return self.remainingTime
    def targetLot(self):
        return -1
class Processing(State):
    def __init__(self, lot):
        super().__init__(1) 
        self.lot = lot
        self.remainingTime = recipeTime[self.lot.getRecipe()]
        
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

def overlap(list1, list2):
    # Convert lists to sets to find the overlapping elements
    set1 = set(list1)
    set2 = set(list2)

    # Find the overlapping elements
    overlapping_elements = set1.intersection(set2)

    # Convert the result back to a list if needed
    overlapping_elements_list = list(overlapping_elements)

    return overlapping_elements_list  

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
    for id in range(len(chosenEvents)):
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
    MlotId = -1
    eventsDict = {}
    
    ### Start simulation per 'time'
    for time in range(SIMULATION_RANGE):
        eventsDict = {}
        for _ in range(len(startingEquipmentList)):
            eventsDict[_] = [[],[]]
        ### lotslist lists here
        for equipment in currentEquipmentList:
            if equipment.getStateId() == 0:
                pass
            elif equipment.getStateId() == 1:
                currlot = equipment.getState().getProcessedLot()
                if equipment.getState().getRemainingTime() == recipeTime[equipment.getState().getProcessedLot().getRecipe()]:
                    ### start a new step
                    if not currlot.getStep() == 0:
                        ### new lot
                        lotsAvailable.remove(equipment.getState().getProcessedLot())
                    
                elif equipment.getState().getRemainingTime() == 1: ## ending one step
                    if not currlot.getStep() == TOTAL_STEPS_ID: ### not complete yet
                        lotsAvailable.append(currlot)
                
            elif equipment.getStateId() == 2:
                if equipment.getState().getRemainingTime() == 1: #ending switching
                    lotsAvailable.remove(equipment.getState().getEndLot())
            
                    
        
        
        
        
        
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
                    # remain idle
                    eventsDict[equipment.getId()][0].append(Idle())
                    eventsDict[equipment.getId()][1].append(MINIMUM_POSSIBILITY)
                    
                    # turn to processing
                    if not lotsAvailable:# if no available then create a new lot
                        MLotId += 1
                        if overlap(stepData[0], recipeList): # and time <= SIMULATION_RANGE - 14: ## if definitely cannot complete a new lot
                            for recipe in overlap(stepData[0], recipeList):
                                newLot = Lot(MLotId, 0, recipe)
                                eventsDict[equipment.getId()][0].append(Processing(newLot))
                                eventsDict[equipment.getId()][1].append(NORMAL_POSSIBILITY)
                                
                                ### profit calculation here
                                
                    else: ## choose lots that have more steps and start processing
                        for lotChosen in lotsAvailable:
                            if overlap(stepData[lotChosen.getStep() + 1], recipeList):# and time <= SIMULATION_RANGE - (TOTAL_STEPS_ID - lotChosen.getStep()) * 3:
                                for recipe in overlap(stepData[lotChosen.getStep() + 1],recipeList):
                                    ### process available lot startp rocessing
                                    newLot = Lot(lotChosen.getId(), lotChosen.getStep() + 1, recipe)
                                    eventsDict[equipment.getId()][0].append(Processing(newLot))
                                    eventsDict[equipment.getId()][1].append(NORMAL_POSSIBILITY)
                    
                        
                            

                            
                elif equipment.getStateId() == 1: # is Processing
                    ## turn to Idle
                    eventsDict[equipment.getId()][0].append(Idle())
                    eventsDict[equipment.getId()][1].append(MINIMUM_POSSIBILITY) 
                    
                    ## can remain working 
                    for lotChosen in lotsAvailable:
                        if overlap(stepData[lotChosen.getStep() + 1], recipeList):
                            for recipe in overlap(stepData[lotChosen.getStep() + 1], recipeList):
                                newLot = Lot(lotChosen.getId(), lotChosen.getStep() + 1, recipe)
                                if recipe == equipment.getState().getProcessedLot().getRecipe():
                                    ### start processing with maximum possibility
                                    
                                    eventsDict[equipment.getId()][0].append(Processing(newLot))
                                    eventsDict[equipment.getId()][1].append(MAXIMUM_POSSIBILITY)
                                    
                                else: #switch
                                    eventsDict[equipment.getId()][0].append(Switching(equipment.getState().getProcessedLot(), newLot))
                                    eventsDict[equipment.getId()][1].append(NORMAL_POSSIBILITY)
                    remain = 0
                    for other in currentEquipmentList:
                        if other.getStateId() == 1 and other.getState.getRemainingTime():
                            remain = other.getState().getRemainingTime()
                                    
                            ## if other state doing this lot remaining time little
                            if overlap(stepData[lotChosen.getStep() + 1], recipeList):
                                for recipe in overlap(stepData[lotChosen.getStep() + 1], recipeList):
                                    if recipe != equipment.getState().getProcessedLot().getRecipe():
                                        if SWITCH_TIME.iloc[equipment.getState().getProcessedLot().getRecipe(), recipe] <= remain:
                                            newLot = Lot(lotChosen.getId(), lotChosen.getStep() + 1, recipe)
                                            newState = Switching(equipment.getState().getProcessedLot(), newLot)
                                            eventsDict[equipment.getId()][0].append(Switching(equipment.getState().getProcessedLot(), newLot))
                                            eventsDict[equipment.getId()][1].append(MAXIMUM_POSSIBILITY)
                    
                else: ## is switching
                    # has to change state
                    newState = Processing(equipment.getState().getEndLot()) 
                    eventsDict[equipment.getId()][0].append(newState)
                    eventsDict[equipment.getId()][1].append(MAXIMUM_POSSIBILITY)
                    
        # update
        events = list(eventsDict.values()) 
        # a list of 3 lists, each list containing two lists: new states and occuring weightages
        ## eg: [[[Processing@0000000F, Switching@0000000A], [2, 1]], [], []]
        chosenEvents = list(map(lambda x: choose_with_probability(x[0], x[1]), events))
        while(isConflicting(chosenEvents)):
            chosenEvents = list(map(lambda x: choose_with_probability(x[0], x[1])))
        
        
        
        
        

        
        # Update currentEquipmentList
        for id in range(len(chosenEvents)):
            if chosenEvents[id]:
                currentEquipmentList[id].changeState(chosenEvents[id])   
        
        
        sample.append(convert(currentEquipmentList))
        print(convert(currentEquipmentList))
    return (profit, x, y, z, sample)
    
    
    



### Initialization
startingEquipmentList = [Equipment(0), Equipment(1), Equipment(2)]

for simulationTime in range(1):
    maxProfit = 0
    resultPair = simulation(startingEquipmentList)
    statusList = []
    if resultPair[0] > maxProfit:
        maxProfit = resultPair[0]
        statusList = resultPair[1]

print("Maximum Profit:\n", maxProfit, "StatusList:\n", statusList)

