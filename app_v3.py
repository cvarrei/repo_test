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
import numpy as np
from sklearn.base import TransformerMixin

df=pd.read_csv("df_dash_dashboard.csv")

############### Nettoyage pour faciliter la représentation graphique
df["year"] = df["year"].astype(str)
df = df.replace('Î', 'I', regex=True)
df = df.replace('Ô', 'O', regex=True)
df = df.replace('ô', 'o', regex=True)
df= df.replace('é', 'e', regex=True)
df = df.replace('è', 'e', regex=True)
df = df.replace('û', 'u', regex=True)
df['month'] = pd.Categorical(df['month'], ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre'])
df.sort_values(['month'], inplace=True)
df.loc[df["nom_region"] == "Nouvelle-Aquitaine", "nom_region"] = "Nouvelle Aquitaine"
df.loc[df["nom_region"] == "Grand Est", "nom_region"] = "Grand-Est"

################# Maps Chloropeths
with open("regions.json", "r") as file:
    regions_data = json.load(file)

with open("departement.json", "r") as file:
    dep_data = json.load(file)

# Create the choropleth map
fig_region = px.choropleth(
    df,  # replace df with your DataFrame
    geojson=regions_data,
    locations='nom_region',  # replace 'id' with the column name containing the regions' ids
    color='Valeur fonciere',  # replace 'value' with the column name containing the values you want to plot
    color_continuous_scale='YlOrRd',
    featureidkey="properties.libgeo",  # replace 'properties.id' with the path to the ids in the geojson
    range_color=[100000, 250000]
)
fig_region.update_geos(
    center={"lat": 45.8, "lon": 1.888334},  # Coordinates of France's centroid
    projection_scale=17,  # Adjust the scale to fit France
    visible=False  # Hide the base map
)
fig_region.update_layout(
    paper_bgcolor="rgb(34,34,34)",
    geo_bgcolor="rgb(34,34,34)",
    coloraxis_showscale=False,
    margin={"r":0,"t":0,"l":0,"b":0}
)
fig_region.update_traces(marker_line=dict(color="rgb(34,34,34)", width=1))


fig_dep = px.choropleth(
    df,  # replace df with your DataFrame
    geojson=dep_data,
    locations='nom_departement',  # replace 'id' with the column name containing the regions' ids
    color='Valeur fonciere',  # replace 'value' with the column name containing the values you want to plot
    color_continuous_scale='YlOrRd',
    featureidkey="properties.libgeo",  # replace 'properties.id' with the path to the ids in the geojson
    range_color=[30000, 300000]
)
fig_dep.update_geos(
    center={"lat": 45.8, "lon": 1.888334},  # Coordinates of France's centroid
    projection_scale=17,  # Adjust the scale to fit France
    visible=False  # Hide the base map
)
fig_dep.update_layout(
    paper_bgcolor="rgb(34,34,34)",
    geo_bgcolor="rgb(34,34,34)",
    coloraxis_showscale=False,
    margin={"r":0,"t":0,"l":0,"b":0}
)
fig_dep.update_traces(marker_line=dict(color="rgb(34,34,34)", width=1))

################### Line plots regions 
order_month = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
fig_month = px.line(df, x="month", y="Valeur fonciere", category_orders={'month': order_month}, color='nom_region')
fig_month.update_layout(
        legend_title="",
        xaxis_title="Mois",
        paper_bgcolor="rgb(34,34,34)",
        plot_bgcolor="rgb(34,34,34)",
        legend_font_color="white",
        coloraxis_showscale=False
    )
fig_month.update_xaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))
fig_month.update_yaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white"))

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

################### Line plots departements 
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


######## Dashboard
title_style = {
    'backgroundColor': 'linear-gradient(to bottom, rgb(155, 40, 20), tomato)',  # Fire brick color
    'color': 'white',  # Text color
    'padding': '10px',  # Padding around the text
    'textAlign': 'center',  # Center the text
    'marginBottom': '20px'  # Margin at the bottom to separate it from other content
}

