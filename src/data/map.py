import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests
import sqlite3

app = dash.Dash(__name__)

# Define external_stylesheets
external_stylesheets = ['styles.css']

# Pass external_stylesheets to the dash.Dash instance
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Earthquake Monitor"),
    
    # Input fields for earthquake data
    dcc.Input(id='latitude-input', type='number', placeholder='Latitude'),
    dcc.Input(id='longitude-input', type='number', placeholder='Longitude'),
    dcc.Input(id='date-time-input', type='text', placeholder='Date and Time'),
    dcc.Input(id='magnitude-input', type='number', placeholder='Magnitude'),
    dcc.Input(id='intensity-input', type='text', placeholder='Intensity'),
    
    html.Button('Add Earthquake', id='add-button', n_clicks=0),
    
    dcc.Graph(id='earthquake-map')
])

manually_added_earthquakes = []

# Create a function to handle database operations
def perform_database_operation(query, *args):
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    conn.close()

@app.callback(
    Output('earthquake-map', 'figure'),
    [Input('add-button', 'n_clicks')],
    [State('latitude-input', 'value'),
     State('longitude-input', 'value'),
     State('date-time-input', 'value'),
     State('magnitude-input', 'value'),
     State('intensity-input', 'value')]
)
def update_map(n_clicks, latitude, longitude, date_time, magnitude, intensity):
    if n_clicks > 0 and latitude is not None and longitude is not None and magnitude is not None:
        new_earthquake = {
            'latitude': latitude,
            'longitude': longitude,
            'date_time': date_time,
            'magnitude': magnitude,
            'intensity': intensity,
            'visible': True  # Set the visibility property for blinking animation
        }
        
        perform_database_operation('''
            INSERT INTO earthquakes (latitude, longitude, date_time, magnitude, intensity)
            VALUES (?, ?, ?, ?, ?)
        ''', latitude, longitude, date_time, magnitude, intensity)
        
        manually_added_earthquakes.append(new_earthquake)
    
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    response = requests.get(url)
    data = response.json()

    features = data['features']
    
    if magnitude is not None:
        filtered_features = [feature for feature in features if 'mag' in feature['properties'] and feature['properties']['mag'] >= magnitude]
    else:
        filtered_features = []
    
    latitudes = [feature['geometry']['coordinates'][1] for feature in filtered_features]
    longitudes = [feature['geometry']['coordinates'][0] for feature in filtered_features]

    figure = {
        'data': [
            {
                'type': 'scattermapbox',
                'lat': latitudes,
                'lon': longitudes,
                'mode': 'markers',
                'marker': {'size': 10, 'color': 'red'}
            },
            {
                'type': 'scattermapbox',
                'lat': [quake['latitude'] for quake in manually_added_earthquakes],
                'lon': [quake['longitude'] for quake in manually_added_earthquakes],
                'mode': 'markers',
                'marker': {
                    'size': [20 if quake['visible'] else 0 for quake in manually_added_earthquakes],  # Increase size
                    'color': 'red',
                    'symbol': 'circle-open-dot blinking',
                    'opacity': 1,
                }
            }
        ],
        'layout': {
            'mapbox': {
                'accesstoken': 'pk.eyJ1IjoicHJvdGVsZXJvbiIsImEiOiJjbGxmaXZpMjkwNDA5M2VtcHFmMTgyeWFzIn0.uNmehPkqQ2Q-YzYOJWCZzQ',
                'center': {'lat': 49.0, 'lon': 43.5},
                'zoom': 6,
            },
            'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0},
        }
    }

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
