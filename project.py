import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sn
import streamlit as st
from datetime import date,datetime
from prj_utils import cleanData, convert_df, defineKeys, fetchData, filter
from streamlit_folium import st_folium
import folium
    



year = 2017
#----------------------------
df = fetchData(year)
df = cleanData(df)
keys = defineKeys(df)

#----------------------------



with st.sidebar:
    option = st.selectbox(
    '',
    ('2021 analysis', '2020 analysis', 'Filter feature'))

    if option == 'Filter feature':
        st.subheader("Choose your preference:")
        dateMutation = st.slider(
            "Select a range for your research",
            datetime(year,1,1),datetime(year,12,31),
            value=(datetime(year,1,1), datetime(year,5,1)),
        )
        natureMutation = st.multiselect(
            'Choose the types of transactions',
            keys["nature_mutation"],
            keys["nature_mutation"][0]
        )
        valeurF = st.slider(
            "Lands value :",
            keys["valeur_fonciere"][0],keys["valeur_fonciere"][1],
            value=(keys["valeur_fonciere"][0], keys["valeur_fonciere"][1]),
            step = int((keys["valeur_fonciere"][1]-keys["valeur_fonciere"][0])/50)
        ) 
        commune = st.multiselect(
            'Choose the municipalities that you interested in:',
            keys["nom_commune"],
            keys["nom_commune"][:2]
        )
        typeLocal = st.multiselect(
            'Choose the types of Property : ',
            keys["type_local"],
            keys["type_local"][:2]
        )
        surfaceT = st.slider(
            "Lands surface :",
            keys["surface_terrain"][0],keys["surface_terrain"][1],
            value=(keys["surface_terrain"][0], keys["surface_terrain"][1]),
            step = (keys["surface_terrain"][1]-keys["surface_terrain"][0])/50
        )
        nbrePieces = st.slider(
            "Number of main rooms : ",
            keys["nombre_pieces_principales"][0],keys["nombre_pieces_principales"][1],
            value=(keys["nombre_pieces_principales"][0], keys["nombre_pieces_principales"][1]),
            step = (keys["nombre_pieces_principales"][1]-keys["nombre_pieces_principales"][0])/50
        )
st.write(keys)
if option == 'Filter feature':
    st.write("# Filter feature")
    limit = 300 # Limit of properties per pages
    filtered = filter(df,dateMutation,natureMutation,valeurF,commune,typeLocal,surfaceT,nbrePieces)
    page = st.select_slider(
        'Select the page',
        options = range(int(len(df)/limit)),
        value = 0
    )
    m = folium.Map(location=[48.856614,2.3522219]) # Paris location
    colors = {"Maison":'lightgreen',"Appartement":'lightblue',"Dépendance":'red',"Local industriel. commercial ou assimilé":'orange'}
    st.write(colors)
    for ind, lat, lon, typ, val in filtered[["latitude","longitude","type_local","valeur_fonciere"]][limit*page:limit*(page+1)].itertuples():     
        folium.Marker(
            [lat,lon],
            icon=folium.Icon(icon="glyphicon-map-marker",color=colors[typ]),
            tooltip = "{} €".format(val)
        ).add_to(m)
    st_data = st_folium(m, width = 800,height=600)
    
    csv = convert_df(filtered)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )

    
