import dash
from dash import callback
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import json

df=pd.read_csv("df_dash_dashboard.csv")

############### Nettoyage pour faciliter la représentation graphique

# On modifie les types de données.
df['month'] = pd.Categorical(df['month'], ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Decembre'])
df.sort_values(['month'], inplace=True)
df["year"] = df["year"].astype(str)

# On enlève tous les caractères spéciaux
df = df.replace('Î', 'I', regex=True)
df = df.replace('Ô', 'O', regex=True)
df = df.replace('ô', 'o', regex=True)
df= df.replace('é', 'e', regex=True)
df = df.replace('è', 'e', regex=True)
# On médifie les noms de régions pour harmoniser notre base de données agrégées avec notre document geojson.
df.loc[df["nom_region"] == "Nouvelle-Aquitaine", "nom_region"] = "Nouvelle Aquitaine"
df.loc[df["nom_region"] == "Grand Est", "nom_region"] = "Grand-Est"

################# Maps Chloropeths
with open("regions.json", "r") as file:
    regions_data = json.load(file)

with open("departement.json", "r") as file:
    dep_data = json.load(file)

# Création de la carte des régions
fig_region = px.choropleth(
    df,  # Données des valeurs foncières
    geojson=regions_data, # Documents Json pour créer la carte
    locations='nom_region',  
    color='Valeur fonciere',  # Valeur qui remplira chaque région
    color_continuous_scale='YlOrRd', # Palette de couleurs
    featureidkey="properties.libgeo",  # ids des régions dans le geojson
    range_color=[100000, 250000] # Rang de valeurs pour la carte
)
fig_region.update_geos(
    center={"lat": 45.8, "lon": 1.888334},  # Coordonnées où centrer la carte (centre de la france)
    projection_scale=17,  # On ajust el'échelle pour être proche du pays
    visible=False  # On enlève la carte du monde derrière
)
fig_region.update_layout(
    paper_bgcolor="rgb(34,34,34)", # On met le fond de la figure de la même couleur que le background de l'application
    geo_bgcolor="rgb(34,34,34)", # On met le fond de la figure de la même couleur que le background de l'application
    coloraxis_showscale=False, # On enlève la légende
    margin={"r":0,"t":40,"l":0,"b":0}
)
fig_region.update_traces(marker_line=dict(color="rgb(34,34,34)", width=1)) # On mets les tracés de la même couleur que le background de l'application


# On réalise ensuite les mêmes manipulations mais pour les départements
fig_dep = px.choropleth(
    df,  # replace df with your DataFrame
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
    paper_bgcolor="rgb(34,34,34)",
    geo_bgcolor="rgb(34,34,34)",
    coloraxis_showscale=False,
    margin={"r":0,"t":40,"l":0,"b":0}
)
fig_dep.update_traces(marker_line=dict(color="rgb(34,34,34)", width=1))



################### Line plots regions 

# On précise l'ordre des mois
order_month = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
fig_month = px.line(df, x="month", y="Valeur fonciere", category_orders={'month': order_month}, color='nom_region') # On crée le line plot pour afficher l'évolution mensuelle des régions
fig_month.update_layout(
        legend_title="", # On enlève le titre de la légende
        xaxis_title="Mois", # On assigne le nom de l'axe x
        paper_bgcolor="rgb(34,34,34)",  # On met le fond de la figure de la même couleur que le background de l'application
        plot_bgcolor="rgb(34,34,34)", # On met le fond de la figure de la même couleur que le background de l'application
        legend_font_color="white", # On change la couleur du texte de la légende
    )

fig_month.update_xaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white")) # On change la couleur du texte des axis et on enlève le grid
fig_month.update_yaxes(gridcolor='rgb(34,34,34)', title_font=dict(color="white"), tickfont=dict(color="white")) # On change la couleur du texte des axis et on enlève le grid

fig_year = px.line(df, x="year", y="Valeur fonciere", color='nom_region')  # On réalise la même manipulation mais pour l'évolution anuelle.
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

# On réalise la même manipulation pour les départements
order_month = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
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
    'backgroundColor': 'tomato', # Couleur du fond du titre
    'color': 'white',  # Couleur du texte du titre
    'padding': '10px',  # Padding autour du texte
    'textAlign': 'center',  # Center the text
    'marginBottom': '20px'  # Margin at the bottom to separate it from other content
}