regions_layout = html.Div([dbc.Row([   
                    dbc.Col(dcc.Dropdown(
                            id="annee-dropdown",
                            options=[{'label': str(annee), 'value': annee} for annee in sorted(df['year'].unique())],
                            value="2018",
                        ), width=3),
                    
                    dbc.Col(dcc.Dropdown(
                            id="region-dropdown",
                            options=[{'label': region, 'value': region} for region in sorted(df['nom_region'].unique())],
                            multi=True
                        ),width=3) 
                    ]),
    
    dbc.Row(
                [   
                    dbc.Col([
                        dbc.Row([
                            dcc.Graph(id='year-plot', figure=fig_year, style={"height": "50vh"})
                        ]),
                        dbc.Row([
                            dcc.Graph(id='month-plot', figure=fig_month, style={"height": "50vh"})
                        ])
                    ]),
                    dbc.Col([
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
            dbc.Row([
                dcc.Graph(id='region-map-plot',figure=fig_region, style={"height": "100vh"})
            ])
        ], width=6)
                ]
            )
])

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
            ])
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
                dcc.Graph(id='departement-map-plot',figure=fig_dep, style={"height": "100vh"})
            ])
        ], width=6)
    ])
])




######### Interface Accueil
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

# Interface du dashboard
dashboard_layout = html.Div([
    html.H2("Evolution des valeurs foncières", className="gradient-title"),

    dbc.Row([
        dbc.Col(dbc.Button("Régions", id="btn-regions", n_clicks=0, className="custom-button"), width="auto"),
        dbc.Col(dbc.Button("Départements", id="btn-departements", n_clicks=0, className="custom-button"), width="auto")
    ], justify="center", className="g-2 mb-4"),  # Added `no_gutters` to remove space between columns

    html.Div(id="contant-container") 
])

######### Interface Prédiction

options_type_bien = [
    {'label': 'Maison', 'value': 'Maison'},
    {'label': 'Appartement', 'value': 'Appartement'},
    {'label': 'Dépendance', 'value': 'Dépendance'}
]

options_exterieur = [
    {'label': 'y', 'value': 'y'},
    {'label': 'n', 'value': 'n'}
]


prediction_layout = html.Div([
    html.H2('Prédisez le prix de votre bien', className="gradient-title"),
    dbc.Row([   # Start of the row containing two columns
        dbc.Col([
            dbc.Row([html.P('Type de bien'),
                     dcc.Dropdown(id='tl',
                                  options=options_type_bien,
                                  value='Maison'
                                  )], style={"padding-left": "10px"}),
            dbc.Row([html.P('Surface habitable du bien'), dcc.Input(id='sr', type='number', value=0, style={"margin-left": "10px"})], style={"padding-left": "10px"}),
            dbc.Row([html.P('Nombre de pieces principales'), dcc.Input(id='nbpp', type='number', value=0, style={"margin-left": "10px"})], style={"padding-left": "10px"}),
            dbc.Row([html.P('Surface du terrain'), dcc.Input(id='st', type='number', value=0, style={"margin-left": "10px"})], style={"padding-left": "10px"}),
            dbc.Row([html.P('Présence d\'un extérieur'),
                     dcc.Dropdown(id='te',
                                  options=options_exterieur,
                                  value='n'
                                  )], style={"padding-left": "10px"}),
            dbc.Row([html.P('Nom du departement'),
                     dcc.Dropdown(id='nom_departement',
                                  options=[{'label': department, 'value': department} for department in sorted(df['nom_departement'].unique())],
                                  value='Ain'
                                  )], style={"padding-left": "10px", "margin-bottom": "20px"}),
            dbc.Row(
                html.Button('Lancement de la prediction', id='mon-bouton', n_clicks=0, className="custom-button", style={"width": "auto", "margin": "0 auto"}), 
                style={"display": "flex", "justify-content": "center", "padding-top": "10px"}
            )
        ], width=6),   # End of the first column with width 6
        dbc.Col([dbc.Row([html.P(id="annonce-pred", children="La valeur estimé du bien est de ")]),
                 dbc.Row([html.P(id='output-texte', children="En attente")])   # Second column with width 6
    ], width=6)  # End of the row
    ])
])


######### Menu Latéral
sidebar = html.Div([
    dbc.Nav(
        [   
            html.Img(src="/assets/logo.png", height="200px"),
            html.Div("SARDE IMMO", className="sidebar-text"),
            html.Div("AGENCY", className="sidebar-text2"),
            dbc.NavLink("Accueil", href="/", active="exact"),
            dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
            dbc.NavLink("Prediction", href="/prediction", active="exact")
        ], 
        vertical=True,
        pills=True, 
        fill=True,
        className="rounded-navbar"
        ),
    ], style={"width":"15%", "position":"fixed", "height": "100%", "background-color": "#FAFAFA"}
)


