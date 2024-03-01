from datetime import datetime
import pandas as pd
import streamlit as st 

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
def calculate_population_difference(input_df, input_year_start, input_year_end,selected_indicator):
    input_df[selected_indicator] = input_df[selected_indicator].apply(lambda x: 0 if x ==-1 else x)
    selected_year_data = input_df[input_df['year'] == str(input_year_end)].reset_index()
    previous_year_data = input_df[input_df['year'] == str(input_year_start)].reset_index()
    selected_year_data['difference'] = selected_year_data[selected_indicator].sub(previous_year_data[selected_indicator], fill_value=0)
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
            # popup = ["Name","Species list"],
            k=5,
            legend=True,
            legend_kwds=dict(colorbar=True),
            )
    return map
def altairLineChart(alt,df,selected_indicator,title,height):
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
    chart = alt.Chart(df).mark_line(interpolate="cardinal",point=alt.OverlayMarkDef(color="#DF7A0F",size=30),color="#DF7A0F",tension=0.6).encode(
                x="year:O",
                # alt.X("year(year):T").scale(zero=False).title("Year"),
                y=selected_indicator,
                # color=publication_types[0]
            ).interactive()
    df["Short value"] = df[selected_indicator].apply( lambda x: format_number(x) )
    text = chart.mark_text(align="center",fontSize=12,opacity=1,color="#000",dy=-15).encode(text="Short value").properties(
            title=alt.Title(title,subtitle=["Copyright WWF"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
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
def altairErrorLineChart(alt,df,selected_indicator,title,height,error):
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
    alt.renderers.set_embed_options(actions={"editor": False})
    
    chart = alt.Chart(df).mark_line(interpolate="cardinal",point=alt.OverlayMarkDef(color="#DF7A0F",size=35),color="#DF7A0F",tension=0.6).encode(
                alt.X("year(year):T").title("Year"),
                y=selected_indicator,
                
                # color=publication_types[0]
            ).interactive()
    error = alt.Chart(df).mark_errorbar(ticks=True).encode(
                # y=selected_indicator,
                alt.X("year(year):T").title("Year"),
                alt.Y(error["min"]).title(selected_indicator),
                alt.Y2(error["max"]),
                color=alt.value("#EABD21"),
                # color=publication_types[0]
            )
    df["Short value"] = df[selected_indicator].apply( lambda x: format_number(x) )
    text = chart.mark_text(align="center",fontSize=12,opacity=1,color="#000",dy=-15).encode(text="Short value").properties(
            title=alt.Title(title,subtitle=["Copyright WWF"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
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
def altairErrorBarChart(alt,df,selected_indicator,title,height,error,x_label,abbreviations,width):
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
    
    chart = alt.Chart(df).mark_bar(interpolate="cardinal",color="#DEDDC2", width=width).encode(
                alt.X(x_label).title(abbreviations),
                y=selected_indicator,
                
                # color=publication_types[0]
            ).interactive()
    error = alt.Chart(df).mark_errorbar(ticks=True).encode(
                # y=selected_indicator,
                # alt.X(x_label+":O").title(),
                alt.X(x_label).axis(
                    title=abbreviations,
                    titleAngle=0,
                    gridColor="black"
                    # titleAlign="left",
                    # titleY=-2,
                    # titleX=0,
                ),
                alt.Y(error["min"]).title(selected_indicator),
                alt.Y2(error["max"]),
                color=alt.value("#EABD21"),
                # color=alt.value("#000"),
                # color=publication_types[0]
            )
    df["Short value"] = df[selected_indicator].apply( lambda x: format_number(x) )
    text = chart.mark_text(align="center",fontSize=12,opacity=1,color="#000",dy=-15).encode(text="Short value").properties(
            title=alt.Title(title,subtitle=["Copyright WWF"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
            height=height
        )
    chart.configure_legend(
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            orient='top-right'
        )
    chart.configure_view(
        continuousHeight=200,
        continuousWidth=200,
        strokeWidth=4,
        fill='#FFEEDD',
        stroke='red',
    )
    # img = alt.Chart(source).mark_image(width=50, height=75).encode(
    #     x='year',
    #     y=selected_indicator,
    #     url='image'
    # )
    return chart+text+error
def altairBarChart(alt,df,selected_indicator,title,height):
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
    
    chart = alt.Chart(df).mark_bar(interpolate="cardinal", width=40,point=alt.OverlayMarkDef(color="#DF7A0F",size=30),color="#DF7A0F",tension=0.6).encode(
                x="year:O",
                y=selected_indicator,
                # color=publication_types[0]
            ).interactive()
    df["Short value"] = df[selected_indicator].apply( lambda x: format_number(x) )
    text = chart.mark_text(align="center",fontSize=12,opacity=1,color="#000",dy=-15).encode(text="Short value").properties(
            title=alt.Title(title,subtitle=["Copyright WWF"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
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
def altairLineChartWithAggregation(alt,df,selected_indicator,title,height,aggregation,x_label):
    # years = df["year"].unique()
    # year = years[int(len(years)/2)]
    # value = df.loc[df["year"]==year][selected_indicator]
    # source = pd.DataFrame.from_records(
    #     [
    #         {'year': year,selected_indicator:value,  'image': './app/static/logo.jpg'},
    #     ]
    # )
    alt.renderers.set_embed_options(actions={"editor": False})
    
    chart = alt.Chart(df).mark_line(interpolate="cardinal",point=alt.OverlayMarkDef(color="#DF7A0F",size=30),color="#DF7A0F",tension=0.6).encode(
                x=x_label+":O",
                # y=selected_indicator,
                y=alt.Y(field=selected_indicator, aggregate=aggregation, type='quantitative')
                # color=publication_types[0]
            ).interactive()
    df["indicator_value"] = df[selected_indicator].apply( lambda x: format_number(x) )
    # text = chart.mark_text(align="center",fontSize=12,opacity=1,color="#000",dy=-15).encode(text="indicator_value").properties(
    #         title=alt.Title(title,subtitle=["Copyright WWF"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
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


"""Area covered automation fonctions."""

"""Cette fonction permet de d'avoir la plus grande superficie couverte par un site indépendament de l'année"""
def get_max_area_covered(df,id):
    # st.write(df)
    maxdf1  = df[(df["site"]==id)&(df["level"] == "Site")]
    # st.write(df)
    # print(max_blockdf.head())
    max = round(maxdf1["coverage_rate"].max(),2)
    if max < 100:
        # print(1)
        # print(id)
        # print(max)
        maxdf  = df[df["site"]==id]
        """Les secteurs appartenant directement au site est considéré comme un block dans cette partie pour faciliter l'implementation de l'algorithme"""
        max_blockdf  = maxdf.loc[((maxdf["block2"]==0)|(maxdf["sector2"]==0))&(df["level"].isin(["Block","Sector"]))]
        # print(id)
        if len(max_blockdf) == 0:
            max = maxdf1["area_covered_km2"].max()
            return max
        else:
        # block_year = max_blockdf["year"].sort_values(ascending=True).unique()
            """ Recupération de la liste de tout les blocks du site"""
            blocklist1 = max_blockdf["block2"].unique() 
            blocklist2 = max_blockdf["sector2"].unique() 
            # st.write(blocklist1)
            # st.write(blocklist2)
            """Creation d'une liste de superficies couvertes par chaque block du site"""
            area_cover1_list =[maxdf.loc[maxdf["block2"]==x]["area_covered_km2"].max() for x in blocklist1 if x!=0]
            area_cover2_list =[maxdf.loc[maxdf["sector2"]==x]["area_covered_km2"].max() for x in blocklist2 if x!=0]
            # print(area_cover1_list)
            # print(area_cover2_list)
            area_cover1 = sum(area_cover1_list)
            area_cover2 = sum(area_cover2_list)
            # print(area_cover1)
            # print(area_cover2)
            # coverage = (area_cover1+area_cover2)*100/maxdf["total_area"].max()
            coverage_km2 = area_cover1+area_cover2
            # print(coverage_km2)
            # max_sectordf  = maxdf.loc[(maxdf["block2"]!=0)&(maxdf["sector2"]!=0)&(df["level"].isin(["Sector"]))]
            max = round(coverage_km2,2)
        # print(blocklist)
    else:
        max = maxdf1["area_covered_km2"].max()
        # print(0)
        # print(id)
        # print(max)
    
    return max
def get_max_area_covered_per_level(df,id,level,leveldf):
    st.write(leveldf)
    if level == "Site":
        level_id = "site"
        # df["total_area"] = df[level_id].apply(lambda x: level_df.loc[level_df["id"]==x]["total_area"].unique()[0])
    elif level == "Landscape" :
        df = df.loc[df["is_parent"]==True]
        if id in [1884,1843,1839]:
            level_id = "main_landscape"
            # df["total_area"] = df[level_id].apply(lambda x: Main_Landscape.objects.get(id=x).total_area)
        else:
            level_id = "landscape"
            # df["total_area"] = df[level_id].apply(lambda x: Landscape.objects.get(id=x).total_area)
    elif level == "Country":
        level_id = "country"
        # df["total_area"] = df[level_id].apply(lambda x: Country.objects.get(id=x).total_area)
    elif level == "Region":
        level_id = "region"
        # df["total_area"] = df[level_id].apply(lambda x: Region.objects.get(id=x).total_area)
    df["total_area"] = df[level_id].apply(lambda x: leveldf.loc[leveldf["id"]==x]["total_area"].unique()[0])
    level_df  = df.loc[(df[level_id]==id)&(df["level"] == "Site")]
    level_df = level_df[["region","country",'main_landscape',"landscape","site",'block2',"sector2","level","total_area","total_coverage_km2"]].groupby(["region","country",'main_landscape',"landscape","site",'block2',"sector2","level"]).max().reset_index()
    # print(level_df)
    max = round(level_df["total_coverage_km2"].sum()*100/level_df["total_area"].max(),2)
    return max

def get_area_covered_and_site_list_per_year(df,year,prec_site_list):
    df = df.sort_values(['year'])
    df = df.loc[df["year"]<=year]
    actual_site_list = df["site"].unique()
    site_list = []
    difference = [x for x in actual_site_list if x not in prec_site_list]
    area_covered =0
    # print(prec_site_list)
    # print(actual_site_list)
    # print(difference)
    if len(difference)>0:
        # prec_site_list.append(",".join(difference))
        prec_site_list = prec_site_list + difference
        site_list = prec_site_list
    else:
        site_list = prec_site_list
    # print(site_list)
    # print(df)
    # print(get_max_area_covered(df,site_list[0]) )
    # if len(site_list)>0:
    area_covered = sum([get_max_area_covered(df,x) for x in site_list])
    # area_covered = sum([df.loc[df["site"]==x]["area_covered_km2"].max() for x in site_list])
    # print(prec_site_list)
    # print(actual_site_list)
    coverage = round(area_covered*100/df["total_area"].max(),2)
    # print(area_covered)
    return {
        "year": year,
        "site_list": site_list,
        "area_covered": area_covered,
        "coverage": coverage
    }
def get_cumulative_max_area_covered_per_level_per_year(df,id,level,type,leveldf):
    
    if level == "Site":
        level_id = "site"
        # df["total_area"] = df[level_id].apply(lambda x: Site.objects.get(id=x).total_area)
    elif level == "Landscape" :
        df = df.loc[df["is_parent"]==True]
        if id in [1884,1843,1839]:
            level_id = "main_landscape"
            # df["total_area"] = df[level_id].apply(lambda x: Main_Landscape.objects.get(id=x).total_area)
        else:
            level_id = "landscape"
            # df["total_area"] = df[level_id].apply(lambda x: Landscape.objects.get(id=x).total_area)
    elif level == "Country":
        level_id = "country"
        # df["total_area"] = df[level_id].apply(lambda x: Country.objects.get(id=x).total_area)
    elif level == "Region":
        level_id = "region"
        # df["total_area"] = df[level_id].apply(lambda x: Region.objects.get(id=x).total_area)
    # if level != "Region":
    df["total_area"] = df[level_id].apply(lambda x: leveldf.loc[leveldf["id"]==x]["total_area"].unique()[0] if x in leveldf["id"].unique() else None)
    level_df  = df.loc[df[level_id]==id]
    years = sorted(level_df["year"].unique())
    i=0 
    prec_site_list =[]
    data =  []
    while i< len(years):
        datadict = get_area_covered_and_site_list_per_year(level_df,years[i],prec_site_list)
        data.append(datadict)
        prec_site_list = datadict["site_list"]
        i=i+1
    # print(data)
    if type == "coverage_rate":
        graph_data = [{"label": k["year"], "x":int(k["year"]), "y":k["coverage"]}
                    for k in data]
    else:
        graph_data = [{"label": k["year"], "x":int(k["year"]), "y":k["area_covered"]}
                    for k in data]
    # print(graph_data)
    # max = round(level_df["total_coverage_km2"].sum()*100/level_df["total_area"].max(),2)
    return graph_data
def set_cumulative_by_year(id,level,df,type,leveldf):
    years = df["year"].unique()
    # if level == "Site":
    #     level_id = "site"
    # elif level == "Landscape" :
    #     df = df.loc[df["is_parent"]==True]
    #     if id in [1884,1843,1839]:
    #         level_id = "main_landscape"
    #     else:
    #         level_id = "landscape"
    # elif level == "Country":
    #     level_id = "country"
    # elif level == "Region":
    #     level_id = "region"
    # df = df.loc[df[level_id]==id]
    
    data = get_cumulative_max_area_covered_per_level_per_year(df,id,level,type,leveldf)
    year_area_covered_dict ={ x["label"] : x["y"] for x in data}
    # print (id)
    # print (year_area_covered_dict)
    return year_area_covered_dict
# def map_cumulative_area_covered_level_year(row,level,df):
#     # print(row)
#     year_area_covered_dict = set_cumulative_by_year(row["id"],level,df)
#     return year_area_covered_dict[row["year"]]
    # print(row)
    
def get_cumulative_max_area_covered_per_level_per_year_table(df,level,type,leveldf):
    
    if level == "Site":
        level_id = "site"
        # df["total_area"] = df[level_id].apply(lambda x: Site.objects.get(id=x).total_area)
    elif level == "Landscape" :
        df = df.loc[df["is_parent"]==True]
        # if id in [1884,1843,1839]:
        #     level_id = "main_landscape"
        #     # df["total_area"] = df[level_id].apply(lambda x: Main_Landscape.objects.get(id=x).total_area)
        # else:
        level_id = "landscape"
            # df["total_area"] = df[level_id].apply(lambda x: Landscape.objects.get(id=x).total_area)
    elif level == "Country":
        level_id = "country"
    elif level == "Region":
        level_id = "region"
        # df["total_area"] = df[level_id].apply(lambda x: Country.objects.get(id=x).total_area)
    # st.write(df[level_id].unique())
    
    # st.write(leveldf.loc[leveldf["id"]==None]["total_area"])
    # leveldf["total_area"] = leveldf["total_area"].fillna(0)
    # st.write(leveldf["total_area"])
    df["total_area"] = df[level_id].apply(lambda x: leveldf.loc[leveldf["id"]==x]["total_area"].unique()[0] if int(x) in leveldf["id"].unique() else None)
    # data = { x["label"] : x["y"] for x in data}
    level_ids = df[level_id].unique()
    years = df["year"].unique()
    # df = df.apply(lambda x : map_cumulative_area_covered_level_year(x,level,df))
    result = {"year":[],"area_covered":[],"level_id":[],"level":[]}
    for id in level_ids:
        for year , area in set_cumulative_by_year(id,level,df,type,leveldf).items():
            result["level_id"].append(id)
            result["year"].append(year)
            # result["level_id"].append(level_id)
            result["level"].append(level)
            result["area_covered"].append(area)
        # set_cumulative_by_year(id,level,df)
    resultdf = pd.DataFrame(result)
    # resultdf.to_excel('cumulative_by_year.xlsx')
    # print (resultdf.head())
    return resultdf

"""Construction de la fonction de création de la table du taux de couverture au niveau block et secteur
"""
def get_area_covered_table(df ,sitesdf):
    max_areadf =  df[["region","country",'main_landscape','site',"landscape","area_covered_km2","level","year"]].groupby(["region","country",'main_landscape',"landscape","site","level"]).max().reset_index()
    # df_coverage1 = df.merge(sitesdf, left_on="site", right_on='id', how="left")
    child_sites = sitesdf[sitesdf["is_child"]==True]["id"].to_list()
    # print(child_sites)
    # st.write(df["area_covered_km2"].unique())
    # st.write(df.shape)
    df["is_parent"] = df["site"].apply(lambda x :True if x not in child_sites else False)
    df=df[df["area_covered_km2"]!=-1]
    # print(df["site"].unique())
    # st.write(df["area_covered_km2"].unique())
    
    # df_coverage = df_coverage[df_coverage["level"].isin(child_sites) == False]
    # print(len(sitesdf[sitesdf["is_child"]==False]))
    # print(len(sitesdf[sitesdf["is_child"]==True]))
    # print(len(df["site"].unique()))
    sitesdf = sitesdf.loc[sitesdf["id"].isin(df["site"].unique())]
    # st.write(df["site"].unique())
    # st.write(sitesdf)
    # print(len(sitesdf["id"].unique()))
    # print(len(df_coverage1["site"].unique()))
        # sites = sites_df["name"].unique()
    df = df[df["site"].isin(sitesdf["id"].unique())]
    df_coverage = df
    # print(len(df_coverage["site"].unique()))
    # print(df_coverage1["name"].unique())
    # print(df_coverage["name"].unique())
    # print(len(df_coverage1[df_coverage1["is_child"]==True]["name"].unique()))
    # print(df_coverage1[df_coverage1["is_child"]==True]["name"].unique())
    # print(df.info())
    # print(df_coverage.info())
    # print(df_coverage.head())
    # st.write(df_coverage)
    # st.write(df_coverage.shape)
    max_areadf_year =  df_coverage[["region","country",'main_landscape','site',"landscape",'block2',"sector2","area_covered_km2","coverage_rate","level",'is_parent',"year"]].groupby(["region","country",'main_landscape',"landscape","site",'block2',"sector2","level","year"]).max().reset_index()
    # max_areadf = df[['main_landscape','country',"landscape","area_covered_km2","level"]].groupby(['main_landscape',"country","landscape","level"]).max().reset_index()
    # max_areadf = df[['main_landscape','country',"landscape","area_covered_km2","level","coverage_rate","year"]].groupby(['main_landscape',"country","landscape","level","year"]).max().reset_index()
    # st.write(max_areadf_year)
    # print(max_areadf_year.info())
    # st.write(max_areadf_year.shape)
    max_areadf = max_areadf[max_areadf["area_covered_km2"]!=-1]
    # st.write(max_areadf_year)
    max_areadf_year = max_areadf_year[max_areadf_year["area_covered_km2"]!=-1].merge(sitesdf[["id","name","total_area"]], left_on="site", right_on='id', how="left")
    # max_areadf_year = max_areadf_year.merge(sitesdf[["id","name","total_area"]], left_on="site", right_on='id', how="left")
    # max_areadf_year["coverage_rate"] = round((max_areadf_year["area_covered_km2"]/max_areadf_year["total_area"])*100,2)
    # main_df = max_areadf[['main_landscape',"area_covered_km2"]].groupby(['main_landscape']).sum().reset_index()
    # # main_df = max_areadf[['main_landscape',"area_covered_km2","year"]].groupby(['main_landscape',"year"]).sum().reset_index()
    # main_df = main_df.merge(mainlandscapesdf, left_on='main_landscape', right_on='id', how="inner")
    # # wildlife_cover = getdata("http://localhost:8000/api/wildlife_cover/2/1843/8")
    # # print(wildlife_cover)
    # main_df["coverage_rate"] =round(main_df["area_covered_km2"]*100/main_df["total_area"],2) 
    # main_df = main_df.sort_values(by=['coverage_rate'], ascending=False)
    # area_covered_storage_df = pd.read_excel('area_covered_storage.xlsx')
    # print(len(area_covered_storage_df))
    # max_areadf_year.to_excel("area_covered_storage.xlsx",sheet_name='Sheet1')
    # st.write(max_areadf_year),
    # print(get_max_area_covered(max_areadf_year,1))
    # st.write(max_areadf_year.shape)
    max_area_sitedf ={x:get_max_area_covered(max_areadf_year,x) for x in max_areadf_year['site'].unique()}
    # print(max_area_sitedf)
    
    max_areadf_year = max_areadf_year[max_areadf_year["level"].isin(["Site","Block","Sector"])]
    max_areadf_year["total_coverage_km2"] =max_areadf_year['site'].apply(lambda x : max_area_sitedf[x]) 
    max_areadf_year["total_coverage"] = round(max_areadf_year['total_coverage_km2']*100/max_areadf_year['total_area'],2)
    max_areadf_site = max_areadf_year[["region","country",'main_landscape',"landscape",'site',"area_covered_km2","coverage_rate"]].groupby(["region","country",'main_landscape',"landscape",'site']).max().reset_index()
    # max_areadf_site.to_excel("area_covered_storage.xlsx",sheet_name='Sheet2')
    # print()
    # st.write(max_areadf_site)
    
    max_areadf_site = max_areadf_site.merge(sitesdf[["id","name","total_area"]], left_on="site", right_on='id', how="left")
    # with pd.ExcelWriter("area_covered_storage.xlsx") as writer:
    #     max_areadf_year.to_excel(writer, sheet_name="Sheet1")  
    #     max_areadf_site.to_excel(writer, sheet_name="Sheet2")
    # for x in df_coverage["site"].unique().to_list():
    #     max_line = max_areadf_year[max_areadf_year]
    #     max_areadf_site["site"] = max_areadf_year[]
    # print(df_coverage[["site","year","area_covered_km2","coverage_rate"]][(df_coverage["area_covered_km2"]!=-1)&(df_coverage["site"].isin([1,2,3,4]))].sort_values(by=["site",'year']))
    # print(max_areadf_year.info())
    # print(max_areadf_year.head(30)
    return max_areadf_year
def cumulative(df,element,min_year,selected_indicator):
    # st.write(element)
    element = int(element)
    df["year"] = df["year"].astype(int)
    if min_year == element:
        value = sum(df.loc[df["year"]==min_year][selected_indicator])
    else:
        value = sum(df.loc[(df["year"]>=int(min_year))&(df["year"]<=element)][selected_indicator])
    return value
def simple_cumlative_data_per_year(df,selected_indicator,level):
    # st.write(df[selected_indicator].unique())
    df = df.loc[df[selected_indicator]!=-1]
    # st.write(df[selected_indicator])
    
    df = df[[level,"year",selected_indicator]].groupby([level,"year"]).sum().reset_index()
    st.write(df)
    years = df["year"].unique()
    min_year = min(years)
    df["Sampling transect effort (Km)"] = df["year"].apply(lambda x : cumulative(df,x,min_year,selected_indicator))
    df["year"] = df["year"].astype(str)
    # st.write(df)
    return df


def generate_metrics(df,leveldf,indicators_name,indicators_metric,start_year,end_year):
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
        with col[i]:
            st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)
            i=i+1

# def wildlife_data_clean(df):