#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from data.load_data import *
from streamlit_option_menu import option_menu
from tools import altairErrorBarChart, altairErrorLineChart, generate_metrics, gethBarWidth
# from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
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
    .vega-embed .vega-actions a, .stDeployButton {
        display: none !important;
    }
    .vega-embed .vega-actions a[target="_blank"]{
        display: block !important;
    }
   .vega-embed summary svg{
        color: black !important;
        margin: 5px !important;
    }
    [data-testid="stActionButtonIcon"]{
        display:none;
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
    /*[data-testid="StyledLinkIconContainer"]{
        text-shadow: 2px 2px 4px #000 ;
        color:white
    }*/
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
			   
        //color:#000;
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
        background-color: #004F45;
        text-align: center;
        color: white;
        padding: 6px 0;
        border-radius:10px !important;
        /*box-shadow: 0px 0 4px #000;*/
    }
    [data-testid="stMetricValue"] {
        /*background-color: #73815E;*/
        font-size:1.7em !important;
        font-weight:bold;
        text-align: center;
        /*color: #FFFFFF;*/
       
        
    }
    [role="tab"] {
        /*background-color: #97B1AB;*/
        padding:5px  !important;
        text-align: center;
        border-radius: 3px;
        font-size: 1em;

       
        
    }
    [data-testid="stMetricLabel"] {
        /*background-color: #73815E;*/
       
        text-align: center;
        padding : 5px;
        word-wrap: break-word;
        font-size: 1.06em;
        color: #FFFFFF;
       
        
    }
    /*[data-testid="stExpander"] {
        border:1px solid #000;
        border-radius:10px !important;
        text-align: center;
       
        
    }*/
    /*[data-testid="stArrowVegaLiteChart"] {
        background-color: #97B1AB;
        border-radius:10px !important;
        text-align: center;
        color: #000;
       
        
    }
    [data-testid="stMetricDelta"] {
        /*background-color: #73815E;*/
       
        text-align: center;
        
        padding:2px;
        background: white;
        border: 0.1px solid #004F45;
        margin-left: 8px;
        margin-right: 8px;
        border-radius:5px

       
        
    }*/

    [data-testid="stMetricLabel"] {
    display: flex;
    justify-content: center;
    align-items: center;
    }
    [data-testid="baseButton-headerNoPadding"]{
        background:#97B1AB;
        font-weight:bold;
        color:black;
        border-radius:5px;
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

    st.markdown(
            ' <span style="font-size:2.2em;font-weight:bold;margin-left:0px;"> IT Expert</span><br><span style="margin-left:0px;font-size:1em;font-weight:bold" >Wildlife dashboard</span><br>',
            unsafe_allow_html=True,
        )
    

    #######################
    # Load data
    localurl = "http://localhost:8000/api/"
    onlineurl = "https://itexpert97.pythonanywhere.com/api/"
    url =onlineurl
    dataurl =url+"wildlife_data_smart/"
    wildlifedataurl =url+"wildlife_data/"
    forestdataurl =url+"forest_cover_data/"
    human_pressuredataurl =url+"human_pressure_data/"
    patroldataurl =url+"patrol_cover_data/"
    species_url =url+"species/"
    # sampling_method_url =onlineurl+"/api/samplingMethod/"
    sites_url =url+"site/"
    urlblock =url+"block/"
    # regional_data_url =onlineurl+"/api/info_pillar/Region/1"
    url_dict  = {
        "wildlife":dataurl,
        "wildlifedata":wildlifedataurl,
        "forest":forestdataurl,
        "human_p":human_pressuredataurl,
        "patrol":patroldataurl,
        "sites":sites_url,
        "species":species_url,
        "blocks":urlblock,
        # "sampling_method":sampling_method_url,
        # "region_data":regional_data_url,
    }
   
    data_dict= load_data(url_dict,st)
    # st.write(data_dict)

    df = pd.json_normalize(data_dict["wildlife"])
    datadf = pd.json_normalize(data_dict["wildlifedata"])[["year","site","species","block","sampling","encounter_rate"]]
    forestdf=pd.json_normalize(data_dict["forest"])[["year","site","species","block","sampling","forest_cover_rate"]]
    human_pdf=pd.json_normalize(data_dict["human_p"])[["year","site","species","block","sampling","encounter_rate"]]
    patroldf=pd.json_normalize(data_dict["patrol"])[["year","site","species","block","sampling","patrol_cover_rate"]]
    all_data = [datadf,forestdf,human_pdf,patroldf]
    i=0
    for d in all_data:
        all_data[i]["year"] = all_data[i]["year"].astype(str)
        all_data[i]["site"] = all_data[i]["site"].astype(str)
        all_data[i]["species"] = all_data[i]["species"].astype(str)
        all_data[i]["block"] = all_data[i]["block"].astype(str)
        all_data[i]["sampling"] = all_data[i]["sampling"].astype(str)
        # all_data[i]["sampling"] = all_data[i]["sampling"].astype(int)
        print(all_data[i].info())
        i=i+1
    # st.write(all_data)
    df_merged1 = pd.merge(pd.merge(datadf,human_pdf,on=["year","site","species","block","sampling"],suffixes=(None,"_humanP")),forestdf,on=["year","site","species","block","sampling"],suffixes=(None,"_forest"))
    # df_merged1 = df_merged1.drop(["year_humanP","site_humanP","species_humanP","sampling_humanP","year_forest","site_forest","species_forest","sampling_forest"], axis=1)
    df_merged = pd.merge(df_merged1,patroldf,on=["year","site","species","block","sampling"],suffixes=(None,"_patrol"))
    # df_merged = df_merged.drop(["year_patrol","site_patrol","species_patrol","sampling_patrol"], axis=1)
    # st.write(all_data)
    # st.write(df_merged)
    regressiondf = df_merged
    sites_df = pd.json_normalize(data_dict["sites"])
    species_df = pd.json_normalize(data_dict["species"])
    # sampling_method_df = pd.json_normalize(data_dict["sampling_method"])
    # landscapes_df = pd.json_normalize(data_dict["landscapes"])
    # main_landscapes_df = pd.json_normalize(data_dict["main_landscapes"])
    blocksdf = pd.json_normalize(data_dict["blocks"])
    # sectorsdf = pd.json_normalize(data_dict["sectors"])
    
    sites = sites_df["name"].unique()
    levels = ["Site","Block"]
    
    df["block"] = df["block"].astype(str)
    # Sidebar
    years = df['year'].unique()
    min_year = df['year'].min()
    max_year = df['year'].max()
    sites_df2 = sites_df.loc[sites_df["id"].isin(df["site"].unique())]
    sites = sites_df2["name"].unique()
    with st.sidebar:
    # st.title('🏂 US Population Dashboard')
    # st.title('Filter')
        selected_site = st.selectbox('Select site', sites)
    site_name_id = { x["name"]: x["id"] for x in sites_df[["id","name"]].T.to_dict().values()}
    site_id = site_name_id[selected_site]
    blocksdf  = blocksdf.loc[blocksdf["site"]==site_id]
    df  = df.loc[df["site"]==site_id]
    # st.write(df)
    with st.sidebar:
        # st.title('🏂 US Population Dashboard')
        # st.title('Filter')
        if (min_year < max_year):
            start_year, end_year = st.select_slider(
                'Select year range',
                options=years,
                value=(min_year, max_year)
            )
        else:
            start_year = end_year = st.selectbox('Year', years)

    df = df.loc[(df["year"] >= start_year) & (df["year"] <= end_year)]
    species_name_color = { x["name"]: x["color"] for x in species_df[["name","color"]].T.to_dict().values()}
    df["year"] = df["year"].astype(str)  
    # df = pd.json_normalize(region_data)
    # wildlife_region(st,df,data,pd)
    indicators_name = {"species": "Species", "site": "Site", "block": "Blocks"}
    indicators_metric = ["species", "site", "block"]
    metric_df = df[df["site"] == site_id]
    # st.write(metric_df)
    generate_metrics(df, metric_df, indicators_name, indicators_metric, start_year, end_year,"")
    st.success("""
            **Please use the tabs (Trends in abundances & Comparison) and filters to see the information you want. Thank you!!**""")
    level_df = {
                "site": sites_df2,
                "block": blocksdf,
                
            }

    abundance_indicators_name = ["Encounter Rate (n/km)"]
    abundance_indicators = {
        "Encounter Rate (n/km)": "encounter_rate",
        }
    abundance_indicators_error = {
       
        "encounter_rate": {"min": "encounter_rate_min", "max": "encounter_rate_max"},
        
    }
    # resultype = option_menu(None, ["Trends in abundances",  "Comparisons","Generalized linear model analyses"], 
    #         # icons=['house', 'cloud-upload', "list-task", 'gear'], 
    #         # menu_icon="cast"
    #         default_index=0, orientation="horizontal",
    #         styles={
    #             "container": {"padding": "0px !important","max-width": "100%","background": "#fff"},
    #             # "icon": {"color": "orange", "font-size": "1em"}, 
    #             "icon": {"color": "#965F36", "font-size": "0.95em"}, 
    #             "nav-link": {"font-size": "0.95em", "text-align": "left","color":"#000", "margin":"0px", "--hover-color": "#B6D96B"},
    #             "nav-link-selected": {"background": "#B6D96B"},
    #         }
    #     )
    trend_tab , comparison_tab, model_tab= st.tabs(["Trends in abundances", "Comparisons","Factors affecting species abundances"])
    with trend_tab:
        col_indicator, col_level, col_species, col2_site = st.columns(4)
        with col_indicator:
                selected_abundace_indicator = st.selectbox('select indicator', abundance_indicators_name)
                abundance_df = df.loc[df[abundance_indicators[selected_abundace_indicator]] != -1]
                abundance_df[selected_abundace_indicator] = abundance_df[
                    abundance_indicators[selected_abundace_indicator]]
                # st.write(abundance_df)
        with col_level:
            selected_level_indicator = st.selectbox('Select level', ["Site", "Block"])
            selected_level_indicator = selected_level_indicator.lower()
            abundance_df = abundance_df.loc[abundance_df["level"] == selected_level_indicator]
            species_df = species_df.loc[species_df["id"].isin(abundance_df["species"].unique())]
            # st.write(abundance_df)
        with col_species:
            species = list(species_df["name"].unique())
            if len(species) > 0:
                selected_species = st.selectbox('Select species ( ' + str(len(species_df)) + ' )', species)
                species_name_id = {x["name"]: x["id"] for x in species_df[["id", "name"]].T.to_dict().values()}
                abundance_df = abundance_df.loc[abundance_df["species"] == species_name_id[selected_species]]
                leveldf = level_df[selected_level_indicator]
                # st.write(abundance_df)
                if selected_level_indicator in ["block"]:
                    level_indicator = selected_level_indicator.lower() 
                    # abundance_df[level_indicator] = abundance_df[level_indicator].astype(str)
                    # st.write(level_indicator)
                    # st.write(abundance_df[level_indicator])
                    # st.write(leveldf["id"])
                    site_abundance_df = leveldf.loc[
                        leveldf["id"].isin(abundance_df[level_indicator].astype(float).unique())]
                    # st.write(site_abundance_df)
                else:
                    level_indicator = selected_level_indicator.lower()
                    # abundance_df[level_indicator] = abundance_df[level_indicator].astype(str)
                    site_abundance_df = leveldf.loc[
                        leveldf["id"].isin(abundance_df[selected_level_indicator.lower()].unique())]

        # st.write(abundance_df)
        with col2_site:
            if len(species) > 0:
                # st.write(site_abundance_df)
                # st.write(list(site_abundance_df["name"].unique()))
                selected_site_abundance = st.selectbox(
                    'Select ' + selected_level_indicator.lower() + ' ( ' + str(len(site_abundance_df)) + ' )',
                    list(site_abundance_df["name"].unique()))
        if len(species) > 0:
            sites_name_id = {x["name"]: x["id"] for x in site_abundance_df[["id", "name"]].T.to_dict().values()}
            # st.write(abundance_df)
            # st.write(str(float(sites_name_id[selected_site_abundance])))
            # st.write(abundance_df.loc[abundance_df["block"] =="12.0"])
            if selected_level_indicator in ["block"]:
                abundance_df = abundance_df.loc[
                    abundance_df[level_indicator] == str(sites_name_id[selected_site_abundance])]
                # st.write(abundance_df)
            else:
                abundance_df = abundance_df.loc[
                    abundance_df[level_indicator] == sites_name_id[selected_site_abundance]]
            # st.write(abundance_df)
            chart_line_abundace = altairErrorLineChart(alt, abundance_df, selected_abundace_indicator,
                                                        "Trends in " + selected_species.capitalize() + " " + selected_abundace_indicator.lower() + " in " + selected_site_abundance.capitalize()+" from "+str(start_year)+" to "+str(end_year),
                                                        480, abundance_indicators_error[
                                                            abundance_indicators[selected_abundace_indicator]],species_name_color[selected_species])
            ##st.markdown('#### Trends in  ' + selected_abundace_indicator.lower())
            # st.write(abundance_df)
            st.altair_chart(chart_line_abundace, theme=None, use_container_width=True)
    
    with comparison_tab : 
        col_indicator_bar, col_level_bar, col_species_bar,col_year = st.columns(4)
        with col_indicator_bar:
            selected_abundace_indicator = st.selectbox('select indicator', abundance_indicators_name,key="abundance_indicators_name_bar")
            abundance_df = df.loc[df[abundance_indicators[selected_abundace_indicator]] != -1]
            abundance_df[selected_abundace_indicator] = abundance_df[
                abundance_indicators[selected_abundace_indicator]]
            # st.write(abundance_df)
        with col_level_bar:
            selected_level_indicator = st.selectbox('Select level', ["Site", "Block"],key="selected_level_indicator_bar")
            selected_level_indicator = selected_level_indicator.lower()
            abundance_df = abundance_df.loc[abundance_df["level"] == selected_level_indicator]
            species_df = species_df.loc[species_df["id"].isin(abundance_df["species"].unique())]
            # st.write(abundance_df)
        with col_species_bar:
            species = list(species_df["name"].unique())
            if len(species) > 0:
                selected_species = st.selectbox('Select species ( ' + str(len(species_df)) + ' )', species,key="selected_species_bar")
                species_name_id = {x["name"]: x["id"] for x in species_df[["id", "name"]].T.to_dict().values()}
                abundance_df = abundance_df.loc[abundance_df["species"] == species_name_id[selected_species]]
                # st.write(abundance_df)
                leveldf = level_df[selected_level_indicator]
                if selected_level_indicator in ["block"]:
                    level_indicator = selected_level_indicator.lower() 
                    # st.write(abundance_df[level_indicator].astype(float))
                    site_abundance_df = leveldf.loc[
                        leveldf["id"].isin(abundance_df[level_indicator].astype(float).unique())]
                else:
                    level_indicator = selected_level_indicator.lower()
                    site_abundance_df = leveldf.loc[leveldf["id"].isin(abundance_df[level_indicator].unique())]
        # st.write(site_abundance_df)
        with col_year:
            if len(species)>0:
                selected_year_abundance = st.selectbox('Select year'+ '( '+str(len(abundance_df["year"].unique()))+' )', list(abundance_df["year"].unique()))
                abundance_df = abundance_df.loc[abundance_df["year"]==selected_year_abundance]
        if len(species) > 0:
            if selected_level_indicator in ["block"]:
                # st.write(site_abundance_df[["id","name"]].T.to_dict().values())
                sites_id_name = {x["id"]: x["name"] for x in site_abundance_df[["id", "name"]].T.to_dict().values()}
                # sites_id_abbr = { x["id"]:}
                abbreviations = ["< " + x["short_name"] + " > " + ": " + x["name"] for x in
                                    site_abundance_df[["id", "short_name", "name"]].T.to_dict().values()]
            else:
                min = abundance_indicators_error[abundance_indicators[selected_abundace_indicator]]["min"]
                max = abundance_indicators_error[abundance_indicators[selected_abundace_indicator]]["max"]
                abundance_df = abundance_df[["site",'block',"level",abundance_indicators[selected_abundace_indicator],selected_abundace_indicator,min,max]].groupby(["site","level"]).max().reset_index()
                # st.write(site_abundance_df[["id","name"]].T.to_dict().values())
                sites_id_name = {x["id"]: x["short_name"] for x in
                                    site_abundance_df[["id", "short_name"]].T.to_dict().values()}
                # sites_id_abbr = { x["id"]:}
                abbreviations = ["< " + x["short_name"] + " > " + ": " + x["name"] for x in
                                    site_abundance_df[["id", "short_name", "name"]].T.to_dict().values() ]
                
            # st.write(len(abbreviations))
            # st.write(abbreviations)
            if len(abbreviations) > 35:
                size = int(len(abbreviations) / 12)
            elif len(abbreviations) > 22:
                size = int(len(abbreviations) / 8)
            elif len(abbreviations) > 18:
                size = int(len(abbreviations) / 6)
            elif len(abbreviations) > 5:
                size = int(len(abbreviations) / 2)
            else:
                size = int(len(abbreviations))
            # st.write(abbreviations)
            if len(abbreviations) > 0:
                abbreviations = [" ; ".join(abbreviations[x:x + size]) for x in range(0, len(abbreviations), size)]
                # st.write(abbreviations)
                # abundance_df = abundance_df.loc[abundance_df[selected_level_indicator.lower()] ==sites_name_id[selected_site_abundance]]
                # values = [abundance_indicators[selected_abundace_indicator]]
                # st.write(values)
                abundance_df[[value for key, value in abundance_indicators_error[
                    abundance_indicators[selected_abundace_indicator]].items()]] = abundance_df[
                    [value for key, value in
                        abundance_indicators_error[abundance_indicators[selected_abundace_indicator]].items()]].astype(
                    str)
                # index= ["region","country",'main_landscape','site',"landscape","level","species"]
                errors_mask = [value for key, value in abundance_indicators_error[
                    abundance_indicators[selected_abundace_indicator]].items()]
                # abundance_df = pd.pivot_table(abundance_df, values=values, index=index,
                #        aggfunc={abundance_indicators[selected_abundace_indicator]: "max"}).reset_index()
                # mask = index+values+errors_mask
                # st.write(mask)
                # st.write(index)

                abundance_df[level_indicator] = abundance_df[level_indicator].astype(float)
                abundance_df[level_indicator] = abundance_df[level_indicator].astype(int)

                # st.write(abundance_df)
                abundance_df[selected_abundace_indicator] = abundance_df[
                    abundance_indicators[selected_abundace_indicator]]
                abundance_df[[value for key, value in abundance_indicators_error[
                    abundance_indicators[selected_abundace_indicator]].items()]] = abundance_df[
                    [value for key, value in
                        abundance_indicators_error[abundance_indicators[selected_abundace_indicator]].items()]].astype(
                    float)

                abundance_df[selected_level_indicator.lower() + ' name'] = abundance_df[level_indicator].apply(
                    lambda x: sites_id_name[x])
                # st.write(abundance_df)
                chart_bar_abundace = altairErrorBarChart(alt, abundance_df, selected_abundace_indicator,
                                                            "Comparison between " + selected_level_indicator.lower() + "s : " + selected_species.capitalize() + " " + selected_abundace_indicator.lower() + " in " + str(
                                                                selected_year_abundance) , 540,
                                                            abundance_indicators_error[
                                                                abundance_indicators[selected_abundace_indicator]],
                                                            selected_level_indicator.lower() + ' name', abbreviations,
                                                            gethBarWidth(abundance_df),species_name_color[selected_species])
                ##st.markdown('#### Comparison between ' + selected_level_indicator.lower() + "s")
                # print(abundance_df.info())
                # st.write(abundance_df)
                st.altair_chart(chart_bar_abundace, theme=None, use_container_width=True)
    with model_tab:
        
        features = ["encounter_rate_humanP","forest_cover_rate","patrol_cover_rate"]
        target = "encounter_rate"
        x= regressiondf[features]
        y=regressiondf[target]
        x2 = sm.add_constant(x)
        model2 = sm.OLS(y, x2)
        results = model2.fit()
        col = st.columns((4, 4), gap='small')
        
        with col[0]:
            st.write("### Summary")
            st.write(results.summary())
        with col[1]:
            st.success("Encouter rate ="+str(round(results.params["const"],3))+" + "+str(round(results.params["encounter_rate_humanP"],3))+"* **Encouter rate human pressure** "+" + "+str(round(results.params["forest_cover_rate"],3))+"* **Forest cover rate** "+" + "+str(round(results.params["patrol_cover_rate"],3))+"* **Patrol cover rate** ")
        # print(results.summary())
        print(f"coefficient of determination stat: {results.rsquared}")
        print(f"regression coefficients: {results.params}")
