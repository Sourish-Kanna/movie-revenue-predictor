import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) 

# --- 1. Load the Trained Machine Learning Model ---
try:
    # This model should predict 'box_office' revenue
    model = joblib.load('movie_revenue_predictor.joblib')
    print("Model 'movie_revenue_predictor.joblib' loaded successfully.")
except FileNotFoundError:
    print("Error: 'movie_revenue_predictor.joblib' not found.")
    model = None
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
    model = None

# --- 2. Define the Main Page Route ---
@app.route('/')
def home():
    return render_template('index.html')

# --- 3. Define the Prediction API Endpoint ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'The machine learning model is not loaded.'}), 500

    try:
        data = request.json
        print(f"Received data for prediction: {data}")

        input_data = {
            'year': [data.get('year')],
            'rating': [data.get('rating')],
            'genres': [data.get('genre')],
            'run_time_minutes': [data.get('run_time')],
            'budget': [data.get('budget')]
        }
        
        input_df = pd.DataFrame(input_data)
        
        predicted_revenue = model.predict(input_df)[0]
        
        budget = float(data.get('budget', 0))
        profit_loss = predicted_revenue - budget
        
        status = "Profit" if profit_loss >= 0 else "Loss"
        
        response = {
            'predicted_revenue': f"{predicted_revenue:,.2f}",
            'status': status,
            'profit_loss': f"{abs(profit_loss):,.2f}"
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 400

# This part is modified for production servers like Render
if __name__ == '__main__':
    # Render provides its own port, so we read it from the environment variables
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

