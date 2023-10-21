# On importe les packages nécessaires
import dash
from dash import callback
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import json
from Prediction2 import preproc, pred
from qualitative_prep import Qual_Standardize
import numpy as np
from sklearn.base import TransformerMixin

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
            
df=pd.read_csv("df_dash_dashboard.csv") # On importe le jeux de données

############### Nettoyage pour faciliter la représentation graphique ###############
df["year"] = df["year"].astype(str) # On change le type de données des années
# On enlève les caractères spéciaux
df = df.replace('Î', 'I', regex=True) 
df = df.replace('Ô', 'O', regex=True)
df = df.replace('ô', 'o', regex=True)
df= df.replace('é', 'e', regex=True)
df = df.replace('è', 'e', regex=True)
df = df.replace('û', 'u', regex=True)
# On change le type de données des mois en catégorie pour garder leur ordre réel
df['month'] = pd.Categorical(df['month'], ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre'])
df.sort_values(['month'], inplace=True)
# On corrige certaines différence entre le jeux de données avec nos valeurs et le geojson.
df.loc[df["nom_region"] == "Nouvelle-Aquitaine", "nom_region"] = "Nouvelle Aquitaine"
df.loc[df["nom_region"] == "Grand Est", "nom_region"] = "Grand-Est"

################# Maps Chloropeths ###############
with open("regions.json", "r") as file:
    regions_data = json.load(file)  # On importe les figures de la carte chloropeth

# On crée la carte chloropeth
fig_region = px.choropleth(
    df,  # Notre jeu de données
    geojson=regions_data, # Notre json avec nos tracés
    locations='nom_region',  # Notre colonne contenant le nom des régions dans notre dataframe
    color='Valeur fonciere',  # Notre couleur que nous voulons utiliser pour le remplissage
    color_continuous_scale='YlOrRd', # La palette de couleur utilisée
    featureidkey="properties.libgeo",  # On indique le path aux ids dans le geoson
    range_color=[100000, 250000] # On indique la plage de la légende
)

# On actualise les coordonnées géographiques
fig_region.update_geos(
    center={"lat": 45.8, "lon": 5},  # On centre la carte sur une coordonnée légèrement sur la droite de la france pour un meilleur affichage
    projection_scale=17,  # On ajuste l'échelle pour zoomer sur la phrance
    visible=False  # On enlève la carte du monde derrière
)

# On ajuste les paramètres graphiques de la carte
fig_region.update_layout(
    # On change ces dimensions
    autosize=False,
    width=500,
    height=600,
    # On change le background de la carte
    paper_bgcolor="rgb(34,34,34)",
    geo_bgcolor="rgb(34,34,34)",
    # On retire la légende couleur
    coloraxis_showscale=False,
    margin={"r":0,"t":0,"l":0,"b":0}
)

# On change la couleur des tracés
fig_region.update_traces(marker_line=dict(color="rgb(34,34,34)", width=1))


# Les commentaires sont les mêmes pour la carte des départements
with open("departement.json", "r") as file:
    dep_data = json.load(file)

fig_dep = px.choropleth(
    df,  
    geojson=dep_data,
    locations='nom_departement',  
    color='Valeur fonciere',  
    color_continuous_scale='YlOrRd',
    featureidkey="properties.libgeo",  
    range_color=[30000, 300000]
)
fig_dep.update_geos(
    center={"lat": 45.8, "lon": 1.888334},  
    projection_scale=17, 
    visible=False 
)
fig_dep.update_layout(
    autosize=False,
    width=600,
    height=600,
    paper_bgcolor="rgb(34,34,34)",
    geo_bgcolor="rgb(34,34,34)",
    coloraxis_showscale=False,
    margin={"r":0,"t":0,"l":0,"b":0}
)
fig_dep.update_traces(marker_line=dict(color="rgb(34,34,34)", width=1))



################### Line plots ###################


order_month = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
# On crée notre line plot entre les mois et la valeur foncière avec une ligne par région
fig_month = px.line(df, x="month", y="Valeur fonciere", category_orders={'month': order_month}, color='nom_region')

# On actualise l'affichage
fig_month.update_layout(
        legend_title="", # On enlève le titre de la légende
        xaxis_title="Mois", # On change le titre de l'axe x
        # On change le fond du plot
        paper_bgcolor="rgb(34,34,34)",
        plot_bgcolor="rgb(34,34,34)",
        # On change la couleur du texte de la légende
        legend_font_color="white",
        coloraxis_showscale=False
    )

# On enlève le grid de chaque x et on change le texte des axes x et y en blanc
fig_month.update_xaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
fig_month.update_yaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))


