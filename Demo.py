import pandas as pd
import numpy as np

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
    
    def replenish(self):
        self.batchLife = 1

class Product:
    def __init__(self, id, batchLife, loadSize):
        self.id = id
        self.remain = 0
        self.batchLife = 1 / batchLife
        self.loadSize = loadSize
        
    def __str__(self):
        return f"Product {self.id}"
    
    
        
        
tank = Tank(80)

#### no replenishment at the end of the week

def forecast(tankSize, productNum, batchLifes, loadSizes, demand, weeks):
    tank = Tank(80)
    products = []
    predictionRange = WEEKMINS * weeks
    usageResult = []
    
    for i in range(productNum):
        new = Product(i, batchLifes[i], loadSizes[i])
        products.append(new)
        print(new)
        
    for time in range(0, predictionRange): ## predictionRange in min
        weekIndex = 0
        weekUsage = 0
        
        if not time % WEEKMINS: ## initiate new week
            weekIndex = time // WEEKMINS
            print(weekIndex)
            weekDemand = []
            for i in range(productNum):
                weekDemand.append(demand.iloc[i, weekIndex])
            processSpeed = sum(weekDemand)/WEEKMINS
        
        if not time % chemicalLife:
            tank.replenish()
        
        
    

# Print Results
print(forecast(80, 2, batchLifes,loadSizes, demand, 10))