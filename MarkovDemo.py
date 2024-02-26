import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
import numpy as np
import random
SIMULATION_RANGE = 150
TOTAL_STEPS_ID = 4
SWITCH_TIME = pd.read_csv("switchTime.csv")
RECIPE_COST = pd.read_csv("recipeCost.csv")
PRICING = pd.read_csv("Pricing.csv")
recipeTime = [4, 3, 5, 2, 6]
equipmentData = ([0, 1, 3, 4],[1, 2, 4],[0, 2, 3])
stepData = ([0,1,3], [2,4], [1,3,4], [1,2],[0,2,3])
price_per_lot = 40000

# testing and protective constants
MAX_LOOP_RANGE = 1000

## Probability assumptions(simple)
MINIMUM_POSSIBILITY = 0.05 # for idle
SCARCE_POSSIBILITY = 0.15
NORMAL_POSSIBILITY = 0.5 # equal choices
MAXIMUM_POSSIBILITY = 100


# priority
stateIdPrio = [MINIMUM_POSSIBILITY,0.7,0.2]
recipeTimePrio = [4, 3, 5, 2, 6] ## negatively
recipeCostPrio = [6, 3, 5, 0.2, 4]
stepPrio = [1, 2, 4, 6, 8]

def weightage(state, time):
    if state.getId() == 1:
        recipe = state.getProcessedLot().getRecipe()
        step = state.getProcessedLot(). getStep()
        if time <= SIMULATION_RANGE - 14:
            return stateIdPrio[1] * recipeCostPrio[recipe]/recipeTimePrio[recipe] * stepPrio[step]
        else:
            return stateIdPrio[1] * recipeCostPrio[recipe]/recipeTimePrio[recipe] * stepPrio[step]
            
    elif state.getId() == 2:
        recipe = state.getEndLot().getRecipe()
        step = state.getEndLot(). getStep()
        if time <= SIMULATION_RANGE - 14:
            return stateIdPrio[1] * recipeCostPrio[recipe]/recipeTimePrio[recipe] * stepPrio[step]
        else:
            return stateIdPrio[1] * recipeCostPrio[recipe] /recipeTimePrio[recipe]/recipeTimePrio[recipe] * stepPrio[step]
    else:
        if time <= SIMULATION_RANGE - 14:
            return MINIMUM_POSSIBILITY
        else:
            return NORMAL_POSSIBILITY


class Lot: 
    ### Init every lot with a recipe and then can change with every steps completed 
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
    def __str__(self):
        return f"State{self.id} "
class Idle(State):
    def __init__(self):
        super().__init__(0)
        self.remainingTime = 1
    def __str__(self):
        return 'idle'
    
    def cutRemainingTime(self):
        self.remainingTime -= 1
        
    def getRemainingTime(self):
        return self.remainingTime
    def targetLot(self):
        return self
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

    def __str__(self):
        return 'processing' + self.lot
    def targetLot(self):
        return self.lot.getId()
    
class Switching(State):
    def __init__(self, startLot, endLot):
        super().__init__(2) 
        self.startLot = startLot
        self.endLot = endLot
        startRecipe = startLot.getRecipe()
        endRecipe = endLot.getRecipe()
        self.remainingTime = int(SWITCH_TIME.iloc[startRecipe, endRecipe])
    def __str__(self):
        return 'switching from ' + self.startLot + ' to ' + self.endtLot 
       
    def getRemainingTime(self):
        return self.remainingTime
    
    def cutRemainingTime(self):
        self.remainingTime -= 1
        
    def getEndLot(self):
        return self.endLot  
    
    def targetLot(self):
        return self.endLot.getId()
    def getStartLot(self):
        return self.startLot
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
            currentLot = equipment.getState().getProcessedLot()
            result.append([currentLot.getId(), currentLot.getRecipe(), currentLot.getStep()])
        if equipment.getStateId() == 2:
            result.append(['switch'] * 3)
    return result

def choose_with_probability(choices, probabilities): 
    ### Choose one of the choices according to their probabilities.
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
                    #print(state.targetLot(), otherState.targetLot())
                    return True
        return False
    elif count == 2:
        x = chosenEvents[eventIdList[0]]
        y = chosenEvents[eventIdList[1]]
        if x.targetLot() == y.targetLot():
            #print(x.targetLot(), y.targetLot())
            return True
        return False
            
    else:
        return False

