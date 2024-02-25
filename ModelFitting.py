import numpy as np
from sklearn.metrics import mean_absolute_error
from Forecast import *
import pandas as pd

actualUsage = pd.read_csv("Datasets/Actual_Usage.csv")

actual_usage = actualUsage.values.flatten()


# Define the ranges for batch life and load size for both products
batch_life_range_A = np.arange(5, 8, 0.1)  # Product A: 5 to 7
load_size_range_A = np.arange(35, 39, 0.1)  # Product A: 35 to 38
batch_life_range_B = np.arange(7, 9, 0.1)  # Product B: 7 to 8
load_size_range_B = np.arange(45, 53, 0.1)  # Product B: 45 to 52
# Placeholder for the best MAE and corresponding parameters
best_mae = float('inf')
best_params = {}

for batch_life_A in batch_life_range_A:
    for load_size_A in load_size_range_A:
        print("current batch_life_A", batch_life_A)
        for load_size_A in load_size_range_A:
            print("load_size__A", load_size_A)
            for batch_life_B in batch_life_range_B:
                print("batch_life_B", batch_life_B)
                for load_size_B in load_size_range_B:
                    print(load_size_B)
                    # Run the forecast with the current set of parameters
                    forecasted_usage_flat = forecast(tankSize, numOfProducts, numOfTanks,[batch_life_A, batch_life_B],[load_size_A, load_size_B],getReclaimEfficiency, demand, weeks)
                    # print(forecasted_usage_flat)

                    # Calculate MAE for this combination
                    # Replace with your actual usage values
                    mae = mean_absolute_error(actual_usage, forecasted_usage_flat)

                    # Update the best MAE and parameters if the current MAE is lower
                    if mae < best_mae:
                        best_mae = mae
                        best_params = {
                            'batch_life_A': batch_life_A,
                            'load_size_A': load_size_A,
                            'batch_life_B': batch_life_B,
                            'load_size_B': load_size_B
                        }

print(f"Best MAE: {best_mae}")
print(f"Best parameters: {best_params}")