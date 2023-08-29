import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json
import requests

def main():

    logo = "logo.png"
    # Display the logo image
    st.image(logo, width=200)  # Adjust the width as needed

    st.title("Air Pollution Pattern Monitoring System")

    # URL to the Lottie animation JSON file
    lottie_url = "time.json"
    
    # Display Lottie animation using the st_lottie function
    st_lottie(lottie_url)
    
    # URL to the Google Sheets CSV export link
    csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"

    # Load CSV data using pandas
    df = pd.read_csv(csv_url)

    # Define a function to preprocess cells with numeric values
    def preprocess_numeric(value):
        if isinstance(value, (int, float)):
            return value * 2  # Perform some operation on the numeric value
        else:
            return value
    
    # Apply the preprocessing function to the entire DataFrame
    df_processed = df.applymap(preprocess_numeric)
    
    # Display the preprocessed DataFrame
    print(df_processed)

    # Create a button to display the DataFrame
    if st.button("Show DataFrame"):
        # Show the DataFrame using Streamlit
        st.write("Loaded DataFrame:")
        st.write(df)  # Display the DataFrame in the app

if __name__ == "__main__":
    main()

