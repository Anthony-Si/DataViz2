
import pandas as pd
import numpy as np


df_stud1=pd.read_csv('student-mat.csv',sep=';')
print(df_stud1.info())


df_stud2=pd.read_csv('student-por.csv',sep=';')
print(df_stud2.info())

df_students = pd.concat([df_stud1, df_stud2], axis=0)
df_students=df_stud1.merge(df_stud2, how='outer', on='school')


print(df_students.info())
male_data=df_students.query('sex_x=="M"')
female_data=df_students.query('sex_x=="F"')

print(male_data)
#sex_infos=df_students.groupby(by="age_x").mean()
#print(sex_infos.head())




