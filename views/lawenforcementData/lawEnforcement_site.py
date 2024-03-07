from data.load_data import *
from tools import *
from streamlit_option_menu import option_menu
import geopandas as gpd
import altair as alt
import folium
from streamlit_folium import st_folium


def lawEnforcement_site(st, selected_site, data, pd):
    st.markdown(
        ' <span style="font-size:2em;font-weight:bold;margin-left:0px;background:white; opacity:0.97">Congo Basin Monitoring and Evaluation Database</span><br><span style="margin-left:0px;font-size:1em;font-weight:bold" >Human activities dashboard</span><br>',
        unsafe_allow_html=True,
    )
    