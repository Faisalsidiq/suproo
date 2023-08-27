import streamlit as st
import pandas as pd

def main():
    # URL to the Google Sheets CSV export link
    csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"

    # Load CSV data using pandas
    df = pd.read_csv(csv_url)

  

if __name__ == "__main__":
    main()

