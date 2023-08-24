import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import os
import pandas as pd

# Define the path where CSV files are located
path_to_csvs = "C:/Users/THOM/Desktop/myflaskap/"

# Function to get all CSV files with "23" in their names from the specified path
def list_csv_files(path):
    all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.csv')]
    return [file for file in all_files if '23' in file]

# Extract the latest date and value from a given CSV file
def get_latest_data(file):
    df = pd.read_csv(os.path.join(path_to_csvs, file))
    
    # Convert to datetime and sort
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['hour'])
    df_sorted = df.sort_values(by='datetime', ascending=False)
    
    # Extract latest information
    latest_entry = df_sorted.iloc[0]
    return latest_entry['date'], latest_entry['hour'], latest_entry['value']

# Start the app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Latest Data for '23' CSV Files"),
    html.Div(id='output-data-wat'),
    html.Div(id='output-data-rad'),
    html.Div(id='output-data-mag')
])

# Upon loading, the app will generate the tables with latest data
@app.callback(
    [Output('output-data-wat', 'children'),
     Output('output-data-rad', 'children'),
     Output('output-data-mag', 'children')],
    [Input('output-data-wat', 'id')]  # Dummy input to ensure callback runs on load
)
def generate_tables(dummy):
    # Extract data from all files and sort by type
    data_wat, data_rad, data_mag = [], [], []
    for file in list_csv_files(path_to_csvs):
        date, hour, value = get_latest_data(file)
        if "WAT" in file:
            data_wat.append({'File': file, 'Date': date, 'Hour': hour, 'Value': value})
        elif "RAD" in file:
            data_rad.append({'File': file, 'Date': date, 'Hour': hour, 'Value': value})
        elif "MAG" in file:
            data_mag.append({'File': file, 'Date': date, 'Hour': hour, 'Value': value})

    # Create tables
    table_wat = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in ['File', 'Date', 'Hour', 'Value']],
        data=data_wat,
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=10
    )

    table_rad = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in ['File', 'Date', 'Hour', 'Value']],
        data=data_rad,
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=10
    )

    table_mag = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in ['File', 'Date', 'Hour', 'Value']],
        data=data_mag,
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=10
    )

    return [html.H3("WAT Files"), table_wat], [html.H3("RAD Files"), table_rad], [html.H3("MAG Files"), table_mag]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
