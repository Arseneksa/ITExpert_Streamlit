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

    