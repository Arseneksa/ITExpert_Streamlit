import streamlit as st

from data.load_data import *
from tools import *
from streamlit_option_menu import option_menu
import geopandas as gpd
import altair as alt
import folium
from streamlit_folium import st_folium
import plotly.express as px
def wildlife_landscape(st,landscape):
    st.title("Wildlfe Landscape app")