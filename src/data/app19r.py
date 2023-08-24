import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Load the radon data
radon_file_paths = {
    "PARA23_RAD": "C:/Users/THOM/Desktop/myflaskap/PARA23_RAD.csv", 
    "AZAT23_RAD": "C:/Users/THOM/Desktop/myflaskap/AZAT23_RAD.csv", 
    "ARTK23_RAD": "C:/Users/THOM/Desktop/myflaskap/ARTK23_RAD.csv", 
    "BAVR23_RAD": "C:/Users/THOM/Desktop/myflaskap/BAVR23_RAD.csv", 
    "VANA23_RAD": "C:/Users/THOM/Desktop/myflaskap/VANA23_RAD.csv", 
    "KOXB23_RAD": "C:/Users/THOM/Desktop/myflaskap/KOXB23_RAD.csv",
    "STEP23_RAD": "C:/Users/THOM/Desktop/myflaskap/STEP23_RAD.csv",
    "SHIR23_RAD": "C:/Users/THOM/Desktop/myflaskap/SHIR23_RAD.csv",
    "GORS23_RAD": "C:/Users/THOM/Desktop/myflaskap/GORS23_RAD.csv",
    "SISN23_RAD": "C:/Users/THOM/Desktop/myflaskap/SISN23_RAD.csv",
    "KADJ23_RAD": "C:/Users/THOM/Desktop/myflaskap/KADJ23_RAD.csv",
    "JERM23_RAD": "C:/Users/THOM/Desktop/myflaskap/JERM23_RAD.csv",
    "NOEM23_RAD": "C:/Users/THOM/Desktop/myflaskap/NOEM23_RAD.csv",
    "EKHG23_RAD": "C:/Users/THOM/Desktop/myflaskap/EKHG23_RAD.csv",
    "VARD23_RAD": "C:/Users/THOM/Desktop/myflaskap/VARD23_RAD.csv",
    "METS23_RAD": "C:/Users/THOM/Desktop/myflaskap/METS23_RAD.csv"
}

radon_dataframes = {name: pd.read_csv(file_path) for name, file_path in radon_file_paths.items()}

# Modify the labels by removing the "_RADON" or other suffixes
cleaned_radon_names = {original: original.split('_')[0] for original in radon_dataframes.keys()}

# Compute the correlation matrix for radon data
radon_correlation_data = []
for name1, radon_df1 in radon_dataframes.items():
    radon_row_data = []
    for name2, radon_df2 in radon_dataframes.items():
        radon_correlation = radon_df1['value'].corr(radon_df2['value'])
        radon_row_data.append(radon_correlation)
    radon_correlation_data.append(radon_row_data)

radon_correlation_matrix = pd.DataFrame(radon_correlation_data, columns=radon_dataframes.keys(), index=radon_dataframes.keys())
radon_correlation_matrix.columns = [cleaned_radon_names[col] for col in radon_correlation_matrix.columns]
radon_correlation_matrix.index = [cleaned_radon_names[idx] for idx in radon_correlation_matrix.index]

# Create the heatmap for radon data
radon_fig, radon_ax = plt.subplots(figsize=(12, 10))
sns.heatmap(radon_correlation_matrix, annot=True, cmap="coolwarm", linewidths=.5, vmin=-1, vmax=1, cbar_kws={'label': 'Correlation Coefficient'}, ax=radon_ax)
radon_ax.set_title('Correlation Matrix of 2023 Radon Levels', pad=25)
radon_ax.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True, pad=5)
plt.xticks(rotation=0, ha='center')

plt.tight_layout()

# Convert the radon plot to an image for Dash
radon_buf = BytesIO()
radon_fig.savefig(radon_buf, format="png")
radon_data = base64.b64encode(radon_buf.getbuffer()).decode("utf8")

# Initialize the Dash app for radon data
radon_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
radon_app.title = 'Correlation Matrix of 2023 Radon Levels'

# Define the radon app layout with Bootstrap for responsiveness
radon_app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Correlation Matrix of 2023 Radon Levels", className="text-center"), width=12)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(html.Img(src="data:image/png;base64,{}".format(radon_data)), width=12, lg=10, xl=8, className="mx-auto")
    ])
], fluid=True)

# Run the radon app
if __name__ == '__main__':
    radon_app.run_server(debug=True)
