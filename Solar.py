import random as rand
import pandas as pd
import math 
import numpy as np
from scipy import ndimage
import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, ALL, MATCH
import dash_html_components as html
import dash_table as dt

def layout(app):
    main_color = "#303030"
    text_color = '#fec036'
    param = ['mass', 'x', 'y', 'z', 'velosity vektror']
    t = ['sec', 'min', 'hod', 'day', 'week']
    return html.Div(children = [
        dcc.RadioItems(id = 'visibility',
            options = [{'label': i, 'value': i} for i in ['Visible', 'Invisible']],
            value = 'Visible', labelStyle={'display': 'inline-block'},
            style={'textAlign': 'center','margin-top': '15px', 'color':main_color}),
        html.Div(id = 'main', className = 'app-div', children = [
            html.Hr(style = {'width': '500px'}),
            html.P('Number of space object...', style = {'color':text_color}),
            dcc.Slider(id = 'num_planet', min = 1, max = 100,
                marks = {i: '{}'.format(i) for i in range(0, 101, 10)}, value = 1),
            html.Hr(style = {'width': '500px'}),
            dcc.Dropdown(id='pozition', style = {'width': '500px', 'padding-left':'25px'},
                options=[{'label': 'Random generated parametres.', 'value': 'rand'}, 
                {'label': 'Solar system', 'value': 'solar'}],value='solar'),
            html.Div(id = 'parametres', style = {'width': '500px', 'padding-left':'25px'},
                className = 'parametres-own', children = [     
                html.Hr(style = {'width': '500px'}),
                dt.DataTable(id='starting_point', columns=[{
                    'name': '{}'.format(i),
                    'id': '{}'.format(i),
                    'deletable': True,
                    'renamable': True} for i in param],
                    data=[],
                    editable=True,
                    row_deletable=True),
                ]),
            html.Div(id = 'start_btn',className='butt', children=[
                html.Hr(style = {'width': '500px'}),
                dcc.Slider(id = 'time', min = 0, max = 4,
                    marks = {i: '{}'.format(t[i]) for i in range(len(t))},
                    value = 4),
                dcc.Input(id = 'num_iteration', placeholder='Enter value of iteration...',
                    type='number',  debounce=True, value = 250),
                html.P('Start your simulation', style = {'color':text_color}),
                html.A(
                    html.Button(
                        id='start',
                        className='satrt_btn',
                        children="Start",
                        n_clicks=0,
                        style = {'color':text_color}
                    ),
                ),
                html.Hr(style = {'width': '500px', 'color':main_color},),
            ]),
            dcc.RadioItems(id = 'zob',
            options = [{'label': i, 'value': i} for i in ['Animation', 'Scatter']],
            value = 'Scatter', labelStyle={'display': 'inline-block'},
            style={'textAlign': 'center','margin-top': '15px', 'color':text_color}),
            html.Hr(style = {'width': '500px'}),
        ]),
        html.Div(children = [
            dcc.Graph(id="graph", style={}),
        ],style = {'float': 'right', 'display':'inline-block'}),
    ],style={})
