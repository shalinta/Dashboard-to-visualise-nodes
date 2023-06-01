import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import networkx as nx
from faker import Faker

app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.GRID,dbc.themes.BOOTSTRAP])

server = app.server
app.title = 'Graph presentation' 

Number_node_box = dbc.Input(type="number", id='input_number',value=50, min=2),

app.layout = html.Div([
    dbc.Container([
     dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Graph presentation'),
                ], style={'textAlign': 'center', "color": "white"})

            ], className="border-0 bg-transparent"),
        ], width=11),],style={'margin-bottom': 20 , 'backgroundColor': '#1C4E80'}),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        
                        dbc.Col(html.Div("Number of Nodes:", className="card-title"), md=5),
                         dbc.Col(Number_node_box, md=5, className="card-text",),
                        dbc.Col(
                        
                        dbc.Button("Submit", id='submit-val', outline=True,color="success", className="me-1"),
                         md=2, className="card-text",),
                      # DatePicker,
                    ],justify="center", align="center")
                ])

            ], style={'height': 80 , }),
            ],   width=6),
            ], style={'margin-bottom': 20 ,  }),
            

            dbc.Card([
                dbc.CardBody([
                      dcc.Graph(id='graph_fig')
                        
                ],style={ "align":"center",
                           
                       
                
                 })])

        ], width=12),


    ]),

],fluid=True)

],style={'backgroundColor':'#F1F1F1', 'background-size': '100%',
          'height': '120vh'})

           




@app.callback(
    dash.dependencies.Output('graph_fig', 'figure'),
    dash.dependencies.Input('submit-val', 'n_clicks'),
    dash.dependencies.State('input_number', 'value')
      )
def update_confirmed(btn1, nb_node):
    
    if nb_node:
        G = nx.random_geometric_graph(nb_node, 0.125)
    else:
        G = nx.random_geometric_graph(50, 0.125)
    #Add edges as disconnected lines in a single trace and nodes as a scatter trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []  

    for node in G.nodes():
        

        x, y = G.nodes[node]['pos']
        
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
    x=node_x, y=node_y,
    
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))
    node_adjacencies = []
    node_text = []


       
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        faker = Faker()  
        node_text.append('IP:'+faker.ipv4()  +'\n# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(

                showlegend=False,
                hovermode='closest',
                margin=dict(b=0,l=0,r=0,t=0),
                annotations=[ dict(
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8051)