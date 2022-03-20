import dash.exceptions
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df_stud1 = pd.read_csv('student-mat.csv', sep=';')
df_stud2 = pd.read_csv('student-por.csv', sep=';')
df_students = pd.concat([df_stud1, df_stud2], axis=0)

male_data = df_students.query('sex=="M"')
female_data = df_students.query('sex=="F"')

df_students = pd.concat([df_stud1, df_stud2], axis=0)
df_students_Join = df_stud1.merge(df_stud2,
                                  on=["school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob",
                                      "Fjob", "reason", "nursery", "internet"])
df_students.groupby(
    ["school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob", "reason", "nursery",
     "internet"]).mean()
df_students

# --------------------------------------------------------------------------------------------------------------#
# A- The effect of Studying Time and having Internet access on th performance of the Students
df_SI_Time = df_students.loc[:, ["studytime", "internet", "G1", "G2", "G3"]]
df_SI_Time["Grade"] = round((df_SI_Time["G1"] + df_SI_Time["G2"] + df_SI_Time["G3"]) / 3, 2)
df_SI_Time = df_SI_Time.loc[:, ["internet", "studytime", "Grade"]]
df_SI_Time = (df_SI_Time.groupby(["internet", "studytime", "Grade"]).size()
              .sort_values(ascending=False)
              .reset_index(name='Number of Students'))
df_SI_Time = df_SI_Time.sort_values(by=["studytime"])
fig0 = px.histogram(df_SI_Time, y="Number of Students", x="Grade", color="internet", facet_col="studytime")
fig0.update_layout(title_text='The effect of Studying Time and having Internet access on the performance of the '
                              'Students', title_x=0.5, margin=dict(t=100))
# --------------------------------------------------------------------------------------------------------------#

# B - the impact of study time and free time on studdent performance
df_SF_Time = df_students.loc[:, ["studytime", "failures", "G1", "G2", "G3"]]
df_SF_Time["Grade"] = round((df_SF_Time["G1"] + df_SF_Time["G2"] + df_SF_Time["G3"]) / 3, 2)
df_SF_Time = df_SF_Time.loc[:, ["studytime", "failures", "Grade"]]
df_SF_Time = (df_SF_Time.groupby(["studytime", "failures", "Grade"]).size()
              .sort_values(ascending=False)
              .reset_index(name='Number of Students'))
df_SF_Time = df_SF_Time.sort_values(by=["studytime", "failures", "Number of Students", "Grade"])
df_SF_Time

fig1 = px.scatter(df_SF_Time, x="Grade", y="Number of Students", color="failures", facet_col="studytime",
                  color_continuous_scale="deep_r")
fig1.update_layout(title_text='The impact of study time on the number of past class Failures',
                   title_x=0.5, margin=dict(t=100))
# --------------------------------------------------------------------------------------------------------------#
# H- the effect of having family, School support and Private classes on performance of students
df_support = df_students.loc[:, ["schoolsup", "famsup", "paid", "G1", "G2", "G3"]]
df_support["Grade"] = round((df_support["G1"] + df_support["G2"] + df_support["G3"]) / 3, 2)
df_support = df_support.loc[:, ["schoolsup", "famsup", "paid", "Grade"]]
df_support["schoolsup"] = df_support.schoolsup.map(dict(yes=1, no=0))
df_support["famsup"] = df_support.famsup.map(dict(yes=1, no=0))
df_support["paid"] = df_support.paid.map(dict(yes=1, no=0))
df_support["support"] = df_support['schoolsup'].astype(str) + df_support['famsup'].astype(str) + df_support[
    'paid'].astype(str)
df_support = df_support.sort_values(by=["support"])
df_support["support"] = df_support.support.replace({'000': 'No support',
                                                    '001': 'Private classes',
                                                    '010': 'Family',
                                                    '100': 'School',
                                                    '011': 'Family & Private classes',
                                                    '110': 'School & Family',
                                                    '101': 'School & Private classes',
                                                    '111': 'School & Family & Private classes'})
df_support = (df_support.groupby(["support", "Grade"]).size()
              .sort_values(ascending=False)
              .reset_index(name='Number of Students'))
df_support = df_support.sort_values(by=["Grade"])

