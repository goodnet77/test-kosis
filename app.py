# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc               # impprt dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__)
server = app.server

# csv 데이터 불러오기
df = pd.read_csv('kosis.csv')
df['Year'] = df['PRD_DE'].astype(str).str[:4]
df['Month'] = df['PRD_DE'].astype(str).str[4:].astype(int)

itm_list = list(zip(df.ITM_NM.unique(), df.ITM_ID.unique()))
sex_list = list(zip(df.C1_NM.unique(), df.C1.unique()))
age_list = list(zip(df.C2_NM.unique(), df.C2.unique()))
year_list = list(zip(df.Year.unique(), df.Year.unique()))

itm_value = 'T90'    # 기본 값: 취업률
sex_value = 0
age_value = 0
year_value = ['2020', '2021', '2022']

fig = go.Figure()
for year in year_value: 
    df_graph = df[(df.ITM_ID == itm_value) & (df.C1 == sex_value) & (df.C2 == age_value) & (df.Year == year)]
    fig.add_trace(go.Scatter(x=df_graph.Month, y=df_graph.DT, name=year, mode='lines+markers'))
    fig.update_xaxes(range=[0.5, 12.5],
        ticktext = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        tickvals = [1,2,3,4,5,6,7,8,9,10,11,12]
    )

app.layout = html.Div([
    html.H3('경제활동 인구 조사(월별 통계)', style={"textAlign":"center"}),
    html.Div([
        dcc.Dropdown(id="itm_dropdown",                
        options = [{'label':i, 'value':j} for i, j in itm_list],
        value = itm_value,
        searchable = False,
        style = dict(width='100%')),
        dcc.Dropdown(id="sex_dropdown",                
        options = [{'label':i, 'value':j} for i, j in sex_list],
        value = sex_value,
        searchable = False,
        style = dict(width='100%')),
    ], style = dict(display = 'flex')),
        html.Div([
        dcc.Dropdown(id="age_dropdown",                
        options = [{'label':i, 'value':j} for i, j in age_list],
        value = age_value,
        searchable = False,
        style = dict(width='100%')),
        dcc.Dropdown(id="year_dropdown",                
        options = [{'label':i, 'value':j} for i, j in year_list],
        value = year_value,
        searchable = False,
        multi = True,
        style = dict(width='100%')),
    ], style = dict(display = 'flex')), 
    html.Div([
        dcc.Graph(id='graph', figure=fig)
    ])
])

@app.callback(
    Output('graph', 'figure'),
    Input('itm_dropdown', 'value'),
    Input('sex_dropdown', 'value'),
    Input('age_dropdown', 'value'),
    [Input('year_dropdown', 'value')]
)

def update_graph(itm_val, sex_val, age_val, year_val):
    fig = go.Figure()
    for year in year_val:
        df_graph = df[(df.ITM_ID == itm_val) & (df.C1 == sex_val) & (df.C2 == age_val) & (df.Year == year)]
        fig.add_trace(go.Scatter(x=df_graph.Month, y=df_graph.DT, name=year, mode='lines+markers'))
        fig.update_xaxes(range=[0.5, 12.5],
            ticktext = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
            tickvals = [1,2,3,4,5,6,7,8,9,10,11,12]
        )
    return fig

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         Dash: 소득, 소비 통계
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

if __name__ == '__main__':
    app.run_server(debug=True)

