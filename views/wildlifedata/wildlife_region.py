import streamlit as st

from data.load_data import *
from tools import calculate_lenght_difference,format_number, naturalbreaksMap
from streamlit_option_menu import option_menu
import geopandas as gpd
import altair as alt
import folium
from streamlit_folium import st_folium
# @st.cache_data(experimental_allow_widgets=True)
def wildlife_region(st,data,pd):
    st.header("Congo Basin wildlfe dashboard")
    df = data["wildlife"]
    df = df.loc[df['year']!=-1]
    years = df['year'].unique()
    min_year = df['year'].min()
    max_year = df['year'].max()
    sitesgdf = gpd.read_file("data/All_site.shp",)
    sitesgdf["site"] = sitesgdf[sitesgdf["Level"]=="Site"]["Site_1"]
    with st.sidebar:
    # st.title('🏂 US Population Dashboard')
    # st.title('Filter')
        start_year, end_year = st.select_slider(
            'Select year range',
            options=years,
            value=(min_year, max_year)
        )
    df = df.loc[(df["year"]>=start_year)&(df["year"]<=end_year)]
    df["year"] = df["year"].astype(str)
    landscapesdf  = data["landscapes"]
    sitesdf  = data["sites"]
    countriesdf  = data["countries"]
    speciesdf  = data["species"]
    species_field_mask = ["name","sites","sites_number", "priority"]
    species_result_df = getspeciesByLevel(df,speciesdf,sitesdf,"region","species","site",1).sort_values(by=['sites_number'], ascending=[ False])
    sites_result_df = getspeciesByLevel(df,sitesdf,speciesdf,"region","site","species",1).sort_values(by=['sites_number'], ascending=[ False])
    species_result_df =species_result_df[species_field_mask]
    sites_result_df =sites_result_df[species_field_mask]
    sites_result_gdf = pd.merge(sites_result_df.sort_values(by=['sites_number'], ascending=[ True]), sitesgdf[['site', 'geometry']], left_on="name", right_on='site', how='left')
    species_result_df =species_result_df.rename(
        columns={
            "name": "Name",
            "priority": "Priority",
            # "scientific_name": "SPECIES_SN",
            
        }
    )
    sites_result_df =sites_result_df.rename(
        columns={
            "name": "Name",
            "priority": "Priority",
            # "scientific_name": "SPECIES_SN",
            
        }
    )
    sites_result_gdf =sites_result_gdf.rename(
        columns={
            "name": "Name",
            "priority": "Priority",
            "sites_number": "Number of species",
            "sites": "Species list",
            
        }
    )
    sites_result_gdf["Species list"] = sites_result_gdf["Species list"].apply(lambda x : 
        """
    <p> <ul>"""+ "".join(["<li>"+l for l in x.split(",")])+""""</li> </p>""")
    sites_result_gdf =gpd.GeoDataFrame(sites_result_gdf)
    sites_result_gdf =sites_result_gdf.to_crs(sitesgdf.crs)
    tab1, tab2 = st.tabs(["# GENERAL INFORMATIONS", "# RESULT BY INDICATORS"])
    with tab1:
        i=0
        indicators_name =  {"species":"Species","country":"Countries","landscape":"Landscapes","site":"Sites"}
        indicators_metric = [ "species","country","landscape","site"]
        col = st.columns((2,2,2,2))
        for indicator in indicators_metric:
                        
            difference = calculate_lenght_difference(df, start_year, end_year,indicator)
            # st.dataframe(df_population_difference_sorted)
            first_state_name = "# **"+indicators_name[indicator]+ ' inventoried** '
            first_state_population = format_number(len(df[indicator].unique()))
            first_state_delta = format_number(difference)
            with col[i]:
                st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)
                i=i+1

        map = naturalbreaksMap(sites_result_gdf,"Number of species",["Name","Number of species"])
        # folium.TileLayer("CartoDB positron", show=False).add_to(
        #     map
        # )
        
        col = st.columns((4,4))

        with col[0]:   
            st.markdown('#### Most common species in the Congo Basin')
            
            st.dataframe(
                species_result_df,
                column_config={
                    "sites_number": st.column_config.ProgressColumn(
                        "Number of site",
                        help="Number of site where species is present",
                        format="%f /"+str(len(sites_result_df)),
                        min_value=0,
                        max_value=len(sites_result_df),
                    ),
                    "sites": st.column_config.ListColumn(
                        "List of sites",
                        help="List of sites where the species is present",
                        width="small",
                    ),
                },
                hide_index=True, use_container_width=True
            )
        with col[1]:
            st.markdown('#### Site with most species in the Congo Basin')
            tabmap, tabTable = st.tabs(["Map", "Species list per site"])
            
            with tabTable:
                st.dataframe(
                    sites_result_df,
                    column_config={
                        "sites": st.column_config.ListColumn(
                            "List of species",
                            help="List of species present in the site",
                            width="small",
                        ),
                        "sites_number": st.column_config.ProgressColumn(
                            "Number of species",
                            
                            help="Number of species present in the site",
                            format="%f /"+str(len(species_result_df)),
                            min_value=0,
                            max_value=len(species_result_df),
                        ),
                        
                    },
                    hide_index=True,height=350, use_container_width=True
                )
            with tabmap:
                st_folium(map,height=350, use_container_width=True)
    with tab2:
        # 3. CSS style definitions
        resultype = option_menu(None, ["Efforts", "Trends in abundances",  "Comparisons"], 
            # icons=['house', 'cloud-upload', "list-task", 'gear'], 
            # menu_icon="cast"
            default_index=0, orientation="horizontal",
            styles={
                "container": {"padding": "0px !important","max-width": "100%","background": "rgb(18, 37, 13)"},
                # "icon": {"color": "orange", "font-size": "1em"}, 
                "icon": {"color": "rgb(25, 249, 96)", "font-size": "0.95em"}, 
                "nav-link": {"font-size": "0.95em", "text-align": "left","color":"#fff", "margin":"0px", "--hover-color": "#2D312C"},
                "nav-link-selected": {"background": "#2D312C"},
            }
        )
        st.write(resultype)
        # result_tab = st.tabs(["# EFFORT ", "# TRENDS IN ABUNDANCES ", "# COMPARISONS "])
        # with result_tab[0]:

        #     st.write("Result page")
        # with result_tab[1]:
            
        #     st.write("Result page")
        # with result_tab[2]:
            
        #     st.write("Result page")
