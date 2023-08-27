import streamlit as st
import pandas as pd

def main():
    # URL to the Google Sheets CSV export link
    csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"

    # Load CSV data using pandas
    df = pd.read_csv(csv_url)

    # Streamlit UI
    st.title("Google Sheets CSV to Streamlit App")
    st.write("This app displays data from a Google Sheets CSV file.")

    # Display the data
    st.dataframe(df)

    # Date and time range selection
    st.write("Select Date and Time Range")
    min_date = pd.to_datetime(df['Date'].min()).date()
    max_date = pd.to_datetime(df['Date'].max()).date()
    selected_start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
    selected_end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

    selected_start_time = st.time_input("Start Time", value=pd.Timestamp("00:00:00").time())
    selected_end_time = st.time_input("End Time", value=pd.Timestamp("23:59:59").time())

    st.write("Line Chart: Time vs. O3")

    # Combine date and time for filtering
    start_datetime = pd.to_datetime(str(selected_start_date) + " " + str(selected_start_time))
    end_datetime = pd.to_datetime(str(selected_end_date) + " " + str(selected_end_time))

    # Filter data based on selected date and time range
    filtered_data = df[(pd.to_datetime(df['Date'] + ' ' + df['Time']) >= start_datetime) &
                       (pd.to_datetime(df['Date'] + ' ' + df['Time']) <= end_datetime)]

    line_chart_data = filtered_data[["Time", "O3"]]
    st.line_chart(line_chart_data.set_index('Time'))

if __name__ == "__main__":
    main()

