import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

demand = pd.read_csv("Datasets/Weekly_Projections.csv")
# Example data
data = np.array(demand.iloc[0,:])
name = "Product 1 Demand Prediction weekly"
future_steps = 10
#data = data1 = np.array(demand.iloc[1,:])

# Function to prepare data for Random Forest Regressor
def prepare_data(data, n_steps):
    X, y = [], []
    for i in range(len(data)):
        # Find the end of this pattern
        end_ix = i + n_steps
        # Check if we are beyond the sequence
        if end_ix > len(data)-1:
            break
        # Gather input and output parts of the pattern
        seq_x, seq_y = data[i:end_ix], data[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

# Define function to train Random Forest Regressor model and make predictions
def train_random_forest_model(data, n_steps, future_steps):
    # Split data into input features and target variable
    X, y = prepare_data(data, n_steps)
    
    # Define the Random Forest Regressor model
    model = RandomForestRegressor(n_estimators= future_steps, random_state=42)
    
    # Fit the model
    model.fit(X, y)
    
    # Make future predictions
    x_input = data[-n_steps:].reshape(1, -1)
    predictions = data
    for _ in range(future_steps):
        y_pred = model.predict(x_input)
        predictions.append(y_pred[0])
        x_input = np.append(x_input[:, 1:], [[y_pred[0]]], axis=1)
    
    return predictions

# Define values of n_steps to test
n_steps_list = [2, 3, 4, 5, 6, 7]

# Plot original data
plt.figure(figsize=(10, 6))
plt.scatter(range(len(data)), data, label='Original Data')

# Loop over different values of n_steps
for n_steps in n_steps_list:
    # Train Random Forest model and make predictions
    predictions = train_random_forest_model(data, n_steps, future_steps)
    np.savetxt(f'OutputPredictionData/RFRpredictions_n_steps_{n_steps}{name}.csv', predictions, delimiter=',')
    # Plot predictions
    plt.plot(range(len(data), len(data) + len(predictions)), predictions, label=f'n_steps={n_steps}')

# Add legend and labels
plt.legend()
plt.xlabel('Time Step')
plt.ylabel('Value')
plt.title(name)
plt.grid(True)
plt.show()