# On applique les mêmes coomentaires pour la valeur foncière en fonction des années en fonction des régions
fig_year = px.line(df, x="year", y="Valeur fonciere", color='nom_region')
fig_year.update_layout(
    legend_title="",
    xaxis_title="Année",
    paper_bgcolor="rgb(34,34,34)",
    plot_bgcolor="rgb(34,34,34)",
    legend_font_color="white",
    coloraxis_showscale=False
)
fig_year.update_xaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
fig_year.update_yaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))


# On applique les mêmes commentaires pour la valeur foncière en fonction des mois en fonction des départements
order_month = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
fig_month_dep = px.line(df, x="month", y="Valeur fonciere", category_orders={'month': order_month}, color='nom_departement')
fig_month_dep.update_layout(
        legend_title="",
        xaxis_title="Mois",
        paper_bgcolor="rgb(34,34,34)",
        plot_bgcolor="rgb(34,34,34)",
        legend_font_color="white",
        coloraxis_showscale=False
    )
fig_month_dep.update_xaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
fig_month_dep.update_yaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))

# On applique les mêmes coomentaires pour la valeur foncière en fonction des années en fonction des départements
fig_year_dep = px.line(df, x="year", y="Valeur fonciere", color='nom_departement')
fig_year_dep.update_layout(
    legend_title="",
    xaxis_title="Année",
    paper_bgcolor="rgb(34,34,34)",
    plot_bgcolor="rgb(34,34,34)",
    legend_font_color="white",
    coloraxis_showscale=False
)
fig_year_dep.update_xaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
fig_year_dep.update_yaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))


################### Dashboard ###################
# Il est composé de deux pages: l'une pour les régions, l'une pour les départements

# Le squelette entre departement Layout et regions Layout étant le même, nous ne détaillerons que ce dernier.
regions_layout = html.Div([dbc.Row([   
                    dbc.Col(dcc.Dropdown( # Liste déroulante des années
                            id="annee-dropdown",
                            options=[{'label': str(annee), 'value': annee} for annee in sorted(df['year'].unique())], # Récupère les différentes années
                            value="2018", # valeur par défaut
                        ), width=3), # Largeur de la colonne de la liste
                    
                    dbc.Col(dcc.Dropdown( # Liste déroulante des régions
                            id="region-dropdown",
                            options=[{'label': region, 'value': region} for region in sorted(df['nom_region'].unique())], # Récupère les différentes régions
                            multi=True # Possibilité de faire plusieurs choix
                        ),width=3) # Largeur de la colonne de la liste
                    ]),
    # Dans une ligne sous les listes déroulantes,
    dbc.Row(
                [   
                    dbc.Col([ # Dans une première colonne, nous affichons les lines plots qui s'étendront sur la moitié de la page
                        dbc.Row([
                            dcc.Graph(id='year-plot', figure=fig_year, style={"height": "50vh"})
                        ]),
                        dbc.Row([
                            dcc.Graph(id='month-plot', figure=fig_month, style={"height": "50vh"})
                        ]),
                            dbc.Row([html.P('Il est possible de télécharger la figure d\'intérêt en png grâce à l\'icone appareil photo en survolant dessus.', className="text-center")
                                    ], justify="center") # On ajoute un texte qui indique la possibilité de télécharger les figures.
                    ]),
                    dbc.Col([ # Dans la deuxième colonne, nous affichons les KPIs et la carte de france
            dbc.Row([
                dbc.Col([
                    html.Div(id='kpi1-reg-value', children='KPI'),
                    html.P('Moyenne des valeurs foncières')
                ], width=6),
                dbc.Col([
                    html.Div(id='kpi2-reg-value', children='KPI'),
                    html.P(id='evolution-text', children=f'Evolution entre 2018 et 2021')
                ], width=6),
            ]),
            dcc.Graph(id='region-map-plot',figure=fig_region, style={"height": "70vh", "width": "100%"})
        ], width=6)
                ]
            )
])

