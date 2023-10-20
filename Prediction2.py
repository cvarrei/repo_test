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
    data = pd.merge(data, df, on="nom_departement", how="left")
        
    df=pd.read_excel("Data/base-cc-bases-tous-salaries-2021.xlsx")
    df=norme(df)
    data = pd.merge(data, df, on="nom_departement", how="left")

    df=pd.read_excel("Data/ecoles2.xlsx")
    df=norme(df)  
    data = pd.merge(data, df, on="nom_departement", how="left")
        
    df=pd.read_csv("Data/m2 copy.csv")
    df=norme(df)   
    data = pd.merge(data, df, on="nom_departement", how="left")

    df=pd.read_csv("Data/nbre_ventes.csv")
    df=norme(df)
    data = pd.merge(data, df, on="nom_departement", how="left")

    data.drop(columns=["code_departement"], inplace=True)

    return data



def pred(data):
    pd.set_option('display.max_columns', None)
    print(data)
    if (data["Type local"][0]=="Maison"):
        data.drop(columns="Type local", inplace=True)
        data["estimated"] = data["Surface reelle bati"] * data["q3_prixm2"]
        with open("Model/maison_preprocessing.pkl", 'rb') as file_prep:
            preprocessing_maison = pickle.load(file_prep)
        datat=preprocessing_maison.transform(data)
        with open("Model/maison_model.pkl", 'rb') as file_reg:
            regression_maison = pickle.load(file_reg)
        predi=regression_maison.predict(datat)

    elif (data["Type local"][0]=="Appartement"):
        data.drop(columns="Type local", inplace=True)
        data["estimated"] = data["Surface reelle bati"] * data["q3_prixm2"]
        with open("Model/appartement_preprocessing.pkl", 'rb') as file_prep:
            preprocessing_app = pickle.load(file_prep)
        datat=preprocessing_app.transform(data)
        with open("Model/appartement_model.pkl", 'rb') as file_reg:
            regression_app = pickle.load(file_reg)
        predi=regression_app.predict(datat)

    elif (data["Type local"][0]=="Dépendance"):
        data.drop(columns="Type local", inplace=True)
        data.drop(columns="Surface reelle bati", inplace=True)
        data.drop(columns="Nombre pieces principales", inplace=True)
        with open("Model/dependance_preprocessing.pkl", 'rb') as file_prep:
            preprocessing_dep = pickle.load(file_prep)
        datat=preprocessing_dep.transform(data)
        with open("Model/dependance_model.pkl", 'rb') as file_reg:
            regression_dep = pickle.load(file_reg)
        predi=regression_dep.predict(datat)

    elif (data["Type local"][0]=="local"):
        print("oui")
        data.drop(columns="Type local", inplace=True)
        print("oui")
        data.drop(columns="nom_departement", inplace=True)
        print("oui")
        data.drop(columns="Nombre pieces principales", inplace=True)
        data["estimated"] = data["Surface reelle bati"] * data["q1_prixm2"]
        print("oui2")
        with open("Model/local_model.pkl", 'rb') as file_reg:
            regression_loc = pickle.load(file_reg)
        print("oui3")
        predi=regression_loc.predict(data)

    print("#####################################")
    print(predi)


    return predi