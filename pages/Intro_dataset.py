

from dash import html, dcc, callback, Input, Output, Dash, register_page
from dash_iconify import DashIconify
import plotly.express as px
import dash_ag_grid as dag
import dash_mantine_components as dmc
import pandas as pd
import numpy as np
import dash

#dash.register_page(__name__, 
#                   name='Dataset and  Overview',
 #                  order=0)

df = pd.read_csv('C:\\Users\\Moritus Peters\\Downloads\\dataset.csv')

#duration_min: Convert duration_ms to minutes for better interpretability
df['duration_min'] = df['duration_ms'] / 60000

#loudness_level: Categorize the loudness into levels (e.g., Quiet, Moderate, Loud).
df['loudness_level'] = pd.cut(df['loudness'], bins=[-60, -20, -10, 0], labels=['Quiet', 'Moderate', 'Loud'])

#energy_level: Categorize energy into low, medium, and high levels.
df['energy_level'] = pd.cut(df['energy'], bins=[0, 0.33, 0.66, 1], labels=['Low', 'Medium', 'High'])

# danceability_level: Create categories for danceability (e.g., Low, Medium, High).
df['danceability_level'] = pd.cut(df['danceability'], bins=[0, 0.33, 0.66, 1], labels=['Low', 'Medium', 'High'])

# tempo_category: Categorize tempo into different musical tempo categories (e.g., Slow, Medium, Fast).
df['tempo_category'] = pd.cut(df['tempo'], bins=[0, 60, 120, 180, 300], labels=['Slow', 'Medium', 'Fast', 'Very Fast'])

# explicit_flag: Convert explicit boolean into a more descriptive text (Explicit, Non-Explicit).
df['explicit_flag'] = df['explicit'].replace({True: 'Explicit', False: 'Non-Explicit'})

# popularity_level: Categorize popularity into levels (e.g., Low, Medium, High).
df['popularity_level'] = pd.cut(df['popularity'], bins=[0, 50, 75, 100], labels=['Low', 'Medium', 'High'])


# mood_indicator: Use valence and energy to create a mood indicator (e.g., Happy, Energetic, Sad, Calm).
conditions = [
    (df['valence'] > 0.5) & (df['energy'] > 0.5),
    (df['valence'] > 0.5) & (df['energy'] <= 0.5),
    (df['valence'] <= 0.5) & (df['energy'] > 0.5),
    (df['valence'] <= 0.5) & (df['energy'] <= 0.5)
]
choices = ['Happy', 'Calm', 'Energetic', 'Sad']

# ensure that the default value is alsoo a string to aviod dta type conflict
df['mood_indicator'] = np.select(conditions, choices, default='Unknown')

# is_acoustic: Binary column indicating whether the track genre is acoustic.
df['is_acoustic'] = df['track_genre'].apply(lambda x: 'acoustic' in x.lower())


columns = df.columns

# fetching columns
column_df = []
for col in columns:
    column_type = 'numericColumn' if pd.api.types.is_numeric_dtype(df[col]) else \
                    'dateColumn' if pd.api.types.is_datetime64_any_dtype(df[col]) else \
                    'textColumn'
    
column_df.append({
    'headerName': col,
    'field': col,
    'type': column_type
    })


dash.register_page(__name__, 
                   name='Dataset and  Overview',
                   order=0)


layout = dmc.MantineProvider([
    dmc.Text('Your welcome, this Dashboad is detail with insightfull information on this Music dataset', ta='center', style={'fontSize': 'lg'}, className='text-center'),
    dmc.Space(h=20),
    dmc.Text('The Music Dataset'),
    dmc.Text('This table has great features that all you to filter, drag theedges of the columns, and intract more dynamically.'),
    dmc.Space(h=20),
        
    dmc.Text(' The Music Dataset'),
    dmc.Text('this table has great feature that you can filter, drag the edge of the columns , the rows or columns and more than excel sheet'),
    dag.AgGrid(
        id='data-table',
        columnDefs=column_df, 
        rowData=df.to_dict('records'),
        style={'height': '400px', 'width': '100%'}, 
        resetColumnState=False,
        exportDataAsCsv=False,
        selectAll=False,
        deselectAll=False,
        enableEnterpriseModules=False,
        updateColumnState=False,
        persisted_props=['selectedRows'],
        persistence_type='local',
        suppressDragLeaveHidesColumns=True,
        dangerously_allow_code=False,
        rowModelType='clientSide',
        defaultColDef={'sortable': True, 'filter': True, 'resizable': True}
    )
])
