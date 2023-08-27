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

    # Display tools content
    st.title('Tools')
    st.write('Choose a tool from the options below.')
    st.write('Correlation tool selected')
    # Select pollutant columns (B to H) and meteorology columns (I to P)
    pollutant_columns = df.columns[5:12]
    meteorology_columns = df.columns[3:4]
    
    # Sidebar inputs
    selected_pollutant = st.sidebar.selectbox('Select Pollutant', pollutant_columns)
    selected_meteorology = st.sidebar.selectbox('Select Meteorology Data', meteorology_columns)
    
    # Start and end date inputs
    start_date = st.sidebar.date_input('Start Date', min_value=df['date'].min().to_pydatetime().date(), max_value=df['date'].max().to_pydatetime().date(), value=df['Waktu'].min().to_pydatetime().date())
    end_date = st.sidebar.date_input('End Date', min_value=df['date'].min().to_pydatetime().date(), max_value=df['date'].max().to_pydatetime().date(), value=df['Waktu'].min().to_pydatetime().date())
    
    # Hour and minute range inputs
    start_hour = st.sidebar.selectbox('Start Hour', range(24), 0)
    start_minute = st.sidebar.selectbox('Start Minute', range(0, 60, 30), 0, format_func=lambda x: f'{x:02d}')
    end_hour = st.sidebar.selectbox('End Hour', range(24), 23)
    end_minute = st.sidebar.selectbox('End Minute', range(0, 60, 30), 1, format_func=lambda x: f'{x:02d}')
    
    # Create start and end datetime objects
    start_datetime = datetime.combine(start_date, time(start_hour, start_minute))
    end_datetime = datetime.combine(end_date, time(end_hour, end_minute))
    
    # Filter data based on selected date and time range
    filtered_data = data[(df['date'] >= start_datetime) & (df['date'] <= end_datetime)]
    
    # Create line plot for the correlation between selected pollutant and meteorology data using Plotly
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=filtered_data['Waktu'], y=filtered_data[selected_pollutant], mode='lines', name=selected_pollutant), secondary_y=False)
    fig.add_trace(go.Scatter(x=filtered_data['Waktu'], y=filtered_data[selected_meteorology], mode='lines', name=selected_meteorology), secondary_y=True)
    
    # Update the layout with titles and y-axis labels
    fig.update_layout(
        title=f'Correlation between {selected_pollutant} and {selected_meteorology}',
        xaxis_title='Time',
        yaxis=dict(title=selected_pollutant, side='left'),
        yaxis2=dict(title=selected_meteorology, side='right')
    )
    
    # Display the correlation line plot
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()

