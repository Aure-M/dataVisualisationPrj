import pandas as pd 
import streamlit as st
from datetime import datetime
from prj_utils import cleanData, defineKeys, fetchData, filterFeature, yearAnalysis
    



#----------------------------
df2019,df2020= fetchData()

df2019 = cleanData(df2019)
df2020 = cleanData(df2020)

keys = defineKeys(df2020)

#----------------------------



with st.sidebar:
    option = st.selectbox(
    '',
    ('2019 analysis', '2020 analysis', 'Filter feature'))

    if option == 'Filter feature':
        st.subheader("Choose your preference:")
        dateMutation = st.slider(
            "Select a range for your research",
            datetime(2020,1,1),datetime(2020,12,31),
            value=(datetime(2020,1,1), datetime(2020,5,1)),
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
            step = int((keys["surface_terrain"][1]-keys["surface_terrain"][0])/50)
        )
        nbrePieces = st.slider(
            "Number of main rooms : ",
            keys["nombre_pieces_principales"][0],keys["nombre_pieces_principales"][1],
            value=(keys["nombre_pieces_principales"][0], keys["nombre_pieces_principales"][1]),
            step = int((keys["nombre_pieces_principales"][1]-keys["nombre_pieces_principales"][0]))
        )
    elif option == '2019 analysis':
        selected = st.selectbox(
            'Choose the municipality that you interested in:',
            tuple(df2019["nom_commune"].value_counts().index)
        )
        showMap = st.checkbox("Should we show the map ?")
    """ else :
        selected = st.selectbox(
            'Choose the municipality that you interested in:',
            tuple(df2020["nom_commune"].value_counts().index)
        )
        showMap = st.checkbox("Should we show the map ?") """

if option == '2019 analysis':
    yearAnalysis(df2019,selected=selected,showMap=showMap)
elif option == '2020 analysis':
    yearAnalysis(df2019,selected=selected,showMap=showMap)
elif option == 'Filter feature':
    filterFeature(df2020,dateMutation,natureMutation,valeurF,commune,typeLocal,surfaceT,nbrePieces)