def tweak(chosenEvents):
    flag = {}
    for i in range(len(chosenEvents)):
        if chosenEvents[i]:
            flag[chosenEvents[i].targetLot] = 1
            for j in range(len(chosenEvents)):
                if (not j == i) and (chosenEvents[j] and chosenEvents[i].targetLot in flag):
                    chosenEvents[j] = Idle()
    return chosenEvents
                           
def exclude(lotsAvailable, lot):
    return list(filter(lambda x: not x.getId() == lot.getId(), lotsAvailable))

def addMaterials(i, materials):
    for m in range(len(materials)):
        materials[m] += int(RECIPE_COST.iloc[m, i])
    return materials
   
def canAdd(lst, lot):
    for other in lst:
        if other.getId() == lot.getId():
            return False
    return True           
def simulation(startingEquipmentList):
    profit = 0
    materials = [0, 0, 0]
    recipeUsed = [0, 0, 0, 0, 0]
    totalRevenue = 0

    
    currentEquipmentList = startingEquipmentList
    
    lotsAvailable = []
    MLotId = -1
    eventsDict = {}
    
    ### initialize three lots
    for i in range(3):
        currentEquipmentList[i].changeState(Processing(Lot(i,0, random.choice(overlap(stepData[0], equipmentData[i])))))
    sample = [convert(currentEquipmentList)]
    ### Start simulation per 'time'
    for time in range(SIMULATION_RANGE):
        
        print(currentEquipmentList[0].getState().getRemainingTime(), \
            currentEquipmentList[1].getState().getRemainingTime(), \
                currentEquipmentList[2].getState().getRemainingTime())
        
        eventsDict = {}
        for _ in range(len(startingEquipmentList)):
            eventsDict[_] = [[],[]]
        ### lotslist lists here
        excludeLst = []
        for equipment in currentEquipmentList:
            if equipment.getStateId() == 0:
                pass
            elif equipment.getStateId() == 1:
                currlot = equipment.getState().getProcessedLot()
                if equipment.getState().getRemainingTime() == \
                    recipeTime[equipment.getState().getProcessedLot().getRecipe()]:
                    ### start a new step
                    materials = addMaterials(currlot.getRecipe(), materials)
                    recipeUsed[currlot.getRecipe()] += 1
                    if not currlot.getStep() == 0:
                        ### new lot
                        #print("remove", currlot)
                        lotsAvailable = exclude(lotsAvailable, currlot)
                    else:
                        MLotId += 1
                    
                if equipment.getState().getRemainingTime() == 1: ## ending one step
                    if not currlot.getStep() == TOTAL_STEPS_ID: ### not complete yet
                        #print("add to available", currlot, currlot.getRecipe(), currlot.getStep())
                        lotsAvailable = exclude(lotsAvailable, currlot)
                        if canAdd(excludeLst, currlot):
                            lotsAvailable.append(currlot)
                    else:
                        excludeLst.append(currlot)
                        profit += price_per_lot
                        totalRevenue += price_per_lot
                
            elif equipment.getStateId() == 2:
                if equipment.getState().getRemainingTime() == \
                    int(SWITCH_TIME.iloc[equipment.getState().getStartLot().getRecipe(), \
                        equipment.getState().getEndLot().getRecipe()]):
                    #print("remove", equipment.getState().getEndLot())
                    lotsAvailable = exclude(lotsAvailable, equipment.getState().getEndLot())
                    excludeLst.append( equipment.getState().getEndLot())
                    
        for currlot in lotsAvailable:
            print("current ava", currlot, currlot.getRecipe(), currlot.getStep())       
        print("maximum id:", MLotId)
        
        
        
        
        
        
        ### event possibilities
        for equipment in currentEquipmentList:
            equipment.getState().cutRemainingTime()
            '''print(currentEquipmentList[0].getState().getRemainingTime(), \
                currentEquipmentList[1].getState().getRemainingTime(), \
                    currentEquipmentList[2].getState().getRemainingTime())'''
            
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
                    
                    ##protection:
                    if time > SIMULATION_RANGE-14 and len(lotsAvailable) <= 1:
                        eventsDict[equipment.getId()][0].append(Idle())
                        eventsDict[equipment.getId()][1].append(SCARCE_POSSIBILITY)                         
                    
                    # turn to processing
                    if not lotsAvailable:# if no available then create a new lot
                        #print('no ava')
                        temLotId = MLotId + 1
                        if overlap(stepData[0], recipeList)\
                            and time <= SIMULATION_RANGE - 14: ## if definitely cannot complete a new lot
                            for recipe in overlap(stepData[0], recipeList):
                                newLot = Lot(temLotId, 0, recipe)
                                #print(newLot)
                                _ = Processing(newLot)
                                eventsDict[equipment.getId()][0].append(_)
                                eventsDict[equipment.getId()][1].append(weightage(_, time)) ## normal
                    else:  ## can still create lot but minimum possibility
                        #print("have")
                        temLotId = MLotId + 1
                        if overlap(stepData[0], recipeList)\
                            and time <= SIMULATION_RANGE - 14: ## if definitely cannot complete a new lot
                            for recipe in overlap(stepData[0], recipeList):
                                newLot = Lot(temLotId, 0, recipe)
                                eventsDict[equipment.getId()][0].append(Processing(newLot))
                                eventsDict[equipment.getId()][1].append(MINIMUM_POSSIBILITY)                        
                        
                                ### profit calculation here
                                
                    ## choose lots that have more steps and start processing
                        for lotChosen in lotsAvailable:
                            if overlap(stepData[lotChosen.getStep() + 1], recipeList):
                                # and time <= SIMULATION_RANGE - (TOTAL_STEPS_ID - lotChosen.getStep()) * 3:
                                for recipe in overlap(stepData[lotChosen.getStep() + 1],recipeList):
                                    ### process available lot start processing
                                    newLot = Lot(lotChosen.getId(), lotChosen.getStep() + 1, recipe)
                                    _ = Processing(newLot)
                                    eventsDict[equipment.getId()][0].append(_)
                                    eventsDict[equipment.getId()][1].append(weightage(_, time))
                    
                        
                            

                            
                elif equipment.getStateId() == 1: # is Processing
                    ## turn to Idle
                    eventsDict[equipment.getId()][0].append(Idle())
                    eventsDict[equipment.getId()][1].append(MINIMUM_POSSIBILITY) 
                    
                    ## create a new lot if no available
                    if not lotsAvailable:# if no available then create a new lot
                        temLotId = MLotId + 1
                        if overlap(stepData[0], recipeList)\
                            and time <= SIMULATION_RANGE - 14: ## if definitely cannot complete a new lot
                            for recipe in overlap(stepData[0], recipeList):
                                newLot = Lot(temLotId, 0, recipe)
                                _ = Processing(newLot)
                                eventsDict[equipment.getId()][0].append(_)
                                eventsDict[equipment.getId()][1].append(weightage(_, time)) ## normal possibilities
                    else:
                        temLotId = MLotId + 1
                        if overlap(stepData[0], recipeList)\
                            and time <= SIMULATION_RANGE - 14: ## if definitely cannot complete a new lot
                            for recipe in overlap(stepData[0], recipeList):
                                newLot = Lot(temLotId, 0, recipe)
                                if recipe == equipment.getState().getProcessedLot().getRecipe():
                                    ### start processing with maximum possibility
                                    _ = Processing(newLot)
                                    eventsDict[equipment.getId()][0].append(_)
                                    eventsDict[equipment.getId()][1].append(SCARCE_POSSIBILITY) ### maximum possibilities
                                else:
                                    _ = Switching(equipment.getState().getProcessedLot(), newLot)
                                    eventsDict[equipment.getId()][0].append(_)
                                    eventsDict[equipment.getId()][1].append(MINIMUM_POSSIBILITY) ###normal possibilities
                                    
                                                                
                    ## can remain working 
                    for lotChosen in lotsAvailable:
                        if overlap(stepData[lotChosen.getStep() + 1], recipeList):
                            for recipe in overlap(stepData[lotChosen.getStep() + 1], recipeList):
                                newLot = Lot(lotChosen.getId(), lotChosen.getStep() + 1, recipe)
                                if recipe == equipment.getState().getProcessedLot().getRecipe():
                                    ### start processing with maximum possibility
                                    _ = Processing(newLot)
                                    eventsDict[equipment.getId()][0].append(_)
                                    eventsDict[equipment.getId()][1].append(weightage(_, time)) ### maximum possibilities
                                    
                                else: #switch
                                    _ = Switching(equipment.getState().getProcessedLot(), newLot)
                                    eventsDict[equipment.getId()][0].append(_)
                                    eventsDict[equipment.getId()][1].append(weightage(_, time)) ###normal possibilities
                    remain = 0
                    for other in currentEquipmentList:
                        if other.getStateId() == 1 and other.getState().getRemainingTime():
                            remain = other.getState().getRemainingTime()
                                    
                            ## if other state doing this lot remaining time little
                            if other.getState().getProcessedLot().getStep() < TOTAL_STEPS_ID:
                                for recipe in overlap(stepData[other.getState().getProcessedLot().getStep() + 1], recipeList):
                                    if not recipe == equipment.getState().getProcessedLot().getRecipe():
                                        if int(SWITCH_TIME.iloc[equipment.getState().\
                                            getProcessedLot().getRecipe(), recipe]) >= remain:
                                            newLot = Lot(other.getState().getProcessedLot().getId(), \
                                                other.getState().getProcessedLot().getStep() + 1, recipe)
                                            newState = Switching(equipment.getState().getProcessedLot(), newLot)
                                            eventsDict[equipment.getId()][0].append(newState)
                                            eventsDict[equipment.getId()][1].append(MAXIMUM_POSSIBILITY)
                    
                else: ## is switching
                    # has to change state
                    newState = Processing(equipment.getState().getEndLot()) 
                    eventsDict[equipment.getId()][0].append(newState)
                    eventsDict[equipment.getId()][1].append(MAXIMUM_POSSIBILITY)
                    
        # update
        #print("event dict: \n", eventsDict)
        events = list(eventsDict.values()) 
        # a list of 3 lists, each list containing two lists: new states and occuring weightages
        ## eg: [[[Processing@0000000F, Switching@0000000A], [2, 1]], [], []]
        chosenEvents = list(map(lambda x: choose_with_probability(x[0], x[1]), events))
        count = 0
        while(isConflicting(chosenEvents)):
            # print("true")
            chosenEvents = list(map(lambda x: choose_with_probability(x[0], x[1]), events))
            count +=1
            if count >= MAX_LOOP_RANGE:
                chosenEvents = tweak(chosenEvents)
                break
                
        
        
        
        # Update currentEquipmentList
        for id in range(len(chosenEvents)):
            if chosenEvents[id]:
                currentEquipmentList[id].changeState(chosenEvents[id])   
        # Record result
        r = convert(currentEquipmentList)
        sample.append(r)
        print(time, r)
        
        ####
    # calculate profit 
    prices = []
    for m in range(len(materials)):
            if materials[m] <= 50:# col = 0
                profit -= materials[m] * int(PRICING.iloc[m, 0])
            elif materials[m] <= 500:# col = 1
                profit -= materials[m] * int(PRICING.iloc[m, 1])
            else: # col = 2
                profit -= materials[m] * int(PRICING.iloc[m, 2])
        
        
    return (profit, sample, totalRevenue, materials, recipeUsed)
    
    
    


