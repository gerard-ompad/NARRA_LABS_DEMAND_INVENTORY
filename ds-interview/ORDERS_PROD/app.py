import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go
import dash
import joblib
import xgboost
from datetime import datetime, date
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State

# Load the trained XGBoost model
xgboost_model = joblib.load('optimized_xgboost_model.joblib')

# Placeholder for storing data
data = []

custom_template = {
    "layout": go.Layout(
        font={"family": "Helvetica", "size": 12, "color": "#1f1f1f"},
        title={"font": {"family": "Helvetica", "size": 16, "color": "#1f1f1f"}},
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        colorway=px.colors.qualitative.G10,
    ),
}

# Components: Input Controls
purchaserange_picker = dmc.TextInput(id="order-id-input", w=200, placeholder="Input Order ID", style={"width": 330})
daterange_picker = dmc.DatePicker(id="date-picker", value=datetime.now().date(), dropdownType="modal", style={"width": 330})
timerange_picker = dmc.TimeInput(id="time-input", withSeconds=True, value=datetime.now().time(), style={"width": 330})
distancerange_picker = dmc.NumberInput(id="distance-input", step=0.01, min=0, value=0, style={"width": 330})
orderrange_picker = dmc.NumberInput(id="order-qty-input", step=1, min=0, value=0, style={"width": 330})
popularityrange_picker = dmc.NumberInput(id="popularity-input", step=0.01, min=1, max=5, value=1, style={"width": 330})
trafficrange_picker = dmc.NumberInput(id="traffic-input", step=1, min=1, max=3, value=1, style={"width": 330})
dmc_select_city = dmc.Select(id="weather-select", value="Clear", data=[{"value": "Clear", "label": "Clear"}, {"value": "Rain", "label": "Rain"}, {"value": "Cloudy", "label": "Cloudy"}, {"value": "Fog", "label": "Fog"}])

# Table for displaying input data
input_table = dash_table.DataTable(
    id='data-table',
    columns=[
        {"name": "Order ID", "id": "order_id"},
        {"name": "Date", "id": "date"},
        {"name": "Time", "id": "time"},
        {"name": "Distance", "id": "distance"},
        {"name": "Order Quantity", "id": "order_qty"},
        {"name": "Popularity", "id": "popularity"},
        {"name": "Traffic", "id": "traffic"},
        {"name": "Weather", "id": "weather"},
        {"name": "Estimated Delivery Time (minutes)", "id": "predicted_time"},  # Add the new column
    ],
    data=[],
    editable=False,
    style_table={'overflowX': 'auto'},
)

# Download CSV Button
dcc_download_csv = dcc.Download(id="download-dataframe-csv")

def description_card():
    return html.Div(
        id="description-card",
        children=[
            html.H5(
                "Delivery",
                style={"color": "#2c8cff", "display": "inline"},
            ),
            html.H5(" + Analytics", style={"display": "inline", "color": "#68c949"}),
            html.H3("Order Demand Inventory"),
            html.Div(
                id="intro",
                children="Ordering Just Made Smarter.",
            ),
        ],
    )

# Layout Components
def generate_control_card():
    return html.Div(
        children=[
            html.P("Order ID:"), purchaserange_picker, html.Br(),
            html.P("Input Date:"), daterange_picker, html.Br(),
            html.P("Input Time:"), timerange_picker, html.Br(),
            html.P("Input Distance:"), distancerange_picker, html.Br(),
            html.P("Number of Orders:"), orderrange_picker, html.Br(),
            html.P("Restaurant Popularity:"), popularityrange_picker, html.Br(),
            html.P("Weather Conditions:"), dmc_select_city, html.Br(),
            html.P("Traffic Conditions:"), trafficrange_picker, html.Br(),
            html.Button("Submit", id="submit-btn", n_clicks=0), html.Br(),  # Submit button
            html.Button("Download Data", id="btn_csv"),  # Download button right below
        ],
    )

def create_layout():
    return dmc.MantineProvider(
        children=[
            html.Div(
                id="app-container",
                children=[
                    html.Div(
                        id="banner",
                        className="banner",
                        children=[
                            html.Img(src=app.get_asset_url("dtn-logo-tag-492x108.webp"))  # Logo reference
                        ],
                    ),
                    html.Div(
                        id="left-column",
                        className="three columns",
                        children=[description_card(),
                            generate_control_card(),  # Contains the submit and download buttons
                            dcc_download_csv,  # This remains for the download functionality
                        ],
                    ),
                    html.Div(
                        id="right-column",
                        className="nine columns",
                        children=[input_table],
                        style={"display": "block"},
                    ),
                ],
            )
        ]
    )

dash._dash_renderer._set_react_version('18.2.0')
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
app.title = "Predictive Inventory"
app.config.suppress_callback_exceptions = True
app.layout = create_layout()

# Callback to update the table and append new data with prediction
@app.callback(
    Output("data-table", "data"),
    Input("submit-btn", "n_clicks"),
    State("order-id-input", "value"),
    State("date-picker", "value"),
    State("time-input", "value"),
    State("distance-input", "value"),
    State("order-qty-input", "value"),
    State("popularity-input", "value"),
    State("traffic-input", "value"),
    State("weather-select", "value"),
    prevent_initial_call=True
)
def update_table(n_clicks, order_id, date_val, time_val, distance, order_qty, popularity, traffic, weather):
    if not n_clicks:
        raise PreventUpdate

    # Prepare input data for the XGBoost model
    input_data = pd.DataFrame([[distance,order_qty, popularity]], columns=['distance_km','order_size','restaurant_popularity'])
    # Predict delivery time using the XGBoost model
    predicted_time = xgboost_model.predict(input_data)[0]

    # Create the new row with the prediction
    new_row = {
        "order_id": order_id,
        "date": date_val,
        "time": time_val,
        "distance": distance,
        "order_qty": order_qty,
        "popularity": popularity,
        "traffic": traffic,
        "weather": weather,
        "predicted_time": predicted_time  # Add the predicted time
    }

    data.append(new_row)
    return data

# Callback to download the CSV
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True
)
def download_csv(n_clicks):
    df = pd.DataFrame(data)
    return dcc.send_data_frame(df.to_csv, "inventory_data.csv")

# Run the server
if __name__ == "__main__":
    app.run_server(host="127.0.0.1", port=9000, debug=True)
