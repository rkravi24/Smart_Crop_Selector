# Smart Crop Selector 


1. **Crop Recommendation System:**  
   - Uses machine learning (ML) to predict the best crop to cultivate based on soil and weather parameters.
   - Includes a complete data analysis and model training pipeline using a crop dataset.
   - Offers endpoints to view crop details, fetch recommended seeds, and perform predictions via a Flask web interface.

2. **Weather Information Display:**  
   - A client-side JavaScript feature that fetches current weather data from the OpenWeatherMap API.
   - Remembers the last searched city using `sessionStorage` to persist data between page loads.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
  - [Flask Web Application](#flask-web-application)
  - [Crop Recommendation Model Training](#crop-recommendation-model-training)
  - [Client-Side Weather Script](#client-side-weather-script)
- [API References](#api-references)
- [License](#license)

---

## Features
- **System:**  
  - Loads a pre-trained model and data scalers (from pickle files).
  - Provides endpoints to get crop details, recommended seeds (from JSONBin.io), and crop predictions based on soil parameters.
  - Displays results using HTML templates (e.g., `home.html`, `find-seeds.html`, `getdetails.html`, `predict_page.html`).

- **Weather App:**  
  - JavaScript fetches current weather (temperature, precipitation, humidity, wind speed) for a user-specified city.
  - Uses `sessionStorage` to cache the last searched city and its weather information.
  - Prevents default form submission to ensure smooth API calls.

- **Model Training Pipeline:**  
  - Reads the `Crop_recommendation.csv` dataset using pandas.
  - Performs data exploration (head, shape, info, null counts, duplicates, describe).
  - Maps crop labels to numeric values.
  - Splits the data into training and test sets.
  - Scales features using `MinMaxScaler`.
  - Trains multiple ML classifiers (e.g., Logistic Regression, Naive Bayes, SVM, Decision Tree, Random Forest, etc.).
  - Evaluates models using accuracy and confusion matrices.
  - Finally selects the best model (RandomForestClassifier) and saves the trained model and scaler(s) as pickle files.

---




---

## Installation


### Prerequisites
- Python 3.x installed on your machine.
- A modern web browser for the frontend.
- Required API keys:
  - **OpenWeatherMap API Key:** Replace the placeholder in the JavaScript (`script.js`) file.
  - **JSONBin.io API Key:** Already included in the Flask app, but you can update it if necessary.

### Setup Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/rkravi24/Smart_Crop_Selector
   cd Smart_Crop_Selector
