import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
# Allow cross-origin requests, essential for connecting frontend to backend
CORS(app) 

# --- 1. Load the Trained Machine Learning Model ---
try:
    # This model should predict 'box_office' revenue
    model = joblib.load('movie_revenue_predictor.joblib')
    print("Model 'movie_revenue_predictor.joblib' loaded successfully.")
except FileNotFoundError:
    print("Error: 'movie_revenue_predictor.joblib' not found. Ensure the model file is in the same directory as this script.")
    model = None
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
    model = None

# --- 2. Define the Main Page Route ---
# This route serves the frontend HTML file.
@app.route('/')
def home():
    return render_template('index.html')

# --- 3. Define the Prediction API Endpoint ---
# This route handles the prediction logic. It's the "brain" of the app.
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'The machine learning model is not loaded. Please check the server logs.'}), 500

    try:
        # Get the JSON data sent from the frontend
        data = request.json
        print(f"Received data for prediction: {data}")

        # Prepare the data in the exact format the model was trained on.
        # The keys must match the feature names used during training.
        input_data = {
            'year': [data.get('year')],
            'rating': [data.get('rating')],
            'genres': [data.get('genre')],
            'run_time_minutes': [data.get('run_time')],
            'budget': [data.get('budget')]
        }
        
        # Create a pandas DataFrame from the input data.
        # Scikit-learn models expect a DataFrame or a similar array-like structure.
        input_df = pd.DataFrame(input_data)
        
        # --- Make a Prediction ---
        # The model's predict method returns a NumPy array, so we get the first element.
        predicted_revenue = model.predict(input_df)[0]
        
        # --- Calculate Profit or Loss ---
        budget = float(data.get('budget', 0))
        profit_loss = predicted_revenue - budget
        
        # Determine the status based on the calculation
        status = "Profit" if profit_loss >= 0 else "Loss"
        
        # Format the response to be sent back to the frontend
        response = {
            'predicted_revenue': f"{predicted_revenue:,.2f}",
            'status': status,
            'profit_loss': f"{abs(profit_loss):,.2f}" # Use absolute value for a clean display
        }
        
        return jsonify(response)
    
    except Exception as e:
        # Handle potential errors, such as missing data or incorrect formats
        print(f"An error occurred during prediction: {e}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 400

# --- 4. Run the Flask Application ---
if __name__ == '__main__':
    # 'debug=True' allows the server to auto-reload when you make code changes
    app.run(debug=True)
