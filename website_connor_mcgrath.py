import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 10000)
stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# pandas dataframe to html table
def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
def new_table(df):
    return dash_table.DataTable( columns=[{"name": i, "id": i} for i in df.columns],data=df.to_dict('records'),style_table={'overflowY': 'scroll'},page_size=10)


app = dash.Dash(__name__, external_stylesheets=stylesheet) # creates a blank dash board in the style of stylesheet.

df = pd.read_csv("end_dataframe.csv")
df = df.iloc[:,2:-1]
df = df.drop(['area1','area2'],axis=1)
for n in range(len(df)):
    str_1 = df.iloc[n,6]
    str_2 = df.iloc[n,7]
    str_3 = df.iloc[n,8]
    if isinstance(str_1, float):
        continue
    str_1 = str(str_1).replace(" ", "")
    df.iloc[n,6]=str_1
    if isinstance(str_2, float):
        continue
    str_2 = str(str_2).replace(" ", "")
    df.iloc[n, 7] = str_2
    if isinstance(str_3, float):
        continue
    str_3 = str(str_3).replace(" ", "")
    df.iloc[n, 8] = str_3
print(df)


fig = px.pie(df,names="genre1",values ="total_mins")
x = generate_table(df.sort_values(["total_mins"],ascending=False))
app.layout = html.Div([html.H1("Need a new show? Try out some of the longest running shows on TV"),
                       html.H2("Sort by rating, genre, total minutes of run time"),
                       html.H5("The default for selection is if any genre matches, an or statement, if you want all values of genre to match select exclusive"),
dcc.Checklist(options=[{"label":"Exclusive",'value':'1'}],value=["1"],labelStyle={'display':'inline-block'},id="and_or"),
dcc.Checklist(options=[{"label":"Drama",'value':'Drama'},{"label":"Crime",'value':'Crime'},
                       {"label":"Family",'value':'Family'},{"label":"News",'value':'News'},{"label":"Comedy",'value':'Comedy'},
                       {"label":"Animation",'value':'Animation'},{"label":"Action",'value':'Action'},{"label":"Documentary",'value':'Documentary'},
                       {"label":"Biography",'value':'Biography'},{"label":"Short",'value':'Short'},{"label":"Game-Show",'value':'Game-Show'},{"label":"Music",'value':'Music'}
                       ,{"label":"Adventure",'value':'Adventure'},{"label":"Horror",'value':'Horror'},{"label":"Sci-Fi",'value':'Sci-Fi'}]
              ,value=["Drama","Comedy"],labelStyle={'display':'inline-block'},id="city_checkbox"),
                       dcc.Graph(figure=fig,id='fig'),
                       html.A('Like watching video speed up? Try the Video speed controlled Google extension', href='https://chrome.google.com/webstore/detail/video-speed-controller/nffaoalbilbmmfgbnbgppjihopabppdk?hl=en',target='_blank'),
dcc.Checklist(options=[{"label":"What you eliminate shows on consider rating?",'value':'Yes'}],value=["Yes"],labelStyle={'display':'inline-block'},id="checkbox_rating"),
                       dcc.Slider(min=0,max=10,step=.5,value=5,marks={i:str(i) for i in range(0,11)},id='slider_id'),
                       #dash_table.DataTable(id='table1', columns=[{"name": i, "id": i} for i in df.columns],data=df.to_dict('records'),style_table={'overflowY': 'scroll'}),
                       html.Div(id="table2")
                       ]) # first object is called childern = text to display
@app.callback(
    Output(component_id='table2',component_property='children'),
    [Input(component_id='city_checkbox',component_property='value'),Input(component_id='checkbox_rating',component_property='value'),
     Input(component_id='slider_id',component_property='value'),
     Input(component_id='and_or',component_property='value')] # where are u getting it from(component id) and what we getting(property)
)
def update_div(genre,bi,slider_value,and_or):
    list_ = []
    for z in range(len(df)):
        list_temp = 0
        for m in range(len(genre)):
            if len(genre)==0:
                continue
            if df.iloc[z, 6]== genre[m]:
                if len(and_or)!=0:
                    continue
                list_temp =list_temp+1
            if df.iloc[z, 7] == genre[m]:
                if len(and_or)!=0:
                    continue
                list_temp = list_temp + 1
            if df.iloc[z, 8] == genre[m]:
                if len(and_or)!=0:
                    continue
                list_temp = list_temp + 1
            if list_temp ==0:
                list_.append(z)
    global xy
    xy = df.drop(list_, axis=0)
    if len(bi)==1:
        xy = xy[xy.rating!="No avaiable"]
        for f in range(len(xy)):
            xy.iloc[f,5] = float(xy.iloc[f,5])
        xy = xy[xy.rating >= float(slider_value)]


    return new_table(xy)

@app.callback(
    Output(component_id='fig2',component_property='children'),
    [Input(component_id='city_checkbox',component_property='value')]
)
def update_fig():
    fig3 = px.bar(xy,x="genre1",y="total_mins")

    print(xy)
    print("HI")
    return fig3

if __name__ == '__main__':
    app.run_server(debug=True)