import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Load the mag data
mag_file_paths = {
    "HOVT23_MAG": "C:/Users/THOM/Desktop/myflaskap/HOVT23_MAG.csv", 
    "ARUC23_MAG": "C:/Users/THOM/Desktop/myflaskap/ARUC23_MAG.csv", 
    "GARN23_MAG": "C:/Users/THOM/Desktop/myflaskap/GARN23_MAG.csv", 
    "EKHG23_MAG": "C:/Users/THOM/Desktop/myflaskap/EKHG23_MAG.csv", 
    "KARC23_MAG": "C:/Users/THOM/Desktop/myflaskap/KARC23_MAG.csv",
    "BAVR23_MAG": "C:/Users/THOM/Desktop/myflaskap/BAVR23_MAG.csv",
    "JERM23_MAG": "C:/Users/THOM/Desktop/myflaskap/JERM23_MAG.csv"
}
mag_dataframes = {name: pd.read_csv(file_path) for name, file_path in mag_file_paths.items()}

# Modify the labels by removing the "_mag" or other suffixes
cleaned_mag_names = {original: original.split('_')[0] for original in mag_dataframes.keys()}

# Compute the correlation matrix for mag data
mag_correlation_data = []
for name1, mag_df1 in mag_dataframes.items():
    mag_row_data = []
    for name2, mag_df2 in mag_dataframes.items():
        mag_correlation = mag_df1['value'].corr(mag_df2['value'])
        mag_row_data.append(mag_correlation)
    mag_correlation_data.append(mag_row_data)

mag_correlation_matrix = pd.DataFrame(mag_correlation_data, columns=mag_dataframes.keys(), index=mag_dataframes.keys())
mag_correlation_matrix.columns = [cleaned_mag_names[col] for col in mag_correlation_matrix.columns]
mag_correlation_matrix.index = [cleaned_mag_names[idx] for idx in mag_correlation_matrix.index]

# Create the heatmap for mag data
mag_fig, mag_ax = plt.subplots(figsize=(10, 8))
sns.heatmap(mag_correlation_matrix, annot=True, cmap="coolwarm", linewidths=.5, vmin=-1, vmax=1, cbar_kws={'label': 'Correlation Coefficient'}, ax=mag_ax)
mag_ax.set_title('Correlation Matrix of 2023 Magnetic Field', pad=25)
mag_ax.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True, pad=5)
plt.xticks(rotation=0, ha='center')

plt.tight_layout()

# Convert the mag plot to an image for Dash
mag_buf = BytesIO()
mag_fig.savefig(mag_buf, format="png")
mag_data = base64.b64encode(mag_buf.getbuffer()).decode("utf8")

# Initialize the Dash app for mag data
mag_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
mag_app.title = 'Correlation Matrix of 2023 Magnetic Field'

# Define the mag app layout with Bootstrap for responsiveness
mag_app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Correlation Matrix of 2023 Magnetic Field", className="text-center"), width=12)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(html.Img(src="data:image/png;base64,{}".format(mag_data)), width=12, lg=10, xl=7, className="mx-auto")
    ])
], fluid=True)

# Run the mag app
if __name__ == '__main__':
    mag_app.run_server(debug=True)
