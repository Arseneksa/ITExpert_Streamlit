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
    # selected_year_data = input_df[input_df['year'] == str(input_year_end)]
    previous_year_data = input_df[input_df['year'] == str(input_year_start)]
    # st.write(selected_indicator,len(input_df[selected_indicator].unique()))
    size_max = len(input_df[selected_indicator].unique())
    size_min = len(previous_year_data[selected_indicator].unique())
    
    
    difference = size_max- size_min
    
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
def altairLineChart(alt,df,selected_indicator,title):
    chart = alt.Chart(df).mark_line(interpolate="cardinal",point=alt.OverlayMarkDef(color="#19F960",size=30),color="#19F960",tension=0.6).encode(
                x="year",
                y=selected_indicator,
                # color=publication_types[0]
            )
    text = chart.mark_text(align="center",fontSize=12,opacity=1,color="white",dy=-15).encode(text=selected_indicator).properties(
            title=alt.Title(title,subtitle=["Copyright WWF"],subtitleFontSize=10,subtitlePadding=10,dx=-20),
            height=450
        )
    chart.configure_legend(
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            orient='top-right'
        )
    return chart+text