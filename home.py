import streamlit as st
import pandas as pd
from lottie_component import LottieAnimation

def main():

    logo = "logo.png"
    # Display the logo image
    st.image(logo, width=200)  # Adjust the width as needed

        # Render the Lottie animation
    
    # URL to the Google Sheets CSV export link
    csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"

    # Load CSV data using pandas
    df = pd.read_csv(csv_url)

    # Create a button to display the DataFrame
    if st.button("Show DataFrame"):
        # Show the DataFrame using Streamlit
        st.write("Loaded DataFrame:")
        st.write(df)  # Display the DataFrame in the app



if __name__ == "__main__":
    main()

