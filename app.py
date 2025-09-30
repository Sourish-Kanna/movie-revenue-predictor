import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This is needed to allow the frontend to access the backend

# --- 1. Load the Model ---
try:
    # Load the new regression model
    model = joblib.load('movie_revenue_predictor.joblib')
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: 'movie_revenue_predictor.joblib' not found. Make sure the file is in the same directory.")
    model = None

# --- 2. Main Page Route ---
@app.route('/')
def home():
    return render_template('index.html')

# --- 3. Prediction API Route ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded.'}), 500

    try:
        data = request.json
        print("Received data:", data)

        # Prepare data for prediction
        input_data = {
            'year': data.get('year'),
            'rating': data.get('rating'),
            'genre': data.get('genre'),
            'run_time_minutes': data.get('run_time'),
            'budget': data.get('budget')
        }
        
        # Create a DataFrame from the input data.
        input_df = pd.DataFrame([input_data])
        
        # Make a prediction using the regression model
        predicted_revenue = model.predict(input_df)[0]
        
        # Calculate profit or loss
        budget = input_data['budget']
        profit_loss = predicted_revenue - budget
        
        # Determine if it's a profit or loss
        status = "Profit" if profit_loss >= 0 else "Loss"
        
        # The app now returns a predicted amount, status, and profit/loss
        response = {
            'predicted_revenue': f"{predicted_revenue:,.2f}",
            'status': status,
            'profit_loss': f"{abs(profit_loss):,.2f}" # Use absolute value for the amount
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# --- 4. Run the App ---
if __name__ == '__main__':
    app.run(debug=True)