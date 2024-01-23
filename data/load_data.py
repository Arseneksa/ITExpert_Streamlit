

import time
import requests
import streamlit as st


@st.cache_data
def load_data(url_dict,st):
    url_login ="https://biomonitoringwebsite.herokuapp.com/api/auth/login"
    data = {

        "username": st.secrets["username"],
        "password": st.secrets["password"]

    }

    x = ''
    while x == '':
        try:
            x = requests.post(url_login, json=data)
            break
        except:

            time.sleep(5)

            continue

    # print(x.json())
    x = x.json()
    token = x["token"]
    # localurl = "http://localhost:8000"
    # onlineurl = "https://biomonitoringwebsite.herokuapp.com"
    # dataurl =onlineurl+"/api/communication/"
    # datapub_typeurl =localurl+"/api/publicationType/"
    data_dict = {}
    # datapub_type = ''
    data=''
    progress_text = "Data loading. Please wait."
    with st.spinner(progress_text):
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
                    data_dict[key] = requests.get(value, headers = {"Authorization":  'Token '+str(token)})
                data = 'ok'
                # datapub_type = requests.get(datapub_typeurl, headers = {"Authorization":  'Token '+str(token)})
                break
            except:

                time.sleep(5)

                continue
    # st.write(data_dict)
    data_dict = {key:value.json() for key,value in data_dict.items()}
    # st.toast('#### data loaded!', icon='🎉')
    st.success('Data loaded!', icon="✅")
    return data_dict