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
def wildlife_region(st,data,pd):
    st.header("Congo Basin wildlfe dashboard")
    df = data["wildlife"]
    df = df.loc[df['year']!=-1]
    df.to_csv("data/wildlife.csv")
    original_df = df
    years = df['year'].unique()
    min_year = df['year'].min()
    max_year = df['year'].max()
    regiondf = pd.DataFrame({
        'id':[1],
        'name':["Congo Basin"],
        "total_area":[4048053]
    })
    sitesgdf = gpd.read_file("data/All_site.shp",)
    sitesgdf["site"] = sitesgdf[sitesgdf["Level"]=="Site"]["Site_1"]
    sampling_methods  = data["sampling_method"]
    sampling_method_ids  = df["sampling_method"].unique()
    sampling_methods = sampling_methods.loc[sampling_methods["id"].isin(sampling_method_ids)][["name","id"]].drop_duplicates()
    # st.write(sampling_methods)
    sampling_name_id = {x.replace("_"," "):sampling_methods.loc[sampling_methods["name"]==x]["id"].unique()[0] for x in sampling_methods["name"].unique() if x != None} 
    sampling_method_names = ["All"]+[key for key,value in sampling_name_id.items() ]
    with st.sidebar:
    # st.title('🏂 US Population Dashboard')
    # st.title('Filter')
        select_sampling_method = st.selectbox(
            'Select sampling method',
            options=sampling_method_names
        )
        start_year, end_year = st.select_slider(
            'Select year range',
            options=years,
            value=(min_year, max_year)
        )
        
    df = df.loc[(df["year"]>=start_year)&(df["year"]<=end_year)]
    if select_sampling_method != "All":
        # st.write(sampling_name_id[select_sampling_method])
        df = df.loc[df["sampling_method"]==sampling_name_id[select_sampling_method]]
    

    landscapesdf  = data["landscapes"]
    sitesdf  = data["sites"]
    countriesdf  = data["countries"]
    speciesdf  = data["species"]
    df["year"] = df["year"].astype(str)
    
    # df["main_landscape"] = df["main_landscape"].astype(str)
    # st.write(df.shape)
    area_cover_df =  get_area_covered_table(df ,sitesdf)
    # print("TRIDOM GAB",get_max_area_covered_per_level(area_cover_df,1,"Country")) 
    # st.write(df[["region","country",'main_landscape',"landscape","site",'block2',"sector2","level","coverage_rate","year"]])
    # st.write(area_cover_df)
    # st.write(get_cumulative_max_area_covered_per_level_per_year(area_cover_df,6,"Site","coverage_rate",sitesdf))
    # st.write(landscapesdf)
    
    # data = get_cumulative_max_area_covered_per_level_per_year(area_cover_df,1,"Region","area_covered")
    # print("Cumulative TRIDOM GAB",data)
    # cumulativedf = get_cumulative_max_area_covered_per_level_per_year_table(area_cover_df,"Site")
   
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
        # st.write(sites_result_gdf.to_json())
        # fig = px.choropleth(sites_result_gdf, geojson=sites_result_gdf.to_json(), locations="Name", color="Number of species").update_layout(
        #     template='plotly_dark',
        #     plot_bgcolor='rgba(0, 0, 0, 0)',
        #     paper_bgcolor='rgba(0, 0, 0, 0)',
        #     margin=dict(l=0, r=0, t=0, b=0),
        #     height=350
        # )
        # fig.update_geos(fitbounds="locations", visible=False)

        # st.plotly_chart(fig)
        

        alt.Chart(sites_result_gdf).mark_geoshape().encode(
            color='Number of species:Q'
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(sites_result_gdf, 'id', ['Number of species'])
        ).project(
            type='albersUsa'
        ).properties(
            width=500,
            height=300
        )
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
        # st.write(resultype)
        if resultype =="Efforts":
            # st.write(get_cumulative_max_area_covered_per_level_per_year_table(area_cover_df,"Region","area_covered",regiondf))
            cumulative_region_area_covered_df = get_cumulative_max_area_covered_per_level_per_year_table(area_cover_df,"Region","area_covered",regiondf)
            cumulative_region_area_covered_df["Area covered (Km²)"] = cumulative_region_area_covered_df["area_covered"]
            region_area_covered_df = df.loc[df["area_covered_km2"]!=-1]
            region_area_covered_df =region_area_covered_df[["region","year","area_covered_km2"]].groupby(["year"]).sum().reset_index()
            region_area_covered_df["Area covered (Km²)"] = region_area_covered_df["area_covered_km2"]
            chart = altairLineChart(alt,cumulative_region_area_covered_df,"Area covered (Km²)","Congo Basin Cumulative area covered",450)
            chart2 = altairBarChart(alt,region_area_covered_df,"Area covered (Km²)","Trend in Area covered in the Congo Basin ",490)
            st.markdown('#### Congo Basin cumulative area covered ')
            st.altair_chart(chart, theme=None, use_container_width=True)
            st.markdown('#### Trend in Area covered in the Congo Basin ')
            st.altair_chart(chart2, theme=None, use_container_width=True)
            
            effort_km = simple_cumlative_data_per_year(original_df,"sampling_effort_transect_Km","region")
        # result_tab = st.tabs(["# EFFORT ", "# TRENDS IN ABUNDANCES ", "# COMPARISONS "])
        # with result_tab[0]:

        #     st.write("Result page")
        # with result_tab[1]:
            
        #     st.write("Result page")
        # with result_tab[2]:
            
        #     st.write("Result page")
