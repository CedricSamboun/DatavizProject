import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import plotly_express as px
import time
import seaborn as sns
import altair as alt
import streamlit.components.v1 as component
from streamlit.proto.Checkbox_pb2 import Checkbox
from functools import wraps

def log(func):
    def wrapper(*args, **kwargs):
        with open("logs.txt", "a") as f:
            start = time.time()
            val = func(*args, **kwargs)
            end = time.time()
            f.write("\nThe function %s " % func.__name__ + " took " + str(end - start) + "s to complete\n")
            f.write('\n-----------------------------------------------------------------\n')
        return val
    return wrapper


def config():

    st.set_page_config(
        page_title = "SAMBOUN'IMMO",
        layout = 'wide',
        page_icon='🏢')
config()
def get_weekday(df):
    return df.weekday()

def get_dom(df):
    return df.day

def get_hours(df):
    return df.hour

@log
def count_rows(rows):
    return len(rows)
@log
def get_months(df):
    return df.months


@log
@st.cache(allow_output_mutation=True)
def read_csv():
    data = pd.read_csv('full_2020.csv',low_memory=False)
    data = data.fillna(0)
    data['date_mutation'] = pd.to_datetime(data['date_mutation'])
    data['valeur_fonciere'] = data['valeur_fonciere'].astype(float)
    data['surface_terrain'] = data['surface_terrain'].astype(float)
    data['longitude'] = data['longitude'].astype(float)
    data['latitude'] = data['latitude'].astype(float)
    data['nombre_pieces_principales'] = data['nombre_pieces_principales'].astype(float)
    data['surface_reelle_bati'] = data['surface_reelle_bati'].astype(float)
    data['date_mutation'] = pd.to_datetime(data['date_mutation'])
    data['hours']= data['date_mutation'].map(get_hours) 
    data['dom']= data['date_mutation'].map(get_dom)
    data['weekday']= data['date_mutation'].map(get_weekday)
    data['months']=data['date_mutation'].dt.month

    del data['id_mutation']
    del data['numero_disposition']
    del data['ancien_code_commune']
    del data['ancien_nom_commune']
    del data['numero_volume']
    del data['ancien_id_parcelle']
    del data['lot1_numero']
    del data['lot1_surface_carrez']
    del data['lot2_numero']
    del data['lot2_surface_carrez']
    del data['lot3_numero']
    del data['lot3_surface_carrez']
    del data['lot4_numero']
    del data['lot4_surface_carrez']
    del data['lot5_numero']
    del data['lot5_surface_carrez']
    del data['nombre_lots']
    del data['code_type_local']
    del data['id_parcelle']

    return data


@log
def prepare_map(df):
    map1 = df[["latitude","longitude","months"]]
    map1.dropna(subset = ["latitude"], inplace=True)
    map1.dropna(subset = ["longitude"], inplace=True)
    return map1

@log
def map(df):
    st.subheader("Carte des transactions immobilières par mois")
    map1=prepare_map(df)
    months_filter = st.slider('Choisir un mois', 0, 12,3) 
    map1_filtered = map1[map1["months"] == months_filter] 
    st.map(map1_filtered,zoom=2)
datas = read_csv()

data_map = pd.DataFrame()

@log
def checkbox1(data):
    data_val_dep=data.groupby(['code_departement']).mean()
    if st.checkbox("Moyenne en France"):
        st.write(data_val_dep.head(96))

options=datas['code_departement'].unique().tolist()

@log
def checkbox2(data):
    arr4 = data.code_departement
    fig4, ax = plt.subplots()
    ax.hist(arr4, bins=100, range=(0,96),orientation='horizontal')
    ax.set_title('Montant des ventes par départements')
    ax.set_yticklabels(options, fontsize=3)

    ax.set_ylabel("some label", fontsize=5)
    ax.set_ylabel('département')

    if st.checkbox('Montant des ventes par départements'):
        st.write("Vous pouvez voir grâce à cet histogramme le montant des ventes en fonction du département.")
        st.pyplot(fig4)
