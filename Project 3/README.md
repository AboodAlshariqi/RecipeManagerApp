# Car MSRP Prediction App

A machine learning web app built with Python and Streamlit. Estimate the Manufacturer's Suggested Retail Price (MSRP) of a vehicle based on its specifications, performance metrics, and features using a pre-trained regression model.

## Problem Statement

Navigating the car market can be difficult when trying to determine a fair price for a vehicle. This app gives you a simple, interactive tool to input a car's specifications—such as make, year, engine horsepower, cylinders, and fuel efficiency—and instantly receive a data-driven MSRP estimation to help you make informed buying or selling decisions.

## Features

### Core Features
- **Comprehensive Input Selection** — specify the car's Make, Model, Year, and structural details like Number of Doors and Vehicle Size/Style.
- **Performance Metrics** — input Engine HP, Engine Cylinders, and Engine Fuel Type to capture the powertrain's value.
- **Efficiency & Popularity** — factor in City and Highway MPG, along with the car brand's popularity score.
- **Real-Time Prediction** — instantly calculates the estimated MSRP using a pre-trained machine learning pipeline.
- **Automated Feature Engineering** — automatically calculates derived metrics (like Engine HP per Cylinder and Engine HP per Year) behind the scenes to feed the model exactly what it needs.

## Tech Used

- **Python** — core logic
- **Streamlit** — interactive web interface
- **pandas** — data structuring and preparation
- **joblib** — loading the pre-trained machine learning model
- **scikit-learn** — (backend) used for training the machine learning model pipeline

## Project Structure

app.py           # Streamlit app — the user interface and prediction logic
model.pkl        # The pre-trained machine learning pipeline/model
data.csv         # The dataset (optional depending on implementation, used for EDA/training)

## How to Run

1. Clone this repository
2. Install the required packages:
   pip install streamlit pandas joblib scikit-learn
3. Ensure `model.pkl` is in the same directory as the script.
4. Run the app:
   streamlit run app.py

## APP link

   Here is the link to the app (Insert your Streamlit Cloud link here)


## Author

Abdulla Alsharqi
