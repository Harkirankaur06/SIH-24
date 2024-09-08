# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from pycaret.regression import setup, compare_models
from autots import AutoTS

# Step 1: Data Collection and Preprocessing
data = pd.read_csv('C:\\Users\\yuvra\\Desktop\\disaster_data.csv')

# Example of preprocessing steps
data['date'] = pd.to_datetime(data['date'])
data.fillna(method='ffill', inplace=True)  # Fill missing values

# Normalizing severity
scaler = MinMaxScaler()
data['severity'] = scaler.fit_transform(data[['severity']])

# Step 2: Exploratory Data Analysis (optional)
plt.plot(data['date'], data['severity'])
plt.title('Disaster Severity Over Time')
plt.xlabel('Date')
plt.ylabel('Severity')
plt.show()

# Step 3: Time Series Modeling with Prophet
df = data[['date', 'severity']]
df.columns = ['ds', 'y']  # Prophet needs these column names

# Fit Prophet model
prophet_model = Prophet()
prophet_model.fit(df)

# Make a prediction for the next 365 days
future = prophet_model.make_future_dataframe(periods=365)
forecast = prophet_model.predict(future)

# Plot forecast
prophet_model.plot(forecast)
plt.show()

# Step 4: LSTM Model for Severity Prediction
# Preparing LSTM input
X = []
y = []
window_size = 10  # Define how many past steps to use
for i in range(window_size, len(data)):
    X.append(data['severity'].values[i-window_size:i])
    y.append(data['severity'].values[i])

X = np.array(X)
y = np.array(y)

# Reshape X to be [samples, time steps, features]
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# Splitting into training and test sets
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Build LSTM model
lstm_model = Sequential()
lstm_model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
lstm_model.add(LSTM(units=50))
lstm_model.add(Dense(units=1))  # Predict one output: severity

lstm_model.compile(optimizer='adam', loss='mean_squared_error')
lstm_model.fit(X_train, y_train, epochs=20, batch_size=32)

# Evaluate LSTM model performance
predicted_severity = lstm_model.predict(X_test)
mse = mean_squared_error(y_test, predicted_severity)
print(f'Mean Squared Error for LSTM: {mse}')

# Step 5: Regression Model for Resource Prediction using PyCaret
# Set up PyCaret for regression
data_for_pycaret = data[['severity', 'resources_needed']]  # Simplified for illustration
exp1 = setup(data_for_pycaret, target='resources_needed') #, silent=True)

# Compare different models
best_model = compare_models()

# Step 5 Alternative: AutoTS for Resource Prediction
autots_model = AutoTS(forecast_length=30, frequency='infer', ensemble='simple')

autots_model = autots_model.fit(data, date_col='date', value_col='resources_needed')
prediction = autots_model.predict()

# Display predictions
print(prediction.forecast)

# Step 6: Flask Deployment Example (optional)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data and run the prediction
    input_data = request.json['data']
    prediction = lstm_model.predict(input_data)  # Use your trained model
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run()
