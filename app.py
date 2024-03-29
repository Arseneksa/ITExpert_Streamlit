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
from views.forest_cover import forest_cover
from views.human_pressure import human_pressure
from views.human_wc import *
from views.patrol_cover import patrol_cover
from views.wildlife import wildlife
# from views.humanA import humanA
# from views.law_enforcement_patrol_data import lawEnforcement
# from views.spatial_data_and_landcover import spacialData
# from views.wildlife import wildlife

st.set_page_config(
    page_title="IT Expert test",
    page_icon="./app/static/logo.png",
    layout="wide",
    initial_sidebar_state="expanded")
st.markdown("""
    <style>

    [data-testid="block-container"],.block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1rem;
        padding-bottom: 0rem;
        margin-bottom: -7rem;
    }

    [data-testid="stVerticalBlock"], .stVerticalBlock {
        padding-left: 0rem;
        padding-right: 0rem;
    }

    [data-testid="stMetric"], .stMetric {
        /*background-color: #393939;*/
        text-align: center;
        padding: 15px 0;
    }

    [data-testid="stMetricLabel"], .stMetricLabel {
    display: flex;
    justify-content: center;
    align-items: center;
    }

    [data-testid="stMetricDeltaIcon-Up"], .stMetricDeltaIcon-Up {
        position: relative;
        left: 38%;
        -webkit-transform: translateX(-50%);
        -ms-transform: translateX(-50%);
        transform: translateX(-50%);
    }

    [data-testid="stMetricDeltaIcon-Down"], .stMetricDeltaIcon-Down {
        position: relative;
        left: 38%;
        -webkit-transform: translateX(-50%);
        -ms-transform: translateX(-50%);
        transform: translateX(-50%);
    }
    .st-emotion-cache-klqnuk{
        display: none;
    }
    .st-emotion-cache-16txtl3 {
        padding: 3rem 1.5rem;
    }
    /*[data-testid='stToolbar']{
        display: none;
    }*/
    </style>
    <script>
    
        //document.querySelector("[data-testid='stToolbar]").style.display = "none");
        //document.querySelector(".st-emotion-cache-klqnuk").innerHtml = "<b>Loading ...</b>");
        
    </script>
    """, unsafe_allow_html=True)
alt.themes.enable("dark")


pillars= [
    "Human wildlife conflict","Wildlife ","Human pressure","Forest cover", "Patrol cover"#,"Law enforcement","Capacity building"
]
with st.sidebar:
    # st.title('🏂 US Population Dashboard')
    st.markdown(
            '<img src="./app/static/logo.png"  style="width:95%"> ',
            unsafe_allow_html=True,
        )
    # st.image("static/logo.jpg")
    st.title('Filter')
    
    # indicator_list = list(df_reshaped.year.unique())[::-1]
    
    selected_pillar = st.selectbox('Select monitoring pillar', pillars)
    
    
content = st.empty()
if selected_pillar =="Human wildlife conflict":
    Human_WC_page(st)
elif selected_pillar =="Wildlife ":
    
    wildlife()
elif selected_pillar =="Human pressure":
    
    human_pressure()
elif selected_pillar =="Forest cover":
    
    forest_cover()
    
elif selected_pillar =="Patrol cover":
    
    patrol_cover()
# elif selected_pillar =="Law enforcement":
    
#     lawEnforcement()
# elif selected_pillar =="Spatial data and landcover":
    
#     spacialData()

    