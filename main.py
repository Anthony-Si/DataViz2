
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np

app = Dash(__name__)



df_stud1=pd.read_csv('C:\\Users\\asiam\\PycharmProjects\\DataViz2\\student-mat.csv',sep=';')
#print(df_stud1.info())

df_stud2=pd.read_csv('C:\\Users\\asiam\\PycharmProjects\\DataViz2\\student-por.csv',sep=';')
#print(df_stud2.info())

df_students = pd.concat([df_stud1, df_stud2], axis=0)
#df_students=df_stud1.merge(df_stud2, how='outer', on='school')
#print(df_students.info())
male_data=df_students.query('sex=="M"')
female_data=df_students.query('sex=="F"')

#sex_infos=df_students.groupby(by="age").mean()
#print(sex_infos.head())
fig=go.Figure()

fig.add_trace(go.Bar(x=male_data['age'], y=male_data['G1'], name='male'))
fig.add_trace(go.Bar(x=female_data['age'], y=female_data['G1'], name='female'))

df_totalG1=df_students.groupby(by='age').sum()
annot =[dict(
    x=xi,
    y=yi,
    text=str(yi),
    xanchor='auto',
    yanchor='bottom',
    showarrow=False
) for xi, yi in zip(df_totalG1.index, df_totalG1['G1'])]

fig.update_layout(barmode='stack', annotations=annot)
fig.show()


#fig = px.treemap(df.sort_values(by="position", ascending=True).head(20), path=['country','city'], values='total score')
#fig.update_traces(root_color="lightgrey")

app.layout = html.Div(children=[
    html.H1(children='Presentation'),

    html.Div(children='''
        Blahblah
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    html.Div(children='''
        presentation 2
    '''),

    dcc.Graph(
        id='example-graph',
        #figure=fig2
    )

])



if __name__ == '__main__':
    app.run_server(debug=True)