def callbacks(app):
    @app.callback(
        [Output('main', 'style'),
        Output('graph', 'style')],
        [Input('visibility', 'value')]
    )
    def show_param(x):
        main_color = "#303030"
        if x == 'Visible':
            return [{'display':'inline-block','width':'550px', 'borderRadius': '20px',
                'textAlign': 'center', "background-color":main_color},
                {'width':'1290px','height': '890px'}]
        else:
            return [{'display':'none'}, {'width':'1900px'}]
    @app.callback(
        Output('parametres', 'style'),
        [Input('pozition', 'value')]
    )
    def show_velic(x):
        if x == 'solar':
            return {'display':'none'}
        else:
            return {'display':'none'}
    @app.callback(
        Output('starting_point', 'data'),
        [Input('num_planet', 'value')],
        [State('starting_point', 'data'),
        State('starting_point', 'columns')]
    )
    def add_row(num, row, column):
        row.clear()
        for _ in range(num):
            if len(row) < num:
                row.append({c['id']: '' for c in column})
        return row
    @app.callback(
        Output('graph', 'figure'),
        [Input('start', 'n_clicks'),
        Input('zob', 'value')],
        [State('num_planet', 'value'),
        State('num_iteration', 'value'),
        State('pozition', 'value'),
        State('time', 'value'),
        State('starting_point', 'data')
        ])
    def display_graph(start, zob, num_planet, num, poziton, time, starting_point):
        parametr = []
        mass = []
        planets = []
        ro = 0 
        if poziton == "rand":
            ro = 10**12
            for i in range(num_planet):
                xyz, veloc = [], []
                v = []
                v.append(rand.randint(6, 2000000) * 10 ** 23) #je to pomerove cislo je na ^22
                vektor = []
                vektor.append(rand.randint(- 0.5 * ro, 0.5 * ro)) #mil kilometru na ^9 m
                vektor.append(rand.randint(- 0.5 * ro, 0.5 * ro)) #mil kilometru na ^9 m
                vektor.append(rand.randint(- 0.5 * ro, 0.5 * ro)) #mil kilometru na ^9 m
                xyz.append(vektor)
                vekto = []
                vekto.append(0)
                vekto.append(0)
                vekto.append(0)
                veloc.append(vekto)
                vekt = []
                vekt.append(xyz)
                vekt.append(veloc)
                for _ in range(num_planet + 1):
                    vekt.append([])
                v.append(vekt)
                mass.append(v[0])
                parametr.append(v)
                planets.append('Planeta {}'.format(i))
        elif poziton == "solar":
            ro = 5*10**12
            planets = ['Slunce', 'Merkur', 'Venuše', 'Země', 'Mars', 'Jupite', 'Saturn', 
                'Uran', 'Neptun']
            mass = [1.989*10**30, 3.287*10**23, 4.867*10**24, 5.972*10**24, 
                6.39*10**23, 1.898*10**27, 5.683*10**26, 8.681*10**25, 1.024*10**26]
            dist = [0, 57.91*10**9, 108.2*10**9, 149.6*10**9, 227.9*10**9, 778.5*10**9, 
                1.434*10**12, 2.871*10**12, 4.495*10**12]
            vel = [0, 170503/3.6, 130074/3.6, 107218/3.6, 86677/3.6, 47002/3.6, 34701/3.6,
                24477/3.6, 19566/3.6]
            phi = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            theta = [0, 245, 295, 198, 166, 97, 75, 212, 130]
            for x in range(len(mass)):
                v, xyz, veloc, vekt, vekto, vektor = [], [], [], [], [], []
                vektor.append(dist[x] * math.sin(theta[x]) * math.cos(phi[x]))
                vektor.append(dist[x] * math.cos(theta[x]))
                vektor.append(dist[x] * math.sin(theta[x]) * math.sin(phi[x]))
                xyz.append(vektor)
                if x == 0:
                    veloc.append([0,0,0])
                else:
                    veloc.append(vector(parametr, vektor, vel[x]))
                vekt.append(xyz)
                vekt.append(veloc)
                for _ in range(len(mass) + 1):
                    vekt.append([])
                v.append(mass[x])
                v.append(vekt)
                parametr.append(v)
        tom = 0
        kok = 1
        if time == 3: 
            kok = 6
        elif time == 4:
            kok = 42
        num *= kok
        while tom < num:
            for i in range(len(parametr)):
                for j in range(i, len(parametr), 1):
                    if i == j:
                        continue
                    else:
                        parametr[i][1][j + 1].append(gravitation(parametr, i, j))
                        vektor = []
                        for k in range(3):
                            vektor.append(-1 * parametr[i][1][j + 1][tom][k])
                        parametr[j][1][i + 2].append(vektor)
            for i in range(len(parametr)):
                parametr[i][1][len(parametr) + 1].append(force_v(parametr, i, len(parametr)))
                parametr[i][1][len(parametr) + 2].append(aceleration(parametr, i, len(parametr)))
                x, v = new_position(parametr, i, len(parametr), time)
                parametr[i][1][0].append(x)
                parametr[i][1][1].append(v)
            tom = tom + 1
        num /= kok
        for k in range(int(num)):
            for i in range(len(parametr)):
                for _ in range(kok - 1):
                    parametr[i][1][0].pop(k)
                    parametr[i][1][1].pop(k)
        delka = len(parametr[0][1][0])
        if zob == 'Animation':
            layout = dict(xaxis = dict(range = [- ro, ro], autorange = False, zeroline = False),
                yaxis = dict(range = [- ro, ro], autorange = False, zeroline = False), 
                hovermode = "closest", updatemenus = [dict(type = "buttons", 
                    buttons = [dict(label = "Play",method = "animate", args = [None])])])
            x, y, z, mass2 = [], [], [], []
            kom = []
            for j in range(len(parametr)):
                mass2.append(mass[j])
                X, Y, Z = [], [], []
                for i in range(delka):
                    X.append(parametr[j][1][0][i][0])
                    Y.append(parametr[j][1][0][i][1])
                    Z.append(parametr[j][1][0][i][2])
                trace = dict(type = 'scatter3d', x = X, y = Y, z = Z, mode = 'lines')
                kom.append(trace)
            for i in range(delka):
                x1, y1, z1 = [], [], []
                for j in range(len(parametr)):
                    x1.append(parametr[j][1][0][i][0])
                    y1.append(parametr[j][1][0][i][1])
                    z1.append(parametr[j][1][0][i][2])
                x.append(x1)
                y.append(y1)
                z.append(z1)
            traceinit = dict(type = 'scatter3d', x = x[0], y = y[0], z = z[0], 
                mode = 'markers', marker = dict(size = 10, color = mass2, colorscale = 'Viridis',))
            kom.append(traceinit)
            frames = [dict(data = [dict(x = x[k], y = y[k], z = z[k])], traces = [len(parametr)])
                 for k in range(delka)]
            fig = dict(data = kom, layout = layout, frames = frames)
            return fig
        else:
            fig = go.Figure(data=[])
            x, y, z, mass2 = [], [], [], []
            for j in range(len(parametr)):
                x.append(parametr[j][1][0][delka - 1][0])
                y.append(parametr[j][1][0][delka - 1][1])
                z.append(parametr[j][1][0][delka - 1][2])
                mass2.append(mass[j])
                X, Y, Z = [], [], []
                for i in range(delka):
                    X.append(parametr[j][1][0][i][0])
                    Y.append(parametr[j][1][0][i][1])
                    Z.append(parametr[j][1][0][i][2])
                fig.add_trace(go.Scatter3d(x = X, y = Y, z = Z, mode = "lines"))
            fig.add_trace(go.Scatter3d(x = x, y = y, z = z, mode = "markers"))
            return fig
    