# --------------------------------------------------------------------------------------------------------------#
# E-  the performance level difference between genders an ages
df_gender_ages = df_students.loc[:, ["sex", "age", "G1", "G2", "G3"]]
df_gender_ages["Grade"] = round((df_gender_ages["G1"] + df_gender_ages["G2"] + df_gender_ages["G3"]) / 3, 2)
df_gender_ages = df_gender_ages.loc[:, ["sex", "age", "Grade"]]
df_gender_ages = (df_gender_ages.groupby(["sex", "age", "Grade"]).size()
                  .sort_values(ascending=False)
                  .reset_index(name='#Students'))
df_gender_ages = df_gender_ages.sort_values(by=["Grade", "#Students", "age"])

# --------------------------------------------------------------------------------------------------------------#
# 6-the effect of mother and father backgounrd(education and jobs) on student aiming for higher education
df_S_bkgrd=df_students.loc[:,["Medu","Fedu","Mjob","Fjob","higher","G1","G2","G3"]]
df_S_bkgrd["Grade"]=round((df_S_bkgrd["G1"]+df_S_bkgrd["G2"]+df_S_bkgrd["G3"])/3,2)
df_S_bkgrd=df_S_bkgrd.loc[:,["Medu","Fedu","Mjob","Fjob","Grade","higher"]]

df_S_bkgrd["Medu1"] = df_S_bkgrd.Medu.map({0: 'Numeric',
                                                    1: 'Primary 1st -> 4th',
                                                    2: 'Primary 5th -> 9th',
                                                    3: 'Secondary',
                                                    4: 'Higher'})
df_S_bkgrd["Fedu1"] = df_S_bkgrd.Fedu.map({0: 'Numeric',
                                                    1: 'Primary 1st -> 4th',
                                                    2: 'Primary 5th -> 9th',
                                                    3: 'Secondary',
                                                    4: 'Higher'})

df_S_bkgrd["Mjob1"]=df_S_bkgrd.Mjob.map(dict(teacher=0, health=1, services=2, at_home=3,other=4))
df_S_bkgrd["back"]=df_S_bkgrd["Mjob"].copy()
df_S_bkgrd["Mjob"]=df_S_bkgrd["Mjob1"].copy()
df_S_bkgrd["Mjob1"]=df_S_bkgrd["back"].copy()

df_S_bkgrd["Fjob1"]=df_S_bkgrd.Fjob.map(dict(teacher=0, health=1, services=2, at_home=3,other=4))
df_S_bkgrd["back1"]=df_S_bkgrd["Fjob"].copy()
df_S_bkgrd["Fjob"]=df_S_bkgrd["Fjob1"].copy()
df_S_bkgrd["Fjob1"]=df_S_bkgrd["back1"].copy()

df_S_bkgrd_MF=df_S_bkgrd.loc[:,["Medu","Medu1","Mjob","Mjob1","Fedu","Fedu1","Fjob","Fjob1","Grade","higher"]]
df_S_bkgrd_MF=(df_S_bkgrd_MF.groupby(["Medu","Medu1","Mjob","Mjob1","Fedu","Fedu1","Fjob","Fjob1","Grade","higher"]).size()
       .sort_values(ascending=False)
       .reset_index(name='Number of Students'))
df_S_bkgrd_MF=df_S_bkgrd_MF.sort_values(by="Grade")
df_S_bkgrd_MF



