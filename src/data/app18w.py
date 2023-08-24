import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Load the data
file_paths = {
    "AMAS23_WAT": "C:/Users/THOM/Desktop/myflaskap/AMAS23_WAT.csv",                            
    "ARTA23_WAT": "C:/Users/THOM/Desktop/myflaskap/ARTA23_WAT.csv",
    "ASHO23_WAT": "C:/Users/THOM/Desktop/myflaskap/ASHO23_WAT.csv",
    "AZAT23_WAT": "C:/Users/THOM/Desktop/myflaskap/AZAT23_WAT.csv",
    "DZOR23_WAT": "C:/Users/THOM/Desktop/myflaskap/DZOR23_WAT.csv",
    "EKHG23_WAT": "C:/Users/THOM/Desktop/myflaskap/EKHG23_WAT.csv",
    "GORS23_WAT": "C:/Users/THOM/Desktop/myflaskap/GORS23_WAT.csv",
    "IJEV23_WAT": "C:/Users/THOM/Desktop/myflaskap/IJEV23_WAT.csv",
    "NOEM23_WAT": "C:/Users/THOM/Desktop/myflaskap/NOEM23_WAT.csv",
    "SHIR23_WAT": "C:/Users/THOM/Desktop/myflaskap/SHIR23_WAT.csv",
    "KARC23_WAT": "C:/Users/THOM/Desktop/myflaskap/KARC23_WAT.csv",
    "SEVN23_WAT": "C:/Users/THOM/Desktop/myflaskap/SEVN23_WAT.csv",
    "METS23_WAT": "C:/Users/THOM/Desktop/myflaskap/METS23_WAT.csv",
    "KUCH23_WAT": "C:/Users/THOM/Desktop/myflaskap/KUCH23_WAT.csv"
}

dataframes = {name: pd.read_csv(file_path) for name, file_path in file_paths.items()}

# Modify the labels by removing the "_WAT" or other suffixes
cleaned_names = {original: original.split('_')[0] for original in dataframes.keys()}

# Compute the correlation matrix
correlation_data = []
for name1, df1 in dataframes.items():
    row_data = []
    for name2, df2 in dataframes.items():
        correlation = df1['value'].corr(df2['value'])
        row_data.append(correlation)
    correlation_data.append(row_data)

correlation_matrix = pd.DataFrame(correlation_data, columns=dataframes.keys(), index=dataframes.keys())
correlation_matrix.columns = [cleaned_names[col] for col in correlation_matrix.columns]
correlation_matrix.index = [cleaned_names[idx] for idx in correlation_matrix.index]

# Create the heatmap
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=.5, vmin=-1, vmax=1, cbar_kws={'label': 'Correlation Coefficient'}, ax=ax)
ax.set_title('Correlation Matrix of 2023 Underground Water Levels', pad=20)
ax.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True, pad=5)
plt.xticks(rotation=0, ha='center')

plt.tight_layout()

# Convert the plot to an image that can be displayed in Dash
buf = BytesIO()
plt.savefig(buf, format="png")
data = base64.b64encode(buf.getbuffer()).decode("utf8")

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Water Level Correlation'

# Define the app layout with Bootstrap for responsiveness
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Correlation Matrix of 2023 Underground Water Levels", className="text-center"), width=12)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(html.Img(src="data:image/png;base64,{}".format(data)), width=12, lg=10, xl=8, className="mx-auto")
    ])
], fluid=True)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
