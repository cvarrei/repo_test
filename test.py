from dash import Dash, html

app = Dash(__name__)
server=app.server

app.layout = html.Div([
    html.Div(children='Hello World Bonjour')
])

if __name__ == '__main__':
    app.run_server(debug=True)
