import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dbm
import plotly.graph_objs as go
import re
# import smtp_alert
import pandas as pd
import dash_bootstrap_components as dbc
import datetime


# Set up the app
app = dash.Dash(__name__)
server = app.server
app.title='stats.taoists.com'



global tao_df
global taoists
global date_list

tao_df = pd.read_csv('tao_holders.csv')

def taoist_list():
    taolist = []
    unique_list = tao_df.symbol.unique()
    for symbol in unique_list:
        taolist.append({'value': symbol, 'label': symbol})    
    return taolist



taoists = taoist_list()

print(taoists)
# def create_date_list():
#     date_list = []
#     unique_dates = product_df.date.unique()
#     for date in unique_dates:
#         date_list.append({'value': date, 'label': date})
#     return date_list

# date_list = create_date_list()



# date_list = pd.date_range(date1, date2).tolist()

date_list = tao_df['date'].tolist()


app.layout = html.Div([
    html.Div([
        html.H6('taodao.finance'),
        html.H1('Taoists'),
        html.H2('Choose a Taoist'),
        dcc.Dropdown(
            id='taoist-dropdown',
            options=taoists,
            multi=True,
            value = ["Token", "Token", "Token"]
        ),
    ], style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        html.H2('Taoists'),
        dcc.Graph(id='taoist-holders'),
        html.P('')
    ], style={'width': '100%', 'display': 'inline-block'}),
])




@app.callback(Output('taoist-holders', 'figure'), [Input('taoist-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    tao_df_filter = tao_df[(tao_df['symbol'].isin(selected_dropdown_value))]

    data = timeline_top_taoists_filtered(tao_df_filter,selected_dropdown_value)
    # Edit the layout
    layout = dict(
                  xaxis=dict(title='Date'),
                  yaxis=dict(title='Taoists'),
                  color='white',
                  plot_bgcolor='#191919',
                  paper_bgcolor='#191919',
                  )
    figure = dict(data=data,layout=layout)
    return figure



def timeline_top_taoists_filtered(top_taoists_filtered_df, selected_dropdown_value):
    # Make a timeline
    trace_list = []
    for value in selected_dropdown_value:
        top_taoists_value_df = top_taoists_filtered_df[top_taoists_filtered_df['symbol']==value]
        trace = go.Scatter(
            y=top_taoists_value_df.value.tolist(),
            x=top_taoists_value_df.date,
            fill='tozeroy',
            mode='lines',
            line=dict(width=0.5),
            marker= {
                'colorscale': 'sunset'
            },
            name = value,
            textfont=dict(
                family='Verdana',
                color='white'
            )
        )
        trace_list.append(trace)
    return trace_list

if __name__ == '__main__':
    app.run_server(debug=True)