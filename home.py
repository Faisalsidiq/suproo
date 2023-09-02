import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json
import requests
import random
import re

def main():

    logo = "logo.png"
    # Display the logo image
    st.image(logo, width=200)  # Adjust the width as needed

    st.title("Airen")
    st.subheader('Air Pattern Monitoring System: Aksi Sementara menjadi "Aksi Berkelanjutan"')
    
    st.write("Airen menjadi langkah revolusioner dalam menjadikan pemantauan polusi udara bukan hanya tugas pasif, tetapi juga mampu menganalisis dan menggambarkan korelasi polusi udara di berbagai sektor.")

    airen = "Airen.png"
    # Display the logo image
    st.image(airen, width=200)  # Adjust the width as needed
    
    # URL to the Google Sheets CSV export link
    csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"

    # Load CSV data using pandas
    df = pd.read_csv(csv_url)

    # Define a function to preprocess cells with numeric values or #NUM!
    def preprocess_value(value):
        if isinstance(value, (int, float)):
            return value  # Leave numeric values as they are
        elif value == "#NUM!":
            return random.randint(0, 100)  # Replace #NUM! with a random number between 0 and 100
        else:
            # Handle values with commas as decimal separators
            cleaned_value = re.sub(r'"|,', '.', value)  # Replace commas with periods
            try:
                return float(cleaned_value)  # Convert to float
            except ValueError:
                return value  # Return original value if conversion fails
    
    # Apply the preprocessing function to the entire DataFrame
    df_processed = df.applymap(preprocess_value)
    
    # Display the preprocessed DataFrame
    print(df_processed)

    # Create a button to display the DataFrame
    if st.button("Show DataFrame"):
        # Show the DataFrame using Streamlit
        st.write("Loaded DataFrame:")
        st.write(df_processed)  # Display the DataFrame in the app

if __name__ == "__main__":
    main()

