import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sn
import streamlit as st
import folium
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
def convert_df(df):
    return df.to_csv().encode('utf-8')

def add_categorical_legend(folium_map, title, color_by_label):
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map