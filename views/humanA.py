#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from data.load_data import *
from views.HumanAdata.humanA_region import humanA_region
from views.HumanAdata.humanA_country import *
from views.HumanAdata.humanA_landscape import *
from views.HumanAdata.humanA_site import *
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
def humanA():
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
    .vega-embed .vega-actions a, .stDeployButton{
        display: none !important;
    }
    .vega-embed .vega-actions a[target="_blank"]{
        display: block !important;
    }
    .vega-embed summary svg{
        color: black !important;
        margin: 5px !important;
    }
    [data-testid="StyledFullScreenButton"]{
        color: black !important;
        margin-top: 5px !important;
        margin-right: 80px !important;
        
    }
    [data-testid="block-container"] {
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1rem;
        padding-bottom: 0rem;
        margin-bottom: -7rem;
    }
    [data-testid="stExpander"] {
       
        opacity: 0.97;
        font-weight: 25;
        border: none;
        background: white;
        border-radius:15px;
    }
    [data-baseweb="tab"], [data-baseweb="tab"]:active {
        padding: 15px;
        opacity: 0.98;
        font-weight: 25;
        background: white;
        border-radius:15px;
    }
    [data-testid="stArrowVegaLiteChart"] {
        padding: 15px;
        opacity: 0.97;
        background: white;
        margin-bottom:10px;
        border-radius:15px;
    }
    [data-testid="StyledLinkIconContainer"]{
        text-shadow: 2px 2px 4px #000 ;
        color:white
    }
    [data-testid="stWidgetLabel"]{
        /*text-shadow: 0px 0px 2px white,
                0px 0px 3px rgba(255, 255, 255, 1), 
               0px 0px 06px rgba(255, 255, 255, 1), 
			   0px 0px 8px rgba(255, 255, 255, 1),
			   0px 0px 20px rgba(73, 255, 24, 1),
			   0px 0px 30px rgba(73, 255, 24, 1),
			   0px 0px 40px rgba(73, 255, 24, 1),
			   0px 0px 55px rgba(73, 255, 24, 1),
			   0px 0px 75px rgba(73, 255, 24, 1);*/
			   
        color:#000;
        font-weight: bold;
        font-size:1.2em;
    }
    /*[data-testid="manage-app-button"],[data-testid="baseButton-headerNoPadding"]{
        /*display: none !important;*/
    }*/
    /*[data-testid="block-container"],[data-testid="stAppViewBlockContainer"]{
        background-color: white;
        /*background: url(https://images.pexels.com/photos/7304987/pexels-photo-7304987.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1);*/
        background-size: cover;
        overflow-y: scroll;

        min-height:100%;
        
    }*/
    [stMarkdownContainer] {
        background: white;
        opacity: 0.97;
        padding: 5px;
    }
    [data-testid="stVerticalBlock"] {
        padding-left: 0rem;
        padding-right: 0rem;
    }

    [data-testid="stMetric"] {
        /*background-color: #91B384;*/
        background-color: #C0DEB1;
        text-align: center;
        padding: 6px 0;
        border-radius:10px !important;
        /*box-shadow: 0px 0 4px #000;*/
    }
    [data-testid="stMetricValue"] {
        /*background-color: #73815E;*/
       
        text-align: center;
        /*color: #FFFFFF;*/
       
        
    }
    [role="tab"] {
        /*background-color: #C0DEB1;*/
        padding:5px  !important;
        text-align: center;
        border-radius: 3px;
        font-size: 1em;

       
        
    }
    [data-testid="stMetricLabel"] {
        /*background-color: #73815E;*/
       
        text-align: center;
        font-size: 1em;
        /*color: #FFFFFF;*/
       
        
    }
    /*[data-testid="stExpander"] {
        border:1px solid #000;
        border-radius:10px !important;
        text-align: center;
       
        
    }*/
    /*[data-testid="stArrowVegaLiteChart"] {
        background-color: #C0DEB1;
        border-radius:10px !important;
        text-align: center;
        color: #000;
       
        
    }
    [data-testid="stMetricDelta"] {
        /*background-color: #73815E;*/
       
        text-align: center;
        
        padding:2px;
        background: white;
        border: 0.1px solid #D3A715;
        margin-left: 8px;
        margin-right: 8px;
        border-radius:5px

       
        
    }*/

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
    dataurl =onlineurl+"/api/human_activities/"
    sites_url =onlineurl+"/api/sites/"
    countries_url =onlineurl+"/api/countries/"
    activityType_url =onlineurl+"/api/human_activities_types/"
    sampling_method_url =onlineurl+"/api/samplingMethod/"
    landscapes_url =onlineurl+"/api/landscapes/"
    main_landscapes_url =onlineurl+"/api/main_Landscapes/"
    urlblock =onlineurl+"/api/blocks/"
    urlsectors =onlineurl+"/api/sectors/"
    # regional_data_url =onlineurl+"/api/info_pillar/Region/1"
    url_dict  = {
        "humanA":dataurl,
        "sites":sites_url,
        "countries":countries_url,
        "activityType":activityType_url,
        "landscapes":landscapes_url,
        "main_landscapes":main_landscapes_url,
        "blocks":urlblock,
        "sectors":urlsectors,
        "sampling_method":sampling_method_url,
        # "region_data":regional_data_url,
    }
   
    data_dict= load_data(url_dict,st)
    # st.write(data_dict)

    df = pd.json_normalize(data_dict["humanA"])
    
    sites_df = pd.json_normalize(data_dict["sites"])
    countries_df = pd.json_normalize(data_dict["countries"])
    activityType_df = pd.json_normalize(data_dict["activityType"])
    sampling_method_df = pd.json_normalize(data_dict["sampling_method"])
    landscapes_df = pd.json_normalize(data_dict["landscapes"])
    main_landscapes_df = pd.json_normalize(data_dict["main_landscapes"])
    blocksdf = pd.json_normalize(data_dict["blocks"])
    sectorsdf = pd.json_normalize(data_dict["sectors"])
    
    sites = sites_df["name"].unique()
    levels = ["Region","Country","Landscape","Site"]
    
    activityType_df = activityType_df.loc[activityType_df["id"]!=3]
    # st.write(activityType_df)
    #st.write(activityType_df.loc[activityType_df["priority"]==1])
    # activityType_df["name"] = activityType_df["name"].apply(lambda x: x+" *" if x in activityType_df.loc[activityType_df["priority"]==1]["name"].unique() else x)
    sites_df["name"] = sites_df["name"].apply(lambda x: x+" *" if x in sites_df.loc[sites_df["priority"]==1]["name"].unique() else x)
    # st.write(df.loc[df["activityType"]==53])
    # df["region"] = df["region"].astype(str)
    df["country"] = df["country"].astype(int)
    # df["main_landscape"] = df["main_landscape"].astype(str)
    # df["landscape"] = df["landscape"].astype(str)
    df["block2"] = df["block2"].astype(str)
    df["sector2"] = df["sector2"].astype(str)
    # st.write(df["area_covered_km2"].unique())
    # df = df[df["activityType"].isin(activityType_df["id"].unique())]
    # df = df[df["country"].isin(countries_df["id"].unique())]
    # df = df[df["landscape"].isin(landscapes_df["id"].unique())]
    # df = df[df["main_landscape"].isin(main_landscapes_df["id"].unique())]
    # df = df[df["sampling_method"].isin(sampling_method_df["id"].unique())]
    # df = df[df["sector2"].isin(sectorsdf["id"].unique())]
    # df = df[df["block2"].isin(blocksdf["id"].unique())]
    #######################
    # Sidebar
    with st.sidebar:
        # st.title('🏂 US Population Dashboard')
        # st.title('Filter')
        selected_level = st.selectbox('Select a level', levels)
    if selected_level =="Region":
        
        # df = pd.json_normalize(region_data)
        # humanA_region(st,df,data,pd)
        data = {
            "humanA":df,
            "sites":sites_df,
            "countries":countries_df,
            "activityType":activityType_df,
            "landscapes":landscapes_df,
            "main_landscapes":main_landscapes_df,
            "blocks":blocksdf,
            "sectors":sectorsdf,
            "sampling_method":sampling_method_df,
            
        }
        humanA_region(st,data,pd)
    if selected_level =="Country":
        countries_df = countries_df.loc[countries_df["id"].isin(df["country"].unique())]
        countries = countries_df["name"].unique()
        with st.sidebar:
        # st.title('🏂 US Population Dashboard')
        # st.title('Filter')
            selected_country = st.selectbox('Select a country', countries)
        country_name_id = { x["name"]: x["id"] for x in countries_df[["id","name"]].T.to_dict().values()}
        country_id = country_name_id[selected_country]
        landscapes_df  = landscapes_df.loc[landscapes_df["country"]==country_id]
        sites_df  = sites_df.loc[sites_df["country"]==country_id]
        df  = df.loc[df["country"]==country_id]
        data = {
            "humanA":df,
            "sites":sites_df,
            "countries":countries_df,
            "activityType":activityType_df,
            "landscapes":landscapes_df,
            "main_landscapes":main_landscapes_df,
            "blocks":blocksdf,
            "sectors":sectorsdf,
            "sampling_method":sampling_method_df,
            
        }
        
        humanA_country(st,selected_country,data,pd)
    if selected_level =="Landscape":
        # landscapes_df = landscapes_df.loc[landscapes_df["id"].isin(df["landscape"].unique())]
        # landscapes = landscapes_df["name"].unique()
        landscapes_df = landscapes_df.loc[landscapes_df["id"].isin(df["landscape"].unique())]
        m_landscape = main_landscapes_df.loc[main_landscapes_df["id"].isin([1839,1843])]
        m_landscapes = list(m_landscape["name"].unique())
        landscapes = list(landscapes_df["name"].unique())
        landscapes_list = m_landscapes+landscapes
        with st.sidebar:
        # st.title('🏂 US Population Dashboard')
        # st.title('Filter')
            selected_landscape = st.selectbox('Select a landscape', landscapes_list)
        if selected_landscape in landscapes:
            landscape_name_id = { x["name"]: x["id"] for x in landscapes_df[["id","name"]].T.to_dict().values()}
            level ="landscape"
        elif selected_landscape in m_landscapes:
            landscape_name_id = { x["name"]: x["id"] for x in m_landscape[["id","name"]].T.to_dict().values()}
            level ="main_landscape"
        # with st.sidebar:
        # # st.title('🏂 US Population Dashboard')
        # # st.title('Filter')
        #     selected_landscape = st.selectbox('Select a landscape', landscapes)
        # landscape_name_id = { x["name"]: x["id"] for x in landscapes_df[["id","name"]].T.to_dict().values()}
        landscape_id = landscape_name_id[selected_landscape]
        # landscapes_df  = landscapes_df.loc[landscapes_df["landscape"]==country_id]
        sites_df  = sites_df.loc[sites_df[level]==landscape_id]
        df  = df.loc[df[level]==landscape_id]
        data = {
            "humanA":df,
            "sites":sites_df,
            "countries":countries_df,
            "activityType":activityType_df,
            "landscapes":landscapes_df,
            "main_landscapes":main_landscapes_df,
            "blocks":blocksdf,
            "sectors":sectorsdf,
            "level":level,
            "sampling_method":sampling_method_df,
            
        }
        
        humanA_landscape(st,selected_landscape,data,pd)
    if selected_level =="Site":
        sites_df2 = sites_df.loc[sites_df["id"].isin(df["site"].unique())]
        sites = sites_df2["name"].unique()
        with st.sidebar:
        # st.title('🏂 US Population Dashboard')
        # st.title('Filter')
            selected_site = st.selectbox('Select site', sites)
        site_name_id = { x["name"]: x["id"] for x in sites_df[["id","name"]].T.to_dict().values()}
        site_id = site_name_id[selected_site]
        blocksdf  = blocksdf.loc[blocksdf["site"]==site_id]
        sectorsdf  = sectorsdf.loc[sectorsdf["site"]==site_id]
        df  = df.loc[df["site"]==site_id]
        data = {
            "humanA":df,
            "sites":sites_df2,
            "activityType":activityType_df,
            "blocks":blocksdf,
            "sectors":sectorsdf,
            "sampling_method":sampling_method_df,
            
        }
        
        humanA_site(st,selected_site,data,pd)
       