regions_layout = html.Div([dbc.Row([   
                    dbc.Col(dcc.Dropdown(
                            id="annee-dropdown",
                            options=[{'label': str(annee), 'value': annee} for annee in df['year'].unique()]
                        ), width=3),
                    
                    dbc.Col(dcc.Dropdown(
                            id="region-dropdown",
                            options=[{'label': region, 'value': region} for region in df['nom_region'].unique()],
                            multi=True
                        ),width=3) 
                    ]),
    # Afficher la valeur foncière
    html.Div(id="valeur-fonciere-output"),
    
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
                    dbc.Col(dcc.Graph(figure=fig_region, style={"height": "100vh"}), width=6)
                ]
            )
])

departments_layout = html.Div([dbc.Row([   
                    dbc.Col(dcc.Dropdown(
                            id="annee-dropdown",
                            options=[{'label': str(annee), 'value': annee} for annee in df['year'].unique()]
                        ), width=3),
                    
                    dbc.Col(dcc.Dropdown(
                            id="departements-dropdown",
                            options=[{'label': region, 'value': region} for region in df['nom_departement'].unique()],
                            multi=True
                        ),width=3) 
                    ]),
    # Afficher la valeur foncière
    html.Div(id="valeur-fonciere-output"),
    
    dbc.Row(
                [   
                    dbc.Col([
                        dbc.Row([
                            dcc.Graph(id='year-plot', figure=fig_year_dep, style={"height": "50vh"})
                        ]),
                        dbc.Row([
                            dcc.Graph(id='month-plot', figure=fig_month_dep, style={"height": "50vh"})
                        ])
                    ]),
                    dbc.Col(dcc.Graph(figure=fig_dep, style={"height": "100vh"}), width=6)
                ]
            )
])

# Interface du dashboard
dashboard_layout = html.Div([
    html.H2("Interface pour la valeur foncière", style=title_style),

    dbc.Row([
    dbc.Col(dbc.Button("Régions", id="btn-regions", n_clicks=0, style={"background-color": "firebrick", "border-color": "firebrick"}), width={"size": 2, "offset": 4}),
    dbc.Col(dbc.Button("Départements", id="btn-departements", n_clicks=0, style={"background-color": "firebrick", "border-color": "firebrick"}), width=2)
    ], justify="center"),

    html.Div(id="contant-container") 
])

######### Interface Prédiction
prediction_layout = html.Div([
    html.H2("Example Page"),
    html.P("Lorem ipsum dolor sit amet")
])


######### Menu Latéral
sidebar = html.Div([
    dbc.Nav(
        [
            dbc.NavLink("Dashboard", href="/", active="exact"),
            dbc.NavLink("Prediction", href="/prediction", active="exact")
        ], 
        vertical=True,
        pills=True,
        ),
    ], style={"width":"15%", "position":"fixed", "height": "100%", "background-color": "lightgrey"}
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
    if pathname == "/prediction":
        return prediction_layout
    else:
        return dashboard_layout

@app.callback(
    Output('month-plot', 'figure'),  # id of the month plot Graph component and property to update
    Input('annee-dropdown', 'value'),  # id of the year dropdown and property to get
    Input('region-dropdown', 'value')  # id of the region dropdown and property to get
)
def update_month_plot(selected_year, selected_regions):
    # Check if regions are selected; if not, display for all regions.
    if not selected_regions:
        selected_regions = df['nom_region'].unique()
    if not selected_year:
        selected_year="2018"

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
    Output("contant-container", "children"),
    [Input("btn-regions", "n_clicks"),
    Input("btn-departements", "n_clicks")]
)

def switch_layout(btn1, btn2):
    change_dash = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "btn-regions" in change_dash:
        return regions_layout
    elif "btn_departements" in change_dash:
        return departments_layout
    else:
        return regions_layout
if __name__ == '__main__':
    app.run_server(debug=True)
