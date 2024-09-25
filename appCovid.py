import dash
from dash import dcc, html, Input, Output
import pandas as pd
import requests
import plotly.graph_objs as go
from datetime import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("COVID-19 Time Series Data Visualization"),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=datetime(2020, 1, 1),
        end_date=datetime.today(),
        display_format='YYYY-MM-DD'
    ),
    dcc.Graph(id='time-series-chart'),
    html.Div(id='output-container')
])

# Callback to update graph based on selected dates
@app.callback(
    Output('time-series-chart', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_graph(start_date, end_date):
    # Fetch data from API
    url = f'https://api.covid19api.com/country/united-states?from={start_date}T00:00:00Z&to={end_date}T00:00:00Z'
    response = requests.get(url)
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Create figure
    figure = {
        'data': [
            go.Scatter(
                x=df['Date'],
                y=df['Confirmed'],
                mode='lines+markers',
                name='Confirmed Cases'
            ),
            go.Scatter(
                x=df['Date'],
                y=df['Deaths'],
                mode='lines+markers',
                name='Deaths'
            )
        ],
        'layout': go.Layout(
            title='COVID-19 Confirmed Cases and Deaths Over Time',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Count'},
            hovermode='closest'
        )
    }
    
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)