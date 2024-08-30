import dash_mantine_components as dmc
import os
from dash import html, dcc, Input, Output, State, _dash_renderer, callback, Dash, page_container
from dash_iconify import DashIconify
import dash
import pandas as pd
import numpy as np

_dash_renderer._set_react_version("18.2.0")



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


# Binary column indicating whether the track genre is acoustic.
df['is_acoustic'] = df['track_genre'].apply(lambda x: 'acoustic' in x.lower())


theme_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon='radix-icons:sun', width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon='radix-icons:moon', width=25), darkHidden=True)
    ],
    variant='transparent',
    color='orange',
    id='color-scheme-toggle',
    size='lg',
    ms='auto'
)

header = dmc.Group(
    [
        dmc.Burger(id='burger-button', opened=False, hiddenFrom='md'),
        dmc.Text(['Music Insight'], size='xl', fw=700),
        theme_toggle
    ],
    justify='flex-start',
)

# developing the sidebar Wrapped in a scrollArea for better Ux
navbar = dmc.ScrollArea(
    [
        dmc.Text('Sidebar Content', fw=700),
        dmc.NavLink(label='Introduction and Data Table', href="/"),
        dmc.NavLink(label='Data Analysis', href="/pages.Intro_dataset"),
        dmc.NavLink(label='Music Recommendation', href="/pages.recommendation_system"),
        dmc.Select(
            id='dropdown_danceability_level',
            label='Select danceabile Music Level',
            data=[{'label': danceability_level, 'value': danceability_level} for danceability_level in df['danceability_level'].dropna().unique()],
            value=df['danceability_level'].dropna().iloc[0],
            clearable=True,
            style={'marginBottom': "20px"}
        ),
        dmc.Select(
            id='dropdown_popularity_level',
            label='Select danceabile Music Level',
            data=[{'label': popularity_level, 'value': popularity_level} for popularity_level in df['popularity_level'].dropna().unique()],
            value=df['popularity_level'].dropna().iloc[0],
            clearable=True,
            style={'marginBottom': "20px"}
        )


    ],
    offsetScrollbars=True,
    type='scroll',
    style={'height': '100%'}, 
),
def chart_content():
    return dmc.Group([
        dmc.BarChart(id="chart", container={}, style={'width': '45%'}),
        dmc.PieChart(id="chart", container={}, style={'width': '45%'}),
        dmc.BarChart(id="chart", container={}, style={'width': '50%'})
],
justify='md'
    )


#page_content = dash.page_container



stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]
# 
app = Dash(__name__, 
           external_stylesheets=stylesheets,
           use_pages=True,
           pages_folder="pages",
           suppress_callback_exceptions=True,
            prevent_initial_callbacks=False,
           )

app_shell = dmc.AppShell(
    children=[
        dmc.AppShellHeader(header, px=26),
        dmc.AppShellNavbar(navbar, p=25),
        dmc.AppShellNavbar(page_container),
     
    ]
)
app.layout = dmc.MantineProvider(
    children=[
        dcc.Store(id='theme_store', storage_type="local", data='light'),
        app_shell,
    ],
    id='mantine-provider',

    forceColorScheme='light'
)
@callback(Output('mantine_provider', 'forceColorScheme'),
          Input('color-scheme-toggle', 'n_clicks'),
          State('mantine-provider', 'forceColorScheme'),
          
          
          )

def switch_theme(n_clicks, theme):
    return "dark" if theme == "light" else "light"

if __name__=="__main__":
    app.run(debug=True, port=6060)