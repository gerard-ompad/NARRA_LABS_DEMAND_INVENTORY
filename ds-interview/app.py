from flask import Flask, request, jsonify
import joblib
import numpy as np
import xgboost as xgb

# Load the saved XGBoost model
model = joblib.load('optimized_xgboost_model.joblib')

app = Flask(__name__)

# Add a default route for troubleshooting
@app.route('/')
def home():
    return 'Flask server is running!'

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the request
        data = request.get_json()

        # Extract the features from the input JSON
        distance_km = data.get('distance_km')
        order_size = data.get('order_size')
        restaurant_popularity = data.get('restaurant_popularity')

        if distance_km is None or restaurant_popularity is None:
            return jsonify({'error': 'Missing input data'}), 400

        # Prepare the input data for prediction
        input_data = np.array([[distance_km, order_size,restaurant_popularity]])

        # Predict using the loaded model
        prediction = model.predict(input_data)

        # Return the prediction as JSON
        return jsonify({'predicted_time_to_delivery': float(prediction[0])})

    except Exception as e:
        # Log the error
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
