import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

df=pd.read_csv("df_dash_dashboard.csv")


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