# Application  Dash
#external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__)
server=app.server
app.layout = html.Div(children=[

    html.H1(children='Student Performance'),

    html.Div(children=[
        dcc.Graph(id='SF_Time',
                  figure=fig0)
    ]),
    dcc.Graph(
        id='SI_Performance',
        figure=fig1
    ),
    html.Div(children=[
        html.H6("Supporter 1"),
        dcc.Dropdown(sorted(df_support['support'].unique()), "Family", id='support_drop')

    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div(children=[
        html.H6("Supporter 2"),
        dcc.Dropdown(sorted(df_support['support'].unique()), "School", id='support_drop1')

    ], style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='ScFmPa_S_Time'),

    html.Div(children=[
        html.H6("From Age"),
        dcc.Dropdown(sorted(df_gender_ages['age'].unique()), 15, id='age_drop')

    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div(children=[
        html.H6("To Age"),
        dcc.Dropdown(sorted(df_gender_ages['age'].unique()), 15, id='age_drop_1')

    ], style={'width': '48%', 'display': 'inline-block'}),
    dcc.Graph(id='Sex_Age_Grades'),

    html.Div(children=[
    html.H6("Mother Education"),
    dcc.Slider(0, 4,
               step=None,
               id='slider_Medu',
               marks={0: 'Numeric',
                      1: 'Primary 1st -> 4th',
                      2: 'Primary 5th -> 9th',
                      3: 'Secondary',
                      4: 'Higher'},
               value=4
               )],style={'width': '50%', 'display': 'inline-block'}),
    html.Div(children=[
        html.H6("Mother Job"),
        dcc.Slider(0, 4,
                   step=None,
                   id='slider_Mjob',
                   marks={0: 'Teacher',
                          1: 'Health',
                          2: 'Services',
                          3: 'At_home',
                          4: 'Other'},
                   value=4
                   )], style={'width': '50%', 'display': 'inline-block'}),
    html.Div(children=[
        html.H6("Father Education"),
        dcc.Slider(0, 4,
                   step=None,
                   id='slider_Fedu',
                   marks={0: 'Numeric',
                          1: 'Primary 1st -> 4th',
                          2: 'Primary 5th -> 9th',
                          3: 'Secondary',
                          4: 'Higher'},
                   value=4
                   )], style={'width': '50%', 'display': 'inline-block'}),
    html.Div(children=[
    html.H6("Father Job"),
    dcc.Slider(0, 4,
               step=None,
               id='slider_Fjob',
               marks={0: 'Teacher',
                      1: 'Health',
                      2: 'Services',
                      3: 'At_home',
                      4: 'Other'},
               value=4
               )],style={'width': '50%', 'display': 'inline-block'}),
    dcc.Graph(id='Medu_Mjob_Higher')


])


@app.callback(
    Output(component_id='ScFmPa_S_Time', component_property='figure'),
    Input(component_id='support_drop', component_property='value'),
    Input(component_id='support_drop1', component_property='value'))
def update_graph(support_drop, support_drop1):
    df = df_support[(df_support['support'] == support_drop) | (df_support['support'] == support_drop1)]
    fig = px.line(df, y="Number of Students", x="Grade", color=df_support.columns[0])
    fig.update_layout(
        title_text='The effect of having Family, School Support and Private Classes on Student Performance',
        title_x=0.5, margin=dict(t=100))
    return fig


@app.callback(
    Output(component_id='Sex_Age_Grades', component_property='figure'),
    Input(component_id='age_drop', component_property='value'),
    Input(component_id='age_drop_1', component_property='value'))
def update_graph_1(age_drop, age_drop_1):
    if age_drop > age_drop_1:
        temp = age_drop
        age_drop = age_drop_1
        age_drop_1 = temp
    df = df_gender_ages[(df_gender_ages['age'] >= age_drop) & (df_gender_ages['age'] <= age_drop_1)]
    df = df.sort_values(by=["age"])
    fig_t = px.area(df, x="Grade", y="#Students", color='sex',
                    facet_row='sex', facet_col='age')
    fig_t.update_layout(
        title_text='Grades analysis between Genders and ages',
        title_x=0.5, margin=dict(t=100))
    return fig_t


@app.callback(
    Output(component_id='Medu_Mjob_Higher', component_property='figure'),
    Input(component_id='slider_Medu', component_property='value'),
    Input(component_id='slider_Mjob', component_property='value'),
    Input(component_id='slider_Fedu', component_property='value'),
    Input(component_id='slider_Fjob', component_property='value'))
def update_graph_2(slider_Medu, slider_Mjob,slider_Fedu, slider_Fjob):
    df = df_S_bkgrd_MF[(df_S_bkgrd_MF['Medu'] == slider_Medu) & (df_S_bkgrd_MF['Mjob'] == slider_Mjob) |
                       (df_S_bkgrd_MF['Fedu'] == slider_Fedu) & (df_S_bkgrd_MF['Fjob'] == slider_Fjob)]
    df = df.sort_values(by=["Grade"])
    fig_t = px.bar(df, x="Grade", y="Number of Students", color='higher')
    fig_t.update_layout(
        title_text='The effect of Mother and Father background on Grades & Number of students aiming for higher education',
        title_x=0.5, margin=dict(t=100))
    return fig_t

if __name__ == '__main__':
    app.run_server(debug=True)