#------------------------------------
def graph1(df, col1, col2):
    x = df[col1]
    y = df[col2]

    compare = pd.concat([x, y], axis=1)

    fig1, ax = plt.subplots()
    ax.set_xlabel("Surface")
    ax.set_ylabel("Prix")
    ax.plot(compare,color="blue")

    st.pyplot(fig1)
@log
def select_type():
    choice = st.selectbox("Choisir le type d'habitation :", ['Maison', 'Appartement'])
    return choice


@log
def func1(df, colu, param):
    return df.loc[df[colu] == param] 


@log
def choix(arg1,arg2,arg3):
    choice = [arg1,arg2,arg3]
    return choice
choice = choix('Présentation générale','Présentation par département','Carte des transactions immobilières')   







df= pd.read_csv('full_2020.csv')
@log
def mask1(nom,valeur2):
    return df.mask(df[nom]!=valeur2)

def option(arg):
    option = st.sidebar.selectbox(arg, choice)
    

    st.set_option('deprecation.showPyplotGlobalUse', False)
    if option == choice[0]:

        st.title('Présentation générale')
        st.write("Vous trouverez sur cette page de nombreuses informations sur les transactions immobilières en France, bonne visite!")
        st.subheader("Introduction aux transactions immobilières en France")
        checkbox1(datas)
        checkbox2(datas)
        st.subheader("Graphique du prix d'un selon sa surface")
        choix_type = select_type()
        df5 = func1(datas, 'type_local', choix_type)
        x = df5['surface_reelle_bati']
        y = df5['valeur_fonciere']
        compare = pd.concat([x, y], axis=1)
        fig1, ax = plt.subplots()
        ax.set_xlabel("Surface")
        ax.set_ylabel("Prix")
        ax.plot(compare,color="blue")
        st.pyplot(fig1)
        
        countfilter=datas["type_local"].value_counts()
        st.subheader("Proportion des types d'habitation")
        fig = px.pie(countfilter, values ="type_local", names=countfilter.index)
        st.plotly_chart(fig)
        st.subheader('Proportion des types de cultures')
        countfilter=datas["nature_culture"].value_counts()
        fig = px.pie(countfilter, values ="nature_culture", names=countfilter.index)
        st.plotly_chart(fig)
        

        datas2=datas.dropna()
        dataf1 = datas2.groupby(['nature_culture', 'type_local']).apply(count_rows).unstack()
        sns.heatmap(dataf1, linewidths = 1)
        st.pyplot()   
        
    elif option == choice[1]:
        
        st.title('Présentation par département')
        st.write("Voici ci-dessous un tableau, veuillez choisir un département afin d'obtenir diverses informations statistiques sur celui-ci.")
        choix_depart = datas['code_departement'].unique().tolist()
        depart=st.selectbox('Sélectionner un département', choix_depart, 0)
        dataf2=datas[datas['code_departement']==depart]
        st.write(dataf2.describe())
        st.write("Vous pouvez voir ci-dessous un graphique représentant le prix d'un bien en fonction de sa surface.")
        choix_type = select_type()
        df5 = func1(dataf2, 'type_local', choix_type)
        x = df5['surface_reelle_bati']
        y = df5['valeur_fonciere']
        compare = pd.concat([x, y], axis=1)
        fig1, ax = plt.subplots()
        ax.set_xlabel("surface")
        ax.set_ylabel("price")
        ax.plot(compare,color="blue")
        st.pyplot(fig1)
        
        st.subheader("Carte des transactions immobilières par département")
        if st.checkbox("Cocher pour sélectionner un département"):
         st.write("Vous pouvez voir ici le location de l'ensemble des transactions immobilières en France par département.")
         departement_selected= st.slider("Choisir un département",1,95)
         map_df = mask1("code_departement",departement_selected)
        else:
   
             map_df = df
    
        map_df.dropna(subset = ["latitude"], inplace = True)
        map_df.dropna(subset = ["longitude"], inplace = True)
        st.map(map_df)
    
        

        
    elif option == choice[2]:
        st.title('Carte des transactions immobilières')
        st.write("Vous pouvez voir ci-dessous la location de l'ensemble des transactions immobilières en France par mois.")
        data_map['lon'] = datas['longitude']
        data_map['lat'] = datas['latitude']
        
        
        map(datas)

    
        
option('Sélectionner')
            