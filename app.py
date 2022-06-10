from calendar import c
from cgitb import reset
from html.entities import html5
from pydoc import classname
from sre_parse import State
from colorama import Style
import pandas as pd
from dash import Dash,html,dcc, Input, Output, State
import plotly.express as px
import plotly.io as pio
from dash import callback_context
import joblib

df = pd.read_csv("CleanData.csv")
df1 = df
df1['report'] = df['Outcome'].map({0: 'Negetive' , 1 : 'Positive'})

col = df.columns
col = col[:len(col)-2]

tot_rec = 'Total Records : '+ str(len(df)) 

colors = {
    'background': '#f2f5f9',
}


#innerfig1 = px.histogram(df, x=["Outcome"], template = 'simple_white')
innerfig1 = px.histogram(df, x=['Positive', 'Negetive'], y= [ (len(df[df['Outcome'] == 1])), (len(df[df['Outcome'] == 0])) ], template = 'simple_white')
innerfig2 = px.pie(df1, values="Glucose", names="report", color_discrete_sequence=px.colors.sequential.RdBu)
fig2 = px.histogram(df, x="Glucose",template = 'simple_white+presentation')
heatfig = px.imshow(df.corr(),text_auto=True ,aspect="auto")

app = Dash(__name__, external_stylesheets = ['/assets/style.css'])
app.title = "Diabetes Prediction "

app.layout = html.Div([

    #Outer 1st Div ----------------------------------------------------------------------------------------------------------------------------

    html.Div([ 

            html.H2('Diabetes Dashboard', className='padding', style={'text-align':'center'}
        )
    ], className='header'
    ),

    #Outer 2nd Div ----------------------------------------------------------------------------------------------------------------------------

    html.Div([

        #inner 1st Div ------------------------------------------------------------------------------------------------------------------------

        html.Div([ 

            # inner inner 1st Div--------------------------------------------------------------------------------------------------------------
            
            html.Div([ 

                html.P(tot_rec, style={'text-align':'center', 'font-size':'20px'}), 
                
                html.Hr(style={'borderWidth': "0.01vh", "width": "99%", }),
                

                # 2 Grpah inner Div------------------------------------------------------------------------------------------------------------
                html.Div([

                    html.Div([ 

                        html.P('Data Distribution', style={'text-align':'center', 'font-size':'13px'}),
                        html.Hr(style={'borderWidth': "0.01vh", "width": "99%", }),

                            dcc.Graph(
                                id = 'inner-graph-1',
                                figure = innerfig1,
                                style={
                                    'width':'90%',
                                    'height':'300px',
                                    'margin-left':'auto',
                                    'margin-right':'auto',
                                    'margin-top':'auto',
                                    'margin-bottom':'auto',    
                                }
                            ),
                    ], style={'width':'50%', 'margin-left':'15px', 'margin-right':'5px','border':'1px solid ','border-radius': '1em' }),

                    html.Div([ 

                        html.P('Column Distribution for Result', style={'text-align':'center', 'font-size':'13px'}),
                        html.Hr(style={'borderWidth': "0.01vh", "width": "99%", }),

                        dcc.Dropdown(
                            col,
                            id="col-drop-down",
                            value=col[1],
                            multi=False,
                            style={
                                'width':'70%',
                                'height': '16px',
                                'margin-left':'auto',
                                'margin-right':'auto',
                            },
                        ),  

                        html.Br(),

                        dcc.Graph(
                            id = 'inner-graph-2',
                            figure = innerfig2,
                            style={
                                'width':'90%',
                                'height':'250px',
                                'margin' : '10px',
                                'margin-left':'auto',
                                'margin-right':'auto',
                            },
                            
                        )
                    ], style={'width':'50%','margin-right':'15px', 'margin-left':'5px', 'border':'1px solid black', 'border-radius': '1em' }),

                ], className='innerlDiv'),
                
            ], className='card'),

            # inner inner 2nd  Div--------------------------------------------------------------------------------------------------------------

            html.Div([

                html.P('Columns Distribution : ', style={'text-align':'center', 'font-size':'20px'}),

                html.Hr(style={'borderWidth': "0.01vh", "width": "99%", }),
                html.Br(),

                html.Div([
                    html.Label(
                        'Columns :', 
                        style={
                            'height': '20px',
                            'margin-right':'7px',
                            'padding-top': '5px',
                        }),
                    dcc.Dropdown(
                        col,
                        id="drop-down",
                        value=col[1],
                        multi=False,
                        style={
                            'width':'400px',
                            'height': '20px',
                        },
                    ),  

                ], className='dropDiv'),

                dcc.Graph(
                    id = 'graph-2',
                    figure = fig2,
                    style={
                        'width':'600px',
                        'height':'380px',
                        'margin-left': 'auto',
                        'margin-right' : 'auto',
                        'margin-bottom' : '15px',
                    }
                ),
                
            ], className='card card-space'),

        ], className='lDiv'),

        #inner 2nd Div ------------------------------------------------------------------------------------------------------------------------

        html.Div([ 

            html.P('Predict Diabetes ', style={'text-align':'center', 'font-size':'20px'}),
            
            html.Hr(style={'borderWidth': "0.01vh", "width": "99%", }),

            html.P('Here you can predict whether the patient has diabetes or not based on some data.', 
                    style={'padding':'0px 2px 0px 2px',}
            ),

            html.Hr(style={'borderWidth': "0.01vh", "width": "99%", }),
            html.Br(),

            html.Label('Glucose :', style={'font-size':'18px'}),
            dcc.Input(id='val-1',placeholder = 'Enter Glucose eg. 80', type='number', className="card-input"),
            html.Br(),

            html.Label('Blood Pressure :', style={'font-size':'18px'}),
            dcc.Input(id='val-2',placeholder = 'Enter Blood Pressure eg. 80', type='number', className="card-input"),
            html.Br(),

            html.Label('Skin Thickness :', style={'font-size':'18px'}),
            dcc.Input(id='val-3',placeholder = 'Enter Skin Thickness(mm) for eg. 20', type='number', className="card-input"),
            html.Br(),
            
            html.Label('Insulin :', style={'font-size':'18px'}),
            dcc.Input(id='val-4',placeholder = 'Enter Insulin level (IU/ml) eg. 80', type='number', className="card-input"),
            html.Br(),

            html.Label('Pregnancies :', style={'font-size':'18px'}),
            dcc.Input(id='val-5',placeholder = 'Enter number of Pregnancies ', type='number', className="card-input"),
            html.Br(),

            html.Label('BMI :', style={'font-size':'18px'}),
            dcc.Input(id='val-6',placeholder = 'Enter Body Mass Index eg. 23.1', type='number', className="card-input"),
            html.Br(),

            html.Label('Diabetes Pedigree Function :', style={'font-size':'18px'}),
            dcc.Input(id='val-7',placeholder = 'Enter Diabetes Pedigree Function eg. 0.52', type='number', className="card-input"),
            html.Br(),

            html.Label('Age :', style={'font-size':'18px'}),
            dcc.Input(id='val-8',placeholder = 'Enter age (years) eg. 30', type='number', className="card-input"),
            html.Br(),

            html.Button('Submit', id='submit-val', className='btn-grad'),

            html.Div([
                html.P(id='output',className='opDiv'),
            ]),

        ], className='rdiv'),

    ], className='body2'),

    #Outer 3rd Div ----------------------------------------------------------------------------------------------------------------------------

    html.Div([ 

        html.P('HEATMAP', style={'text-align':'center', 'font-size':'20px'}),
            
        html.Hr(style={'borderWidth': "0.01vh", "width": "99%", }),
        html.Br(),

        dcc.Graph(
            id = 'heatfig',
            figure = heatfig,
            style={
                'width':'90%',
                'height':'600px',
                'margin-left': 'auto',
                'margin-right' : 'auto',
                'margin-bottom' : '15px',
            }
        )

    ], className='heatDiv'),

], className='body')

