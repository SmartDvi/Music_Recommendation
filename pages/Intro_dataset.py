

from dash import html, dcc, callback, Input, Output, Dash, register_page
import plotly.express as px
import dash_ag_grid as dag
import dash_mantine_components as dmc
import pandas as pd
import numpy as np


register_page(__name__, path="/",
                   name='Dataset and  Overview',
                   order=0)

from utils import df

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
        resetColumnState=True,
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
