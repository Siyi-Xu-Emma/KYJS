import pandas as pd
import numpy as np
import random

# Constants
WEEKMINS = 7 * 24 * 60 
CHEMICAL_LIFE = 500
# Read Data
demand = pd.read_csv("Datasets/Weekly_Projections.csv")


class Tank: 
    def __init__(self, id, size):
        self.size = size
        self.remainBatchLife = 1
        self.processingStatus = 0
        self.chemicalLife = CHEMICAL_LIFE
        self.id = id
        
    def __str__(self):
        return f"tank sized {self.size}L"
    
    def replenish(self, reclaimEfficiency):
        self.chemicalLife = CHEMICAL_LIFE
        self.remainBatchLife = 1
        
        return self.size * (1- reclaimEfficiency)
    
    def processOneBatch(self, product):
        return 0
    
    def getRemainBatchLife(self):
        return self.remainBatchLife
    
    def isProcessing(self):
        return self.processingStatus
    
    def shiftProcessing(self):
        self.processingStatus = not self.processingStatus
    
    def cutBatchLife(self, product):
        self.remainBatchLife -= product.getCostPerBatch()
        
    def cutChemicalLife(self):
        self.chemicalLife -= 1
        
    def getChemicalLife(self):
        return self.chemicalLife
    
    def getId(self):
        return self.id

class Product:
    def __init__(self, id, batchLife, loadSize):
        self.id = id
        self.costPerBatch = 1 / batchLife
        # print(self.costPerBatch)
        self.loadSize = loadSize
        
    def getId(self):
        return self.id
    
    def getLoadSize(self):
        return self.loadSize
    
    def __str__(self):
        return f"Product {self.id}"
    
    def getCostPerBatch(self):
        return self.costPerBatch
    
    
        
        

###reclaimEfficiency changes with time
def getReclaimEfficiency(time):
    return random.randint(4,9)/100
    #return 0.09

def chooseProduct(tank, product, weekProducts):
    if weekProducts:
        # return weekProducts[0]
        return random.choice(weekProducts)
    else:
        print("demand met alr")
        return None
    
def turnToIdle(tanks):
    for tank in tanks:
        if tank.isProcessing():
            tank.shiftProcessing() 

def forecast(tankSize, productNum, numOfTanks, batchLifes, loadSizes, getReclaimEfficiency, demand, weeks):
    # iniitialize tanks
    tanks = []
    for id in range(numOfTanks):
        tanks.append(Tank(id, tankSize))
    usageResult = []
    

    
    ##initialize week info
    weekIndex = 0
    weekUsage = 0 
    weekProducts = []
    for i in range(productNum):  ##initialization products
        new = Product(i, batchLifes[i], loadSizes[i])
        weekProducts.append(new)
    weekDemand = {}
    for i in range(productNum):
        weekDemand[i] = demand.iloc[i, weekIndex] 
    processSpeed = sum(weekDemand.values())/WEEKMINS / numOfTanks
    currentProductsTanks = [weekProducts[0]] * numOfTanks
    remainWafersTanks = list(map(lambda x: x.getLoadSize(), currentProductsTanks))
    

    
    #######################
    ## simulation in min ##
    #######################
    predictionRange = WEEKMINS * weeks
    for time in range(0, predictionRange): 
        if not (time + 1) % WEEKMINS and weekIndex < weeks - 1: ## initiate new week after one week
            # print("\n", weekIndex, weekDemand)
            weekIndex += 1
            weekDemand = {}
            for i in range(productNum):
                weekDemand[i] = demand.iloc[i, weekIndex]
            processSpeed = sum(weekDemand.values())/WEEKMINS / numOfTanks
            
            
            usageResult.append(weekUsage)
            weekUsage = 0
            
            weekProducts = []
            for i in range(productNum):  ##initialization products
                new = Product(i, batchLifes[i], loadSizes[i])
                weekProducts.append(new)
            turnToIdle(tanks)
            
        for tank in tanks:
            tank.cutChemicalLife()
            # print(tank.getId(), tank.getChemicalLife())
            if tank.getChemicalLife() <= 0:
                weekUsage += tank.replenish(getReclaimEfficiency(time))
                ## print(tank.getId(), "replenish chemicalLife", tank.getId())       
    
        ### Start processing
            if not tank.isProcessing():
                tank.shiftProcessing()
            ## put in new batch and start processing
                currentProductsTanks[tank.getId()] = chooseProduct(tank, currentProductsTanks[tank.getId()], weekProducts)
                if not currentProductsTanks[tank.getId()]:
                    continue
                remainWafersTanks[tank.getId()] = currentProductsTanks[tank.getId()].getLoadSize()
            ### cut remainbatchlife
                tank.cutBatchLife(currentProductsTanks[tank.getId()])
                if tank.getRemainBatchLife() <= 0:
                    # print(tank.getRemainBatchLife())
                    ## replenish
                    ## print(tank.getId(), "replenish", currentProductsTanks[tank.getId()])
                    weekUsage += tank.replenish(getReclaimEfficiency(time))
                    
            if currentProductsTanks[tank.getId()]:
                weekDemand[currentProductsTanks[tank.getId()].getId()] -= processSpeed
                #print(weekDemand)
                if weekDemand[currentProductsTanks[tank.getId()].getId()] <= 0:
                    if tank.isProcessing():
                        tank.shiftProcessing()
                    for h in range(len(weekProducts)):
                        if weekProducts[h].getId() == currentProductsTanks[tank.getId()].getId():
                            weekProducts.pop(h)
                            break               
            
            remainWafersTanks[tank.getId()] -= processSpeed
            if remainWafersTanks[tank.getId()] <= 0:  ### end one batch
                if tank.isProcessing():
                    tank.shiftProcessing()
            
    usageResult.append(weekUsage)
    return usageResult



#Test
# Parameter predefined
tankSize =80
numOfProducts = 2
batchLifes = [5, 7]
loadSizes = [35, 48]
numOfTanks = 1
weeks = 5
# Print Results
#print(forecast(tankSize, numOfProducts, numOfTanks, batchLifes,loadSizes, getReclaimEfficiency, demand, weeks))