# Les commentaires sont similaires pour le départments_layout
departments_layout = html.Div([
    dbc.Row([   
        dbc.Col(dcc.Dropdown(
                id="annee-dropdown",
                options=[{'label': str(annee), 'value': annee} for annee in sorted(df['year'].unique())],
                value="2018",
            ), width=3),

        dbc.Col(dcc.Dropdown(
                id="departements-dropdown",
                options=[{'label': department, 'value': department} for department in sorted(df['nom_departement'].unique())],
                multi=True
            ), width=3) 
    ]),

    dbc.Row([   
        dbc.Col([
            dbc.Row([
                dcc.Graph(id='year-dep-plot', figure=fig_year_dep, style={"height": "50vh"})
            ]),
            dbc.Row([
                dcc.Graph(id='month-dep-plot', figure=fig_month_dep, style={"height": "50vh"})
            ]),
            dbc.Row([html.P('Il est possible de télécharger la figure d\'intérêt en png grâce à l\'icone appareil photo en survolant dessus.', className="text-center")
                    ], justify="center")
        ]),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div(id='kpi1-value', children='KPI'),
                    html.P('Moyenne des valeurs foncières')
                ], width=6),
                dbc.Col([
                    html.Div(id='kpi2-value', children='KPI'),
                     html.P(id='evolution-dep-text', children=f'Evolution entre 2018 et 2021')
                ], width=6),
            ]),
            dbc.Row([
                dcc.Graph(id='departement-map-plot',figure=fig_dep, style={"height": "70vh"})
            ])
        ], width=6)
    ])
])


# Interface principale du dashboard
dashboard_layout = html.Div([
    html.H2("Evolution des valeurs foncières", className="gradient-title"), #Titre 
    # On affiche deux boutons qui switcheront entre la layout régions et celle département
    dbc.Row([
        dbc.Col(dbc.Button("Régions", id="btn-regions", n_clicks=0, className="custom-button"), width="auto"),
        dbc.Col(dbc.Button("Départements", id="btn-departements", n_clicks=0, className="custom-button"), width="auto")
    ], justify="center", className="g-2 mb-4"),

    # On affiche le layout correspondant au bouton
    html.Div(id="contant-container") 
])



################### Accueil ###################
accueil_layout = html.Div([
    html.H2("Bienvenue sur ImmoPred", className="custom-h2-title"),

    html.P("Découvrez l'immobilier sous un nouvel angle avec notre application intuitive. Que vous soyez un investisseur, un acheteur ou simplement curieux des tendances du marché immobilier en France, nous avons tout ce dont vous avez besoin pour prendre des décisions éclairées.",
           style={'text-align': 'center'}),
    
    html.H3("Explorez les Données Clés", style={'text-align': 'center'}, className="custom-h3-title"),
    html.P("Plongez dans les tableaux de bord graphiques riches en KPI pour obtenir une vue d'ensemble complète du marché immobilier. Visualisez les tendances de prix, l'évolution des départements et régions et bien plus encore. Nos indicateurs de performance clés vous aident à prendre des décisions éclairées.",
           style={'text-align': 'center'}),
    
    html.H3("Prédisez les Valeurs Foncières", style={'text-align': 'center'}, className="custom-h3-title"),
    html.P("Notre menu de prédiction vous permet de calculer les valeurs foncières potentielles en fournissant simplement quelques informations clés. Obtenez des estimations précises pour votre futur investissement ou évaluez la valeur de votre bien immobilier actuel.",
           style={'text-align': 'center'}),
    
    html.H3("Restez Informé", style={'text-align': 'center'}, className="custom-h3-title"),
    html.P("Restez au courant des dernières actualités et analyses du marché immobilier en France grâce à nos mises à jour en temps réel. Abonnez-vous à nos alertes pour ne rien manquer.",
           style={'text-align': 'center'}),
    
    html.P("Rejoignez-nous dès aujourd'hui pour explorer le monde passionnant de l'immobilier en France, que ce soit pour investir, acheter ou simplement vous informer. Votre avenir immobilier commence ici.",
           style={'text-align': 'center'}),
    html.P("Une application réalisée par Adrien Castex, Victor Sigogneau et Clovis Varangot-Reille", style={'text-align': 'center', 'color': 'rgb(226, 142, 127)'} ),
], style={'text-align': 'center', 'margin': 'auto', 'max-width': '80%'})


################### Prédiction ###################

