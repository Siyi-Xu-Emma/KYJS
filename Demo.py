import pandas as pd
import numpy as np
import random

# Constants
WEEKMINS = 7 * 24 * 60 * 60
chemicalLife = 500

# Parameter predefined
reclaimEfficiency = 0.09
batchLifes = [7, 8]
loadSizes = [38, 50]



# Read Data
demand = pd.read_csv("Datasets/Weekly_Projections.csv")
print(demand)


class Tank: 
    def __init__(self, size):
        self.size = size
        self.chemicalLife = 500
        self.batchLife = 1
        
    def __str__(self):
        return f"tank sized {self.size}L"
    
    def replenish(self, reclaimEfficiency):
        self.batchLife = 1
        return self.size * (1- reclaimEfficiency)

class Product:
    def __init__(self, id, batchLife, loadSize):
        self.id = id
        self.remain = 0
        self.batchLife = 1 / batchLife
        self.loadSize = loadSize
        
    def __str__(self):
        return f"Product {self.id}"
    
    
        
        
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
    
    for i in range(productNum):  ##initialization
        new = Product(i, batchLifes[i], loadSizes[i])
        products.append(new)
    
    
        
    weekUsage = 0
    for time in range(0, predictionRange): ## predictionRange in min
        weekIndex = 0
        
        if not time % chemicalLife: ## replenish when chemical life reached
            weekUsage += tank.replenish(reclaimEfficiency(time))
            
        if not time % WEEKMINS: ## initiate new week
            weekIndex = time // WEEKMINS
            print(weekIndex)
            weekDemand = []
            for i in range(productNum):
                weekDemand.append(demand.iloc[i, weekIndex])
            processSpeed = sum(weekDemand)/WEEKMINS
            usageResult.append(weekUsage)
            weekUsage = 0
        

            
        
    return usageResult
    

# Print Results
print(forecast(80, 2, batchLifes,loadSizes, reclaimEfficiency, demand, 10))