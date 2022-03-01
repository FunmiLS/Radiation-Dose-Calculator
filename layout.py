#Import Libraries
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import time
from header import get_header
from title import get_title

from questions.xray import get_question1, pplant_image
from questions.ct import get_question2
from questions.coffee import get_question3, coffee_image
from questions.banana import get_question4, banana_image
from questions.beer import get_question5, beer_image
from questions.home import get_question6
from questions.holiday import get_question7
from questions.background import get_question8
from questions.answer import get_answer


#Hex Colours
EDF_BLUE = '#103579'
EDF_ORANGE = '#ff5716'
Miles_Blue = '#64c3db'
Miles_Orange = '#e3652e'

#Database
database = pd.read_csv('assets/database.csv')
location = pd.read_csv('assets/radon_data.csv')

#Quick clean
clean_location = location.drop(labels=0, axis=0)
Name = clean_location["County or Area Name"].tolist()
Dose = clean_location["Effective Dose"].tolist()

def get_dashboard_layout(app):

    #Layout begins
    layout = html.Div([

        #Header
        get_header(app=app),
        #Title
        get_title(app=app),

        #Questions
        get_question1(app=app),

        html.Br(),

        get_question2(app=app),

        html.Br(),

        get_question3(app=app),

        html.Br(),

        get_question4(app=app),

        html.Br(),

        get_question5(app=app),

        html.Br(),

        get_question6(app=app),

        html.Br(),

        get_question7(app=app),

        html.Br(),
        get_question8(app=app),

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.I('')
            ], width=1),
            dbc.Col([
                dbc.Button('Calculate', id='submit-val', n_clicks=0, style={'textTransform': 'none'}),
                dcc.Loading(
                    id="loading-1",
                    type="default",
                    children=html.Div(id="loading-output-1")
                ),
            ], width=10),
            dbc.Col([
                html.I('')
            ], width=1)
        ], id='calculate-row'),

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.I('')
            ], width=1),
            dbc.Col([
                html.Div(id='total-radiation'),
                html.Div(id='tabs-graph'),
                html.Div(id='tabs-content'),
                dcc.Store(id='store-data-output')
            ], width=10),
            dbc.Col([
                html.I('')
            ], width=1)
        ], id='output-row'),

        html.Br(),
        html.Br(),
        dbc.Row(),
        dbc.Row(),

        dbc.Row([
            dbc.Col([
                html.I('')
            ], width=1),
            dbc.Col([
                html.Div(
                         'Created by: Max Talberg & Funmi Looi-Somoye'
                )
            ], width=10),
            dbc.Col([
                html.I('')
            ], width=1)
        ], id='contact-row'),

        html.Br()

    ])

    @app.callback(
        Output(component_id='store-data-output', component_property='data'),
        [Input(component_id='Q-1a-ddown', component_property='value'),
         Input(component_id='Q-1b-ddown', component_property='value'),
         Input(component_id='Q-2a-ddown', component_property='value'),
         Input(component_id='Q-2b-ddown', component_property='value'),
         Input(component_id='Q-2c-ddown', component_property='value'),
         Input(component_id='Q-3a-ddown', component_property='value'),
         Input(component_id='Q-4a-ddown', component_property='value'),
         Input(component_id='Q-5a-ddown', component_property='value'),
         Input(component_id='Q-6a-ddown', component_property='value'),
         Input(component_id='Q-7a-ddown', component_property='value'),
         Input(component_id='Q-7b-ddown', component_property='value'),
         Input(component_id='Q-7c-ddown', component_property='value')

         ]
    )
    def organise_data(dental, wrist, head, chest, abdomen, coffee, bananas, beer, location, long, short, days):
        count = 0
        if location is None:
            location = 0
        else:
            location = float(Dose[(Name.index(location))])
        weeks = 52.1429
        values = dental, wrist, head, chest, abdomen, coffee, bananas, beer, location, long, short, days
        conv = lambda i: i or 0
        res = [conv(i) for i in values]
        values = res[:]

        q1 = (values[0]*database['Dental'][0]) + (values[1]*database['Wrist'][0])
        q2 = (values[2]*database['CT_head'][0]) + (values[3]*database['CT_chest'][0]) + (values[4]*database['CT_abdomen'][0])
        q3 = (values[5]*database['Coffee'][0]) * weeks # For an annual dose
        q4 = (values[6]*database['Banana'][0]) * weeks
        q5 = (values[7]*database['Pint'][0]) * weeks
        q6 = (values[8])
        q7 = (values[9]*database['Plane'][0]) + (values[11]*(database['Cornwall'][0]/3)) # Longhaul flight !?
        Total_ED = q1 + q2 + q3 + q4 + q5 + q6 + q7 + database['Cosmic'][0]
        data_output = [Total_ED, q1, q2, q3, q4, q5, q6, q7]
        return data_output

    @app.callback(
        Output(component_id='loading-output-1', component_property='children'),
        [Input(component_id='submit-val', component_property='n_clicks')]
    )
    def load_sign(n_clicks):
        time.sleep(1)
        return

    @app.callback(
        Output(component_id='tabs-graph', component_property='children'),
        [Input(component_id='submit-val', component_property='n_clicks'),
         Input(component_id='store-data-output', component_property='data')]
    )
    def update_output(n_clicks, data):
        total = data[0]
        time.sleep(1.1)
        card_content = html.Div(children=[
            dbc.CardHeader(

                html.Div(children=[
                    html.H5(children=['Total Effective Dose'], style={ 'textAlign': 'center'}),

                ])
            ),
            dbc.CardBody(
                dbc.Row(
                    dbc.Col(children=[
                        html.Div(children=[
                            html.H5('{:,} mSv'.format(round(total, 2)).replace(',', ' ,')),
                        ], style={'textAlign': 'center'}),
                    ], width=12),
                ),

                    )
                ])
        while n_clicks != 0:
            tabs = html.Div([
                html.Div(
                    dbc.Row([

            #Margin 1

            dbc.Col([
                html.I('')
            ], width=1),

            dbc.Col([
                dbc.Card(card_content, color="warning", inverse=True)
            ], width=5),

            dbc.Col([
                html.I('')
            ], width=6),

        ]),
    ),
                html.Br(),
                html.Br(),
                html.Div(
                    dcc.Tabs(id='tab-graph', value='tab-graph-value', children=[
                        dcc.Tab(label='Results', value='tab-3'),
                        dcc.Tab(label='Compare to Nuclear Powerplants', value='tab-1'),
                        dcc.Tab(label='Breakdown', value='tab-2'),
                    ])
                ),
                             ]),

            return tabs

    @app.callback(
        Output(component_id='tabs-content', component_property='children'),
        [Input(component_id='tab-graph', component_property='value'),
         Input(component_id='store-data-output', component_property='data')]
    )
    def render_content(tab, data):
        # [Total_ED, q1, q2, q3, q4, q5, q6, q7]
        xrays = data[1]
        ct = data[2]
        coffee = data[3]
        banana = data[4]
        pint = data[5]
        home = data[6]
        travel = data[7]
        background = database['Cosmic'][0]
        total = data[0]

        if tab == 'tab-1':
            return html.Div([
                html.H6(''),
                dcc.Graph(
                    id='graph-1-tabs',
                    figure={
                        'data': [
                            {'x': [1], 'y': [total], 'type': 'bar','name': 'Total radiation'},
                            {'x': [2], 'y': [database['living_plant'][0]], 'type': 'bar', 'name': 'Living 50 miles from a nuclear powerplant'},
                            {'x': [3], 'y': [database['nuclear_worker'][0]], 'type': 'bar', 'name': u'Working in a nuclear plant'},
                            {'x': [0, 3.5], 'y': [database['uk_limit'][0], database['uk_limit'][0]],
                             'type': 'line', 'name': 'UK Limit for Occupational Workers'}
                        ],
                        'layout': {
                        }
                    }
                )
            ])
        if tab == 'tab-2':
            return html.Div([
                html.H6(''),
                dcc.Graph(
                    id='graph-2-tabs',
                    figure={
                        'data': [
                            {'x': [1], 'y': [banana], 'type': 'bar', 'name': 'Bananas'},
                            {'x': [2], 'y': [coffee], 'type': 'bar', 'name': u'Coffee'},
                            {'x': [3], 'y': [pint], 'type': 'bar', 'name': u'Beer'},
                            {'x': [4], 'y': [xrays], 'type': 'bar', 'name': u'Xrays'},
                            {'x': [5], 'y': [ct], 'type': 'bar', 'name': u'CT'},
                            {'x': [6], 'y': [home], 'type': 'bar', 'name': u'Location'},
                            {'x': [7], 'y': [travel], 'type': 'bar', 'name': u'Travel'},
                            {'x': [8], 'y': [background], 'type': 'bar', 'name': u'Background'},
                            {'x': [9], 'y': [total], 'type': 'bar', 'name': u'Total'},
                        ],
                        'layout': {

                        }
                    }
                )
            ])
        elif tab == 'tab-3':
            return html.Div([
                dbc.Row(children=[
                    dbc.Col(children=[
                        html.Div(id='radio-items')
                    ], width=3),
                    dbc.Col(children=[
                        html.Div(id='radio-content')
                    ], width=6),
                    dbc.Col(children=[
                        html.Div(id='radio-image')
                    ], width=3)
                ]),
            ])

    @app.callback(
        Output(component_id='radio-items', component_property='children'),
        [Input(component_id='submit-val', component_property='n_clicks')]
    )
    def render_items(n_clicks):
        while n_clicks != 0:
            radio_items = html.Div([
                html.H4('Select an option'),
                dcc.RadioItems(id='radio-items',
                    options=[
                        {'label': 'Pints of Beer', 'value': 'beer'},
                        {'label': 'Bananas', 'value': 'banana'},
                        {'label': 'Working in a power plant', 'value': 'power-plant'},
                        {'label': 'Cups of Coffee', 'value': 'coffee'},
                    ], labelStyle={'display': 'block'})
            ])
            return radio_items

    @app.callback(
        Output(component_id='radio-content', component_property='children'),
        Output(component_id='radio-image', component_property='children'),
        [Input(component_id='radio-items', component_property='value'),
         Input(component_id='store-data-output', component_property='data')]
    )
    def render_output(value, data_output):
        Total_ED = data_output[0]
        pints = Total_ED/database['Pint'][0]
        bananas = Total_ED/database['Banana'][0]
        pplant = Total_ED/database['nuclear_worker'][0]
        coffees = Total_ED/database['Coffee'][0]
        if value == 'beer':
            out = html.Div([
                html.Br(),
                html.Div([
                    html.H4('Your activities across a year expose you to the same radiation as:')
                ], style={"textAlign": "center"}),
                html.Br(),
                html.Div([
                    html.H1('{:,}'.format(round(pints)).replace(',', ' ,'))
                ], style={"textAlign": "center"}),
                html.Br(),
                html.Div([
                    html.H4('pints of beer!')
                ], style={"textAlign": "center"})
            ])
            image = html.Div([
                html.Br(),
                html.Br(),
                beer_image])
        elif value == 'banana':
            out = html.Div([
                html.Br(),
                html.Div([
                    html.H4('Your activities across a year expose you to the same radiation as:')
                ], style={"textAlign": "center"}),
                html.Br(),
                html.Div([
                    html.H1('{:,}'.format(round(bananas)).replace(',', ' ,'))
                ], style={"textAlign": "center"}),
                html.Br(),
                html.Div([
                    html.H4('bananas!')
                ], style={"textAlign": "center"})
            ])
            image = html.Div([
                html.Br(),
                html.Br(),
                banana_image])
        elif value == 'power-plant':
            out = html.Div([
                html.Br(),
                html.Div([
                    html.H4('Your activities across a year expose you to the same radiation as:')
                ], style={"textAlign": "center"}),
                html.Br(),
                html.Div([
                    html.H1('{:,}'.format(round(pplant)).replace(',', ' ,'))
                ], style={"textAlign": "center"}),
                html.Br(),
                html.Div([
                    html.H4('years working in a nuclear power plant!')
                ], style={"textAlign": "center"})
            ])
            image = html.Div([
                html.Br(),
                html.Br(),
                pplant_image])
        elif value == 'coffee':
            out = html.Div([
                html.Br(),
                html.Div([
                    html.H4('Your activities across a year expose you to the same radiation as:')
                ], style={"textAlign": "center"}),
                html.Br(),
                html.Div([
                    html.H1('{:,}'.format(round(coffees)).replace(',', ' ,'))
                ], style={"textAlign": "center"}),
                html.Br(),
                html.Div([
                    html.H4('cups of coffee!')
                ], style={"textAlign": "center"})
            ])
            image = html.Div([
                html.Br(),
                html.Br(),
                coffee_image])
        else:
            out = html.Div([
                html.Br(),
                html.Br(),
                html.I('Select an activity...')
            ], style={"textAlign": "center"}),
            image = html.Div([
            ])
        return out, image

    return layout