# On crée une liste des options pour les petites listes drop-downs.
options_type_bien = [
    {'label': 'Maison', 'value': 'Maison'},
    {'label': 'Appartement', 'value': 'Appartement'},
    {'label': 'Dépendance', 'value': 'Dépendance'},
    {'label': 'Local', 'value': 'Local'}
]

# On crée une liste des options pour les petites listes drop-downs.
options_exterieur = [
    {'label': 'y', 'value': 'y'},
    {'label': 'n', 'value': 'n'}
]


prediction_layout = html.Div([
    html.H2('Prédisez le prix de votre bien', className="gradient-title"), # Titre de la page
    dbc.Row([ 
        dbc.Col([ # On place tous les inputs sur la partie gauche de la page
            dbc.Row([html.P('Type de bien'), 
                     dcc.Dropdown(id='tl', # Liste avec les types de biens
                                  options=options_type_bien,
                                  value='Maison'
                                  )], style={"padding-left": "10px"}),
            # Série d'Inputs numériques
            dbc.Row([html.P('Surface habitable du bien'), dcc.Input(id='sr', type='number', value=0, style={"margin-left": "10px"})], style={"padding-left": "10px"}),
            dbc.Row([html.P('Nombre de pieces principales'), dcc.Input(id='nbpp', type='number', value=0, style={"margin-left": "10px"})], style={"padding-left": "10px"}),
            dbc.Row([html.P('Surface du terrain'), dcc.Input(id='st', type='number', value=0, style={"margin-left": "10px"})], style={"padding-left": "10px"}),
            dbc.Row([html.P('Présence d\'un extérieur'),
                     dcc.Dropdown(id='te', # Liste avec la possibilité d'extérieur ou non
                                  options=options_exterieur,
                                  value='n'
                                  )], style={"padding-left": "10px"}),
            dbc.Row([html.P('Nom du departement'), # Liste avec les noms de départements
                     dcc.Dropdown(id='nom_departement',
                                  options=[{'label': department, 'value': department} for department in sorted(df['nom_departement'].unique())],
                                  value='Ain'
                                  )], style={"padding-left": "10px", "margin-bottom": "20px"}),
            dbc.Row( # On place en bas un bouton qui lancera la prédiction
                html.Button('Lancement de la prediction', id='mon-bouton', n_clicks=0, className="custom-button", style={"width": "auto", "margin": "0 auto"}), 
                style={"display": "flex", "justify-content": "center", "padding-top": "10px"}
            )
        ], width=6), 
        dbc.Col([dbc.Row([html.P(id="annonce-pred", children="La valeur estimé du bien est de ")]),
                 dbc.Row([html.P(id='output-texte', children="En attente")])   # Second column with width 6
    ], width=6) 
    ])
])


################### Menu Latéral ###################
sidebar = html.Div([ # On crée un menu latéral qui nous permettra de naviguer entre les pages
    dbc.Nav(
        [   
            html.Img(src="/assets/logo.png", height="200px"), # On y place un logo créée pour l'entreprise
            html.Div("SARDE IMMO", className="sidebar-text"), # On place le nom de l'entreprise
            html.Div("AGENCY", className="sidebar-text2"),
            # On place les différents liens
            dbc.NavLink("Accueil", href="/", active="exact"),
            dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
            dbc.NavLink("Prediction", href="/prediction", active="exact")
        ], 
        vertical=True,
        pills=True, 
        fill=True,
        className="rounded-navbar"
        ),
    ], style={"width":"18%", "position":"fixed", "height": "100%", "background-color": "#FAFAFA"}
)


################### Contenu de la page active ###################
# Selon la page cliqué dans le menu latéral, le contenu de la page s'actualisera
content = html.Div(id="page-content", style={"margin-left": "18%"})


#################################################################################################################################################

######## Application

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY]) # On incorpore un thème extérieur de dbc "DARKLY"
server=app.server

# Définir la mise en page de l'interface utilisateur avec le menu latéral et le contenu de la page correspondant au lien
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


######### Interface
# FONCTION: Selon le lien url obtenu par le menu latéral (NAVLINK), on renvoie le contenu de la page correspondant à la valeur "content"
@app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return accueil_layout
    elif pathname == "/dashboard":
        return dashboard_layout
    elif pathname == "/prediction":
        return prediction_layout


######### Dashboard

