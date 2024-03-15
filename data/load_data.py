

import time
import requests
import streamlit as st


@st.cache_data
def load_data(url_dict,st):
    # url_login ="https://biomonitoringwebsite.herokuapp.com/api/auth/login"
    # data = {

    #     "username": st.secrets["username"],
    #     "password": st.secrets["password"]

    # }

    # x = ''
    # while x == '':
    #     try:
    #         x = requests.post(url_login, json=data)
    #         break
    #     except:

    #         time.sleep(5)

    #         continue

    # # print(x.json())
    # x = x.json()
    # token = x["token"]
    # localurl = "http://localhost:8000"
    # onlineurl = "https://biomonitoringwebsite.herokuapp.com"
    # dataurl =onlineurl+"/api/communication/"
    # datapub_typeurl =localurl+"/api/publicationType/"
    data_dict = {}
    # datapub_type = ''
    data=''
    # progress_text = "Data loading. Please wait."
    # with st.spinner(progress_text):
    while data == '':
        try:
            # blocks = requests.get(urlblock, headers = {"Authorization":  'Token '+str(token)})
            # sectors = requests.get(urlsectors, headers = {"Authorization":  'Token '+str(token)})
            # sites = requests.get(urlsites, headers = {"Authorization":  'Token '+str(token)})
            # sublandscapes = requests.get(urllandscapes, headers = {"Authorization":  'Token '+str(token)})
            # landscapes = requests.get(urlmain_Landscapes, headers = {"Authorization":  'Token '+str(token)})
            # species = requests.get(urlspecies, headers = {"Authorization":  'Token '+str(token)})
            # samplingMethod = requests.get(urlsamplingMethods, headers = {"Authorization":  'Token '+str(token)})
            for key, value in url_dict.items():
                # st.write(key + '=' + value)
                data_dict[key] = requests.get(value)
            data = 'ok'
            # datapub_type = requests.get(datapub_typeurl, headers = {"Authorization":  'Token '+str(token)})
            break
        except:

            time.sleep(5)

            continue
    # st.write(data_dict)
    data_dict = {key:value.json() for key,value in data_dict.items()}
    # st.toast('#### data loaded!', icon='🎉')
    # st.success('Data loaded!', icon="✅")
    return data_dict
# @st.cache_data
def getspeciesByLevel(df,df1,df2,field,field1,field2,id):
    if len(df) == 0: 
        return []
    else:
        df = df[df[field]==id]
        # print(df[[field,field1,field2]])
        # print(df[field1].unique())
        species_result_df = df[[field1
                                ]].drop_duplicates().merge(df1, left_on=field1, right_on='id', how="inner")
        # species_result_df = species_result_df[[field1]].drop_duplicates()
        species_sites_df = df[[field1,field2]].drop_duplicates().merge(df2, left_on=field2, right_on='id', how="inner")
        # print(species_result_df)
        species_result_df["sites"] = species_result_df[field1].apply(lambda x: " , ".join(species_sites_df[(species_sites_df[field1]==x)&(species_sites_df["name"]!="na")]["name"].dropna().to_list()))
        # print(species_result_df["sites"])
        species_result_df["sites_number"] = species_result_df[field1].apply(lambda x: len(species_sites_df[(species_sites_df[field1]==x)&(species_sites_df["name"]!="na")]["name"].dropna().to_list()))
        species_result_df = species_result_df.sort_values(by=["sites_number"], ascending=False)
        if('created_at' in species_result_df.columns): 
            species_result_df = species_result_df.drop(['created_at','updated_at'], axis=1)
        return species_result_df
def getactivity_typeByLevel(df,df1,df2,field,field1,field2,id):
    if len(df) == 0: 
        return []
    else:
        df = df[df[field]==id]
        # print(df[[field,field1,field2]])
        # print(df[field1].unique())
        species_result_df = df[[field1
                                ]].drop_duplicates().merge(df1, left_on=field1, right_on='id', how="inner")
        # species_result_df = species_result_df[[field1]].drop_duplicates()
        species_sites_df = df[[field1,field2]].drop_duplicates().merge(df2, left_on=field2, right_on='id', how="inner")
        # print(species_result_df)
        species_result_df["sites"] = species_result_df[field1].apply(lambda x: " , ".join(species_sites_df[(species_sites_df[field1]==x)&(species_sites_df["name"]!="na")]["name"].dropna().to_list()))
        # print(species_result_df["sites"])
        species_result_df["sites_number"] = species_result_df[field1].apply(lambda x: len(species_sites_df[(species_sites_df[field1]==x)&(species_sites_df["name"]!="na")]["name"].dropna().to_list()))
        species_result_df = species_result_df.sort_values(by=["sites_number"], ascending=False)
        if('created_at' in species_result_df.columns): 
            species_result_df = species_result_df.drop(['created_at','updated_at'], axis=1)
        return species_result_df
