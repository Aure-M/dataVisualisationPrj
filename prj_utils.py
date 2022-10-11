import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sn
import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

links = {
    2020:"https://drive.google.com/u/0/uc?id=1-3aYJTGnwPDh8K0vIPXNuoGg4plRk0sb&export=download&confirm=t&uuid=f90aed2b-688d-4fa2-be31-316fbf3ee936",
    2019:"https://drive.google.com/u/0/uc?id=16B0R6ZfzpaaGpzTAl0vncB7WN5vWjz_K&export=download&confirm=t&uuid=f90aed2b-688d-4fa2-be31-316fbf3ee936"
}

@st.cache(suppress_st_warning=True)
def fetchData(year = 2020):
    data = pd.read_csv(links[2020])
    return data


@st.cache(suppress_st_warning=True)
def cleanData(data):
    if data["date_mutation"].dtype==type(object):
        data["date_mutation"] = [datetime.strptime(str(i), '%Y-%m-%d') for i in data["date_mutation"]]
    data = data.loc[(~data["latitude"].isna()) & (~data["longitude"].isna())&(~data["type_local"].isna())&(~data["valeur_fonciere"].isna())]
    return data


@st.cache(suppress_st_warning=True)
def defineKeys(data):
    return {
        "nature_mutation": list(data["nature_mutation"].value_counts().index),
        "valeur_fonciere": [int(data["valeur_fonciere"].min()), int(data["valeur_fonciere"].max())],
        "nom_commune": list(data["nom_commune"].value_counts().index),
        "nombre_lots": [int(data["nombre_lots"].min()),int(data["nombre_lots"].max())],
        "type_local": list(data["type_local"].value_counts().index),
        "surface_reelle_bati": [int(data["surface_reelle_bati"].min()), int(data["surface_reelle_bati"].max())],
        "nombre_pieces_principales": [int(data["nombre_pieces_principales"].min()),int(data["nombre_pieces_principales"].max())],
        "surface_terrain": [int(data["surface_terrain"].min()), int(data["surface_terrain"].max())]
    }

@st.cache(suppress_st_warning=True)
def filter(data,dateMutation,natureMutation,valeurF,commune,typeLocal,surfaceT,nbrePieces):
    print(dateMutation)
    data = data.loc[
        (data["nature_mutation"].isin(natureMutation))&
        (data["nom_commune"].isin(commune))&
        (data["type_local"].isin(typeLocal))&
        (data["valeur_fonciere"].between(valeurF[0],valeurF[1]))&
        (data["date_mutation"].between(dateMutation[0],dateMutation[1]))&
        (data["surface_terrain"].between(surfaceT[0],surfaceT[1]))&
        (data["nombre_pieces_principales"].between(nbrePieces[0],nbrePieces[1]))
        
    ]
    return data

@st.cache(suppress_st_warning=True)
def convert_df(data):
    return data.to_csv().encode('utf-8')

def repartition_communes_BAR(data):
  fig = plt.figure()
  répartition_communes = data["nom_commune"].value_counts().sort_values(axis=0, ascending=False,)
  top20_communes = répartition_communes.head(20)
  top20_communes.plot(kind = "bar")
  st.pyplot(fig)


@st.cache(suppress_st_warning=True)
def yearAnalysis(data):
	st.write("## Cities ranking based on the number of real estate operations")
	repartition_communes_BAR(data)
	
def filterFeature(data,dateMutation,natureMutation,valeurF,commune,typeLocal,surfaceT,nbrePieces):
	st.write("# Filter feature for the year 2020")
	limit = 300 # Limit of properties per pages
	filtered = filter(data,dateMutation,natureMutation,valeurF,commune,typeLocal,surfaceT,nbrePieces)
	page = st.select_slider(
        'Select the page',
        options = range(int(len(data)/limit)),
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
	st.download_button(
        label="Download data as CSV",
        data=convert_df(filtered),
        file_name='properties.csv',
        mime='text/csv',
    )
	
