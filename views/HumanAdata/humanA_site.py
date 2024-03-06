from data.load_data import *
from tools import *
from streamlit_option_menu import option_menu
import geopandas as gpd
import altair as alt
import folium
from streamlit_folium import st_folium


def humanA_site(st, selected_site, data, pd):
    st.markdown(
        ' <span style="font-size:2em;font-weight:bold;margin-left:0px;background:white; opacity:0.97">Congo Basin Monitoring and Evaluation Database</span><br><span style="margin-left:0px;font-size:1em;font-weight:bold" >Human activities dashboard</span><br>',
        unsafe_allow_html=True,
    )
    # st.subheader("wildlfe dashboard")
    df = data["humanA"]
    df = df.loc[df['year'] != -1]
    # df.to_csv("data/wildlife.csv")
    regiondf = pd.DataFrame({
        'id': [1],
        'name': ["Congo Basin"],
        "total_area": [4048053]
    })
    sitesdf = data["sites"]
    blockdf = data["blocks"]
    sectordf = data["sectors"]
    site_name_id = {x["name"]: x["id"] for x in sitesdf[["id", "name"]].T.to_dict().values()}
    site_id = site_name_id[selected_site]
    activityTypedf = data["activityType"]
    sitesgdf = gpd.read_file("data/All_site.shp", )

    sitesgdf["site"] = sitesgdf[sitesgdf["Level"] == "Site"]["Site_1"]

    sampling_methods = data["sampling_method"]
    sampling_method_ids = df[df["site"] == site_id]["sampling_method"].dropna().unique()
    # st.write(sampling_method_ids,sampling_methods["id"].unique())
    sampling_methods = sampling_methods.loc[sampling_methods["id"].isin(sampling_method_ids)][
        ["name", "id"]].drop_duplicates()
    sampling_methods = sampling_methods.loc[sampling_methods["id"].isin(df["sampling_method"].unique())]
    sampling_method_ids = sampling_methods.loc[sampling_methods["id"].isin(df["sampling_method"].unique())][
        "id"].unique()
    # st.write(sampling_method_ids,sampling_methods["id"].unique())
    # st.write(sampling_methods_list)
    sampling_name_id = {x.replace("_", " "): sampling_methods.loc[sampling_methods["name"] == x]["id"].unique()[0] for x
                        in sampling_methods["name"].unique() if x != None}
    sampling_method_names = ["All"] + [key for key, value in sampling_name_id.items()]
    with st.sidebar:
        # st.title('🏂 US Population Dashboard')
        # st.title('Filter')
        select_sampling_method = st.selectbox(
            'Select sampling method',
            options=sampling_method_names
        )
        # start_year, end_year = st.select_slider(
        #     'Select year range',
        #     options=years,
        #     value=(min_year, max_year)
        # )

    if select_sampling_method != "All":
        # st.write(sampling_name_id[select_sampling_method])

        df = df.loc[df["sampling_method"] == sampling_name_id[select_sampling_method]]
        years = df['year'].unique()
        min_year = df['year'].min()
        max_year = df['year'].max()
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

    else:
        years = df['year'].unique()
        min_year = df['year'].min()
        max_year = df['year'].max()
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
    original_df = df

    df["year"] = df["year"].astype(str)

    # df["main_landscape"] = df["main_landscape"].astype(str)
    # st.write(df.shape)
    #area_cover_df = get_area_covered_table(df, sitesdf)
    # st.write(area_cover_df)
    # print("TRIDOM GAB",get_max_area_covered_per_level(area_cover_df,1,"Country")) 
    # st.write(df[["region","country",'main_landscape',"landscape","site",'block2',"sector2","level","coverage_rate","year"]])
    # st.write(area_cover_df)
    # st.write(get_cumulative_max_area_covered_per_level_per_year(area_cover_df,6,"Site","coverage_rate",sitesdf))
    # st.write(landscapesdf)

    # data = get_cumulative_max_area_covered_per_level_per_year(area_cover_df,1,"Region","area_covered")
    # print("Cumulative TRIDOM GAB",data)
    # cumulativedf = get_cumulative_max_area_covered_per_level_per_year_table(area_cover_df,"Site")

    # activityType_field_mask = ["name", "sites", "sites_number", "priority"]
    # activityType_result_df = getactivityTypeByLevel(df, activityTypedf, sitesdf, "region", "activityType", "site", 1).sort_values(
    #     by=['sites_number'], ascending=[False])
    # sites_result_df = getactivityTypeByLevel(df, sitesdf, activityTypedf, "region", "site", "activityType", 1).sort_values(
    #     by=['sites_number'], ascending=[False])
    # activityType_result_df = activityType_result_df[activityType_field_mask]
    # sites_result_df = sites_result_df[activityType_field_mask]
    # sites_result_gdf = pd.merge(sites_result_df.sort_values(by=['sites_number'], ascending=[True]),
    #                             sitesgdf[['site', 'geometry']], left_on="name", right_on='site', how='left')
    # activityType_result_df = activityType_result_df.rename(
    #     columns={
    #         "name": "Name",
    #         "priority": "Priority",
    #         # "scientific_name": "SPECIES_SN",

    #     }
    # )
    # sites_result_df = sites_result_df.rename(
    #     columns={
    #         "name": "Name",
    #         "priority": "Priority",
    #         # "scientific_name": "SPECIES_SN",

    #     }
    # )
    # sites_result_gdf = sites_result_gdf.rename(
    #     columns={
    #         "name": "Name",
    #         "priority": "Priority",
    #         "sites_number": "Number of activityType",
    #         "sites": "Species list",

    #     }
    # )
    # sites_result_gdf["Species list"] = sites_result_gdf["Species list"].apply(lambda x:
    #                                                                           """
    # <p> <ul>""" + "".join(["<li>" + l for l in x.split(",")]) + """"</li> </p>""")
    # sites_result_gdf = gpd.GeoDataFrame(sites_result_gdf)
    # sites_result_gdf = sites_result_gdf.to_crs(sitesgdf.crs)
    tab1, tab2 = st.tabs(["# GENERAL INFORMATIONS", "# RESULT BY INDICATORS"])
    with tab1:
        indicators_name = {"activityType": "Activity types", "block2": "Blocks", "sector2": "Sectors"}
        indicators_metric = ["activityType", "block2", "sector2"]
        metric_df = df[df["site"] == site_id]
        # st.write(metric_df)
        generate_metrics(df, metric_df, indicators_name, indicators_metric, start_year, end_year)
        # # geo_chart = alt.Chart(sites_result_gdf, title="Vega-Altair").mark_geoshape().encode( #     alt.Color(
        # "Number of activityType:N").scale(None) # ).project(type="identity", reflectY=True) # st.altair_chart(geo_chart)
        # try: # map = naturalbreaksMap(sites_result_gdf,"Number of activityType",["Name","Number of activityType"]) finally:
        # print("teste") # folium.TileLayer("CartoDB positron", show=False).add_to( #     map # ) # st.write(
        # sites_result_gdf.to_json()) # fig = px.choropleth(sites_result_gdf, geojson=sites_result_gdf.to_json(),
        # locations="Name", color="Number of activityType").update_layout( #     template='plotly_dark',
        #     plot_bgcolor='rgba(0, 0, 0, 0)', #     paper_bgcolor='rgba(0, 0, 0, 0)', #     margin=dict(l=0, r=0,
        #     t=0, b=0), #     height=350 # ) # fig.update_geos(fitbounds="locations", visible=False)

        #     # st.plotly_chart(fig)

        #     # alt.Chart(sites_result_gdf).mark_geoshape().encode(
        #     #     color='Number of activityType:Q'
        #     # ).transform_lookup(
        #     #     lookup='id',
        #     #     from_=alt.LookupData(sites_result_gdf, 'id', ['Number of activityType'])
        #     # ).project(
        #     #     type='albersUsa'
        #     # ).properties(
        #     #     width=500,
        #     #     height=300
        #     # )
        #     col = st.columns((4,4))
        # tab_richness, tab_occurence = st.tabs(["# Species richness by site", "# Species occurence in site"])

        # with tab_richness:
        #     #st.markdown('#### Species richness by site')
        #     # tabmap, tabTable = st.tabs(["Map", "Species list per site"])

        #     # with tabmap:

        #     with st.expander("Table", True):
        #         # st.success('Double-click in the activityType list cell to see all the activityType', icon="ℹ️")
        #         # time.sleep(10)
        #         # msg = ''
        #         st.dataframe(
        #             sites_result_df,
        #             column_config={
        #                 "sites": st.column_config.ListColumn(
        #                     "Species list ( **Double-click on each  cell to see all the activityType**)",
        #                     help="List of activityType present in the site",
        #                     width="large",
        #                 ),
        #                 "sites_number": st.column_config.ProgressColumn(
        #                     "Number of activityType",

        #                     help="Number of activityType present in the site",
        #                     format="%f /" + str(len(activityType_result_df)),
        #                     min_value=0,
        #                     max_value=len(activityType_result_df),
        #                 ),

        #             },
        #             hide_index=True, height=350, use_container_width=True
        #         )
        #     # with st.expander("Map",expanded=True):
        #     #     st_folium(map,height=650, use_container_width=True)

        # with tab_occurence:
        #     #st.markdown('#### Species occurence in site')
        #     # st.success('Double-click in the site list cell to see all the sites', icon="ℹ️")
        #     st.dataframe(
        #         activityType_result_df,
        #         column_config={
        #             "sites_number": st.column_config.ProgressColumn(
        #                 "Number of site ",
        #                 help="Number of site where activityType is present",
        #                 format="%f /" + str(len(sites_result_df)),
        #                 min_value=0,
        #                 max_value=len(sites_result_df),
        #             ),
        #             "sites": st.column_config.ListColumn(
        #                 "List of sites ( **Double-click on each  cell to see all sites**)",
        #                 help="List of sites where the activityType is present",
        #                 width="large",
        #             ),
        #         },
        #         hide_index=True, use_container_width=True
        #     )
        #     # with tabTable:

    with tab2:
        # st.write(st.config["secondaryBackgroundColor"])
        # 3. CSS style definitions
        resultype = option_menu(None, ["Trends in abundances", "Comparisons"],
                                # icons=['house', 'cloud-upload', "list-task", 'gear'],
                                # menu_icon="cast"
                                default_index=0, orientation="horizontal",
                                styles={
                                    "container": {"padding": "0px !important", "max-width": "100%",
                                                  "background": "#fff"},
                                    # "icon": {"color": "orange", "font-size": "1em"},
                                    "icon": {"color": "#D3A715", "font-size": "0.95em"},
                                    "nav-link": {"font-size": "0.95em", "text-align": "left", "color": "#000",
                                                 "margin": "0px", "--hover-color": "#DEDDC2"},
                                    "nav-link-selected": {"background": "#DEDDC2"},
                                }
                                )
        # st.write(resultype)
        # if resultype == "Efforts":
        #     # st.write(get_cumulative_max_area_covered_per_level_per_year_table(area_cover_df,"Region","area_covered",regiondf))

        #     effort_indicators = ["Area covered (Km²)", "Area coverege rate (%)", "Sampling transect effort (Km)"]
        #     col_indicator_effort, col_efffort_graph_type = st.columns(2)
        #     with col_indicator_effort:
        #         selected_effort_indicator = st.selectbox('Select a indicator', effort_indicators)
        #     with col_efffort_graph_type:
        #         selected_effort_graph_type = st.selectbox('Select graph type', ["Cumulative", "Trends"])
        #     if selected_effort_indicator == "Area covered (Km²)":
        #         cumulative_site_area_covered_df = get_cumulative_max_area_covered_per_level_per_year_table(
        #             area_cover_df, "Site", "area_covered_km2", sitesdf)
        #         # st.write(cumulative_site_area_covered_df)
        #         cumulative_site_area_covered_df[selected_effort_indicator] = cumulative_site_area_covered_df[
        #             "area_covered"]
        #         site_area_covered_df = df.loc[(df["area_covered_km2"] != -1) & (df["level"] == "Site")]
        #         # st.write(site_area_covered_df)
        #         site_area_covered_df = site_area_covered_df[["site", "year", "area_covered_km2"]].groupby(
        #             ["year"]).max().reset_index()
        #         site_area_covered_df[selected_effort_indicator] = site_area_covered_df["area_covered_km2"]
        #         chart_cumulative_area_covered = altairLineChart(alt, cumulative_site_area_covered_df,
        #                                                         selected_effort_indicator,
        #                                                         selected_site.capitalize() + "cumulative area covered",
        #                                                         480)
        #         chart_trend_in_area_covered = altairBarChart(alt, site_area_covered_df, selected_effort_indicator,
        #                                                      "Trend in Area covered in " + selected_site.capitalize(),
        #                                                      490)
        #         if selected_effort_graph_type == "Cumulative":
        #             ##st.markdown('#### ' + selected_site.capitalize() + ' cumulative area covered ')
        #             st.altair_chart(chart_cumulative_area_covered, theme=None, use_container_width=True)
        #         else:
        #             #st.markdown('#### Trend in Area covered in  ' + selected_site.capitalize())
        #             st.altair_chart(chart_trend_in_area_covered, theme=None, use_container_width=True)
        #     if selected_effort_indicator == "Area coverege rate (%)":
        #         cumulative_site_area_covered_df2 = get_cumulative_max_area_covered_per_level_per_year_table(
        #             area_cover_df, "Site", "coverage_rate", sitesdf)
        #         # st.write(cumulative_site_area_covered_df)
        #         if len(cumulative_site_area_covered_df2) > 0:
        #             cumulative_site_area_covered_df2[selected_effort_indicator] = cumulative_site_area_covered_df2[
        #                 "area_covered"]
        #             site_area_covered_df2 = df.loc[(df["coverage_rate"] != -1) & (df["level"] == "Site")]
        #             # st.write(site_area_covered_df)
        #             site_area_covered_df2 = site_area_covered_df2[["site", "year", "coverage_rate"]].groupby(
        #                 ["year"]).max().reset_index()
        #             site_area_covered_df2[selected_effort_indicator] = site_area_covered_df2["coverage_rate"]
        #             chart_cumulative_area_covered = altairLineChart(alt, cumulative_site_area_covered_df2,
        #                                                             selected_effort_indicator,
        #                                                             selected_site.capitalize() + "cumulative area covered",
        #                                                             480)
        #             chart_trend_in_area_covered = altairBarChart(alt, site_area_covered_df2, selected_effort_indicator,
        #                                                          "Trend in Area covered in " + selected_site.capitalize(),
        #                                                          490)
        #             if selected_effort_graph_type == "Cumulative":
        #                 #st.markdown('#### ' + selected_site.capitalize() + ' cumulative area covered ')
        #                 st.altair_chart(chart_cumulative_area_covered, theme=None, use_container_width=True)
        #             else:
        #                 #st.markdown('#### Trend in Area covered in  ' + selected_site.capitalize())
        #                 st.altair_chart(chart_trend_in_area_covered, theme=None, use_container_width=True)
        #     elif selected_effort_indicator == "Sampling transect effort (Km)":

        #         sampling_effort_df = original_df.loc[original_df["sampling_effort_transect_Km"] != -1]

        #         if len(sampling_effort_df) > 0:
        #             region_sampling_transect_effort_df = sampling_effort_df[
        #                 ["site", "year", "sampling_effort_transect_Km"]].groupby(["year"]).sum().reset_index()

        #             cumulmative_effort_km = simple_cumlative_data_per_year(sampling_effort_df,
        #                                                                    "sampling_effort_transect_Km", "site")
        #             region_sampling_transect_effort_df[selected_effort_indicator] = region_sampling_transect_effort_df[
        #                 "sampling_effort_transect_Km"]
        #             chart_cumulative_sampling_transect_effort = altairLineChart(alt, cumulmative_effort_km,
        #                                                                         selected_effort_indicator,
        #                                                                         "Congo Basin cumulative " + selected_effort_indicator.lower(),
        #                                                                         480)
        #             chart_trend_in_sampling_transect_effort = altairBarChart(alt, region_sampling_transect_effort_df,
        #                                                                      selected_effort_indicator,
        #                                                                      "Trend in " + selected_effort_indicator.lower() + " in the Congo Basin ",
        #                                                                      490)

        #             if selected_effort_graph_type == "Cumulative":
        #                 ##st.markdown('#### Congo Basin cumulative area covered ')
        #                 st.altair_chart(chart_cumulative_sampling_transect_effort, theme=None, use_container_width=True)
        #             else:
        #                 ##st.markdown('#### Trend in Area covered in the Congo Basin ')
        #                 st.altair_chart(chart_trend_in_sampling_transect_effort, theme=None, use_container_width=True)
        if resultype == "Trends in abundances":
            abundance_indicators_name = ["Encounter Rate (n/km)"]
            abundance_indicators = {
                "Density (n/km²)": "density",
                "Encounter Rate (n/km)": "encounterRate",
                "Population Size (n)": "populationSize",
                "Capture Rate": "captureRate",
                "Occupancy Rate": "occupancyRate"}
            abundance_indicators_error = {
                "density": {"min": "densityMinimumError", "max": "density_maximumError"},
                "encounterRate": {"min": "encounterRateMinimumError", "max": "encounterRateMaximumError"},
                "populationSize": {"min": "populationSizeMinimumError", "max": "populationSizeMaximumError"},
                "captureRate": {"min": "captureRateMinimumError", "max": "captureRateMaximumError"},
                "occupancyRate": {"min": "occupancyRateMinimumError", "max": "occupancyRateMaximumError"}
            }

            level_df = {
                "Site": sitesdf,
                "Block": blockdf,
                "Sector": sectordf,
            }
            col_indicator, col_level, col_activityType, col2_site = st.columns(4)
            with col_indicator:
                selected_abundace_indicator = st.selectbox('Select a indicator', abundance_indicators_name)
                abundance_df = original_df.loc[original_df[abundance_indicators[selected_abundace_indicator]] != -1]
                abundance_df[selected_abundace_indicator] = abundance_df[
                    abundance_indicators[selected_abundace_indicator]]
                # st.write(abundance_df)
            with col_level:
                selected_level_indicator = st.selectbox('Select level', ["Site", "Block", "Sector"])
                abundance_df = abundance_df.loc[abundance_df["level"] == selected_level_indicator]
                activityTypedf = activityTypedf.loc[activityTypedf["id"].isin(abundance_df["activityType"].unique())]
                # st.write(abundance_df)
            with col_activityType:
                activityType = list(activityTypedf["name"].unique())
                if len(activityType) > 0:
                    selected_activityType = st.selectbox('Select activityType ( ' + str(len(activityTypedf)) + ' )', activityType)
                    activityType_name_id = {x["name"]: x["id"] for x in activityTypedf[["id", "name"]].T.to_dict().values()}
                    abundance_df = abundance_df.loc[abundance_df["activityType"] == activityType_name_id[selected_activityType]]
                    leveldf = level_df[selected_level_indicator]
                    # st.write(abundance_df)
                    if selected_level_indicator in ["Block", "Sector"]:
                        level_indicator = selected_level_indicator.lower() + "2"
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
                if len(activityType) > 0:
                    # st.write(site_abundance_df)
                    # st.write(list(site_abundance_df["name"].unique()))
                    selected_site_abundance = st.selectbox(
                        'Select ' + selected_level_indicator.lower() + ' ( ' + str(len(site_abundance_df)) + ' )',
                        list(site_abundance_df["name"].unique()))
            if len(activityType) > 0:
                sites_name_id = {x["name"]: x["id"] for x in site_abundance_df[["id", "name"]].T.to_dict().values()}
                # st.write(abundance_df)
                # st.write(abundance_df.loc[abundance_df["block2"] =="12.0"])
                if selected_level_indicator in ["Block", "Sector"]:
                    abundance_df = abundance_df.loc[
                        abundance_df[level_indicator] == str(float(sites_name_id[selected_site_abundance]))]
                else:
                    abundance_df = abundance_df.loc[
                        abundance_df[level_indicator] == sites_name_id[selected_site_abundance]]
                # st.write(abundance_df)
                chart_line_abundace = altairErrorLineChart(alt, abundance_df, selected_abundace_indicator,
                                                           "Trends in " + selected_activityType.lower() + " " + selected_abundace_indicator.lower() + " in " + selected_site_abundance.lower(),
                                                           480, abundance_indicators_error[
                                                               abundance_indicators[selected_abundace_indicator]],"#b7a51d")
                ##st.markdown('#### Trends in  ' + selected_abundace_indicator.lower())
                # st.write(abundance_df)
                st.altair_chart(chart_line_abundace, theme=None, use_container_width=True)
        if resultype == "Comparisons":
            abundance_indicators_name = ["Encounter Rate (n/km)"]
            abundance_indicators = {
                "Density (n/km²)": "density",
                "Encounter Rate (n/km)": "encounterRate",
                "Population Size (n)": "populationSize",
                "Capture Rate": "captureRate",
                "Occupancy Rate": "occupancyRate"}
            abundance_indicators_error = {
                "density": {"min": "densityMinimumError", "max": "density_maximumError"},
                "encounterRate": {"min": "encounterRateMinimumError", "max": "encounterRateMaximumError"},
                "populationSize": {"min": "populationSizeMinimumError", "max": "populationSizeMaximumError"},
                "captureRate": {"min": "captureRateMinimumError", "max": "captureRateMaximumError"},
                "occupancyRate": {"min": "occupancyRateMinimumError", "max": "occupancyRateMaximumError"}
            }

            level_df = {
                "Site": sitesdf,
                "Block": blockdf,
                "Sector": sectordf,
            }
            col_indicator_bar, col_level_bar, col_activityType_bar = st.columns(3)
            with col_indicator_bar:
                selected_abundace_indicator = st.selectbox('Select a indicator', abundance_indicators_name)
                abundance_df = original_df.loc[original_df[abundance_indicators[selected_abundace_indicator]] != -1]
                abundance_df[selected_abundace_indicator] = abundance_df[
                    abundance_indicators[selected_abundace_indicator]]
                # st.write(abundance_df)
            with col_level_bar:
                selected_level_indicator = st.selectbox('Select level', ["Site", "Block", "Sector"])
                abundance_df = abundance_df.loc[abundance_df["level"] == selected_level_indicator]
                activityTypedf = activityTypedf.loc[activityTypedf["id"].isin(abundance_df["activityType"].unique())]
                # st.write(abundance_df)
            with col_activityType_bar:
                activityType = list(activityTypedf["name"].unique())
                if len(activityType) > 0:
                    selected_activityType = st.selectbox('Select activityType ( ' + str(len(activityTypedf)) + ' )', activityType)
                    activityType_name_id = {x["name"]: x["id"] for x in activityTypedf[["id", "name"]].T.to_dict().values()}
                    abundance_df = abundance_df.loc[abundance_df["activityType"] == activityType_name_id[selected_activityType]]
                    # st.write(abundance_df)
                    leveldf = level_df[selected_level_indicator]
                    if selected_level_indicator in ["Block", "Sector"]:
                        level_indicator = selected_level_indicator.lower() + "2"
                        # st.write(abundance_df[level_indicator].astype(float))
                        site_abundance_df = leveldf.loc[
                            leveldf["id"].isin(abundance_df[level_indicator].astype(float).unique())]
                    else:
                        level_indicator = selected_level_indicator.lower()
                        site_abundance_df = leveldf.loc[leveldf["id"].isin(abundance_df[level_indicator].unique())]
            # st.write(site_abundance_df)
            # with col2_site:
            #     if len(activityType)>0:
            # selected_site_abundance = st.selectbox('Select '+selected_level_indicator.lower()+' ( '+str(len(site_abundance_df))+' )', list(site_abundance_df["name"].unique()))
            if len(activityType) > 0:
                if selected_level_indicator in ["Sector", "Block"]:
                    # st.write(site_abundance_df[["id","name"]].T.to_dict().values())
                    sites_id_name = {x["id"]: x["name"] for x in site_abundance_df[["id", "name"]].T.to_dict().values()}
                    # sites_id_abbr = { x["id"]:}
                    abbreviations = ["< " + x["short_name"] + " > " + ": " + x["name"] for x in
                                     site_abundance_df[["id", "short_name", "name"]].T.to_dict().values()]
                else:
                    sites_id_name = {x["id"]: x["short_name"] for x in
                                     site_abundance_df[["id", "short_name"]].T.to_dict().values()}
                    # sites_id_abbr = { x["id"]:}
                    abbreviations = ["< " + x["short_name"] + " > " + ": " + x["name"] for x in
                                     site_abundance_df[["id", "short_name", "name"]].T.to_dict().values() if
                                     x["short_name"] != x["name"]]
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
                if len(abbreviations) > 0:
                    abbreviations = [" ; ".join(abbreviations[x:x + size]) for x in range(0, len(abbreviations), size)]
                    # st.write(abbreviations)
                    # abundance_df = abundance_df.loc[abundance_df[selected_level_indicator.lower()] ==sites_name_id[selected_site_abundance]]
                    # values = [abundance_indicators[selected_abundace_indicator]]
                    # st.write(values)
                    abundance_df["main_landscape"] = abundance_df["main_landscape"].astype(str)
                    abundance_df[[value for key, value in abundance_indicators_error[
                        abundance_indicators[selected_abundace_indicator]].items()]] = abundance_df[
                        [value for key, value in
                         abundance_indicators_error[abundance_indicators[selected_abundace_indicator]].items()]].astype(
                        str)
                    # index= ["region","country",'main_landscape','site',"landscape","level","activityType"]
                    errors_mask = [value for key, value in abundance_indicators_error[
                        abundance_indicators[selected_abundace_indicator]].items()]
                    # abundance_df = pd.pivot_table(abundance_df, values=values, index=index,
                    #        aggfunc={abundance_indicators[selected_abundace_indicator]: "max"}).reset_index()
                    # mask = index+values+errors_mask
                    # st.write(mask)
                    # st.write(index)

                    abundance_df[level_indicator] = abundance_df[level_indicator].astype(float)
                    abundance_df[level_indicator] = abundance_df[level_indicator].astype(int)
                    # print(abundance_df.info())
                    # print(site_abundance_df.info())
                    max_indicator_per_level_df = {"activityType": [], level_indicator: [],
                                                  abundance_indicators[selected_abundace_indicator]: [],
                                                  errors_mask[0]: [], errors_mask[1]: [], }
                    # st.write(site_abundance_df["id"].unique())
                    for id in site_abundance_df["id"].unique():
                        max_value = abundance_df.loc[abundance_df[level_indicator] == id][
                            abundance_indicators[selected_abundace_indicator]].max()
                        max_line = abundance_df.loc[
                            (abundance_df[abundance_indicators[selected_abundace_indicator]] == max_value) & (
                                        abundance_df[level_indicator] == id)]
                        max_line_min = max_line[errors_mask[0]].min()
                        max_err = max_line.loc[max_line[errors_mask[0]] == max_line_min]
                        max_line = max_err
                        max_line_min2 = max_line[errors_mask[1]].min()
                        max_err2 = max_line.loc[max_line[errors_mask[1]] == max_line_min2]
                        max_line = max_err2
                        # st.write(max_line)
                        # st.write(max_line[level_indicator].unique())
                        max_indicator_per_level_df[level_indicator].append(max_line[level_indicator].unique()[0])
                        max_indicator_per_level_df[abundance_indicators[selected_abundace_indicator]].append(
                            max_line[abundance_indicators[selected_abundace_indicator]].unique()[0])
                        max_indicator_per_level_df[errors_mask[0]].append(max_line[errors_mask[0]].unique()[0])
                        max_indicator_per_level_df[errors_mask[1]].append(max_line[errors_mask[1]].unique()[0])
                        max_indicator_per_level_df["activityType"].append(max_line["activityType"].unique()[0])
                    max_indicator_per_level_df = pd.DataFrame(max_indicator_per_level_df).drop_duplicates()
                    # st.write(max_indicator_per_level_df)

                    # st.write(abundance_df)
                    abundance_df = max_indicator_per_level_df
                    # abundance_df = abundance_df[mask].groupby(index).max().reset_index()
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
                                                             "Comparison between " + selected_level_indicator.lower() + "s : " + selected_activityType + " " + selected_abundace_indicator.lower() + " from " + str(
                                                                 start_year) + " to " + str(end_year), 540,
                                                             abundance_indicators_error[
                                                                 abundance_indicators[selected_abundace_indicator]],
                                                             selected_level_indicator.lower() + ' name', abbreviations,
                                                             gethBarWidth(abundance_df),"#b7a51d")
                    ##st.markdown('#### Comparison between ' + selected_level_indicator.lower() + "s")
                    # print(abundance_df.info())
                    # st.write(abundance_df)
                    st.altair_chart(chart_bar_abundace, theme=None, use_container_width=True)
        # result_tab = st.tabs(["# EFFORT ", "# TRENDS IN ABUNDANCES ", "# COMPARISONS "])
        # with result_tab[0]:
        #
        #     st.write("Result page")
        # with result_tab[1]:
        #
        #     st.write("Result page")
        # with result_tab[2]:
        #
        #     st.write("Result page")
