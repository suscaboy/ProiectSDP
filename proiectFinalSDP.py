# -*- coding: utf-8 -*-
"""proiectFinalSDP

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Af8pUrEFyg0S_T53y2ATPBhWw-QviBVp

# Proiect final SDP 
# Tema lucrarii : Paralelizare în limbajul python : libraria Dask

Setul de date se gaseste la adresa https://catalog.data.gov/dataset/arrest-data-from-2020-to-present

Datele se refera la numarul persoane arestate in Los Angeles(S.U.A.) incepand cu data de 01.01.2020
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install "dask[complete]"

"""Importul librariilor """

import numpy as np 
import pandas as pd 

import dask 
import dask.array as da
import dask.dataframe as dd
import dask.delayed as delayed
import datetime
from datetime import datetime

"""# Calculul pentru timpul scurs pentru citirea fisierului .csv

Libraria pandas
"""

times_start = datetime.now()
dfPandas = pd.read_csv('/content/Arrest_Data_from_2020_to_Present.csv')
time_elapsed = datetime.now () - times_start
print('Timpul scurs (hh:mm:ss.ms) = ',format(time_elapsed))

"""Libraria dask"""

times_start = datetime.now()
dfDask = dd.read_csv('/content/Arrest_Data_from_2020_to_Present.csv', blocksize = '2 MB', dtype={'Time': 'float32', 'Age' : 'float32'} )
time_elapsed = datetime.now () - times_start
print('Timpul scurs (hh:mm:ss.ms) = ',format(time_elapsed))

dfDask.npartitions

"""Din cele doua secvente de cod de mai sus se poate observa importul datelor in structurile de tip DataFrame a fost net superior in cazul librariei Dask."""

dfDask.columns

"""# Cateva date statistice referitoare la setul de date """

import os 

numeFisier = '/content/Arrest_Data_from_2020_to_Present.csv'
marimeFisier = os.path.getsize(numeFisier)
print(f' Marimea fisierului .CSV este de {marimeFisier / (1024 * 1024)} MB')

dfDask.info

dfDask.columns.size

dfDask.dtypes

dfPandas.shape

"""# Gruparea datelor

Am grupat tipul de raport dupa sex

Pandas
"""

times_start = datetime.now()

dfPandas1 = dfPandas.groupby(['Sex Code'])['Report Type'].count()

time_elapsed = datetime.now () - times_start
print('Timpul scurs (hh:mm:ss.ms) = ',format(time_elapsed))

dfPandas1

"""Dask"""

times_start = datetime.now()

dfDask1 = dfDask.groupby(['Sex Code'])['Report Type'].count()

time_elapsed = datetime.now () - times_start
print('Timpul scurs (hh:mm:ss.ms) = ',format(time_elapsed))

dfDask1

"""Si in acest caz se observa timpul superior de rulare a Dataframe-ului Dask

Afisarea GRAFULUI  de taskuri

- cercurile reprezinta taskurile sau functiile 
 - patratele reprezinta output-urile sau rezultatele
"""

dfDask.visualize()

dfDask1.visualize()

"""# Partitionarea si indexarea dataframe-ului Dask

Un exemplu de diferente intre partitia 4 si partitia 5 a dataframe-ului dask

Partitia 4
"""

dfDask2 = dfDask.get_partition(3)

dfDask2.index.min().compute()

dfDask2.index.max().compute()

"""Partitia 5"""

dfDask3 = dfDask.get_partition(4)

dfDask3.index.min().compute()

dfDask3.index.max().compute()

"""Din exemplele de mai sus se observa faptul ca nu exista un index comun care sa se intinda pe toate partitiile. 
Deci fiecare partitie are propriul sau index.
Aceasta inseamna ca nu putem diviza dataframe-ul dupa index.

Totusi o solutie ar fi selectia unei coloane care poate fi folosita ca index, insa aceasta duce la un timp de rulare foarte mare, motiv pentru care este indicat sa se foloseasca decat o singura data.

Pentru setul de date ales de catre mine am selectat ca index coloana "Report ID"
"""

dfDask.divisions

dfDask4 = dfDask.set_index('Report ID')

dfDask4.divisions

dfDask4.visualize()

"""# Curatarea datelor

Pandas
"""

times_start = datetime.now()

dfPandasClean = dfPandas.drop(['Time','Area ID','Area Name','Reporting District', 'Descent Code', 'Charge Group Code',
                               'Arrest Type Code', 'Charge', 'Charge Description', 'Disposition Description', 'Address',
                               'Cross Street', 'Location', 'Booking Date', 'Booking Time', 'Booking Location',
                               'Booking Location Code'], axis = 1).dropna()

time_elapsed = datetime.now () - times_start
print('Timpul scurs (hh:mm:ss.ms) = ',format(time_elapsed))

print(dfPandasClean['Charge Group Description'])

"""Dask"""

times_start = datetime.now()

dfDaskClean = dfDask.drop(['Time','Area ID','Area Name','Reporting District', 'Descent Code', 'Charge Group Code',
                               'Arrest Type Code', 'Charge', 'Charge Description', 'Disposition Description', 'Address',
                               'Cross Street', 'Location', 'Booking Date', 'Booking Time', 'Booking Location',
                               'Booking Location Code'], axis = 1).dropna()

time_elapsed = datetime.now () - times_start
print('Timpul scurs (hh:mm:ss.ms) = ',format(time_elapsed))

dfDaskClean.visualize()

# Commented out IPython magic to ensure Python compatibility.
# %time df = dfDaskClean.compute()   # optional

"""# Vizualizarea datelor """

df.shape           # dupa curatarea datelor am ramas cu 54138 randuri

df['Arrest Date'] = pd.to_datetime(df['Arrest Date'], infer_datetime_format=True )
df['Age'] = df['Age'].astype(int)

df = df.loc[(df['Age'] > 18) & (df['Age'] < 100 )]

df.info()

import matplotlib.pyplot as plt
import seaborn as sns

fig = plt.figure(figsize=(10, 10)) 
sns.set(style = 'white')
df['Report Type'].value_counts().plot(kind='bar',color='r',align='center')
plt.title('Tipul de rapoarte', fontsize=20)
plt.ylabel('NUmarul de Rapoarte')

fig = plt.figure(figsize=(10, 10)) 
sns.set(style = 'white')
df['Charge Group Description'].value_counts().plot(kind='bar',color='r',align='center')
plt.title('Categorii de infractiuni ', fontsize=20)
plt.ylabel('Numar de persoane')
plt.xticks(rotation = '90')

df1= df.loc[(df['Charge Group Description'] == 'Driving Under Influence') & (df['Sex Code'] == 'F')]

df1

df1.info()

fig = plt.figure(figsize=(5, 5)) 
sns.set(style = 'white')
df1['Charge Group Description'].value_counts().plot(kind='bar',color='b',align='center')
plt.title('Persoane de sex feminin aflate sub influenta ', fontsize=20)
plt.ylabel('Numar de persoane')
plt.xticks(rotation = '90')

old = df[df.Age == df.Age.max()]

old