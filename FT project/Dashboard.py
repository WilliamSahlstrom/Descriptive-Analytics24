import dash
from dash import html, dcc
import pandas as pd
import os

# Load the data
script_dir = os.path.dirname(__file__)
csv_path = os.path.join(script_dir, "results", "article_texts_with_vader_scores.csv")
df = pd.read_csv(csv_path)

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Sentiment Analysis Dashboard'),

    # Bar chart for comparing sentiment scores between the two periods
    dcc.Graph(
        id='sentiment-comparison',
        figure={
            'data': [
                {'x': df[df['MM/YYYY'] == "03/2020"]['Headline'], 'y': df[df['MM/YYYY'] == "03/2020"]['Vader score'], 'type': 'bar', 'name': '03/2020'},
                {'x': df[df['MM/YYYY'] == "03/2022"]['Headline'], 'y': df[df['MM/YYYY'] == "03/2022"]['Vader score'], 'type': 'bar', 'name': '03/2022'}
            ],
            'layout': {
                'title': 'Sentiment Score Comparison',
                'barmode': 'group'
            }
        }
    ),

    # Bar chart for displaying individual sentiment scores
    dcc.Graph(
        id='individual-sentiment',
        figure={
            'data': [
                {'x': df['Headline'], 'y': df['Vader score'], 'type': 'bar', 'name': 'Vader score'}
            ],
            'layout': {
                'title': 'Individual Vader Compound Scores',
                'barmode': 'stack'
            }
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
