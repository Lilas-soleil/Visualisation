#Library

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_timeline import timeline
from PIL import Image 
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd

#==============================================================================================================================================

#Chargement des fichiers

noms_fichiers = ["history_pandemics_epidemic.csv","history_science.csv"]

# Créer une liste vide pour stocker les DataFrames

dataframes = []

# Parcourir les noms de fichiers et lire chaque fichier dans un DataFrame

for nom_fichier in noms_fichiers:
    chemin_fichier = "data/"+ nom_fichier
    try:
        df = pd.read_csv(chemin_fichier, encoding='ISO-8859-1',sep=';')
        dataframes.append(df)
    except FileNotFoundError:
        print(f"Fichier non trouvé : {nom_fichier}")
#==============================================================================================================================================

#Chargement du dataframe dans une variable et convertion de la colonnne "Mort (moyenne)" en int

df_history_pandemic_epidemic = dataframes[0]

df_history_pandemic_epidemic['Mort (moyenne)'] = pd.to_numeric(df_history_pandemic_epidemic['Mort (moyenne)'], errors='coerce')

#===============================================================================================================================

# Cnnfiguration de la page streamlit

st.set_page_config(page_title="MicroBioQuest", layout="wide", page_icon="🔬",)


colonne_logo, colonne_titre = st.columns([1, 4])
with colonne_logo:
    logo = Image.open("image/logo.png")
    logo_reduit = logo.resize((100,100))
    st.image(logo_reduit)
with colonne_titre:
    st.title("Epidemics and Pandemics in World History for 3300 years")

#=================================================================================================================================

#Sidebar

df = df_history_pandemic_epidemic

# Créer une sidebar
st.sidebar.title("Filter 🦠")

# Ajouter des filtres pour sélectionner la maladie
selected_disease = st.sidebar.multiselect("Sélectionnez la maladie", df['Disease cleaned'].unique())

# Ajouter des filtres pour sélectionner les continents
continent_columns = ['Europe Affected', 'Asia Affected', 'Africa Affected', 'Oceania Affected', 'North America Affected', 'South America Affected']
selected_continents = st.sidebar.multiselect("Sélectionnez les continents", continent_columns)

# Ajouter un bouton de réinitialisation
if st.sidebar.button("Réinitialiser les filtres"):
    selected_disease = df['Disease cleaned'].unique()
    selected_continents = continent_columns

# Filtrer les données en fonction des filtres sélectionnés
filtered_data = df[df['Disease cleaned'].isin(selected_disease) & (df[selected_continents].sum(axis=1) > 0)]

#=================================================================================================================================

# Métriques

colonne_metric, colonne_chart_pie = st.columns([1, 3])

with colonne_metric:
    
    total_events = len(filtered_data)
    total_deaths = filtered_data["Death toll upper limit"].sum()
    total_deaths = round(total_deaths / 1000000, 1)
    st.metric("Estimated Deaths", f"{total_deaths} million", )
    
    st.metric("Number of recorded epidemics/pandemics", total_events)

#=================================================================================================================================

#Chart pie: "Distribution of events by continent"

with colonne_chart_pie:

    # Conversion des colonnes booléennes en 1 pour True et 0 pour False
    continent_columns = ['Europe Affected', 'Asia Affected', 'Africa Affected', 'Oceania Affected', 'North America Affected', 'South America Affected']
    filtered_data[continent_columns] = filtered_data[continent_columns].astype(int)

    # Créer un graphique à secteurs basé sur les valeurs du DataFrame filtré
    totals = filtered_data[continent_columns].sum()
    totals_df = pd.DataFrame({'Continent': totals.index, 'Events': totals.values})
    fig = px.pie(totals_df, names='Continent', values='Events', title="Distribution of events by continent")
    
    # Centrer le titre 
    fig.update_layout(title_x=0.4, title_y=0.95)

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

#=================================================================================================================================

# Bar chart : Estimated Number of Deaths Based on Pathologies

# Triez le DataFrame en fonction du nombre de décès moyens
filtered_data = filtered_data.sort_values(by='Death toll upper limit', ascending=False)

# Sélectionnez les 5 premières maladies
top_5_diseases = filtered_data['Disease cleaned'].head(5)

# Créez le graphique à barres pour les 5 premières maladies
fig = px.bar(filtered_data[filtered_data['Disease cleaned'].isin(top_5_diseases)], x='Disease cleaned', y='Death toll upper limit', title="Estimated Number of Deaths Based on Pathologies")

# Personnalisez les noms des axes x et y
fig.update_xaxes(title_text="Diseases")
fig.update_yaxes(title_text="Average number of deaths")

# Centrer le titre en utilisant du CSS
fig.update_layout(title_x=0.4, title_y=0.95)  # Ajustez les valeurs pour un centrage précis
st.plotly_chart(fig)

#=========================================================================================

with st.expander("Filter selection output table"):
    # Sélectionnez les colonnes spécifiques et affichez-les directement
    columns_to_display = ['Event', 'Date', 'Location', 'Disease', 'Death toll (estimate)', 'Death toll lower limit', 'Mort (moyenne)', 'Death toll upper limit', 'LatestDate', 'EarliestDate']

    st.dataframe(filtered_data[columns_to_display])
    
#=================================================================================================================================

#Timeline
st.subheader('Timeline from 2600 BC to 2022:')

# Définissez le code HTML pour l'iframe avec des styles CSS

iframe_html = f'''
<iframe src='https://cdn.knightlab.com/libs/timeline3/latest/embed/index.html?source=15ZYhxdna0TcZGJCzrv_HZbCS4QGNivEJleRakZy2638&font=Default&lang=en&timenav_position=top&initial_zoom=2&height=650' width='100%' height='650' webkitallowfullscreen mozallowfullscreen allowfullscreen frameborder='0'></iframe>
'''
# Utilisez st.markdown pour afficher le composant iframe avec les styles personnalisés
st.markdown(iframe_html, unsafe_allow_html=True)
