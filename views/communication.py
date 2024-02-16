#######################
# Import libraries
# import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
# import plotly.express as px
# import pandas_profiling
# from streamlit_pandas_profiling import st_profile_report
# from pydantic_settings import BaseSettings 
from data.load_data import *
from colour import Color

from tools import altairLineChart, calculate_population_difference,format_number
#######################
# Page configuration

def communication_page(st):
    
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
        background-color: #95B393;
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
    st.markdown(
            ' <span style="font-size:2em;font-weight:bold;margin-left:0px;">Congo Basin Monitoring and Evaluation Database</span><br><span style="margin-left:0px;font-size:1em;font-weight:bold" >Communication dashboard</span><br>',
            unsafe_allow_html=True,
        )
    
    localurl = "http://localhost:8000"
    onlineurl = "https://biomonitoringwebsite.herokuapp.com"
    dataurl =onlineurl+"/api/communication/"
    interestScoreBreakdown_url =onlineurl+"/api/communication_combined/"+str(3)+"/pie"
    datapub_typeurl =onlineurl+"/api/publicationType/"
    url_dict  = {
        "communication":dataurl,
        "publicationType":datapub_typeurl,
        "interestScoreBreakdown":interestScoreBreakdown_url,
    }
   
    data_dict= load_data(url_dict,st)
    # st.write(data_dict)
    data = data_dict["communication"]
    datapub_type = data_dict["publicationType"]
    interestScoreBreakdown = data_dict["interestScoreBreakdown"]
    value  = [x["y"] for x in interestScoreBreakdown["data"]]
    topics= [x["name"] for x in interestScoreBreakdown["data"]]
    interestScoreBreakdown = {
        "Topic":topics,
        "value": value
    }
    
    
    df = pd.json_normalize(data)
    datapub_type_df = pd.json_normalize(datapub_type)
    df = df.loc[df['year']!=-1]
    years = df['year'].unique()
    min_year = df['year'].min()
    max_year = df['year'].max()
    indcicator_name  = {
                "researchInterestScore": "Research Interest Score",
                "citations": "Number of Citations",
                "reads": "Number of Reads",
                "recommendations": "Number of Recommendations",
                "fullTextReads": "Number of Full text Reads",
                "cumulResearchInterestScore": "Cumulative Research Interest Score",
                "cumulativeCitations": "Cumulative Citations",
                "cumulativeReads": "Cumulative Reads",
                "cumulativeRecommendations": "Cumulative Recommendations",
                "cumulativeFullTextReads": "Cumulative Full Text reads",
                "otherReads": "Number of Other Reads",
            }
    indcicator_name2 = indcicator_name
    indicators = [value for key, value in indcicator_name.items()]
    indicators2 = [key for key, value in indcicator_name.items()]
    indcicator_name = { value: key for key, value in indcicator_name.items()}
    publication_types = datapub_type_df["name"].unique()
    # pr = df.profile_report()
    # st_profile_report(pr)
    df = pd.merge(df, datapub_type_df[["id","name"]],left_on='publication_type', right_on='id', how='left')
    # df['publication type'] =df["publication_type"].apply(lambda x: datapub_type_df.loc[datapub_type_df['id']==x]["name"].first()) 
    #######################
    # Sidebar

    # df
    with st.sidebar:
        # st.title('🏂 US Population Dashboard')
        # st.title('Filter')
        
        # indicator_list = list(df_reshaped.year.unique())[::-1]
        
        
        start_year, end_year = st.select_slider(
            'Select year range',
            options=years,
            value=(min_year, max_year)
        )
        # selected_indicator = st.selectbox('Select a indicator', indicators)
        # st.write('You selected wavelengths between', start_color, 'and', end_color)
        # selected_pub_type = st.selectbox('Select a publication', publication_types)
        # df_selected_year = df_reshaped[df_reshaped.year == selected_year]
        # df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

        # color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        # selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
        
    # df["year"] = df["yemax_year1, 1).year)
    
    
    
    tab1, tab2 = st.tabs([publication_types[0], publication_types[1]])
    with tab1:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        coordinator_pub_df = df.loc[df["name"]==publication_types[0]]
        coordinator_pub_df = coordinator_pub_df.loc[(coordinator_pub_df["year"]>=start_year)&(coordinator_pub_df["year"]<=end_year)]
        coordinator_pub_df["year"] = coordinator_pub_df["year"].astype(str)
        
        
        col = st.columns((3, 5), gap='medium')
        with col[0]:
            with st.container():
                
                # st.markdown('#### Data table')
                
                # st.dataframe(df[["year","name"]])
                st.markdown('#### Gains/Losses')
                indicators_metric = [ "researchInterestScore","reads","citations","recommendations"]
                for indicator in indicators_metric:
                    
                    df_population_difference_sorted = calculate_population_difference(coordinator_pub_df, start_year, end_year,indicator)
                    # st.dataframe(df_population_difference_sorted)
                    first_state_name = indcicator_name2[indicator]
                    first_state_population = format_number(df_population_difference_sorted[indicator].iloc[0])
                    first_state_delta = format_number(df_population_difference_sorted["difference"].iloc[0])
                    st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)
            # st.write(df[indicators2].stack().rename("indicator").reset_index().groupby(by=["level_1"]).count())
        with col[1]:
            
            # st.write(interestScoreBreakdown)
            st.markdown('#### Overall publications stats')
            selected_indicator = st.selectbox('Select indicator', indicators,key="#coordinatorindicatorselect")
            coordinator_pub_df[selected_indicator] = coordinator_pub_df[indcicator_name[selected_indicator]]
            coordinator_pub_df = coordinator_pub_df.loc[coordinator_pub_df[selected_indicator]!=-1]
            df_pub1 = coordinator_pub_df.loc[(coordinator_pub_df[selected_indicator]!=-1)&(coordinator_pub_df["name"]==publication_types[0])]
            # st.line_chart( df_pub1[[selected_indicator,'year']], x="year", y=selected_indicator)
            chart = altairLineChart(alt,df_pub1,selected_indicator,publication_types[0].replace("Interest", "Trends in "+selected_indicator),450)
            # st.write(df_pub1)
            # text = chart.mark_text(align="center",fontSize=10,opacity=0.6,color="white").encode(text={"value":"Copyright WWF"})
            
            st.altair_chart(chart, theme=None, use_container_width=True)
            if selected_indicator == "Research Interest Score":
                # st.markdown('#### Research Interest Score Breakdown')
                start = Color("#12783D")
                end = Color("#99DAB4")
                ramp = ["%s"% x for x in list(start.range_to(end, len(value)))]
                source = pd.DataFrame(interestScoreBreakdown)
                source = source.sort_values(by='value', ascending=False)
                source["Topic"] = source["Topic"].astype(str)+' ( '+source["value"].astype(str)+' %) '
                topics = source["Topic"].unique()
                # st.dataframe(source)
                # plot = alt.Chart(source).mark_arc(innerRadius=50, cornerRadius=8).encode(
                #     theta=alt.Theta("value:Q").stack(True),
                #     color= alt.Color("Topic:N",
                #                     scale=alt.Scale(
                #                         #domain=['A', 'B'],
                #                         domain=topics,
                #                         # range=['#29b5e8', '#155F7A']),  # 31333F
                #                         ),
                #                     legend=None),
                # ).properties(width=230, height=30)
                plot = alt.Chart(source).mark_arc(innerRadius=50, cornerRadius=1,outerRadius=120).encode(
                    theta=alt.Theta(field="value", type="quantitative"),
                    color=alt.Color(field="Topic", type="nominal",scale=alt.Scale(
                                        #domain=['A', 'B'],
                                        domain=topics,
                                        range=ramp),  # 31333F
                                        )).properties(
                    title=alt.Title("Research Interest Score Breakdown",subtitle=["Copyright WWF"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
                )
                # plot
                # text = plot.mark_text(radius=140, size=15, fontStyle="italic", align="center",font="Lato" ,color="white").encode(
                #         text="value:Q"
                #     )
                # text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text="value" )
                st.altair_chart(plot, theme=None, use_container_width=True)
            # st.altair_chart(chart+text+watermark, theme=None, use_container_width=True)
            # chart + text
            # st.plotly_chart(fig, theme="streamlit")

    with tab2:
        # Use the native Plotly theme.
        # selected_indicator = st.selectbox('Select a indicator', indicators,key="#wwf_pub_indicatorselect")
        # df[selected_indicator] = df[indcicator_name[selected_indicator]]
        # df = df.loc[df[selected_indicator]!=-1]
        wwf_pub_df = df.loc[df["name"]==publication_types[1]] 
        
        
        # start_year = 2018
        wwf_pub_df = wwf_pub_df.loc[(wwf_pub_df["year"]>=start_year)&(wwf_pub_df["year"]<=end_year)]
        wwf_pub_df["year"] = wwf_pub_df["year"].astype(str)
        col = st.columns((3, 5), gap='medium')
        with col[0]:
            with st.container():
                
                # st.markdown('#### Data table')
                
                # st.dataframe(df[["year","name"]])
                st.markdown('#### Gains/Losses')
                indicators_metric = [ "researchInterestScore","reads","citations","recommendations"]
                for indicator in indicators_metric:
                    
                    df_population_difference_sorted = calculate_population_difference(wwf_pub_df, start_year, end_year,indicator)
                    # st.dataframe(df_population_difference_sorted)
                    first_state_name = indcicator_name2[indicator]
                    if len(df_population_difference_sorted[indicator]>0):
                        first_state_population = format_number(df_population_difference_sorted[indicator].iloc[0])
                        first_state_delta = format_number(df_population_difference_sorted["difference"].iloc[0])
                    else:
                        first_state_population = 0
                        first_state_delta = 0
                    st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)
            # st.write(df[indicators2].stack().rename("indicator").reset_index().groupby(by=["level_1"]).count())
        with col[1]:
            
            
            st.markdown('#### Overall publications stats')
            selected_indicator = st.selectbox('Select indicator', indicators,key="#wwfpub_indicatorselect")
            
            wwf_pub_df[selected_indicator] = wwf_pub_df[indcicator_name[selected_indicator]]
            wwf_pub_df = wwf_pub_df.loc[wwf_pub_df[selected_indicator]!=-1]
            df_pub2 = wwf_pub_df.loc[(wwf_pub_df[selected_indicator]!=-1)&(wwf_pub_df["name"]==publication_types[1])]
            # st.dataframe(df)
            # st.dataframe(df_pub2)
            # st.line_chart( df_pub1[[selected_indicator,'year']], x="year", y=selected_indicator)
            chart2 = altairLineChart(alt,df_pub2,selected_indicator,publication_types[1].replace("Interest", "Trends in "+selected_indicator),450)
            st.altair_chart(chart2, theme=None, use_container_width=True)
        
    
    