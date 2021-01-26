### libs
from dash.dependencies import State, Input, Output
import plotly.graph_objects as go
import plotly.offline as plotly
import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
import pandas as pd
import os

## vars and functions
global cat_g ,sample_type
cat_g = ["good","bad","worst"] 
sampletype=["beta",]

def datagen():
    my_sample_data = np.random.random_sample([13,3])
    sample_Cat = [cat_g[np.random.randint(0,3)] for i in range(13)]
    #Base_Data = pd.DataFrame(my_sample_data,columns=["val_1","val_2","val_3"])
    data=pd.read_excel("C:/Users/Narcys/sync/python/concat/dane/output.xlsx",engine='openpyxl')
    data["sample_Cat"] = sample_Cat = ['good' for i in range(13)]
    return(data)

def fig_generator(data):
    data = data.reset_index(drop=True)
    plot_data =[]

    for i in range(4,10):
        plot_data.append(go.Scatter(x=data.index, y=data[data.columns[i]], name = data.columns[i] ))
        plot_layout = go.Layout(title = " This plot is generated using plotly  ")

    fig = go.Figure( data = plot_data ,layout = plot_layout)

    return(fig.data,fig.layout)
    
##options
cat_g = ["good","bad","worst"] 
options_list = []
for i in cat_g:
    options_list.append({'label': i, 'value': i})

## html Layout
app = dash.Dash()
app.layout=html.Div(children=[html.Div("My dashboard", style={
                                                    "color":"red",
                                                    "text-align":"center", "background-color":"blue",
                                                    "display":"inline-block", "width":"80%"
                                                }),
                     html.Div(dcc.Dropdown(id = "drop_down_1",options = options_list, value='good'), style={
                                                    "color":"red",
                                                    "text-align":"center", "background-color":"darkorange",
                                                    "display":"inline-block", "width":"40%"
                                                }),
                     html.Div(children= [
                         html.P(
                                id = "map-title",
                                children = "Forecast and validation"
                                ), 
                         html.Div(children = [
                                 dcc.Graph( id = "plot_area",
                                            figure = {  'data' : [],
                                                        'layout' : [] })
                                ])], 
                     style={
                                                    "color":"red",
                                                    "text-align":"center", "background-color":"yellow",
                                                    "display":"inline-block", "width":"40%"}
                                        )]
                                    ,style={"width": "100%",'paffing': 10}
                    )

## Creating Callback
@app.callback(Output("plot_area", 'figure'),
              
              [Input("drop_down_1", "value")])

def updateplot(input_cat):
    
    df= datagen()
    data = df[df["sample_Cat"] == input_cat ]
    
    trace,layout = fig_generator(data)
    
    return {
        'data': trace,
        'layout':layout
    }    
## run                                 
if __name__=='__main__':
    app.run_server()