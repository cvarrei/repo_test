import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import json

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

# Create the choropleth map
fig_region = px.choropleth(
    df_dashboard,  # replace df with your DataFrame
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

# Show the map
fig_region.show()

app = dash.Dash(__name__)
server=app.server

# Définir la mise en page de l'interface utilisateur
app.layout = html.Div([
    html.H1("Interface pour la valeur foncière"),
    
    # Sélectionnez les années
    dcc.Dropdown(
        id="annee-dropdown",
        options=[{'label': str(annee), 'value': annee} for annee in df['year'].unique()],
        multi=True
    ),
    
    # Sélectionnez les régions
    dcc.Dropdown(
        id="region-dropdown",
        options=[{'label': region, 'value': region} for region in df['nom_region'].unique()],
        multi=True
    ),
    
    # Afficher la valeur foncière
    html.Div(id="valeur-fonciere-output")

     dcc.Graph(
        id='example-graph',
        figure=fig_region
    )
    
])

# Créez une fonction de rappel pour mettre à jour la valeur foncière en fonction des filtres sélectionnés
@app.callback(
    Output("valeur-fonciere-output", "children"),
    [Input("annee-dropdown", "value"), Input("region-dropdown", "value")]
)
def update_valeur_fonciere(selected_annees, selected_regions):
    filtered_data = df[(df["year"].isin(selected_annees)) & (df["nom_region"].isin(selected_regions))]
    valeur_fonciere = filtered_data["Valeur fonciere"].mean()  # Vous pouvez utiliser une autre méthode de consolidation si nécessaire
    return f"Valeur foncière totale : {valeur_fonciere}"



if __name__ == '__main__':
    app.run_server(debug=True)

