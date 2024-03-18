from datetime import datetime
import pandas as pd
import streamlit as st 
import plotly.express as px
import numpy as np
@st.cache_data
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    if num > 1000:
        return f'{round(num / 1000,2)} K'
    else:
        return f'{round(num,2)} '
# @st.cache_data
# Calculation year-over-year population migrations
theme = "vox"
# @st.cache_data
def calculate_population_difference(input_df, input_year_start, input_year_end,selected_indicator):
    input_df[selected_indicator] = input_df[selected_indicator].apply(lambda x: 0 if x ==-1 else x)
    selected_year_data = input_df[input_df['year'] == str(input_year_end)].reset_index()
    previous_year_data = input_df[input_df['year'] == str(input_year_start)].reset_index()
    # st.write(previous_year_data)
    # st.write(selected_year_data)
    selected_year_data['difference'] = selected_year_data[selected_indicator].sub(previous_year_data[selected_indicator], fill_value=0)
    # st.write(selected_year_data)
    return selected_year_data.sort_values(by="difference", ascending=False)
    # return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)

# @st.cache_data
def calculate_lenght_difference(input_df, input_year_start, input_year_end,selected_indicator):
    input_df[selected_indicator] = input_df[selected_indicator].dropna()
    input_df= input_df.loc[input_df[selected_indicator] != "nan"]
    # selected_year_data = input_df[input_df['year'] == str(input_year_end)]
    previous_year_data = input_df[input_df['year'] == str(input_year_start)]
    # st.write(selected_indicator,len(input_df[selected_indicator].unique()))
    
    size_max = len(input_df[selected_indicator].unique())
    size_min = len(previous_year_data[selected_indicator].unique())
    
    # st.write(input_df[selected_indicator].unique(),size_max,previous_year_data[selected_indicator],size_min )
    difference = size_max- size_min
    difference = difference
    # st.write(selected_indicator,size_max,size_min,difference)
    return difference
    # return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)
# @st.cache_data
def naturalbreaksMap(gdf,column,fields):
    map = gdf.explore(
            column=column,
            scheme="naturalbreaks",
            tooltip = fields,
            popup = True,
            k=5,
            legend=True,
            legend_kwds=dict(colorbar=True),
            )
    return map
def naturalbreaksMapChart(gdf,column,fields,chart):
    map = gdf.explore(
            column=column,
            scheme="naturalbreaks",
            tooltip = fields,
            popup = chart,
            k=5,
            legend=True,
            legend_kwds=dict(colorbar=True),
            )
    return map
