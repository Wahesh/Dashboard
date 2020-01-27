# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
import plotly_express as px
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
app.config['suppress_callback_exceptions'] = True




# Load data
df = pd.read_csv(DATA_PATH.joinpath("data.csv"), low_memory=False)
Indicators = df['Indicator']
provinces =['Province 1','Province 2','Province 3','Province 4','Province 5','Province 6','Province 7',]



# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("UNICEF_Logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "National Dashboard for Provincial Analysis",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Based on 77 Indicators across Budget, health, Education and Finance", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://Unicef.org.np/",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filter By Provinces",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="Province_Select",
                            options=[
                            {'label':'Province 1','value':'Province 1'}  ,
                            {'label':'Province 2','value':'Province 2'}  ,
                            {'label':'Province 3','value':'Province 3'}  ,
                            {'label':'Province 4','value':'Province 4'}  ,
                            {'label':'Province 5','value':'Province 5'}  ,
                            {'label':'Province 6','value':'Province 6'}  ,
                            {'label':'Province 7','value':'Province 7'}  
                            ], multi=True, value =provinces,
                          
                            className="dcc_control",
                        ),
                       
                       
                        
                        html.P("Choose an Indicator", className="Indicator"),
                        dcc.Dropdown(
                            id="Indicator_Select",
                            options=[{'label':Indicator, 'value':Indicator} for Indicator in Indicators],
                             value =Indicators[0],
                         
                           className="dcc_control",
                        ),
                       
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                       
                        html.Div(
                            [dcc.Graph(id="count_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="seven columns",
                ),
            ],
            className="row flex-display",
        ),
        ##################################
        # 
            html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container six columns",
                ),
                html.Div(
                    [
                 
                        
                    dcc.Graph(id="pie_graphs")],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
            
             html.Div([
                   
                    html.Div([
                    dcc.Markdown('X Axis'),
                    dcc.Dropdown(
                            id="ScatX",
                            options=[{'label':Indicator, 'value':Indicator} for Indicator in Indicators],
                            value ='HDI',
                            placeholder="Select X axis",
                            className="dcc_control")],style={"width":"100%"},
                            ),

                    
                    html.Div([
                    dcc.Markdown('Y Axis'),
                    dcc.Dropdown(
                            id="ScatY",
                            options=[{'label':Indicator, 'value':Indicator} for Indicator in Indicators],
                            value ='IMR',
                            placeholder="Select Y Axis",
                            className="dcc_control")
                             
                            ],style={"width":"100%"},
                     ),
                    html.Div([
                    dcc.Markdown('Size'),
                    dcc.Dropdown(
                            id="Size",
                            options=[{'label':Indicator, 'value':Indicator} for Indicator in Indicators],
                            value ='U5MR',
                            placeholder="Size of the Plot",
                            className="dcc_control")
                            ],style={"width":"100%"})

                ],className="pretty_container four columns" )
                
                ,

                html.Div([                    
                    dcc.Graph(id="individual_graph")
                    ],className="pretty_container eight columns",)
                
            ],
            className="row flex-display",
        ),
        
       
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)









# Selectors -> Bar Graph
@app.callback(
    Output("main_graph", "figure"),
    [
        Input("Province_Select", "value"),
        Input("Indicator_Select", "value"),
     
    ],
 
)
def make_main_figure(
    Province_Select, Indicator_Select):
    
    new_df = df[['Indicator'] + Province_Select]
    print(new_df.loc[new_df['Indicator'] == str(Indicator_Select)][Province_Select])
    print(Indicator_Select)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=Province_Select,
        y=new_df.loc[new_df['Indicator'] == str(Indicator_Select)][Province_Select].values.tolist()[0],
        # name='Primary Product',
        # marker_color='indianred'
    )
    )

    fig.update_layout(
    title=Indicator_Select + ' by ' + 'Provinces',
    xaxis_title='Provinces' ,
    yaxis_title=Indicator_Select,
    xaxis_tickangle=-45,
   
    )
    return fig

################################



# Selectors -> Bar Graph
@app.callback(
    Output("countgraph", "figure"),
    [
        Input("Province_Select", "value"),
        Input("Indicator_Select", "value"),
     
    ],
 
)
def make_main_figure(
    Province_Select, Indicator_Select):
    
    new_df = df[['Indicator'] + Province_Select]
    print(new_df.loc[new_df['Indicator'] == str(Indicator_Select)][Province_Select])
    print(Indicator_Select)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=Province_Select,
        y=new_df.loc[new_df['Indicator'] == str(Indicator_Select)][Province_Select].values.tolist()[0],
        # name='Primary Product',
        # marker_color='indianred'
    )
    )

    fig.update_layout(
    title=Indicator_Select + ' by ' + 'Provinces',
    xaxis_title='Provinces' ,
    yaxis_title=Indicator_Select,
    xaxis_tickangle=-45,
   
    )
    return fig



#Selectors -> Pie Chart
@app.callback(
    Output("pie_graphs", "figure"),
    [
        Input("Province_Select", "value"),
        Input("Indicator_Select", "value"),
     
    ],
 
)
def make_pie(
    Province_Select, Indicator_Select):
    
    new_df = df[['Indicator'] + Province_Select]
    print(new_df.loc[new_df['Indicator'] == str(Indicator_Select)][Province_Select])
    print(Indicator_Select)
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=Province_Select,
        values=new_df.loc[new_df['Indicator'] == str(Indicator_Select)][Province_Select].values.tolist()[0],
        hole=0.45,
        # name='Primary Product',
        # marker_color='indianred'
    ))
    
    fig.update_layout(
    title=Indicator_Select + ' by ' + 'Provinces',
    xaxis_title='Provinces' ,
    yaxis_title=Indicator_Select,
    #xaxis_tickangle=-45,
   
    )
    return fig
    
   #####################################




   #Selectors -> Scatter Plot
@app.callback(
    Output("individual_graph", "figure"),
    [
        Input("ScatY", "value"),
        Input("ScatX", "value"),
        Input("Size", "value"),
     
    ],
 
)
def make_scatter(
    ScatY, ScatX, Size):
    
    # new_df = df[['Indicator'] + Province_Select]
    # print(new_df.loc[new_df['Indicator'] == str(ScatY)][Province_Select])
    print(ScatX, ScatY, Size)
    plotx=df.loc[df['Indicator'] == ScatX][provinces].values
    ploty=df.loc[df['Indicator'] == ScatY][provinces].values
    plotsize=df.loc[df['Indicator'] == Size][provinces].values

    print(plotx[0], ploty[0], plotsize[0])
    fig = px.scatter(      
       x=plotx[0].tolist(), #df.loc[df['Indicator'] == ScatX][provinces].values,
       y=ploty[0].tolist(), #df.loc[df['Indicator'] == ScatY][provinces].values,
       
       color=provinces,
       size= plotsize[0]

    )
    
    fig.update_layout(
    title=ScatX + ' by ' + ScatY,
    xaxis_title=ScatX,
    yaxis_title=ScatY,
    xaxis_tickangle=-45,
   
    )
    return fig
    
   
   
   



# Main
if __name__ == "__main__":
    app.run_server(debug=True)