### test weightage
A = {}
A[0] = Lot(0, 1, 3)
A[1] = Lot(0, 2, 1)
A[2] = Lot(0, 4, 2)
A[3] = Lot(0, 1, 4)
A[4] = Lot(0, 3, 1)
A[5] = Lot(0, 4, 3)
A[6] = Lot(0, 2, 2)
for i in range(5):
    print(weightage(Processing(A[i]),0), weightage(Processing(A[i]),SIMULATION_RANGE-1), weightage(Switching(A[i], A[i+1]),0), weightage(Switching(A[i], A[i+1]),SIMULATION_RANGE-1))



### Initialization

maxProfit = 0
totalRevenue = 0
materials = []
recipeUsed = []
for _ in range(1):
    print(_)
    startingEquipmentList = [Equipment(0), Equipment(1), Equipment(2)]
    resultPair = simulation(startingEquipmentList)
    if resultPair[0] >= maxProfit:
        maxProfit = resultPair[0]
        statusList = resultPair[1]
        totalRevenue = resultPair[2]
        materials = resultPair[3]
        recipeUsed = resultPair[4]
        
        
    # print(resultPair[0])


print("\nStatusList:\n", pd.DataFrame(statusList))
print("Maximum Profit:", maxProfit)
print(f"totalRevenue: {totalRevenue}\ntotalCost: {totalRevenue - maxProfit}\ncompletedLots: {totalRevenue//price_per_lot}")
print("materials: ", materials)
print("recipes: ", recipeUsed)


