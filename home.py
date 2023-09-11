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

    st.image("Airen.png", caption="Airen", use_column_width=True)
    


if __name__ == "__main__":
    main()

