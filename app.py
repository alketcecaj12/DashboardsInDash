import dash 
from dash import html
from dash import dcc 
import plotly.express as px
import pandas as pd
import yfinance as yf

ticker = yf.Ticker("AAPL")
data = ticker.history("5Y")
data = data.reset_index()


fig = px.line(data, x = "Date", y = "Close", title = "Apple stock trend!")


app = dash.Dash(__name__)
app.title = "Apple stock trend"


app.layout = html.Div(
    id = "app-container",
    children = [
        html.H1("Apple stock trend day by day!"),
        html.P("Results in USD!"),
        dcc.Graph(figure = fig)
    ]
)


if __name__ == "__main__":
    app.run_server(debug = True)