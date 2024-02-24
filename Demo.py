import pandas as pd
import numpy as np

# Constants
WEEKHRS = 10080
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
products = [Product(0), Product(1)]
print(tank, products[0], products[1])

def forecast(tankSize, productNum, batchLifes, loadSizes, demand, predictionRange):
    products = []
    for i in range(productNum):
        
    productNum = len(products)
    for time in range(0, predictionRange): ## predictionRange in min
        weekIndex = 0
        if not time % WEEKHRS:
            weekIndex = time // WEEKHRS
        weekDemand = []
        for i in range(productNum):
            weekDemand.append(demand.iloc[i, weekIndex])
        
    return weekDemand

# Print Results
print(80, batchLifes,loadSizes, demand, 10)