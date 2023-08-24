import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os
import pandas as pd

# Define the path where CSV files are located
path_to_csvs = "C:/Users/THOM/Desktop/myflaskap/"

# Function to get all CSV files with "23" in their names from the specified path
def list_csv_files(path):
    all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.csv')]
    detected_files = [file for file in all_files if '23' in file]
    print("Detected Files:", detected_files)
    return detected_files

# Start the app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Select CSV File"),
    dcc.Dropdown(
        id='dropdown-files',
        options=[{'label': file, 'value': file} for file in list_csv_files(path_to_csvs)],
        value=list_csv_files(path_to_csvs)[0]  # Default value is the first file in the list
    ),
    html.Div(id='output-data')
])

# Define callback to update the output div based on selected file
@app.callback(Output('output-data', 'children'),
              [Input('dropdown-files', 'value')])
def update_output(selected_file):
    df = pd.read_csv(os.path.join(path_to_csvs, selected_file))
    
    # Convert to datetime and sort
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['hour'])
    df_sorted = df.sort_values(by='datetime', ascending=False)
    
    # Extract latest information
    latest_entry = df_sorted.iloc[0]
    latest_date, latest_hour, latest_value = latest_entry['date'], latest_entry['hour'], latest_entry['value']

    return html.Div([
        html.H5(f"Latest Data for {selected_file}:"),
        html.P(f"Date: {latest_date}"),
        html.P(f"Hour: {latest_hour}"),
        html.P(f"Value: {latest_value}")
    ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
