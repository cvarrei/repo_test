# On importe les packages nécessaires
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
from qualitative_prep import Qual_Standardize

class Qual_Standardize(TransformerMixin):
        # On standardize les valeurs qualitatives en utilisant la racine carré de p_k.
        def __init__(self):
            self.p_k = None
        # Notre fit calcule la valeur p_k nécessaire à la transformation.
        def fit(self, X, y=None):
            qual_int = X.astype(int)
            # On calcule la valeur p_k comme la proportion de True dans la colonne
            self.p_k = np.sum(qual_int, axis=0) / qual_int.shape[0]
            return self
        def transform(self, X, y=None):
            qual_int = X.astype(int)    
            # On transforme chaque valeur du tableau disjonctif complet par la racine carré de p_k
            qual_trans = qual_int / (np.sqrt(self.p_k))

            return qual_trans
            
# On crée une fonction qui enlève les caractères spéciaux
def norme(df):
    df = df.replace('Î', 'I', regex=True)
    df = df.replace('Ô', 'O', regex=True)
    df = df.replace('ô', 'o', regex=True)
    df= df.replace('é', 'e', regex=True)
    df = df.replace('è', 'e', regex=True)
    return df


# On crée une fonction qui ajoute les variables supplémentaires
def preproc(tl,sr,nbpp,st,te,nom_departement):

    # On transforme "te" en booléen
    if(te=="y"):
        te=True
    else:
        te=False

    # On renomme les colonnes
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

    # On enlève code_departement
    data.drop(columns=["code_departement"], inplace=True)
    data.drop(columns=["nom_departement"], inplace=True)

    return data


# On crée une fonction qui selon la modalité utilisera le fichier pickle adéquat de préprocessing (si modèle le nécessitant) et utilise le modèle de prédiction correspondant
def pred(data):
    
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
        data.drop(columns="Type local", inplace=True)
        data.drop(columns="nom_departement", inplace=True)
        data.drop(columns="Nombre pieces principales", inplace=True)
        data["estimated"] = data["Surface reelle bati"] * data["q1_prixm2"]
        with open("Model/local_model.pkl", 'rb') as file_reg:
            regression_loc = pickle.load(file_reg)
        predi=regression_loc.predict(data)


    return predi
