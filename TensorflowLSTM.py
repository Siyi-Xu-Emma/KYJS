import pandas as pd
import numpy as np
import random

from Forecast import *

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Example data
demand = pd.read_csv("Datasets/Weekly_Projections.csv")
data = np.array(demand.iloc[0,:])
name = "Product 1 Demand Prediction weekly"
#data = data1 = np.array(demand.iloc[1,:])
# Function to prepare data for LSTM

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

# Define function to train LSTM model and make predictions
def train_lstm_model(data, n_steps, future_steps):
    # Split data into input features and target variable
    X, y = prepare_data(data, n_steps)
    
    # Reshape input features for LSTM [samples, timesteps, features]
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    
    # Define the LSTM model
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    
    # Fit the model
    model.fit(X, y, epochs=200, verbose=0)
    
    # Make predictions for future steps
    x_input = data[-n_steps:]
    x_input = x_input.reshape((1, n_steps, n_features))
    predictions = []
    for _ in range(future_steps):
        y_pred = model.predict(x_input, verbose=0)
        predictions.append(y_pred[0,0])
        x_input = np.append(x_input[0,1:,:], [[y_pred[0,0]]], axis=0)
        x_input = x_input.reshape((1, n_steps, n_features))
    
    return predictions

# Define values of n_steps to test
n_steps_list = [2, 3, 4, 5, 6, 7]

# Plot original data
plt.figure(figsize=(10, 6))
plt.scatter(range(len(data)), data, label='Original Data')

# Loop over different values of n_steps
for n_steps in n_steps_list:
    # Train LSTM model and make predictions
    predictions = train_lstm_model(data, n_steps, future_steps=100)  
    np.savetxt(f'OutputPredictionData/LSTMPredictions_n_steps_{n_steps}{name}.csv', predictions, delimiter=',')
    # Plot predictions
    plt.plot(range(len(data), len(data) + len(predictions)), predictions, label=f'n_steps={n_steps}')

# Add legend and labels
plt.legend()
plt.xlabel('Time Step')
plt.ylabel('Value')
plt.title('Original Data and LSTM Predictions')
plt.grid(True)
for n_step in n_steps_list:
    mse = np.mean((data - np.array(predictions[:10])) ** 2)
    print("n_steps_MSE:", mse)
plt.show()


    