# @st.cache_data
def altairLineChart(alt,df,selected_indicator,title,height,color):
    alt.themes.enable(theme)
    title = title.replace("*", '')
    # years = df["year"].unique()
    # year = years[int(len(years)/2)]
    # value = df.loc[df["year"]==year][selected_indicator]
    # source = pd.DataFrame.from_records(
    #     [
    #         {'year': year,selected_indicator:value,  'image': './app/static/logo.jpg'},
    #     ]
    # )
    alt.renderers.set_embed_options(actions={"editor": False})
    # df["year"] = df["year"].apply(lambda x: datetime.strptime(str(x), "%Y"))
    chart = alt.Chart(df).mark_line(interpolate="cardinal",point=alt.OverlayMarkDef(color=color,size=30),color=color,tension=0.6).encode(
                
                alt.X("year:O", axis=alt.Axis(title="Year",titleFontSize=16,labelFontSize=15,gridColor="lightgrey",titleFontWeight="bold")),
                alt.Y(selected_indicator, axis=alt.Axis(titleFontSize=16,labelFontSize=15,gridColor="lightgrey",titleFontWeight="bold")),
                # color=publication_types[0]
            ).interactive()
    df["Short value"] = df[selected_indicator].apply( lambda x: format_number(x) )
    text = chart.mark_text(align="center",fontSize=13,opacity=1,color="#000",dy=-15).encode(text="Short value").properties(
            title=alt.Title(title, color=color, fontWeight="bold",fontSize=17,subtitle=["Copyright"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
            height=height
        )
    chart.configure_legend(
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            orient='top-right'
        )
    # img = alt.Chart(source).mark_image(width=50, height=75).encode(
    #     x='year',
    #     y=selected_indicator,
    #     url='image'
    # )
    return chart+text
# @st.cache_data
def altairErrorLineChart(alt,df,selected_indicator,title,height,error,color):
    alt.themes.enable(theme)
    title = title.replace("*", '')
    # years = df["year"].unique()
    # year = years[int(len(years)/2)]
    # value = df.loc[df["year"]==year][selected_indicator]
    # source = pd.DataFrame.from_records(
    #     [
    #         {'year': year,selected_indicator:value,  'image': './app/static/logo.jpg'},
    #     ]
    # )
    df[error["min"]] = df[error["min"]].apply(lambda x: int(0) if x ==-1 else x)
    df[error["max"]] = df[error["max"]].apply(lambda x: int(0) if x ==-1 else x)
    df["year"] = df["year"].apply(lambda x: datetime.strptime(str(x), "%Y"))
    # alt.renderers.set_embed_options(actions={"editor": False})
    
    chart = alt.Chart(df).mark_line(interpolate="cardinal",point=alt.OverlayMarkDef(color=color,size=35),color=color,tension=0.6).encode(
                alt.X("year(year):T", axis=alt.Axis(title="Year",titleFontSize=17,labelFontSize=15,gridColor="lightgrey",titleFontWeight="bold")),
                alt.Y(selected_indicator, axis=alt.Axis(titleFontSize=17,labelFontSize=15,gridColor="lightgrey",titleFontWeight="bold")),
            
                
                # color=publication_types[0]
            ).interactive()
    error = alt.Chart(df).mark_errorbar(ticks=True).encode(
                # y=selected_indicator,
                alt.X("year(year):T").title("Year"),
                alt.Y(error["min"]).title(selected_indicator),
                alt.Y2(error["max"]),
                color=alt.value("#004F45"),
                # color=publication_types[0]
            )
    df["Short value"] = df[selected_indicator].apply( lambda x: format_number(x) )
    text = chart.mark_text(align="center",fontSize=13,opacity=1,color="#000",dy=-15).encode(text="Short value").properties(
            title=alt.Title(title, color=color, fontWeight="bold",fontSize=17,subtitle=["Copyright"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
            height=height
        )
    chart.configure_legend(
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            orient='top-right'
        )
    # img = alt.Chart(source).mark_image(width=50, height=75).encode(
    #     x='year',
    #     y=selected_indicator,
    #     url='image'
    # )
    return chart+text+error
@st.cache_data
def gethBarWidth(df):
    #st.write(len(df))
    if len(df) >50:
        width = 1
    if len(df) >40:
        width = 10
    if len(df) >30:
        width = 15
    if len(df)>20:
        width = 25
    else:
        width=50
    return width
# @st.cache_data
def altairErrorBarChart(alt,df,selected_indicator,title,height,error,x_label,abbreviations,width, color):
    alt.themes.enable(theme)
    title = title.replace("*", '')
    
    # years = df["year"].unique()
    # year = years[int(len(years)/2)]
    # value = df.loc[df["year"]==year][selected_indicator]
    # source = pd.DataFrame.from_records(
    #     [
    #         {'year': year,selected_indicator:value,  'image': './app/static/logo.jpg'},
    #     ]
    # )
    df[error["min"]] = df[error["min"]].apply(lambda x: int(0) if x ==-1 else x)
    df[error["max"]] = df[error["max"]].apply(lambda x: int(0) if x ==-1 else x)
    # df["year"] = df["year"].apply(lambda x: datetime.strptime(str(x), "%Y"))
    alt.renderers.set_embed_options(actions={"editor": False})
    
    chart = alt.Chart(df).mark_bar(interpolate="cardinal",color=color, width=width).encode(
                
                alt.X(x_label, axis=alt.Axis(title=abbreviations,titleFontSize=14,labelFontSize=14,gridColor="lightgrey",titleFontWeight=500)),
                alt.Y(selected_indicator, axis=alt.Axis(titleFontSize=17,labelFontSize=15,gridColor="lightgrey",titleFontWeight="bold")),
                
                # color=publication_types[0]
            ).interactive()
    error = alt.Chart(df).mark_errorbar(ticks=True).encode(
                # y=selected_indicator,
                # alt.X(x_label+":O").title(),
                alt.X(x_label).axis(
                    title=abbreviations,
                    titleAngle=0,
                    
                    # titleAlign="left",
                    # titleY=-2,
                    # titleX=0,
                ),
                alt.Y(error["min"]).title(selected_indicator),
                alt.Y2(error["max"]),
                color=alt.value("#004F45"),
                # color=alt.value("#000"),
                # color=publication_types[0]
            )
    df["Short value"] = df[selected_indicator].apply( lambda x: format_number(x) )
    text = chart.mark_text(align="center",fontSize=12,opacity=1,color="#000",dy=-15).encode(text="Short value").properties(
            title=alt.Title(title,color=color, fontSize=17,subtitle=["Copyright"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
            height=height
        )
    # chart.configure_legend(
    #         strokeColor='gray',
    #         fillColor='#EEEEEE',
    #         padding=10,
    #         cornerRadius=10,
    #         orient='top-right'
    #     )
    # chart.configure_view(
    #     continuousHeight=200,
    #     continuousWidth=200,
    #     strokeWidth=4,
    #     fill='#FFEEDD',
    #     stroke='red',
    # )
   
    # img = alt.Chart(source).mark_image(width=50, height=75).encode(
    #     x='year',
    #     y=selected_indicator,
    #     url='image'
    # )
    return chart+text+error
# @st.cache_data
def altairBarChart(alt,df,selected_indicator,title,height,color):
    alt.themes.enable(theme)
    title = title.replace(" *",'')
    # years = df["year"].unique()
    # year = years[int(len(years)/2)]
    # value = df.loc[df["year"]==year][selected_indicator]
    # source = pd.DataFrame.from_records(
    #     [
    #         {'year': year,selected_indicator:value,  'image': './app/static/logo.jpg'},
    #     ]
    # )
    alt.renderers.set_embed_options(actions={"editor": False})
    
    chart = alt.Chart(df).mark_bar(interpolate="cardinal", width=40,point=alt.OverlayMarkDef(color=color,size=30),color=color,tension=0.6).encode(
               
                alt.X("year:O", axis=alt.Axis(title="Year",titleFontSize=17,labelFontSize=15,gridColor="lightgrey",titleFontWeight="bold")),
                alt.Y(selected_indicator, axis=alt.Axis(titleFontSize=17,labelFontSize=15,gridColor="lightgrey",titleFontWeight="bold")),
                # color=publication_types[0]
            ).interactive()
    df["Short value"] = df[selected_indicator].apply( lambda x: format_number(x) )
    text = chart.mark_text(align="center",fontSize=12,opacity=1,color="#000",dy=-15).encode(text="Short value").properties(
            title=alt.Title(title,color=color, fontSize=17,subtitle=["Copyright"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
            height=height
        )
    chart.configure_legend(
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            orient='top-right'
        )
    # img = alt.Chart(source).mark_image(width=50, height=75).encode(
    #     x='year',
    #     y=selected_indicator,
    #     url='image'
    # )
    return chart+text
def altairBarChartWithLabel(alt,df,selected_indicator,title,height,color,label,abbreviations):
    alt.themes.enable(theme)
    title = title.replace(" *",'')
    # years = df["year"].unique()
    # year = years[int(len(years)/2)]
    # value = df.loc[df["year"]==year][selected_indicator]
    # source = pd.DataFrame.from_records(
    #     [
    #         {'year': year,selected_indicator:value,  'image': './app/static/logo.jpg'},
    #     ]
    # )
    alt.renderers.set_embed_options(actions={"editor": False})
    
    chart = alt.Chart(df).mark_bar(interpolate="cardinal", width=40,point=alt.OverlayMarkDef(color=color,size=30),color=color,tension=0.6).encode(
               
                alt.X(label+":O", axis=alt.Axis(title=abbreviations,titleFontSize=14,labelFontSize=15,gridColor="lightgrey")),
                alt.Y(selected_indicator, axis=alt.Axis(titleFontSize=17,labelFontSize=15,gridColor="lightgrey",titleFontWeight="bold")),
                # color=publication_types[0]
            ).interactive()
    df["Short value"] = df[selected_indicator].apply( lambda x: format_number(x) )
    text = chart.mark_text(align="center",fontSize=12,opacity=1,color="#000",dy=-15).encode(text="Short value").properties(
            title=alt.Title(title,color=color, fontSize=17,subtitle=["Copyright"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
            height=height
        )
    chart.configure_legend(
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            orient='top-right'
        )
    # img = alt.Chart(source).mark_image(width=50, height=75).encode(
    #     x='year',
    #     y=selected_indicator,
    #     url='image'
    # )
    return chart+text
# @st.cache_data
def altairLineChartWithAggregation(alt,df,selected_indicator,title,height,aggregation,x_label):
    alt.themes.enable(theme)
    # years = df["year"].unique()
    # year = years[int(len(years)/2)]
    # value = df.loc[df["year"]==year][selected_indicator]
    # source = pd.DataFrame.from_records(
    #     [
    #         {'year': year,selected_indicator:value,  'image': './app/static/logo.jpg'},
    #     ]
    # )
    alt.renderers.set_embed_options(actions={"editor": False})
    
    chart = alt.Chart(df).mark_line(interpolate="cardinal",point=alt.OverlayMarkDef(color="#004F45",size=30),color="#004F45",tension=0.6).encode(
                x=x_label+":O",
                # y=selected_indicator,
                y=alt.Y(field=selected_indicator, aggregate=aggregation, type='quantitative')
                # color=publication_types[0]
            ).interactive()
    df["indicator_value"] = df[selected_indicator].apply( lambda x: format_number(x) )
    # text = chart.mark_text(align="center",fontSize=12,opacity=1,color="#000",dy=-15).encode(text="indicator_value").properties(
    #         title=alt.Title(title,subtitle=["Copyright"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
    #         height=height
    #     )
    chart.configure_legend(
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            orient='top-right'
        )
    # img = alt.Chart(source).mark_image(width=50, height=75).encode(
    #     x='year',
    #     y=selected_indicator,
    #     url='image'
    # )
    return chart
# def pieChart():
    # start = Color("#004F45")
    # end = Color("#F9DFC5")
    # ramp = ["%s"% x for x in list(start.range_to(end, len(value)))]
    # source = pd.DataFrame(interestScoreBreakdown)
    # source = source.sort_values(by='value', ascending=False)
    # source["Topic"] = source["Topic"].astype(str)+' ( '+source["value"].astype(str)+' %) '
    # topics = source["Topic"].unique()
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
    # plot = alt.Chart(source).mark_arc(innerRadius=50, cornerRadius=1,outerRadius=120).encode(
    #     theta=alt.Theta(field="value", type="quantitative"),
    #     color=alt.Color(field="Topic", type="nominal",scale=alt.Scale(
    #                         #domain=['A', 'B'],
    #                         domain=topics,
    #                         range=ramp),  # 31333F
    #                         )).properties(
    #     title=alt.Title("Research Interest Score Breakdown",subtitle=["Copyright"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
    # )
# def make_choropleth(px,input_df, input_id, selected_indicator, input_color_theme):
#         choropleth = px.choropleth(input_df, locations=input_id, color=selected_indicator, locationmode="USA-states",
#                             color_continuous_scale=input_color_theme,
#                             range_color=(0, max((input_df[selected_indicator]))),
#                             scope="usa",
#                             labels={'population':'Population'}
#                             )
#         choropleth.update_layout(
#             template='plotly_dark',
#             plot_bgcolor='rgba(0, 0, 0, 0)',
#             paper_bgcolor='rgba(0, 0, 0, 0)',
#             margin=dict(l=0, r=0, t=0, b=0),
#             height=350
#         )
#         # choropleth = make_choropleth(df_selected_year, 'states_code', 'population', selected_color_theme)
#         # st.plotly_chart(choropleth, use_container_width=True)
#         return choropleth



# @st.cache_data
def generate_metrics(df,leveldf,indicators_name,indicators_metric,start_year,end_year,orientation):
    # st.write(df,indicators_name)
    box_number = len(indicators_metric)
    # col =[0,0,0,0]
    # if box_number == 4:
    #     col[0],col[1],col[2],col[3] = st.columns(box_number)
    # elif box_number == 3:
    #     col[0],col[1],col[2] = st.columns(box_number)
    # elif box_number == 2:
    #     col[0],col[1] = st.columns(box_number)
    # elif box_number == 1:
    #     col[0] = st.columns(box_number)
    col= st.columns(box_number)
    
    metric_df = leveldf
    # st.write(col)
    # metric_df = df[df["site"].isin(leveldf["id"].unique())]
    # st.write(len(metric_df["site"].unique()))
    i=0
    for indicator in indicators_metric:
        if indicator== "species":
        
            metric_df = metric_df.loc[metric_df["species"]!=53]
        difference = calculate_lenght_difference( metric_df, start_year, end_year,indicator)
        metrics = metric_df.loc[metric_df[indicator]!="nan"][indicator].unique()
        
        size = len(metrics)
        # if size ==1 :
        #     if metrics[0]== "nan" :
        #         size =0
            
        #st.write(metrics,size)
        # st.dataframe(df_population_difference_sorted)
        first_state_name = "# **"+indicators_name[indicator]+ '** '
        first_state_population = format_number(size)
        first_state_delta = format_number(difference)
        if orientation=="vertical":
            st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)
        else:
                 
            with col[i]:
                st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)
                i=i+1
# @st.cache_data
def generate_metrics_indicator(df,leveldf,indicators_name,indicators_metric,start_year,end_year,orientation):
    # st.write(df,indicators_name)
    box_number = len(indicators_metric)
    # col =[0,0,0,0]
    # if box_number == 4:
    #     col[0],col[1],col[2],col[3] = st.columns(box_number)
    # elif box_number == 3:
    #     col[0],col[1],col[2] = st.columns(box_number)
    # elif box_number == 2:
    #     col[0],col[1] = st.columns(box_number)
    # elif box_number == 1:
    #     col[0] = st.columns(box_number)
    col= st.columns(box_number)
    
    metric_df = leveldf
    # st.write(col)
    # metric_df = df[df["site"].isin(leveldf["id"].unique())]
    # st.write(len(metric_df["site"].unique()))
    i=0
    for indicator in indicators_metric:
        if indicator== "species":
        
            metric_df = metric_df.loc[metric_df["species"]!=53]
        metric_df["year"] = metric_df["year"].astype(str)
        difference = calculate_population_difference( metric_df, start_year, end_year,indicator)
        metrics = metric_df.loc[metric_df[indicator]!="nan"][indicator].unique()
        
        # st.write(difference)
        # size = len(metrics)
        # # if size ==1 :
        # #     if metrics[0]== "nan" :
        # #         size =0
            
        # #st.write(metrics,size)
        # # st.dataframe(df_population_difference_sorted)
        
        first_state_name = "# **"+indicators_name[indicator]+ '** '
        first_state_population = format_number(difference[indicator].iloc[0])
        first_state_delta = format_number(difference["difference"].iloc[0])
        if orientation=="vertical":
            st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)
        else:
                 
            with col[i]:
                st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)
                i=i+1
# def wildlife_data_clean(df):