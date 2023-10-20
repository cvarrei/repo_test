import pandas as pd
import sklearn
import os 
import pickle 
from sklearn.base import TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA as ACP
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

import numpy as np



def norme(df):
    df = df.replace('Î', 'I', regex=True)
    df = df.replace('Ô', 'O', regex=True)
    df = df.replace('ô', 'o', regex=True)
    df= df.replace('é', 'e', regex=True)
    df = df.replace('è', 'e', regex=True)
    return df


def preproc(nlot,tl,sr,nbpp,st,te,nom_region):
    
    if(te=="y"):
        te=True
    else:
        te=False
    
    data=pd.DataFrame([[nlot,tl,sr,nbpp,st,te,nom_region]],columns=["Nombre de lots","Type local","Surface reelle bati","Nombre pieces principales","Surface terrain","exterieur","nom_departement"])

    # Concatenation de l'open data
    df=pd.read_excel("/Users/adriencastex/Documents/Adrien/Cours/immo_TD/Data/doc_geo_varsupp/pop_active.xlsx")
    df=norme(df)
    data["pop_active"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["pop_active"]
    
    df=pd.read_excel("/Users/adriencastex/Documents/Adrien/Cours/immo_TD/Data/doc_geo_varsupp/base-cc-bases-tous-salaries-2021.xlsx")
    df=norme(df)
    data["salaire_moyen"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["salaire_moyen"]
    
    df=pd.read_excel("/Users/adriencastex/Documents/Adrien/Cours/immo_TD/Data/doc_geo_varsupp/ecoles2.xlsx")
    df=norme(df)  
    data["nb_etab_elem"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["nb_etab_elem"]
    
    df=pd.read_csv("/Users/adriencastex/Documents/Adrien/Cours/immo_TD/Clovis/m2.csv")
    df=norme(df)   
    data["mean_prixm2"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["mean_prixm2"]
    data["q1_prixm2"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["q1_prixm2"]
    data["q3_prixm2"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["q3_prixm2"]

    df=pd.read_csv("/Users/adriencastex/Documents/Adrien/Cours/immo_TD/Clovis/nbre_ventes.csv")
    df=norme(df)
    data["Total_Mutations"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["Total_Mutations"]




    return data





def pred(data):

    if (data["Type local"][0]=="Maison"):
        data.drop(columns="Type local", inplace=True)
        data.drop(columns="Nombre de lots", axis=0, inplace=True)
        data["estimated"] = data["Surface reelle bati"] * data["q3_prixm2"]
        with open("/Users/adriencastex/Documents/Adrien/Cours/immo_TD/Clovis/maison_preprocessing.pkl", 'rb') as file_prep:
            preprocessing_maison = pickle.load(file_prep)
        datat=preprocessing_maison.transform(data)
        with open("/Users/adriencastex/Documents/Adrien/Cours/immo_TD/Clovis/maison_model.pkl", 'rb') as file_reg:
            regression_maison = pickle.load(file_reg)
        predi=regression_maison.predict(datat)


    elif (data["Type local"][0]=="Appartement"):
        data.drop(columns="Type local", inplace=True)
        data["estimated"] = data["Surface reelle bati"] * data["q3_prixm2"]
        with open("/Users/adriencastex/Documents/Adrien/Cours/immo_TD/Clovis/Appartement_preprocessing.pkl", 'rb') as file_prep:
            preprocessing_app = pickle.load(file_prep)
        datat=preprocessing_app.transform(data)
        with open("/Users/adriencastex/Documents/Adrien/Cours/immo_TD/Clovis/Appartement_model.pkl", 'rb') as file_reg:
            regression_app = pickle.load(file_reg)
        predi=regression_app.predict(datat)

    elif (data["Type local"][0]=="Dépendance"):
        data.drop(columns="Type local", inplace=True)
        data.drop(columns="Surface reelle bati", inplace=True)
        with open("/Users/adriencastex/Documents/Adrien/Cours/immo_TD/Clovis/dependance_preprocessing.pkl", 'rb') as file_prep:
            preprocessing_dep = pickle.load(file_prep)
        datat=preprocessing_dep.transform(data)
        with open("/Users/adriencastex/Documents/Adrien/Cours/immo_TD/Clovis/dependance_model.pkl", 'rb') as file_reg:
            regression_dep = pickle.load(file_reg)
        predi=regression_dep.predict(datat)

    return predi


