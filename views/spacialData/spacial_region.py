import streamlit as st

from data.load_data import *
from tools import *
from streamlit_option_menu import option_menu
import geopandas as gpd
import altair as alt
import folium
from streamlit_folium import st_folium
import plotly.express as px
# @st.cache_data(experimental_allow_widgets=True)
# alt.themes.enable('powerbi')
# alt.themes.enable('default')
def spacial_region(st,data,pd):
    st.markdown(
        ' <span style="font-size:2em;font-weight:bold;margin-left:0px;background:white; opacity:0.97">Congo Basin Monitoring and Evaluation Database</span><br><span style="margin-left:0px;font-size:1em;font-weight:bold" >Spatial data and landcover dashboard</span><br>',
        unsafe_allow_html=True,
    )
    # st.subheader("wildlfe dashboard")
    df = data["spacial"]
    df = df.loc[df['year']!=-1]
    # df.to_csv("data/wildlife.csv")
    
    
    regiondf = pd.DataFrame({
        'id':[1],
        'name':["Congo Basin"],
        "total_area":[4048053]
    })
    landscapesdf  = data["landscapes"]
    sitesdf  = data["sites"]
    countriesdf  = data["countries"]
    # sitesgdf = gpd.read_file("data/All_site.shp",)
    # sitesgdf["site"] = sitesgdf[sitesgdf["Level"]=="Site"]["Site_1"]
    
    years = df['year'].unique()
    min_year = df['year'].min()
    max_year = df['year'].max()
        # st.write(df)
    with st.sidebar:
    # st.title('🏂 US Population Dashboard')
    # st.title('Filter')
        if(min_year<max_year):
            start_year, end_year = st.select_slider(
                'Select year range',
                options=years,
                value=(min_year, max_year)
            )
        else:
            start_year=end_year = st.selectbox('Year', years)
    df = df.loc[(df["year"]>=start_year)&(df["year"]<=end_year)]
    original_df = df
    
    df["year"] = df["year"].astype(str)
    
    # df["main_landscape"] = df["main_landscape"].astype(str)
    # st.write(df.shape)
    # st.write(sitesdf.shape)
    
    #area_cover_region_df =  get_area_covered_table(df ,sitesdf)
    # print("TRIDOM GAB",get_max_area_covered_per_level(area_cover_region_df,1,"Country")) 
    # st.write(df[["region","country",'main_landscape',"landscape","site",'block2',"sector2","level","coverage_rate","year"]])
    # st.write(area_cover_region_df)
    # st.write(get_cumulative_max_area_covered_per_level_per_year(area_cover_region_df,6,"Site","coverage_rate",sitesdf))
    # st.write(landscapesdf)
    
    # data = get_cumulative_max_area_covered_per_level_per_year(area_cover_region_df,1,"Region","area_covered")
    # print("Cumulative TRIDOM GAB",data)
    # cumulativedf = get_cumulative_max_area_covered_per_level_per_year_table(area_cover_region_df,"Site")
   
    # spacial_field_mask_region = ["name","sites","sites_number", "priority"]
    # # spacial_result_df_region = getspacialByLevel(df,spacialdf,sitesdf,"region","spacial","site",1).sort_values(by=['sites_number'], ascending=[ False])
    # # sites_result_df_region = getspacialByLevel(df,sitesdf,spacialdf,"region","site","spacial",1).sort_values(by=['sites_number'], ascending=[ False])
    # spacial_result_df_region =spacial_result_df_region[spacial_field_mask_region]
    # sites_result_df_region =sites_result_df_region[spacial_field_mask_region]
    # sites_result_gdf_region = pd.merge(sites_result_df_region.sort_values(by=['sites_number'], ascending=[ True]), sitesgdf[['site', 'geometry']], left_on="name", right_on='site', how='left')
    # spacial_result_df_region =spacial_result_df_region.rename(
    #     columns={
    #         "name": "Name",
    #         "priority": "Priority",
    #         # "scientific_name": "SPECIES_SN",
            
    #     }
    # )
    # sites_result_df_region =sites_result_df_region.rename(
    #     columns={
    #         "name": "Name",
    #         "priority": "Priority",
    #         # "scientific_name": "SPECIES_SN",
            
    #     }
    # )
    # sites_result_gdf_region =sites_result_gdf_region.rename(
    #     columns={
    #         "name": "Name",
    #         "priority": "Priority",
    #         "sites_number": "Number of spacial",
    #         "sites": "Species list",
            
    #     }
    # )
    # sites_result_gdf_region["Species list"] = sites_result_gdf_region["Species list"].apply(lambda x : 
    #     """
    # <p> <ul>"""+ "".join(["<li>"+l for l in x.split(",")])+""""</li> </p>""")
    # sites_result_gdf_region =gpd.GeoDataFrame(sites_result_gdf_region)
    # sites_result_gdf_region =sites_result_gdf_region.to_crs(sitesgdf.crs)
    # st.write(df)
    tab1, tab2 = st.tabs(["# GENERAL INFORMATIONS", "# RESULT BY INDICATORS"])
    with tab1:
        i=0
        indicators_name =  {"country":"Countries","main_landscape":"Landscapes","site":"Sites"}
        indicators_metric = ["country","main_landscape","site"]
        metric_df = df
        # metric_df = df[df["site"].isin(sitesdf["id"].unique())]
        st.write(metric_df)
        generate_metrics(df,metric_df,indicators_name,indicators_metric,start_year,end_year)
        
            
    with tab2:
        # st.write(st.config["secondaryBackgroundColor"])
        # 3. CSS style definitions
        resultype = option_menu(None, ["Trends in patrols",  "Comparisons"], 
            # icons=['house', 'cloud-upload', "list-task", 'gear'], 
            # menu_icon="cast"
            default_index=0, orientation="horizontal",
            styles={
                "container": {"padding": "0px !important","max-width": "100%","background": "#fff"},
                # "icon": {"color": "orange", "font-size": "1em"}, 
                "icon": {"color": "#D3A715", "font-size": "0.95em"}, 
                "nav-link": {"font-size": "0.95em", "text-align": "left","color":"#000", "margin":"0px", "--hover-color": "#DEDDC2"},
                "nav-link-selected": {"background": "#DEDDC2"},
            }
        )
        
        if resultype == "Trends in patrols":
            # patrol_indicators_name = ["Density (n/km²)","Encounter Rate (n/km)","Population Size (n)", "Capture Rate", "Occupancy Rate"]
            patrol_indicators_name = [
                "Spatial coverage rate (%)",
                "Effort foot patrol (km)",
                "Effort active  (hour)", 
                "Effective patrol  (days)", 
                "Man-days (days)", 
                "Number of patrol", 
                "Total patrol  (days)"]
            patrol_indicators = {
                "Spatial coverage rate (%)":"spatial_coverage_rate",
                "Effort foot patrol (km)":"effort_foot_patrol_km",
                "Effort active (hour)":"effort_active_hour", 
                "Effective patrol (days)":"effective_patrol_days", 
                "Man-days (days)":"man_days", 
                "Number of patrol":"number_Patrol", 
                "Total patrol (days)":"total_patrol_days"}
           
            
            level_df  ={
                "Site":sitesdf,
                "Landscape":landscapesdf,
            }
            col_indicator,col_level, col2_site= st.columns(3)
            with col_indicator:
                selected_patrol_indicator = st.selectbox('Select a indicator', patrol_indicators_name)
                patrol_df = original_df.loc[original_df[patrol_indicators[selected_patrol_indicator]]!=-1]
                patrol_df[selected_patrol_indicator]=patrol_df[patrol_indicators[selected_patrol_indicator]]
                # st.write(patrol_df)
            with col_level:
                selected_level_indicator = st.selectbox('Select level', ["Site","Landscape"])
                patrol_df = patrol_df.loc[patrol_df["level"] ==selected_level_indicator]
                leveldf = level_df[selected_level_indicator]
                site_patrol_df  = leveldf.loc[leveldf["id"].isin(patrol_df[selected_level_indicator.lower()].unique())]
                # st.write(patrol_df)
            # st.write(patrol_df)
            with col2_site:
                if len(site_patrol_df)>0:
                    selected_site_patrol = st.selectbox('Select '+selected_level_indicator.lower()+' ( '+str(len(site_patrol_df))+' )', list(site_patrol_df["name"].unique()))
            if len(site_patrol_df)>0:
                sites_name_id = { x["name"]: x["id"] for x in site_patrol_df[["id","name"]].T.to_dict().values()}
                
                patrol_df = patrol_df.loc[patrol_df[selected_level_indicator.lower()] ==sites_name_id[selected_site_patrol]]
                
                chart_line_patrol = altairLineChart(alt,patrol_df,selected_patrol_indicator,"Trends in "+selected_patrol_indicator.lower()+" in "+selected_site_patrol.lower(),480,"#b7a51d")
                    #st.markdown('#### Trends in  '+ selected_patrol_indicator.lower())
                    # st.write(patrol_df)
                st.altair_chart(chart_line_patrol, theme=None, use_container_width=True)
        if resultype == "Comparisons":
            patrol_indicators_name = [
                "Spatial coverage rate (%)",
                "Effort foot patrol (km)",
                "Effort active  (hour)", 
                "Effective patrol  (days)", 
                "Man-days (days)", 
                "Number of patrol", 
                "Total patrol  (days)"]
            patrol_indicators = {
                "Spatial coverage rate (%)":"spatial_coverage_rate",
                "Effort foot patrol (km)":"effort_foot_patrol_km",
                "Effort active (hour)":"effort_active_hour", 
                "Effective patrol (days)":"effective_patrol_days", 
                "Man-days (days)":"man_days", 
                "Number of patrol":"number_Patrol", 
                "Total patrol (days)":"total_patrol_days"}
            
            level_df  ={
                "Site":sitesdf,
                "Landscape":landscapesdf,
            }
            col_indicator_bar,col_level_bar, col_year= st.columns(3)
            with col_indicator_bar:
                selected_patrol_indicator = st.selectbox('Select a indicator', patrol_indicators_name)
                patrol_df = original_df.loc[original_df[patrol_indicators[selected_patrol_indicator]]!=-1]
                patrol_df[selected_patrol_indicator]=patrol_df[patrol_indicators[selected_patrol_indicator]]
                # st.write(patrol_df)
            with col_level_bar:
                selected_level_indicator = st.selectbox('Select level', ["Site","Landscape"])
                patrol_df = patrol_df.loc[patrol_df["level"] ==selected_level_indicator]
                
                # spacialdf  = spacialdf.loc[spacialdf["id"].isin(patrol_df["spacial"].unique())]
                # st.write(patrol_df)
            # with col_spacial_bar:
            #     spacial = list(spacialdf["name"].unique())
            #     if len(spacial)>0:
            #         selected_spacial = st.selectbox('Select spacial ( '+str(len(spacialdf))+' )',spacial )
            #         spacial_name_id = { x["name"]: x["id"] for x in spacialdf[["id","name"]].T.to_dict().values()}
            #         patrol_df = patrol_df.loc[patrol_df["spacial"] ==spacial_name_id[selected_spacial]]
            #         leveldf = level_df[selected_level_indicator]
            #         patrol_df  = leveldf.loc[leveldf["id"].isin(patrol_df[selected_level_indicator.lower()].unique())]
            # st.write(patrol_df)
            with col_year:
                if len(patrol_df)>0:
                    selected_year_patrol = st.selectbox('Select year ( '+str(len(patrol_df["year"].unique()))+' )', list(patrol_df["year"].unique()))
                    
                    patrol_df =patrol_df.loc[patrol_df["year"] == selected_year_patrol]
                    leveldf = level_df[selected_level_indicator]
                    site_patrol_df  = leveldf.loc[leveldf["id"].isin(patrol_df[selected_level_indicator.lower()].unique())]
            # st.write(patrol_df)
            if len(patrol_df)>0:
                sites_id_name = { x["id"]:x["short_name"]  for x in site_patrol_df[["id","short_name"]].T.to_dict().values()}
                # sites_id_abbr = { x["id"]:}
                abbreviations = ["< "+x["short_name"]+" > "+": "+x["name"]  for x in site_patrol_df[["id","short_name","name"]].T.to_dict().values() if x["short_name"] != x["name"] ]
                # st.write(len(abbreviations))
                if len(abbreviations)>35:
                    size = int(len(abbreviations)/12)
                elif len(abbreviations) > 22:
                    size = int(len(abbreviations)/8)
                
                elif len(abbreviations) > 18:
                    size = int(len(abbreviations)/6)
                elif len(abbreviations) > 6:
                    size = int(len(abbreviations)/3)
                elif len(abbreviations)>3:
                    size = int(len(abbreviations)/2)
                else:
                    size = int(len(abbreviations))
                abbreviations = [" ; ".join(abbreviations[x:x+size]) for x in range(0, len(abbreviations), size)]
                # st.write(abbreviations)
                # patrol_df = patrol_df.loc[patrol_df[selected_level_indicator.lower()] ==sites_name_id[selected_site_patrol]]
                # values = [patrol_indicators[selected_patrol_indicator]]
                # st.write(values)
                patrol_df["main_landscape"] = patrol_df["main_landscape"].astype(str)
                # patrol_df[[value for key , value in patrol_indicators_error[patrol_indicators[selected_patrol_indicator]].items()]] = patrol_df[[value for key , value in patrol_indicators_error[patrol_indicators[selected_patrol_indicator]].items()]].astype(str)
                # index= ["region","country",'main_landscape','site',"landscape","level","spacial"]
                # errors_mask = [value for key , value in patrol_indicators_error[patrol_indicators[selected_patrol_indicator]].items()]
                # patrol_df = pd.pivot_table(patrol_df, values=values, index=index,
                #        aggfunc={patrol_indicators[selected_patrol_indicator]: "max"}).reset_index()
                # mask = index+values+errors_mask 
                # st.write(mask)
                # st.write(index)
                max_indicator_per_level_df= {selected_level_indicator.lower():[],patrol_indicators[selected_patrol_indicator]: []}
                # st.write(patrol_df[selected_level_indicator.lower()])
                # st.write(site_patrol_df["id"].unique())
                for id in site_patrol_df["id"].unique():
                    # st.write(id)
                    # st.write(patrol_df.loc[patrol_df[selected_level_indicator.lower()]==id][patrol_indicators[selected_patrol_indicator]])
                    max_value = patrol_df.loc[patrol_df[selected_level_indicator.lower()]==id][patrol_indicators[selected_patrol_indicator]].max()
                    # st.write(max_value)
                    # st.write(patrol_df.loc[patrol_df[selected_level_indicator.lower()]==id])
                    max_line = patrol_df.loc[(patrol_df[patrol_indicators[selected_patrol_indicator]]==max_value)&(patrol_df[selected_level_indicator.lower()]==id)]
                    # max_line_min = max_line[errors_mask[0]].min()
                    # max_err = max_line.loc[max_line[errors_mask[0]]==max_line_min]
                    # max_line = max_err
                    # max_line_min2 = max_line[errors_mask[1]].min()
                    # max_err2 = max_line.loc[max_line[errors_mask[1]]==max_line_min2]
                    # max_line = max_err2
                    # st.write(max_line)
                    max_indicator_per_level_df[selected_level_indicator.lower()].append(max_line[selected_level_indicator.lower()].unique()[0])
                    max_indicator_per_level_df[patrol_indicators[selected_patrol_indicator]].append(max_line[patrol_indicators[selected_patrol_indicator]].unique()[0])
                    # max_indicator_per_level_df[errors_mask[0]].append(max_line[errors_mask[0]].unique()[0])
                    # max_indicator_per_level_df[errors_mask[1]].append(max_line[errors_mask[1]].unique()[0])
                    # max_indicator_per_level_df["spacial"].append(max_line["spacial"].unique()[0])
                max_indicator_per_level_df = pd.DataFrame(max_indicator_per_level_df).drop_duplicates()  
                # st.write(max_indicator_per_level_df)
                    
                # st.write(patrol_df)
                patrol_df = max_indicator_per_level_df
                # patrol_df = patrol_df[mask].groupby(index).max().reset_index()
                patrol_df[selected_patrol_indicator]=patrol_df[patrol_indicators[selected_patrol_indicator]]
                # patrol_df[[value for key , value in patrol_indicators_error[patrol_indicators[selected_patrol_indicator]].items()]] = patrol_df[[value for key , value in patrol_indicators_error[patrol_indicators[selected_patrol_indicator]].items()]].astype(float)

                
                patrol_df[selected_level_indicator.lower()+' name'] = patrol_df[selected_level_indicator.lower()].apply( lambda x: sites_id_name[x])
                patrol_df[selected_level_indicator.lower()] = patrol_df[selected_level_indicator.lower()].apply( lambda x:sites_id_name[x])
                # st.write(patrol_df)
                chart_bar_patrol = altairBarChartWithLabel(alt,patrol_df,selected_patrol_indicator,"Comparison between "+selected_level_indicator.lower() +"s of "+selected_patrol_indicator.lower() +" in "+str(selected_year_patrol),500,"#b7a51d",selected_level_indicator.lower(),abbreviations)
                #st.markdown('#### Comparison between '+selected_level_indicator.lower()+"s")
                # print(patrol_df.info())
                # st.write(patrol_df)
                st.altair_chart(chart_bar_patrol, theme=None, use_container_width=True)
        # result_tab = st.tabs(["# EFFORT ", "# TRENDS IN patrolS ", "# COMPARISONS "])
        # with result_tab[0]:

        #     st.write("Result page")
        # with result_tab[1]:
            
        #     st.write("Result page")
        # with result_tab[2]:
            
        #     st.write("Result page")
