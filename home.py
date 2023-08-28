import streamlit as st
import pandas as pd

def main():
    # URL to the Google Sheets CSV export link
    csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"

    # Load CSV data using pandas
    df = pd.read_csv(csv_url)

    # Create a button to display the DataFrame
    if st.button("Show DataFrame"):
        # Show the DataFrame using Streamlit
        st.write("Loaded DataFrame:")
        st.write(df)  # Display the DataFrame in the app

    import streamlit as st
    import pandas as pd
    import folium
    
    # URL to the Google Sheets CSV export link
    csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"
    
    # Load CSV data using pandas
    df = pd.read_csv(csv_url, parse_dates=[['Date', 'Time']])
    df['Date_Time'] = pd.to_datetime(df['Date_Time'])
    
    # Get the latest row
    latest_row = df.iloc[-1]
    
    # Create a folium map centered around the given latitude and longitude
    m = folium.Map(location=[-7.783000, 110.410538], zoom_start=15)
    
    # Add a marker for the given latitude and longitude
    folium.Marker(
        location=[-7.783000, 110.410538],
        popup=f"Click here to load latest value",
        icon=folium.Icon(color="blue"),
    ).add_to(m)
    
    # Display the map
    st.title("Map with Latest Data Value")
    st.write("Click the blue marker to load the latest value from the CSV.")
    
    # Display the map using Streamlit's map component
    st.map(m)
    
    # When the marker is clicked, display the latest value
    if st.button("Click to Load Latest Value"):
        st.write("Latest Value:")
        selected_column = st.selectbox("Select a column", df.columns[1:])
        st.write(f"{selected_column}: {latest_row[selected_column]}")


if __name__ == "__main__":
    main()

