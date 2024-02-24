import pandas as pd
import numpy as np
import random

# Constants
WEEKMINS = 7 * 24 * 60 
CHEMICAL_LIFE = 500
# Read Data
demand = pd.read_csv("Datasets/Weekly_Projections.csv")
# print(demand)


class Tank: 
    def __init__(self, size):
        self.size = size
        self.remainBatchLife = 1
        self.processingStatus = 0
        self.chemicalLife = CHEMICAL_LIFE
        
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
    #return random.randint(4,9)/10
    return 0.04

def chooseProduct(tank, product, weekProducts):
    if weekProducts:
        #print(weekProducts[0])
        # return weekProducts[0]
        return random.choice(weekProducts)
    else:
        print("demand met alr")
        return None
    
    

def forecast(tankSize, productNum, batchLifes, loadSizes, getReclaimEfficiency, demand, weeks):
    tank = Tank(80)
    products = []
    predictionRange = WEEKMINS * weeks
    usageResult = []
    
    for i in range(productNum):  ##initialization products
        new = Product(i, batchLifes[i], loadSizes[i])
        products.append(new)
    weekProducts = products
    
        
    weekUsage = 0 ##initialize week info
    weekIndex = 0
    weekDemand = {}
    currentProduct = weekProducts[0]
    for i in range(productNum):
        weekDemand[i] = demand.iloc[i, weekIndex] 
    processSpeed = sum(weekDemand.values())/WEEKMINS
    
    ## simulation in min
    for time in range(0, predictionRange): 
        if not time % CHEMICAL_LIFE: ## replenish when chemical life reached replenish at start
            tank.cutChemicalLife()
            if tank.getChemicalLife() <= 0:
                amount = tank.replenish(getReclaimEfficiency(time))
                weekUsage += amount
                print("replenish chemicalLife", amount)
            
        ### Start processing
        if not tank.isProcessing():
            ## put in new batch and start processing
            currentProduct = chooseProduct(tank, currentProduct, weekProducts)
            #print(currentProduct)
            if currentProduct:
                remainWafers = currentProduct.getLoadSize()
                
                ### cut remainbatchlife
                tank.cutBatchLife(currentProduct)
                #print(tank.getRemainBatchLife())
                if tank.getRemainBatchLife() <= 0:
                    print(tank.getRemainBatchLife())
                    ## replenish
                    print("replenish", currentProduct)
                    weekUsage += tank.replenish(getReclaimEfficiency(time))
                tank.shiftProcessing()
 
        if currentProduct:    
            #print(weekDemand, weekProducts, currentProduct)
            weekDemand[currentProduct.getId()] -= processSpeed
            # print(weekDemand)
            if weekDemand[currentProduct.getId()] <= 0:
                # print(weekDemand[currentProduct.getId()] )
                if tank.isProcessing():
                    tank.shiftProcessing()
                weekDemand.pop(currentProduct.getId())  
                # print(weekProducts, currentProduct)
                
                for h in range(len(weekProducts)):
                    if weekProducts[h].getId() == currentProduct.getId():
                        # print("finish one",h,len(weekProducts))
                        weekProducts.pop(h)
                        break

            # print(remainWafers)              
            remainWafers -= processSpeed
            if remainWafers <= 0:  ### end one batch
                if tank.isProcessing():
                    tank.shiftProcessing()
            

                
        ### check remainbatchLife
        if not (time + 1) % WEEKMINS and weekIndex < weeks - 1: ## initiate new week after one week
            # print("\n", weekDemand)
            weekIndex += 1
            weekDemand = {}
            for i in range(productNum):
                weekDemand[i] = demand.iloc[i, weekIndex]
            processSpeed = sum(weekDemand.values())/WEEKMINS
            
            
            usageResult.append(weekUsage)
            weekUsage = 0
            
            weekProducts = []
            for i in range(productNum):  ##initialization products
                new = Product(i, batchLifes[i], loadSizes[i])
                weekProducts.append(new)
                
            print(weekIndex, weekDemand, processSpeed)
            for product in weekProducts:
                print(product)
            if tank.isProcessing():
                tank.shiftProcessing()
            
            
    usageResult.append(weekUsage)
    return usageResult



#Test
# Parameter predefined
batchLifes = [6, 7.5]
loadSizes = [36, 50]
# Print Results
print(forecast(80, 2, batchLifes,loadSizes, getReclaimEfficiency, demand, 1))