#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from data.load_data import *
from views.wildlifedata.wildlife_region import wildlife_region
from views.wildlifedata.wildlife_country import *
from views.wildlifedata.wildlife_landscape import *
from views.wildlifedata.wildlife_site import *
#######################
# Plots

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                            legend=None,
                            scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap




# Donut chart
def make_donut(input_response, input_text, input_color):
    if input_color == 'blue':
        chart_color = ['#29b5e8', '#155F7A']
    if input_color == 'green':
        chart_color = ['#27AE60', '#12783D']
    if input_color == 'orange':
        chart_color = ['#F39C12', '#875A12']
    if input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']
    
    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })
    
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            #domain=['A', 'B'],
                            domain=[input_text, ''],
                            # range=['#29b5e8', '#155F7A']),  # 31333F
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
        
    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=130, height=130)
    return plot_bg + plot + text

# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Calculation year-over-year population migrations
def calculate_population_difference(input_df, input_year):
    selected_year_data = input_df[input_df['year'] == input_year].reset_index()
    previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
    selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
    return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)


#######################
# Page configurationmax_ymax_year
def wildlife():
    # st.set_page_config(
    #     page_title="US Population Dashboard",
    #     page_icon="🏂",
    #     layout="wide",
    #     initial_sidebar_state="expanded")

    # alt.themes.enable("dark")

    #######################
    # CSS styling
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


    #######################
    # Load data
    localurl = "http://localhost:8000"
    onlineurl = "https://biomonitoringwebsite.herokuapp.com"
    dataurl =onlineurl+"/api/wildlife/"
    sites_url =onlineurl+"/api/sites/"
    countries_url =onlineurl+"/api/countries/"
    # regional_data_url =onlineurl+"/api/info_pillar/Region/1"
    url_dict  = {
        "wildlife":dataurl,
        "sites":sites_url,
        "countries":countries_url,
        # "region_data":regional_data_url,
    }
   
    data_dict= load_data(url_dict,st)
    # st.write(data_dict)
    data = data_dict["wildlife"]
    sites = data_dict["sites"]
    countries = data_dict["countries"]
    
    # value  = [x["y"] for x in interestScoreBreakdown["data"]]
    # topics= [x["name"] for x in interestScoreBreakdown["data"]]
    # interestScoreBreakdown = {
    #     "Topic":topics,
    #     "value": value
    # }
    
    # st.write(sites)
    df = pd.json_normalize(data)
    sites_df = pd.json_normalize(sites)
    countries_df = pd.json_normalize(countries)
    df = df.loc[df['year']!=-1]
    years = df['year'].unique()
    min_year = df['year'].min()
    max_year = df['year'].max()
    levels = ["Region","Country","Landscape","Site"]
    countries = countries_df["name"].unique()
    sites = sites_df["name"].unique()
    #######################
    # Sidebar
    with st.sidebar:
        # st.title('🏂 US Population Dashboard')
        # st.title('Filter')
        selected_level = st.selectbox('Select a level', levels)
    if selected_level =="Region":
        regional_data_url =localurl+"/api/info_pillar/Region/wildlife/1"
        url_dict  = {
            "region_data":regional_data_url,
        }
    
        data_dict= load_data(url_dict,st)
        region_data = data_dict["region_data"]
        # df = pd.json_normalize(region_data)
        wildlife_region(st,region_data,pd)
    if selected_level =="Country":
        with st.sidebar:
        # st.title('🏂 US Population Dashboard')
        # st.title('Filter')
            selected_country = st.selectbox('Select a country', countries)
        wildlife_country(st,selected_country)
    if selected_level =="Site":
        with st.sidebar:
        # st.title('🏂 US Population Dashboard')
        # st.title('Filter')
            selected_site = st.selectbox('Select a site', sites)
        wildlife_site(st,selected_site)

   