import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import json

df=pd.read_csv("df_dash_dashboard.csv")


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
server=app.server

################CARTE 
df=pd.read_csv("df_dash_dashboard.csv")

df = df.replace('Î', 'I', regex=True)
df = df.replace('Ô', 'O', regex=True)
df = df.replace('ô', 'o', regex=True)
df= df.replace('é', 'e', regex=True)
df = df.replace('è', 'e', regex=True)

df.loc[df["nom_region"] == "Nouvelle-Aquitaine", "nom_region"] = "Nouvelle Aquitaine"
df.loc[df["nom_region"] == "Grand Est", "nom_region"] = "Grand-Est"

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
    color_continuous_scale='Inferno',
    featureidkey="properties.libgeo",  # replace 'properties.id' with the path to the ids in the geojson
    range_color=[100000, 250000]
)

# Update the geos layout to focus on France
fig_region.update_geos(
    center={"lat": 46.603354, "lon": 1.888334},  # Coordinates of France's centroid
    projection_scale=15,  # Adjust the scale to fit France
    visible=False  # Hide the base map
)

# Update the layout
fig_region.update_layout(
    title="Choropleth Map of France",
    margin={"r":0,"t":40,"l":0,"b":0}
)

# Create the choropleth map
fig_dep = px.choropleth(
    df,  # replace df with your DataFrame
    geojson=dep_data,
    locations='nom_departement',  # replace 'id' with the column name containing the regions' ids
    color='Valeur fonciere',  # replace 'value' with the column name containing the values you want to plot
    color_continuous_scale='Inferno',
    featureidkey="properties.libgeo",  # replace 'properties.id' with the path to the ids in the geojson
    range_color=[30000, 300000]
)

# Update the geos layout to focus on France
fig_dep.update_geos(
    center={"lat": 46.603354, "lon": 1.888334},  # Coordinates of France's centroid
    projection_scale=15,  # Adjust the scale to fit France
    visible=False  # Hide the base map
)

# Update the layout
fig_dep.update_layout(
    
    title="Choropleth Map of France",
    margin={"r":0,"t":40,"l":0,"b":0}
)


# Définir la mise en page de l'interface utilisateur
# Définir la mise en page de l'interface utilisateur
app.layout = html.Div([
    # Conteneur principal
    html.Div(className="container", children=[
        # Menu à gauche
        html.Div(className="menu", children=[
            dcc.Tabs(id="tabs", value='departements', children=[
                dcc.Tab(label='Départements', value='departements'),
                dcc.Tab(label='Régions', value='regions'),
            ]),
        ],style={'float' : 'left'}),
        
        # Contenu
        html.Div(className="content", children=[
            html.H1("Interface pour la valeur foncière"),
            
            # Sélectionnez les années
            dcc.Dropdown(
                id="annee-dropdown",
                options=[{'label': str(annee), 'value': annee} for annee in df['year'].unique()],
                multi=True
            ),

            #Selectionne departement
            dcc.Dropdown(
                id="departement-dropdown",
                options=[{'label': departement, 'value': departement} for departement in df['nom_departement'].unique()],
                multi=True # Affiché par défaut
            ),
            
            #Seleectionne regions
            dcc.Dropdown(
                id="region-dropdown",
                options=[{'label': region, 'value': region} for region in df['nom_region'].unique()],
                multi=True # Masqué par défaut
            ),
            
            # Contenu des onglets
            html.Div(id="tabs-content"),

            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=fig_region), width=6),
                    dbc.Col(dcc.Graph(figure=fig_dep), width=6),
                ]
            )

        ])
    ])
])

# Créez une fonction de rappel pour mettre à jour le contenu des onglets
@app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value"),
    Input("annee-dropdown", "value"),
    Input("region-dropdown", "value"),
    Input("departement-dropdown", "value")
)

def update_tab_content(selected_tab, selected_annees, selected_regions, selected_departements):
    
    if selected_tab == 'departements':
        filtered_data = df[(df["year"].isin(selected_annees)) & (df["nom_departement"].isin(selected_departements))]
        mean_valeur_fonciere = filtered_data["Valeur fonciere"].mean()
        mean_valeur_fonciere = "{:,.2f}".format(mean_valeur_fonciere)
        count_valeur_fonciere = filtered_data["Valeur fonciere"].count()
        return [html.H2(f"Valeur foncière moyenne : {mean_valeur_fonciere} €"), html.H2(f"Nombre de ventes : {count_valeur_fonciere}")]

    elif selected_tab == 'regions':
        filtered_data = df[(df["year"].isin(selected_annees)) & (df["nom_region"].isin(selected_regions))]
        mean_valeur_fonciere = filtered_data["Valeur fonciere"].mean()
        mean_valeur_fonciere = "{:,.2f}".format(mean_valeur_fonciere)
        count_valeur_fonciere = filtered_data["Valeur fonciere"].count()
        return [html.H2(f"Valeur foncière moyenne : {mean_valeur_fonciere} €"), html.H2(f"Nombre de ventes : {count_valeur_fonciere}")]

    
if __name__ == '__main__':
    app.run_server(debug=True)
