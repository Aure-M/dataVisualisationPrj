import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import st_folium
import bokeh.plotting as bk
import plotly.express as px
from datetime import datetime


links = {
    2020:"https://drive.google.com/u/0/uc?id=1-3aYJTGnwPDh8K0vIPXNuoGg4plRk0sb&export=download&confirm=t&uuid=f90aed2b-688d-4fa2-be31-316fbf3ee936",
    2019:"https://drive.google.com/u/0/uc?id=16B0R6ZfzpaaGpzTAl0vncB7WN5vWjz_K&export=download&confirm=t&uuid=f90aed2b-688d-4fa2-be31-316fbf3ee936"
}

@st.cache(suppress_st_warning=True)
def fetchData(year):
    data = pd.read_csv(links[year])
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
	#fig = plt.figure()
	répartition_communes = data["nom_commune"].value_counts().sort_values(axis=0, ascending=False,)
	top20_communes = répartition_communes.head(20)
	
	fig = bk.figure(x_range=list(top20_communes.index), height=250, title="Cities",
			toolbar_location=None, tools="", plot_width=600, plot_height=500)

	fig.vbar(x=top20_communes.index, top=top20_communes, width=0.9)

	fig.xgrid.grid_line_color = None
	fig.xaxis.major_label_orientation = 1.2
	#top20_communes.plot(kind = "bar")
	st.bokeh_chart(fig, use_container_width=True)
	return top20_communes.index[:2]

def repartission_TypeLocal_PIE(data,city):
	fig = plt.figure(figsize=(10,10))
	colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#fffc52']
	repartition = []
	explode = []
	repartition = data["type_local"].value_counts()
	for i in range(len(repartition)):
		explode.append(0.05)

	plt.pie(repartition, labels=repartition.index, explode=explode, colors= colors, startangle=65, autopct='%1.1f%%',shadow='True')
	plt.title(label= 'Distribution of the type_local variable at '+city)
	plt.legend()
	st.pyplot(fig)

def repartission_Mutation_PIE(data,city):
	fig = plt.figure(figsize=(10,10))
	colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#fffc52',"#da70d6"]
	repartition = []
	explode = []
	repartition = data[data["nom_commune"] == city]["nature_mutation"].value_counts()
	for i in range(len(repartition)):
		explode.append(0.05)
	plt.pie(repartition.to_numpy(), explode=explode, colors= colors, startangle=65, autopct='%1.1f%%',shadow='True')
	plt.title(label= 'Répartition des mutations à '+city)
	plt.legend(labels = repartition.index)
	st.pyplot(fig)

def scatterPlot(data):
 
	plot = px.scatter(data, x="surface_terrain", y="valeur_fonciere", color="type_local")
	st.plotly_chart(plot, use_container_width=True)
 

def yearAnalysis(data,selected=None,showMap=False):
	st.write("# General analysis on the dataset")
	st.write("## Cities ranking based on the number of real estate operations")
	cities = repartition_communes_BAR(data)
	cities = list(cities)
	st.write("---")
	for city in cities:
		st.write("## Let's study ",city)
		col1, col2 = st.columns(2)
		with col1:
			st.caption('Distribution of the property at '+city)
			repartission_TypeLocal_PIE(data[data["nom_commune"]==city],city)
		with col2:
			st.caption('Distribution of the type of mutation at '+city)
			repartission_Mutation_PIE(data,city)
	
	st.write("---")
	st.write("# Focus on ", selected)
	st.write("### Relation between the lands value and their area")
	focus = data[data["nom_commune"]==selected]
	scatterPlot(focus)
	if showMap:
		st.map(focus[["latitude","longitude"]])
		


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
	

