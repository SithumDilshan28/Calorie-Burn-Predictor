import streamlit as st
import pandas as pd
from xgboost import XGBRegressor
import pickle

# Load the trained model
with open('Calories_Burnt.pkl', 'rb') as file:
    model = pickle.load(file)

# Set page layout and title
st.set_page_config(page_title="Calories Burnt Prediction", layout="wide", page_icon="🔥")
st.title("🔥 Calories Burnt Prediction App")
st.subheader("Estimate the number of calories burnt during your workout based on exercise details.")

# Function to make predictions
def predict_calories_burnt(data):
    prediction = model.predict(data)
    return prediction

# Function to style text
def style_text(prediction):
    if prediction < 100:
        label_color = "green"
    elif prediction >= 100 and prediction < 200:
        label_color = "orange"
    else:
        label_color = "red"

    styled_text = f'<span style="color: {label_color}; font-size: 20px;">Predicted Calories Burnt: {prediction[0]:.2f}</span>'
    return styled_text

# Streamlit UI
def main():
    # Apply CSS styling
    st.markdown("""
        <style>
        body {
            background-color: #f0f2f6;
            color: #333;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px 24px;
            border-radius: 10px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar with additional options
    with st.sidebar:
        st.image("fitness_banner.png", use_column_width=True)  # You can replace this with your custom image
        st.header("About")
        st.write(
            """
            This app predicts the number of calories burnt based on your exercise details. 
            Input your data to get an estimate of calories burnt during your workout session.
            """
        )
        st.write("Developed by: U-Connect")

    # Input features
    st.subheader("Input Exercise Details")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.slider("Age", 20, 80, 30)
    height = st.slider("Height (cm)", 120.0, 230.0, 170.0)
    weight = st.slider("Weight (kg)", 30.0, 150.0, 70.0)
    duration = st.slider("Exercise Duration (minutes)", 1.0, 60.0, 30.0)
    heart_rate = st.slider("Heart Rate", 60.0, 150.0, 90.0)
    body_temp = st.slider("Body Temperature (°C)", 35.0, 42.0, 37.0)

    # Convert gender to numerical value
    gender_encoded = 0 if gender == "Male" else 1

    # Predict button
    if st.button("Predict"):
        # Create a DataFrame with user input
        input_data = pd.DataFrame({
            "Gender": [gender_encoded],
            "Age": [age],
            "Height": [height],
            "Weight": [weight],
            "Duration": [duration],
            "Heart_Rate": [heart_rate],
            "Body_Temp": [body_temp],
            "Dummy": [0]  # Add a dummy feature for the encoded gender
        })

        # Make prediction
        prediction = predict_calories_burnt(input_data)

        # Style and display prediction
        styled_text = style_text(prediction)
        st.markdown(styled_text, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
