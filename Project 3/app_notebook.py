import streamlit as st
import joblib
import pandas as pd

st.set_page_config(
    page_title="Car MSRP Prediction",
    page_icon="🚗",
    layout="wide"
)
## LOAD MODEL ##
@st.cache_resource
def load_pipe():
    return joblib.load('model.pkl')

@st.cache_data
def load_data():
    return pd.read_csv('data.csv')

pipe = load_pipe()
df = load_data()

## INPUT FROM USER  ##
st.sidebar.header("Enter Car Information")

make = st.sidebar.selectbox("Make", sorted(df["Make"].unique()))

model = st.sidebar.selectbox("Model", sorted(df["Model"].unique()))

year = st.sidebar.slider(
    "Year",
    min_value=1990,
    max_value=2020,
    value=2015
)

engine_fuel_type = st.sidebar.selectbox(
    "Engine Fuel Type",
    [
        "premium unleaded (required)",
        "premium unleaded (recommended)",
        "regular unleaded",
        "flex-fuel (unleaded/E85)",
        "diesel",
        "electric"
    ]
)

engine_hp = st.sidebar.number_input(
    "Engine HP",
    min_value=50,
    value=250
)

engine_cylinders = st.sidebar.number_input(
    "Engine Cylinders",
    min_value=0,
    value=6
)

transmission_type = st.sidebar.selectbox(
    "Transmission Type",
    [
        "AUTOMATIC",
        "MANUAL",
        "AUTOMATED_MANUAL",
        "DIRECT_DRIVE"
    ]
)

driven_wheels = st.sidebar.selectbox(
    "Driven Wheels",
    [
        "front wheel drive",
        "rear wheel drive",
        "all wheel drive",
        "four wheel drive"
    ]
)

number_of_doors = st.sidebar.selectbox(
    "Number of Doors",
    [2, 4]
)

vehicle_size = st.sidebar.selectbox(
    "Vehicle Size",
    [
        "Compact",
        "Midsize",
        "Large"
    ]
)

vehicle_style = st.sidebar.selectbox(
    "Vehicle Style",
    [
        "Coupe",
        "Sedan",
        "SUV",
        "Convertible",
        "Wagon",
        "4dr Hatchback",
        "2dr Hatchback",
        "Crew Cab Pickup"
    ]
)

highway_mpg = st.sidebar.number_input(
    "Highway MPG",
    min_value=5,
    value=30
)

city_mpg = st.sidebar.number_input(
    "City MPG",
    min_value=5,
    value=22
)

popularity = st.sidebar.number_input(
    "Popularity",
    min_value=0,
    value=2000
)

## PREPARE the data for model
new_data = {'Make':make,
            'Model':model,
            'Year':year,
            'Engine Fuel Type':engine_fuel_type,
            'Engine HP':engine_hp,
            'Engine Cylinders':engine_cylinders,
            'Transmission Type':transmission_type,
            'Driven_Wheels':driven_wheels,
            'Number of Doors':number_of_doors,
            'Vehicle Size':vehicle_size,
            'Vehicle Style':vehicle_style,
            'highway MPG':highway_mpg,
            'city mpg':city_mpg,
            'Popularity':popularity,
            'Engine HP per Cylinder':engine_hp / engine_cylinders if engine_cylinders != 0 else 0,
            'Engine HP per Year':engine_hp / year}

new_data_df = pd.DataFrame(new_data, index=[0])

## Prediction
button = st.button("Predict")
if button:
    result = pipe.predict(new_data_df)
    st.write(result[0])