####### Contenu de la page active
content = html.Div(id="page-content", style={"margin-left": "15%"})


######## Application
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
server=app.server

# Définir la mise en page de l'interface utilisateur
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

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

@app.callback(
    Output('month-plot', 'figure'),  # id of the month plot Graph component and property to update
    Input('annee-dropdown', 'value'),  # id of the year dropdown and property to get
    Input('region-dropdown', 'value')  # id of the region dropdown and property to get
)
def update_month_plot(selected_year, selected_regions):
    # Check if regions are selected; if not, display for all regions.
    if not selected_regions:
        selected_regions = df['nom_region'].unique()

    filtered_df = df[(df['year'] == selected_year) & (df['nom_region'].isin(selected_regions))]
    grouped_df = filtered_df.groupby(['nom_region',"month"])['Valeur fonciere'].mean().reset_index()
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
    
    return fig_month_updated

@app.callback(
    Output('year-plot', 'figure'),  # id of the year plot Graph component and property to update
    Input('region-dropdown', 'value')  # id of the region dropdown and property to get
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

@app.callback(
    Output('year-dep-plot', 'figure'),  # id of the year plot Graph component and property to update
    Input('departements-dropdown', 'value')  # id of the region dropdown and property to get
)
def update_year_plot_dep(selected_dep):
    # Check if regions are selected; if not, display for all regions.
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

@app.callback(
    Output('region-map-plot', 'figure'),  # Assuming the id of your dcc.Graph component for the region is 'region-plot'
    [Input('annee-dropdown', 'value')]
)
def update_region_plot(selected_year):
    # Filter the dataframe based on the selected year
    filtered_df = df[df['year'] == selected_year]
    filtered_df = filtered_df.groupby('nom_region')['Valeur fonciere'].mean().reset_index()
    filtered_df.columns = ['nom_region', 'Valeur fonciere']

    # Create the updated figure
    fig_region = px.choropleth(
    filtered_df,  # replace df with your DataFrame
    geojson=regions_data,
    locations='nom_region',  # replace 'id' with the column name containing the regions' ids
    color='Valeur fonciere',  # replace 'value' with the column name containing the values you want to plot
    color_continuous_scale='YlOrRd',
    featureidkey="properties.libgeo",  # replace 'properties.id' with the path to the ids in the geojson
    range_color=[100000, 350000]
    )
    fig_region.update_geos(
    center={"lat": 45.8, "lon": 1.888334},  # Coordinates of France's centroid
    projection_scale=17,  # Adjust the scale to fit France
    visible=False  # Hide the base map
    )
    fig_region.update_layout(
    paper_bgcolor="rgb(34,34,34)",
    geo_bgcolor="rgb(34,34,34)",
    coloraxis_showscale=False,
    margin={"r":0,"t":0,"l":0,"b":0}
    )
    fig_region.update_traces(marker_line=dict(color="rgb(34,34,34)", width=1))
    
    return fig_region

@app.callback(
    Output('departement-map-plot', 'figure'),  # Assuming the id of your dcc.Graph component for the region is 'region-plot'
    [Input('annee-dropdown', 'value')]
)
def update_departement_plot(selected_year):
    # Filter the dataframe based on the selected year
    filtered_df = df[df['year'] == selected_year]
    filtered_df = filtered_df.groupby('nom_departement')['Valeur fonciere'].mean().reset_index()
    filtered_df.columns = ['nom_departement', 'Valeur fonciere']

    # Create the updated figure
    fig_dep = px.choropleth(
    filtered_df,  # replace df with your DataFrame
    geojson=dep_data,
    locations='nom_departement',  # replace 'id' with the column name containing the regions' ids
    color='Valeur fonciere',  # replace 'value' with the column name containing the values you want to plot
    color_continuous_scale='YlOrRd',
    featureidkey="properties.libgeo",  # replace 'properties.id' with the path to the ids in the geojson
    range_color=[100000, 350000]
    )
    fig_dep.update_geos(
    center={"lat": 45.8, "lon": 1.888334},  # Coordinates of France's centroid
    projection_scale=17,  # Adjust the scale to fit France
    visible=False  # Hide the base map
    )
    fig_dep.update_layout(
    paper_bgcolor="rgb(34,34,34)",
    geo_bgcolor="rgb(34,34,34)",
    coloraxis_showscale=False,
    margin={"r":0,"t":0,"l":0,"b":0}
    )
    fig_dep.update_traces(marker_line=dict(color="rgb(34,34,34)", width=1))
    
    return fig_dep

@app.callback(
    Output('kpi2-value', 'children'),
    Output('evolution-dep-text', 'children'),  
    Output('kpi1-value', 'children'),
    Input('annee-dropdown', 'value'),
    Input('departements-dropdown', 'value')
)

def update_kpi_dep_content(selected_year, selected_dep):

    # Check if regions are selected; if not, display for all regions.
    if not selected_dep:
        selected_dep = df['nom_departement'].unique()
    # Ensure selected_region is a list to handle cases where single values are selected
    if not isinstance(selected_dep, list):
        selected_dep = [selected_dep]

    filtered_df = df[(df['year'] == selected_year) & (df['nom_departement'].isin(selected_dep))]
    
    # Compute a specific scalar value, for instance, the mean
    kpi1_value = filtered_df["Valeur fonciere"].mean()

    df_2021 = df[(df['year'] == "2021") & (df['nom_departement'].isin(selected_dep))]
    df_2021_value = df_2021["Valeur fonciere"].mean()

    # Make sure to handle NaN or None values here (if any)   
    diff = ((df_2021_value - kpi1_value) / kpi1_value) * 100

    if diff > 0:
        diff_text = f"+{diff:.2f}%"
    else:
        diff_text = f"{diff:.2f}%"

    updated_evolution_text = f"Evolution entre {selected_year} et 2021"

    return diff_text, updated_evolution_text, f"{kpi1_value:,.2f}€"


@app.callback(
    Output('kpi2-reg-value', 'children'), 
    Output('evolution-text', 'children'),
    Output('kpi1-reg-value', 'children'),
    Input('annee-dropdown', 'value'),  # id of the year dropdown and property to get
    Input('region-dropdown', 'value')  # id of the region dropdown and property to get
)

def update_kpi_region_content(selected_year, selected_region):

    # Check if regions are selected; if not, display for all regions.
    if not selected_region:
        selected_region = df['nom_region'].unique()
    # Ensure selected_region is a list to handle cases where single values are selected
    if not isinstance(selected_region, list):
        selected_region = [selected_region]

    filtered_df = df[(df['year'] == selected_year) & (df['nom_region'].isin(selected_region))]
    
    # Compute a specific scalar value, for instance, the mean
    kpi1_value = filtered_df["Valeur fonciere"].mean()

    df_2021 = df[(df['year'] == "2021") & (df['nom_region'].isin(selected_region))]
    df_2021_value = df_2021["Valeur fonciere"].mean()

    # Make sure to handle NaN or None values here (if any)   
    diff = ((df_2021_value - kpi1_value) / kpi1_value) * 100

    if diff > 0:
        diff_text = f"+{diff:.2f}%"
    else:
        diff_text = f"{diff:.2f}%"

    updated_evolution_text = f"Evolution entre {selected_year} et 2021"

    return diff_text, updated_evolution_text, f"{kpi1_value:,.2f}€"


@app.callback(
    Output("contant-container", "children"),
    [Input("btn-regions", "n_clicks"),
    Input("btn-departements", "n_clicks")]
)
def switch_layout(btn1, btn2):
    change_dash = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "btn-regions" in change_dash:
        return regions_layout
    elif "btn-departements" in change_dash:
        return departments_layout
    else:
        return regions_layout

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
    # Check which input triggered the callback
    ctx = dash.callback_context
    if not ctx.triggered:
        return "En attente"
    else:
        button_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

    if button_id == 'mon-bouton.n_clicks':
        data = preproc( tl, sr, nbpp, st, te, nom_departement)
        res = pred(data)
        return f"{res[0]:.2f} €"
    else:
        return "En attente"

if __name__ == '__main__':
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
    app.run_server(debug=True)
