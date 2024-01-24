def wildlife_region(st,data,pd):
    st.title("Wildlfe region app")
    
    landscapesdf  = pd.json_normalize(data["landscapes_list"])
    sitesdf  = pd.json_normalize(data["sites_list"])
    countriesdf  = pd.json_normalize(data["countries_list"])
    speciesdf  = pd.json_normalize(data["species_list"])
    st.write(speciesdf)
