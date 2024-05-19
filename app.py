# Importação do Dash e das bibliotecas relacionadas
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from Extracoes import pega_acao, retorno_mm
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import pandas as pd
from dash_bootstrap_templates import load_figure_template

geral = pd.read_parquet("geral_ativo.parquet")

estilos = [dbc.themes.MATERIA, 'https://api.freepik.com/v1/resources?locale=en-US&page=1&limit=2&order=latest&term=car', dbc.icons.BOOTSTRAP]

card_icons = {
    "color": "White",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto"
}

# Criação do aplicativo Dash
app = dash.Dash(__name__, external_stylesheets = estilos)
load_figure_template("material")

# Definição do layout usando Dash Bootstrap Components
app.layout = html.Div(children=[
    dcc.Store(id='data-store-origin', data=geral.to_dict('records')),
    dcc.Store(id='data-store-update'),
    dcc.Store(id='data-store-graphs'),
    dcc.Store(id='radio-value', data='Adicionar'),
    dcc.Store(id='acoes-store', data=geral['Ativo'].unique().tolist()),
    dbc.Row(children=[
                dbc.Col([
                    dbc.Card([
                                dbc.CardBody([
                                        html.H5("Controle de ações", className="card-title"),
                                        html.Hr(),
                                        html.H6("Descrição do projeto", className="card-subtitle"),
                                        html.P(
                                            "Dashboard em desenvolvimento com o intuito de desenvolver analises do mercado financeiro.",
                                            className="card-text",
                                        ),
                                        dbc.CardLink("Linkdin", href="https://www.linkedin.com/in/ruanan-terra-de-lima-88b774210/"),
                                        dbc.CardLink("Github", href="https://github.com/Ruanan-Terra"),
                                        html.Hr(),
                                        html.Div([
                                            dbc.Button("Atualizar página",
                                                outline=True,
                                                color="primary",
                                                className="me-1",
                                                id = "atualizar-dados-button") 
                                            ])
                                        ])                                
                                ], style = {'height' : '100vh'})
                        ], sm = 2, style={"height": "100vh", "padding": "7px"}),
                dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                    dbc.Card([
                                        dbc.CardBody([
                                        html.Legend("Gestão de ativos:"),
                                        html.Div([dcc.RadioItems([{'label': 'Adicionar', 'value': 'Adicionar'}, {'label': 'Excluir', 'value': 'Excluir'}]
                                                                 ,'Adicionar', inline=True, id = "Radio_status")]),
                                        html.Div([
                                            dbc.InputGroup(
                                            [
                                                dbc.Input(id="input_ativo", placeholder="Ativo"),
                                                dbc.Button("Executar", id="input-button-ativo", n_clicks=0)
                                            ]
                                            ),
                                            html.Div(id='output-n-clicks'),
                                        ], style={"margin-top" : "10px"}),
                                        html.Legend("Filtros", style={"margin-top" : "10px"}),
                                        html.Div([
                                            dcc.DatePickerRange(
                                                month_format='MMM Do, YY',
                                                end_date_placeholder_text='MMM Do, YY',
                                                start_date= pd.to_datetime(geral['Date'].min()),
                                                end_date = pd.to_datetime(geral['Date'].max()),
                                                id = "date_filter"
                                        ),
                                        ]),
                                            html.Div([
                                                dcc.Dropdown(
                                                    geral['Ativo'].unique(),
                                                    geral['Ativo'].unique(),
                                                    multi=True,
                                                id = "dropdown_filter")
                                            ], style={"margin-top" : "10px"})
                                        ])
                                    ], style={"height": "calc(48vh + 14px)"})
                            ], sm = 8),
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.CardGroup([
                                            dbc.Card([
                                                html.Div([
                                                html.Legend("Teste Graph",className="text-center"),
                                                html.H4("2.26%",id = "value-1",className="text-center")
                                                ], style={"padding": "25px"})
                                            ],className="text-center", style={"width": "80%"}),
                                            dbc.Card([
                                                html.Div(className = 'bi bi-percent', style = card_icons)
                                            ],style={"maxWidth": "20%", "margin-left":"-10px","backgroundColor":"Black"})
                                        ], style = {"height" : "16vh", "margin-top" : "-10px", "margin-right" : "7px"})
                                    ])
                                ], className = 'main_row g-2 my-auto'),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.CardGroup([
                                            dbc.Card([
                                                html.Div([
                                                html.Legend("Teste Graph",className="text-center"),
                                                html.H4("R$256",id = "value-2",className="text-center")
                                                ], style={"padding": "25px"})
                                            ], style = {"textAlign": "center"}),
                                            dbc.Card([
                                                html.Div(className = 'bi bi-cash', style = card_icons)
                                            ],style={"maxWidth": "20%", "margin-left":"-10px", "backgroundColor":"Black"})
                                        ], style = {"height" : "16vh", "margin-right" : "7px",})
                                    ])
                                ], className = 'main_row g-2 my-auto'),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.CardGroup([
                                            dbc.Card([
                                                html.Div([
                                                # html.Legend("Teste Graph",className="text-center"),
                                                html.H4("Mini Graph",id = "value-3",className="text-center")
                                                ], style={"padding": "25px"})
                                            ], style = {"textAlign": "center"}),
                                            dbc.Card([
                                                html.Div(className = 'bi bi-bar-chart', style = card_icons)
                                            ],style={"maxWidth": "20%", "margin-left":"-10px", "backgroundColor":"Black"})
                                        ], style = {"height" : "16vh", "margin-right" : "7px",})
                                    ])
                                ], className = 'main_row g-2 my-auto'),                                
                            ], sm = 4, className='my-2')
                        ], className = 'main_row g-2 my-auto', style={"height": "calc(50vh + 14px)"}),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.Tabs(
                                                [
                                                    dbc.Tab(label="Valor histórico", tab_id="valor_hist"),
                                                    dbc.Tab(label="Valorização histórica", tab_id="percent_hist"),
                                                ],
                                                id="tabs",
                                                active_tab="valor_hist",
                                            ),
                                            # dcc.Store(id="store"),
                                            html.Div(id="tab-content", className="p-4")
                                    ], style={"height": "calc(48vh + 6px)", "margin-right" : "7px"})
                            ], sm = 12)
                        ], className = 'main_row g-2 my-auto', style = {"height": "45vh", "margin-top" : "7px"}),
                    ], sm = 10)
        ], className = 'main_row g-2 my-auto', style={"height": "100vh"})
    ])

