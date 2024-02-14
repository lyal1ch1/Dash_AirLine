import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=["assets/style.css"])
airline_data = pd.read_csv('airline_data.csv')

def calculate_average_delay(df, delay_type):
    avg_delay = df.groupby(['Month', 'Year', 'Reporting_Airline'])[delay_type].mean().reset_index()
    return avg_delay

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Среднемесячная задержки отчетной авиакомпании", className="heading"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in range(2010, 2021)],
        value=2010,
        style={'width': '100%'}
    ),
    html.Div([
        dcc.Graph(id='carrier-delay-graph'),
        dcc.Graph(id='weather-delay-graph')
    ], style={'display': 'flex', "marginBottom" : "32px"}),
    html.Div([
        dcc.Graph(id='nas-delay-graph'),
        dcc.Graph(id='security-delay-graph')
    ], style={'display': 'flex', "marginBottom" : "32px"}),
    dcc.Graph(id='late-aircraft-delay-graph')
], className="container")

@app.callback(
    Output('carrier-delay-graph', 'figure'),
    Output('weather-delay-graph', 'figure'),
    Output('nas-delay-graph', 'figure'),
    Output('security-delay-graph', 'figure'),
    Output('late-aircraft-delay-graph', 'figure'),
    Input('year-dropdown', 'value')
)
def update_graphs(selected_year):
    filtered_data = airline_data[airline_data['Year'] == selected_year]
    carrier_delay = calculate_average_delay(filtered_data, 'CarrierDelay')
    weather_delay = calculate_average_delay(filtered_data, 'WeatherDelay')
    nas_delay = calculate_average_delay(filtered_data, 'NASDelay')
    security_delay = calculate_average_delay(filtered_data, 'SecurityDelay')
    late_aircraft_delay = calculate_average_delay(filtered_data, 'LateAircraftDelay')
    
    fig1 = px.line(carrier_delay, x='Month', y='CarrierDelay', color='Reporting_Airline',
                   title='Среднее время задержки перевозчика (минуты)')
    fig1.update_xaxes(title_text='Месяц')
    fig1.update_yaxes(title_text='Среднее время задержки (минуты)')
    
    fig2 = px.line(weather_delay, x='Month', y='WeatherDelay', color='Reporting_Airline',
                   title='Среднее время задержки из-за погоды (минуты)')
    fig2.update_xaxes(title_text='Месяц')
    fig2.update_yaxes(title_text='Среднее время задержки (минуты)')
    
    fig3 = px.line(nas_delay, x='Month', y='NASDelay', color='Reporting_Airline',
                   title='Среднемесячная задержка отчетной авиакомпании из-за национальной воздушной системы (минуты)')
    fig3.update_xaxes(title_text='Месяц')
    fig3.update_yaxes(title_text='Среднее время задержки (минуты)')
    
    fig4 = px.line(security_delay, x='Month', y='SecurityDelay', color='Reporting_Airline',
                   title='Среднее время задержки из-за безопасности (минуты)')
    fig4.update_xaxes(title_text='Месяц')
    fig4.update_yaxes(title_text='Среднее время задержки (минуты)')
    
    fig5 = px.line(late_aircraft_delay, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
                   title='Среднее время задержки из-за опоздания самолета (минуты)')
    fig5.update_xaxes(title_text='Месяц')
    fig5.update_yaxes(title_text='Среднее время задержки (минуты)')
    
    return fig1, fig2, fig3, fig4, fig5

if __name__ == '__main__':
    app.run_server(debug=True)