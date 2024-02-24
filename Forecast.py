import pandas as pd
import numpy as np
import random

# Constants
WEEKMINS = 7 * 24 * 60 
chemicalLife = 500





# Read Data
demand = pd.read_csv("Datasets/Weekly_Projections.csv")
print(demand)


class Tank: 
    def __init__(self, size):
        self.size = size
        self.remainBatchLife = 1
        self.processingStatus = 0
        
    def __str__(self):
        return f"tank sized {self.size}L"
    
    def replenish(self, reclaimEfficiency):
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

class Product:
    def __init__(self, id, batchLife, loadSize):
        self.id = id
        self.remain = 0
        self.costPerBatch = 1 / batchLife
        self.loadSize = loadSize
        
    def getId(self):
        return self.id
    
    def getLoadSize(self):
        return self.loadSize
    
    def __str__(self):
        return f"Product {self.id}"
    
    def getCostPerBatch(self):
        return self.getCostPerBatch
    
    
        
        
tank = Tank(80)

###reclaimEfficiency changes with time
def reclaimEfficiency(time):
    return random.randint(4,9)/10

#### no replenishment at the end of the week

def forecast(tankSize, productNum, batchLifes, loadSizes, reclaimEfficiency, demand, weeks):
    tank = Tank(80)
    products = []
    predictionRange = WEEKMINS * weeks
    usageResult = []
    
    for i in range(productNum):  ##initialization products
        new = Product(i, batchLifes[i], loadSizes[i])
        products.append(new)
    
    
        
    weekUsage = 0 ##initialize week info
    weekIndex = 0
    weekDemand = []
    for i in range(productNum):
        weekDemand.append(demand.iloc[i, weekIndex])   
    processSpeed = sum(weekDemand)/WEEKMINS
    
    for time in range(0, predictionRange): ## predictionRange in min
        if not time % chemicalLife: ## replenish when chemical life reached replenish at start
            weekUsage += tank.replenish(reclaimEfficiency(time))
        
        ### Start processing
        
        if not tank.isProcessing():
            tank.shiftProcessing()
            ## put in new batch and start processing
            currentProduct = random.choice(products)
            
            remainWafers = currentProduct.getLoadSize()
            
            ### cut remainbatchlife
            tank.cutBatchLife(currentProduct)
            if tank.getRemainBatchLife() <= 0:
                ## replenish
                weekUsage += tank.replenish(reclaimEfficiency(time))
        
        remainWafers -= precre
                
        
        
            
        
        ### check remainbatchLife
        
        
        if not (time + 1) % WEEKMINS and weekIndex < weeks - 1: ## initiate new week after one week
            weekIndex += 1
            print(weekIndex)
            weekDemand = []
            for i in range(productNum):
                weekDemand.append(demand.iloc[i, weekIndex])
            processSpeed = sum(weekDemand)/WEEKMINS
            usageResult.append(weekUsage)
            weekUsage = 0
        

            
        
    return usageResult



#Test

# Parameter predefined
reclaimEfficiency = 0.09
batchLifes = [7, 8]
loadSizes = [38, 50]
# Print Results
print(forecast(80, 2, batchLifes,loadSizes, reclaimEfficiency, demand, 10))