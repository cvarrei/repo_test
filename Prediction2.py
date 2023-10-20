import numpy as np
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


def norme(df):
    df = df.replace('Î', 'I', regex=True)
    df = df.replace('Ô', 'O', regex=True)
    df = df.replace('ô', 'o', regex=True)
    df= df.replace('é', 'e', regex=True)
    df = df.replace('è', 'e', regex=True)
    return df


def preproc(tl,sr,nbpp,st,te,nom_departement):
    
    if(te=="y"):
        te=True
    else:
        te=False
    
    data=pd.DataFrame([[tl,sr,nbpp,st,te,nom_departement]],columns=["Type local","Surface reelle bati","Nombre pieces principales","Surface terrain","exterieur","nom_departement"])

    # Concatenation de l'open data
    df=pd.read_excel("Data/pop_active.xlsx")
    df=norme(df)
    data["pop_active"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["pop_active"]
    
    df=pd.read_excel("Data/base-cc-bases-tous-salaries-2021.xlsx")
    df=norme(df)
    data["salaire_moyen"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["salaire_moyen"]
    
    df=pd.read_excel("Data/ecoles2.xlsx")
    df=norme(df)  
    data["nb_etab_elem"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["nb_etab_elem"]
    
    df=pd.read_csv("Data/m2.csv")
    df=norme(df)   
    data["mean_prixm2"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["mean_prixm2"]
    data["q1_prixm2"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["q1_prixm2"]
    data["q3_prixm2"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["q3_prixm2"]

    df=pd.read_csv("Data/nbre_ventes.csv")
    df=norme(df)
    data["Total_Mutations"]=df.loc[df['nom_departement'] == data["nom_departement"][0]]["Total_Mutations"]

    return data



def pred(data):
    print(data)

    return predi