# FONCTION: Selon quel est le dernier bouton clické dans la page dashboard, on affiche la page en relation aux départements ou regions.
@app.callback(
    Output("contant-container", "children"),
    [Input("btn-regions", "n_clicks"),
    Input("btn-departements", "n_clicks")]
)
def switch_layout(btn1, btn2):
    change_dash = [p["prop_id"] for p in dash.callback_context.triggered][0] # Permet de récupérer le nom du dernier bouton clické.
    if "btn-regions" in change_dash:
        return regions_layout
    elif "btn-departements" in change_dash:
        return departments_layout
    else:
        return regions_layout


# FONCTION: Selon la valeur de l'année et de région(s) sélectionnées dans les dropdowns list, on actualise notre line plot mensuelle 
@app.callback(
    Output('month-plot', 'figure'),  
    Input('annee-dropdown', 'value'),  
    Input('region-dropdown', 'value')
)
def update_month_plot(selected_year, selected_regions):
    if not selected_regions: # Si aucune région n'a été sélectionné, on les affiche toutes
        selected_regions = df['nom_region'].unique()

    filtered_df = df[(df['year'] == selected_year) & (df['nom_region'].isin(selected_regions))] # On filtre notre dataframe pour n'avoir que l'année et région(s) correspondantes
    grouped_df = filtered_df.groupby(['nom_region',"month"])['Valeur fonciere'].mean().reset_index() # On récupère la moyenne de ces valeurs

    # On réalise les mêmes paramètres graphiques que précédemment.
    fig_month_updated = px.line(grouped_df, x="month", y="Valeur fonciere", category_orders={'month': order_month}, color='nom_region')  
    fig_month_updated.update_layout(
        legend_title="",
        xaxis_title="Mois",
        paper_bgcolor="rgb(34,34,34)",
        plot_bgcolor="rgb(34,34,34)",
        legend_font_color="white",
        coloraxis_showscale=False
    )
    fig_month_updated.update_xaxes(type='category',gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
    fig_month_updated.update_yaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
    
    return fig_month_updated # On renvoie notre line plot mensuelle actualisée

# FONCTION: Selon la valeur de la/les région(s) sélectionnées dans les dropdowns list, on actualise notre line plot anuelle
# La structure étant la même, nous ne détaillerons pas les commentaires des autres fonctions avec line plots 
@app.callback(
    Output('year-plot', 'figure'),  
    Input('region-dropdown', 'value')  
)
def update_year_plot(selected_regions):
    # Check if regions are selected; if not, display for all regions.
    if not selected_regions:
        selected_regions = df['nom_region'].unique()

    filtered_df = df[df['nom_region'].isin(selected_regions)]
    grouped_df = filtered_df.groupby(['year', 'nom_region'])['Valeur fonciere'].mean().reset_index()
    fig_year_updated = px.line(grouped_df, x="year", y="Valeur fonciere", color='nom_region')
    
    fig_year_updated.update_layout(
        legend_title="",
        xaxis_title="Année",
        paper_bgcolor="rgb(34,34,34)",
        plot_bgcolor="rgb(34,34,34)",
        legend_font_color="white",
        coloraxis_showscale=False
    )
 
    fig_year_updated.update_xaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
    fig_year_updated.update_yaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
    
    return fig_year_updated

# FONCTION: Selon la valeur de l'année et de département(s) sélectionnées dans les dropdowns list, on actualise notre line plot mensuelle 
@app.callback(
    Output('month-dep-plot', 'figure'),  # id of the month plot Graph component and property to update
    Input('annee-dropdown', 'value'),  # id of the year dropdown and property to get
    Input('departements-dropdown', 'value')  # id of the region dropdown and property to get
)
def update_month_dep_plot(selected_year, selected_dep):
    # Check if regions are selected; if not, display for all regions.
    if not selected_dep:
        selected_dep = df['nom_departement'].unique()

    filtered_df = df[(df['year'] == selected_year) & (df['nom_departement'].isin(selected_dep))]
    grouped_df = filtered_df.groupby(['nom_departement',"month"])['Valeur fonciere'].mean().reset_index()
    fig_month_dep_updated = px.line(grouped_df, x="month", y="Valeur fonciere", category_orders={'month': order_month}, color='nom_departement')
    
    fig_month_dep_updated.update_layout(
        legend_title="",
        xaxis_title="Mois",
        paper_bgcolor="rgb(34,34,34)",
        plot_bgcolor="rgb(34,34,34)",
        legend_font_color="white",
        coloraxis_showscale=False
    )
    fig_month_dep_updated.update_xaxes(type='category',gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
    fig_month_dep_updated.update_yaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
    
    return fig_month_dep_updated

# FONCTION: Selon la valeur de(s) département(s) sélectionnées dans les dropdowns list, on actualise notre line plot annuelle 
@app.callback(
    Output('year-dep-plot', 'figure'),  
    Input('departements-dropdown', 'value')  
)
def update_year_plot_dep(selected_dep):
    if not selected_dep:
        selected_dep = df['nom_departement'].unique()

    filtered_df = df[df['nom_departement'].isin(selected_dep)]
    grouped_df = filtered_df.groupby(['year', 'nom_departement'])['Valeur fonciere'].mean().reset_index()
    fig_year_dep_updated = px.line(grouped_df, x="year", y="Valeur fonciere", color='nom_departement')
    
    fig_year_dep_updated.update_layout(
        legend_title="",
        xaxis_title="Année",
        paper_bgcolor="rgb(34,34,34)",
        plot_bgcolor="rgb(34,34,34)",
        legend_font_color="white",
        coloraxis_showscale=False
    )
 
    fig_year_dep_updated.update_xaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
    fig_year_dep_updated.update_yaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
    
    return fig_year_dep_updated


# FONCTION: Selon la valeur de l'année sélectionnée dans la dropdowns list, on actualise notre map plot des régions 
@app.callback(
    Output('region-map-plot', 'figure'),  
    [Input('annee-dropdown', 'value')]
)
# Les modifications étant identiques aux lines plots, nous ne détaillerons pas plus les commentaires
def update_region_plot(selected_year):

    filtered_df = df[df['year'] == selected_year]
    filtered_df = filtered_df.groupby('nom_region')['Valeur fonciere'].mean().reset_index()
    filtered_df.columns = ['nom_region', 'Valeur fonciere']

    fig_region = px.choropleth(
    filtered_df,  
    geojson=regions_data,
    locations='nom_region',  
    color='Valeur fonciere',  
    color_continuous_scale='YlOrRd',
    featureidkey="properties.libgeo",  
    range_color=[100000, 350000]
    )
    fig_region.update_geos(
    center={"lat": 45.8, "lon": 5},  
    projection_scale=17, 
    visible=False 
    )
    fig_region.update_layout(
    autosize=False,
    width=600,
    height=600,
    paper_bgcolor="rgb(34,34,34)",
    geo_bgcolor="rgb(34,34,34)",
    coloraxis_showscale=False,
    margin={"r":0,"t":0,"l":0,"b":0}
    )
    fig_region.update_traces(marker_line=dict(color="rgb(34,34,34)", width=1))
    
    return fig_region

# FONCTION: Selon la valeur de l'année sélectionnée dans la dropdowns list, on actualise notre map plot des départements 
@app.callback(
    Output('departement-map-plot', 'figure'),  
    [Input('annee-dropdown', 'value')]
)
# Les modifications étant identiques aux lines plots, nous ne détaillerons pas plus les commentaires

def update_departement_plot(selected_year):
    filtered_df = df[df['year'] == selected_year]
    filtered_df = filtered_df.groupby('nom_departement')['Valeur fonciere'].mean().reset_index()
    filtered_df.columns = ['nom_departement', 'Valeur fonciere']

    fig_dep = px.choropleth(
    filtered_df,  
    geojson=dep_data,
    locations='nom_departement',  
    color='Valeur fonciere',  
    color_continuous_scale='YlOrRd',
    featureidkey="properties.libgeo",  
    range_color=[100000, 350000]
    )
    fig_dep.update_geos(
    center={"lat": 45.8, "lon": 5},  
    projection_scale=17,  
    visible=False 
    )
    fig_dep.update_layout(
    autosize=False,
    width=600,
    height=600,
    paper_bgcolor="rgb(34,34,34)",
    geo_bgcolor="rgb(34,34,34)",
    coloraxis_showscale=False,
    margin={"r":0,"t":0,"l":0,"b":0}
    )
    fig_dep.update_traces(marker_line=dict(color="rgb(34,34,34)", width=1))
    
    return fig_dep


# FONCTION: Selon la valeur de l'année et de département(s) sélectionnées dans les dropdowns list, on actualise nos kpis
@app.callback(
    Output('kpi2-value', 'children'),
    Output('evolution-dep-text', 'children'),  
    Output('kpi1-value', 'children'),
    Input('annee-dropdown', 'value'),
    Input('departements-dropdown', 'value')
)

def update_kpi_dep_content(selected_year, selected_dep):
    if not selected_dep:
        selected_dep = df['nom_departement'].unique()
    if not isinstance(selected_dep, list):
        selected_dep = [selected_dep]

    # On filtre notre dataframe
    filtered_df = df[(df['year'] == selected_year) & (df['nom_departement'].isin(selected_dep))]
    
    # On calcule la valeur foncière moyenne pour cette année et département(s) choisis
    kpi1_value = filtered_df["Valeur fonciere"].mean()

    # On compare ensuite notre kpi1 avec 2021 pour avoir l'évolution
    df_2021 = df[(df['year'] == "2021") & (df['nom_departement'].isin(selected_dep))]
    df_2021_value = df_2021["Valeur fonciere"].mean()

    # On calcule le pourcentage de différence   
    diff = ((df_2021_value - kpi1_value) / kpi1_value) * 100

    # Si le pourcentage de différence est supérieur à 0, on ajoute + sinon le chiffre sera dans tous les cas négatifs
    if diff > 0:
        diff_text = f"+{diff:.2f}%"
    else:
        diff_text = f"{diff:.2f}%"

    # On ajoute un texte qui indique l'année choisi pour voir l'évolution.
    updated_evolution_text = f"Evolution entre {selected_year} et 2021"

    return diff_text, updated_evolution_text, f"{kpi1_value:,.2f}€"

# FONCTION: Selon la valeur de l'année et de région(s) sélectionnées dans les dropdowns list, on actualise nos kpis
@app.callback(
    Output('kpi2-reg-value', 'children'), 
    Output('evolution-text', 'children'),
    Output('kpi1-reg-value', 'children'),
    Input('annee-dropdown', 'value'),  
    Input('region-dropdown', 'value') 
)

# La structure étant la même que précédemment, nous ne détaillerons pas les commentaires.
def update_kpi_region_content(selected_year, selected_region):

    if not selected_region:
        selected_region = df['nom_region'].unique()
    if not isinstance(selected_region, list):
        selected_region = [selected_region]

    filtered_df = df[(df['year'] == selected_year) & (df['nom_region'].isin(selected_region))]
    
    kpi1_value = filtered_df["Valeur fonciere"].mean()

    df_2021 = df[(df['year'] == "2021") & (df['nom_region'].isin(selected_region))]
    df_2021_value = df_2021["Valeur fonciere"].mean()

    diff = ((df_2021_value - kpi1_value) / kpi1_value) * 100

    if diff > 0:
        diff_text = f"+{diff:.2f}%"
    else:
        diff_text = f"{diff:.2f}%"

    updated_evolution_text = f"Evolution entre {selected_year} et 2021"

    return diff_text, updated_evolution_text, f"{kpi1_value:,.2f}€"


######### Prédiction

# FONCTION: A chaque fois que le bouton "Lancer la prédiction" est clické, notre fonction Prédiction2 est appelé pour réaliser la prédiction selon les inputs

@app.callback(
    Output('output-texte', 'children'),
    [Input('mon-bouton','n_clicks'),
     Input('tl', 'value'),
     Input('sr', 'value'),
     Input('nbpp', 'value'),
     Input('st', 'value'),
     Input('te', 'value'),
     Input('nom_departement', 'value')
]
)

def mettre_a_jour_output(n_clicks,  tl, sr, nbpp, st, te, nom_departement):
    
    ctx = dash.callback_context # Regarde le dernier bouton cliqué
    if not ctx.triggered: # Si bouton n'a pas été cliqué ou inputs en modifications, "en attente"
        return "En attente"
    else:
        button_id = [p["prop_id"] for p in dash.callback_context.triggered][0] # Sinon regarde le dernier bouton cliqué

    # Si c'est bien mon bouton, je réalise le préprocessing adéquat
    if button_id == 'mon-bouton.n_clicks':
        data = preproc( tl, sr, nbpp, st, te, nom_departement) # Ajout des variables supplémentaires
        res = pred(data) # Traitement selon la modalité puis prédiction
        return f"{res[0]:.2f} €" # On récupère la valeur du bien prédite.
    else:
        return "En attente"

if __name__ == '__main__':
    # On lance le serveur.
    app.run_server(debug=True)
