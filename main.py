import pandas as pd
import numpy as np
from dash import dcc, Dash, Input, Output, callback,html, State, _dash_renderer
import dash_ag_grid
from dash_iconify import DashIconify
import dash_mantine_components as dmc

_dash_renderer._set_react_version("18.2.0")

df = pd.read_csv('C:\\Users\\Moritus Peters\\Downloads\\dataset.csv')

#Convert duration_ms to minutes for better interpretability
df['duration_min'] = df['duration_ms'] / 60000

#Categorize the loudness into levels (e.g., Quiet, Moderate, Loud).
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
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ],
    variant='transparent',
    color='yellow',
    id="color-scheme-toggle",
    ms='auto')

header =dmc.Group(
    [
        dmc.Burger(id="burger-button", opened=False, hiddenFrom="md"),
        dmc.Text(["Spotify Music Analysis"], size="xl", fw=700),
        theme_toggle
    ],
    justify="flex-start",
)

navbar = dcc.Loading(
    dmc.ScrollArea(
        [
            dmc.Text('Sidebar Content', fw=700),
            dmc.Space(h="md"),
            dmc.NavLink(label='Introduction and Data Table', href="/intro_dataset"),
            dmc.Space(h="md"),
            dmc.NavLink(label='Data Analysis', href="/data_analysis"),
            dmc.Space(h="md"),
            dmc.NavLink(label='Music Recommendation', href="/pages.recommendation_system"),
            dmc.Space(h="md"),
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
        type="scroll",
        style={"height": "100%"},
    ),
)
"""
def chart_content():
    return dmc.Group(
        [
            dcc.Graph(id="chart-1", figure={}, style={"width": "45%"}),
            dcc.Graph(id="chart-2", figure={}, style={"width": "45%"})
        ]
    )
# Define the layouts for different pages
page_1_layout = dmc.Container([chart_content()])
page_2_layout = dmc.Container([chart_content()])
page_3_layout = dmc.Container([chart_content()])

page_content = [dmc.Text("Your page content"), 
                chart_content()]"""

stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]


app = Dash(__name__, 
           external_stylesheets=stylesheets,
           use_pages=True,
           pages_folder="pages",
           suppress_callback_exceptions=True,
            prevent_initial_callbacks=False,
           )

app_shell = dmc.AppShell(
    [
        dmc.AppShellHeader(header, px=25),
        dmc.AppShellNavbar(navbar, p=24),
        dmc.AppShellAside("Aside", withBorder=False),
        #dmc.AppShellMain(page_content),
        dmc.AppShellFooter("Footer")
    ],
    header={"height": 70},
    padding="xl",
    navbar={
        "width": 375,
        "breakpoint": "md",
        "collapsed": {"mobile": True},
    },
    aside={
        "width": 300,
        "breakpoint": "xl",
        "collapsed": {"desktop": False, "mobile": True},
    },
    id="app-shell",
)


app.layout = dmc.MantineProvider(
    [
        dcc.Store(id="theme-store", storage_type="local", data="light"),
        app_shell
    ],
    id="mantine-provider",
    forceColorScheme="light",
)




@callback(
    Output("app-shell", "navbar"),
    Input("burger-button", "opened"),
    State("app-shell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar




@callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def switch_theme(_, theme):
    return "dark" if theme == "light" else "light"

"""
# Define pages with dynamic content
app.validation_layout = html.Div([
    page_1_layout,
    page_2_layout,
    page_3_layout
])

# Register the pages
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/page2":
        return page_2_layout
    elif pathname == "/page3":
        return page_3_layout
    else:
        return page_1_layout


"""
if __name__ == "__main__":
    app.run_server(debug=True, port = 8080)