# graph callback
@app.callback(
    Output('graph-2', 'figure'),
    Input('drop-down', 'value'))

def change_fig(col_name):
    fig2 = px.histogram(df, x=df[col_name],template = 'simple_white+presentation')
    return fig2    


#2nd graph callback

@app.callback(
    Output('inner-graph-2', 'figure'),
    Input('col-drop-down', 'value'))

def change_fig(col_name):
    innerfig2 = px.pie(df1, values=df[col_name], names="report", color_discrete_sequence=px.colors.sequential.RdBu)
    return innerfig2    



# Predict callback
@app.callback(
    Output('output', 'children'),
    Input('submit-val', 'n_clicks'),
    State(component_id='val-1', component_property='value'),
    State(component_id='val-2', component_property='value'),
    State(component_id='val-3', component_property='value'),
    State(component_id='val-4', component_property='value'),
    State(component_id='val-5', component_property='value'),
    State(component_id='val-6', component_property='value'),
    State(component_id='val-7', component_property='value'),
    State(component_id='val-8', component_property='value'),)

def show_res(n_clicks, ip1,ip2,ip3,ip4,ip5,ip6,ip7,ip8):
    loaded_model = joblib.load('rfc_model.sav')
    data=[[ip5,ip1,ip2,ip3,ip4,ip6,ip7,ip8]]
   
    if loaded_model.predict(data) == 0:
        print("Person is likely to NOT have diabetes")
        return f'Person is likely to NOT have diabetes'
    else:
        print("Person is likely to have diabetes")
        return f'Person is likely to have diabetes'

if __name__ == '__main__':
    app.run_server(debug=False)