### --->>> CALLBACKS <<<--- ###
@app.callback(
        Output('data-store-update', 'data'),
        [Input('input-button-ativo', 'n_clicks'),
        Input('date_filter', 'start_date'),
        Input('date_filter', 'end_date'),
        Input('dropdown_filter', 'value')],
        [State('radio-value', 'data'),  # Estado para o valor do RadioItem
        State('input_ativo', 'value'),
        State('data-store-origin', 'data')]
)
def update_data(button, date_filter_start, date_filter_end, dropdown_filter, radio_value, input_ativo, data_origin):
    df = pd.DataFrame(data = data_origin)

    df['Date'] = pd.to_datetime(df['Date'], format = "%Y-%m-%d")

    acoes = list(df['Ativo'].unique())
    input_ativo = str(input_ativo)
    if button:
        if input_ativo is not None:
            if radio_value == "Adicionar":
                    if input_ativo:
                        acoes.append(input_ativo)  # Adiciona a nova ação à lista de ações
                        df = pega_acao(ativo=acoes)
            else:
                    if input_ativo in acoes:
                        acoes.remove(input_ativo)  # Remove a ação da lista de ações se ela estiver presente
                        df = pega_acao(ativo=acoes)
        elif input_ativo is None:
            df = pega_acao(ativo=acoes)
            df['Date'] = pd.to_datetime(df['Date'], format = "%Y-%m-%d")

    date_filter_start = pd.to_datetime(date_filter_start)
    if date_filter_end:
        date_filter_end = pd.to_datetime(date_filter_end)
    else:
        date_filter_end = pd.to_datetime(date.today())

    df = df[df['Ativo'].isin(list(dropdown_filter))]

    df = df[(df['Date'] >= date_filter_start) & (df['Date'] <= date_filter_end)]

    df_retorno = pd.DataFrame()
    resultantList = df['Ativo'].unique()
    for acao in resultantList:
        df_temp = df[df['Ativo'] == acao].copy()  # Filtra o DataFrame apenas para a ação atual
        df_temp.reset_index(drop=True, inplace=True)  # Reinicia o índice
        df_temp['Retorno'] = (df_temp['Adj Close'] / df_temp['Adj Close'].iloc[0]) - 1  # Calcula o retorno do ativo
        df_retorno = pd.concat([df_retorno, df_temp], ignore_index=True)  # Concatena os dados ao DataFrame final

    # Reseta o índice no final
    df_retorno.reset_index(drop=True, inplace=True)
    # print(df_retorno)

    df_teste = df_retorno.to_dict('records')
    print(df_teste[0]["Date"])

    df_teste2 = pd.DataFrame(df_teste)
    print(df_teste[0])

    return df_retorno.to_dict('records'), dcc.Location(pathname='/', id='redirect-location')

@app.callback(
    Output("data-store-graphs", "data"),
    Input("data-store-update", "data")
)
def render_graph(data):
    df = pd.DataFrame(data)

    df['Date'] = pd.to_datetime(df['Date'], format = "%Y-%m-%d")

    template = "material"

    graph_period = px.line(df, x="Date", y='Adj Close', color='Ativo', template=template, title="Valor ativos")
    graph_period.update_layout(height=380)

    graph_period_mean = px.line(df, x="Date", y='Retorno', color='Ativo', template=template, title="Análise percentual")
    graph_period_mean.update_layout(height=380)

    return {"valor_hist": graph_period, "percent_hist": graph_period_mean}

@app.callback(
        Output("tab-content", "children"),
        [Input("tabs", "active_tab"),
        Input("data-store-graphs", "data")],
)
def tab_content(active_tab, data):
    if active_tab and data:
        if active_tab == 'valor_hist':
            return dbc.Card([
                dcc.Graph(figure=data["valor_hist"], id="Graph-1")
            ], style={"height": "calc(30vh + 14px)", "margin-right": "7px"})
        elif active_tab == 'percent_hist':
            return dbc.Card([
                dcc.Graph(figure=data["percent_hist"], id="Graph-2")
            ], style={"height": "calc(30vh + 14px)"})
    # Retorne algo padrão caso active_tab ou data seja None
    return html.Div("Nenhum dado disponível para exibir.")

@app.callback(
    Output('radio-value', 'data'),  # Atualiza o valor do RadioItem quando ele é alterado
    Input('Radio_status', 'value')
)
def update_radio_value(value):
    return value

# Função para iniciar o servidor web
if __name__ == '__main__':
    app.run_server(debug=True)