def force_v(params, planet, num_planet):
    fv = []
    delka = len(params[planet][1][2])
    for j in range(3):
        sum = 0
        for i in range(num_planet -2):
            sum += params[planet][1][i + 2][delka - 1][j]
        fv.append(sum)
    return fv

def gravitation(parametr, planet1, planet2):
        force = []
        fs = 0
        delka = len(parametr[planet1][1][0])
        g = 6.674*10**-11
        for i in range(3):
            force.append(parametr[planet2][1][0][delka - 1][i] - 
                parametr[planet1][1][0][delka - 1][i])
        distance = round(math.sqrt(force[0]**2 + force[1]**2 + force[2]**2), 6)
        fs = round(g * parametr[planet1][0] * parametr[planet2][0] / distance**2, 6)
        for j in range(3):
            force[j] = round(force[j] / distance * fs, 6)
        return force

def aceleration(param, id, num_planet):
    a = []
    delka = len(param[id][1][0])
    for i in range(3):
        a.append(param[id][1][num_planet + 1][delka - 1][i] / param[id][0])
    return a

def new_position(param, id, num_planet, time):
    xyz, vel = [], []
    if time == 0:
        times = 1
    elif time == 1:
        times = 60
    elif time == 2:
        times = 3600
    elif time == 3:
        times = 14400
    elif time == 4:
        times = 14400
    delka = len(param[id][1][0])
    for i in range(3):
        xyz.append(0.5 * param[id][1][num_planet + 2][delka - 1][i] * times**2 + 
            param[id][1][1][delka - 1][i] * times + param[id][1][0][delka - 1][i])
        vel.append(param[id][1][num_planet + 2][delka - 1][i] * times + 
            param[id][1][1][delka - 1][i])
    return xyz, vel

def vector(param, data, vel):
    vec = [param[0][1][0][0][0] - data[0], param[0][1][0][0][1] - data[1], 0]
    distance = round(math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2), 6)
    vec = [vel * vec[1] / distance, vel * (- vec[0]) / distance, vel * vec[2] / distance]
    return vec


app = dash.Dash(__name__, 
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
    suppress_callback_exceptions=True)
app.layout = layout(app)
callbacks(app)
if __name__ == '__main__':
    app.run_server(debug=True)