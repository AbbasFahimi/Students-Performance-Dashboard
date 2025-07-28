import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load the dataset
df = pd.read_csv("../Data/StudentsPerformance.csv")

# Init app
app = dash.Dash(__name__)
app.title = "Student Performance Dashboard"

# Layout
app.layout = html.Div([
    html.H1("📊 Students Performance Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Test Type:"),
        dcc.Dropdown(
            id='score-type',
            options=[
                {'label': 'Math Score', 'value': 'math score'},
                {'label': 'Reading Score', 'value': 'reading score'},
                {'label': 'Writing Score', 'value': 'writing score'}
            ],
            value='math score',
            clearable=False
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Select Gender:"),
        dcc.Checklist(
            id='gender-filter',
            options=[{'label': g, 'value': g} for g in df['gender'].unique()],
            value=df['gender'].unique().tolist(),
            inline=True
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='boxplot'),
    dcc.Graph(id='histogram'),
    dcc.Graph(id='scatter'),
    dcc.Graph(id='bar-parental-edu')
])

# Callback
@app.callback(
    [Output('boxplot', 'figure'),
     Output('histogram', 'figure'),
     Output('scatter', 'figure'),
     Output('bar-parental-edu', 'figure')],
    [Input('score-type', 'value'),
     Input('gender-filter', 'value')]
)
def update_graphs(score_type, selected_genders):
    filtered_df = df[df['gender'].isin(selected_genders)]

    boxplot = px.box(
        filtered_df,
        x='gender',
        y=score_type,
        color='gender',
        title=f'{score_type.title()} Distribution by Gender'
    )

    histogram = px.histogram(
        filtered_df,
        x=score_type,
        color='gender',
        barmode='overlay',
        title=f'{score_type.title()} Histogram'
    )

    scatter = px.scatter(
        filtered_df,
        x='reading score',
        y='writing score',
        color='gender',
        title='Reading vs Writing Score'
    )

    bar_parental = px.bar(
        filtered_df.groupby('parental level of education')[score_type].mean().reset_index(),
        x='parental level of education',
        y=score_type,
        title=f'Average {score_type.title()} by Parental Education',
        labels={score_type: f'Average {score_type.title()}'}
    )

    return boxplot, histogram, scatter, bar_parental

if __name__ == '__main__':
    app.run(debug=True)
