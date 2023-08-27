import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

def main():
    # URL to the new Google Sheets CSV export link
    csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"

    # Load CSV data using pandas
    df = pd.read_csv(csv_url)

    # Streamlit UI
    st.title("Google Sheets CSV to Streamlit App")
    st.write("This app displays data from a Google Sheets CSV file.")

    # Display the data
    st.dataframe(df)

    # Create a line chart using "Time" and "O3" columns
    st.write("Line Chart: Time vs. O3")
    line_chart_data = df[["Time", "O3"]]
    st.line_chart(line_chart_data.set_index('Time'))

if __name__ == "__main__":
    main()
