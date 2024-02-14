import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

data = pd.read_excel('covid_polymatica.xlsx')
# print(data.columns)
app = dash.Dash(__name__, external_stylesheets=["assets/style.css"])


def plot_data(region, start_date, end_date):
    filtered_data = data[(data['Регион'] == region) & (data['дата'] >= start_date) & (data['дата'] <= end_date)]
    fig1 = px.line(filtered_data, x='дата', y='случаи заболевания', title='Количество заболевших')
    fig2 = px.line(filtered_data, x='дата', y='количество смертей', title='Количество смертей')
    return fig1, fig2

# Определение макета
app.layout = html.Div([
    html.H1("Статистика COVID-19 в разных регионах России", className="heading"),
    html.Div([
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in data['Регион'].unique()],
            value=data['Регион'].iloc[0]
        ),
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=data['дата'].min(),
            max_date_allowed=data['дата'].max(),
            initial_visible_month=data['дата'].min(),
            start_date=data['дата'].min(),
            end_date=data['дата'].max()
        )
    ], style={'width': '100%', "margin-bottom" : "32px"}),
    html.Div([
        dcc.Graph(id='cases-graph'),
        dcc.Graph(id='deaths-graph')
    ])
],)

@app.callback(
    [Output('cases-graph', 'figure'),
     Output('deaths-graph', 'figure')],
    [Input('region-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graphs(selected_region, start_date, end_date):
    fig1, fig2 = plot_data(selected_region, start_date, end_date)
    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)
