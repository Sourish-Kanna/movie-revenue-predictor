# 🎬 Movie Revenue Predictor

## Overview
This project is a complete **machine learning web application** that predicts the potential box office revenue of a movie.  
Users can input details such as the movie's **budget, genre, rating, and runtime**, and the application will return a **predicted revenue figure** along with the **potential profit or loss**.

The project is composed of two main parts:
1. **Machine Learning Model** – trained on the TMDB 5000 movie dataset to understand the relationship between a movie's features and its financial success.  
2. **Web Application** – built with Flask to provide a user-friendly interface and real-time predictions using the trained model.

---

## Tech Stack
- **Backend:** Python, Flask  
- **Machine Learning:** Scikit-learn, Pandas, NumPy  
- **Frontend:** HTML, Tailwind CSS, JavaScript  
- **Dataset:** TMDB 5000 Movie Dataset  

---

## File Structure
It is recommended to place `index.html` inside a `templates` folder for the Flask application to function correctly.

``` text
.
├── app.py                         # The Flask web server
├── movie_revenue_predictor.joblib # The pre-trained machine learning model
├── requirements.txt               # Python dependencies for the project
├── templates/
│   └── index.html                 # The frontend HTML file
├── Copy_of_ml_mini_project.ipynb  # Jupyter Notebook with the model training process
└── tmdb_5000_movies.csv           # The raw dataset used for training

````

## Setup and Installation

### 1. Clone the Repository (or download the files)
Ensure all files are in the same directory, with `index.html` inside a sub-folder named `templates`.

### 2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.

```bash
# Create the environment
python -m venv venv

# Activate the environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
````

### 3. Install Dependencies

Install all the required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Run the Flask Application

Start the backend server by running the `app.py` script.

```bash
python app.py
```

### 5. Open the Application

Once the server is running, it will provide a local URL (usually `http://127.0.0.1:5000`).
Open this URL in your web browser to use the application.

---

## How It Works

### 1. Model Training (`Copy_of_ml_mini_project.ipynb`)

The machine learning model is the "brain" of the application. It was built and trained using the provided Jupyter Notebook.

* **Data Loading:** Load the `tmdb_5000_movies.csv` dataset into a pandas DataFrame.
* **Data Cleaning:**

  * Parse the `genres` column (JSON format) into simple, comma-separated strings.
  * Remove rows with invalid financial data (e.g., budget or revenue of 0).
* **Feature Selection:** Key features like budget, genres, rating, runtime, and year are selected.
* **Model Training:** A `RandomForestRegressor` model from Scikit-learn is trained on the cleaned data.
* **Model Export:** The trained model pipeline is saved to `movie_revenue_predictor.joblib`.

---

### 2. Web Application (`app.py` & `index.html`)

The web application provides a simple interface for users to interact with the trained model.

* **Backend:**

  * The Flask app (`app.py`) loads the `movie_revenue_predictor.joblib` model.
  * Exposes an API endpoint at `/predict`.

* **Frontend:**

  * The user fills out the form in `index.html`.
  * When "Predict Revenue" is clicked, JavaScript sends the data to `/predict` as JSON.

* **Prediction:**

  * The backend formats the data into a pandas DataFrame matching the model input.
  * The model predicts the revenue.

* **Response:**

  * The backend calculates profit/loss and sends results back in JSON format.

* **Display:**

  * JavaScript dynamically updates the UI.
  * The result card is **color-coded** (✅ green for profit, ❌ red for loss).
