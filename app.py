#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
# import pandas_profiling
# from streamlit_pandas_profiling import st_profile_report
import time
import requests
# from pydantic_settings import BaseSettings 
import datetime
from streamlit_option_menu import option_menu
#######################
# Page configuration
from views.communication import *
from views.wildlife import wildlife

st.set_page_config(
    page_title="Congo Basin Monitoring and Evaluation database",
    # page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
st.markdown("""
    <style>

    [data-testid="block-container"] {
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1rem;
        padding-bottom: 0rem;
        margin-bottom: -7rem;
    }

    [data-testid="stVerticalBlock"] {
        padding-left: 0rem;
        padding-right: 0rem;
    }

    [data-testid="stMetric"] {
        background-color: #393939;
        text-align: center;
        padding: 15px 0;
    }

    [data-testid="stMetricLabel"] {
    display: flex;
    justify-content: center;
    align-items: center;
    }

    [data-testid="stMetricDeltaIcon-Up"] {
        position: relative;
        left: 38%;
        -webkit-transform: translateX(-50%);
        -ms-transform: translateX(-50%);
        transform: translateX(-50%);
    }

    [data-testid="stMetricDeltaIcon-Down"] {
        position: relative;
        left: 38%;
        -webkit-transform: translateX(-50%);
        -ms-transform: translateX(-50%);
        transform: translateX(-50%);
    }

    </style>
    """, unsafe_allow_html=True)

pillars= [
    "wildlife","communication","human activity","law enforcement","spatial data and landcover","capacity building"
]
with st.sidebar:
    # st.title('🏂 US Population Dashboard')
    st.markdown(
            '<img src="./app/static/logo.jpg" height="120" style="">',
            unsafe_allow_html=True,
        )
    # st.image("static/logo.jpg")
    st.title('Congo Basin Monitoring and Evaluation Database')
    
    # indicator_list = list(df_reshaped.year.unique())[::-1]
    
    selected_pillar = st.selectbox('Select Pillar', pillars)
    
    
content = st.empty()
if selected_pillar =="communication":
    communication_page(st)
elif selected_pillar =="wildlife":
    wildlife()

    