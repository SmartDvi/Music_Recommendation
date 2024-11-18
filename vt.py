import dash_mantine_components as dmc
from dash import *

from utils import df


register_page(__name__, path="/insights",
              name='insight', order=2)



# Reusable function for metric cards
def create_metric_card(title, value, color):
    return dmc.Card(
        dmc.Group(
            [
                dmc.Text(title, size="sm", c="dimmed"),
                dmc.Text(value, size="xl", c=color, fw=700)
            ],
            justify="center"
        ),
        withBorder=True, shadow="sm", radius="md", p="lg"
    )

# Layout
layout = dmc.MantineProvider(
    [
        # Header
        dmc.Container(
            dmc.Text(
                'Insight Dashboard',
                tt="uppercase", size="xl", c="indigo", ta="center",
                td="underline", fw=700, py=20
            ),
            fluid=True
        ),

        # Key Metrics Section
        dmc.Container(
            dmc.Grid(
                [
                    dmc.GridCol(create_metric_card("Total Tracks", "1,200", "blue"), span=3),
                    dmc.GridCol(create_metric_card("Average Popularity", "68%", "green"), span=3),
                    dmc.GridCol(create_metric_card("Top Genre", "Acoustic", "purple"), span=3),
                    dmc.GridCol(create_metric_card("Average Duration (min)", "3.5", "teal"), span=3),
                ],
                gutter="xl"
            ),
            fluid=True, py=20
        ),

        # Main Insights Section
        dmc.Container(
            dmc.Grid(
                [
                    # Long GridCol in the center
                    dmc.GridCol(
                        dmc.Paper(
                            [
                                dmc.Text(
                                    "Key Matrix Analysis", size="lg", fw=600,
                                    ta="center", mb=15
                                ),
                                dmc.Container(id="key_matrix", style={"height": "700px"})
                            ],
                            p="lg", shadow="sm", radius="md", withBorder=True
                        ),
                        span=4 
                    ),

                    # Supporting Charts - Left Side
                    dmc.GridCol(
                        dmc.Paper(
                            [
                                dmc.Text("Popularity Insights", size="sm", fw=600, mb=10),
                                dmc.Container(id="popularity_chart", style={"height": "300px"})
                            ],
                            p="md", shadow="sm", radius="md", withBorder=True
                        ),
                        span=3
                    ),

                    # Supporting Charts - Right Side
                    dmc.GridCol(
                        dmc.Grid(
                            [
                                # Genre Distribution and Mood Analysis
                                dmc.GridCol(
                                    dmc.Paper(
                                        [
                                            dmc.Text("Genre Distribution", size="sm", fw=600, mb=10),
                                            dmc.Container(id="genre_chart", style={"height": "300px"})
                                        ],
                                        p="md", shadow="sm", radius="md", withBorder=True
                                    ),
                                    span=5
                                ),
                                dmc.GridCol(
                                    dmc.Paper(
                                        [
                                            dmc.Text("Mood Analysis", size="sm", fw=600, mb=10),
                                            dmc.Container(id="mood_chart", style={"height": "300px"})
                                        ],
                                        p="md", shadow="sm", radius="md", withBorder=True
                                    ),
                                    span=5
                                ),
                                # Acoustic Features
                                dmc.GridCol(
                                    dmc.Paper(
                                        [
                                            dmc.Text("Acoustic Features", size="sm", fw=600, mb=10),
                                            dmc.Container(id="acoustic_chart", style={"height": "300px"})
                                        ],
                                        p="md", shadow="sm", radius="md", withBorder=True
                                    ),
                                    span=12  # Full-width under Genre and Mood
                                ),
                            ],
                            gutter="sm"
                        ),
                        span=3
                    ),
                ],
                gutter="xl"
            ),
            fluid=True, py=20
        ),
    ]
)










def popularity_level(danceability_level, loudness_level):
    filtered_df = df[(df['loudness_level'] == danceability_level) & (df['loudness_level'] == loudness_level)]
    df_ch = filtered_df.groupby('danceability_level').agg(
        {
          'danceability': 'sum',
          'energy': 'summ'  
        }
    ).reset_index()

    sd = [
        {
            'name':'danceability',
            'data': df_ch.to_dict('records'),
            'color':'red',

        },
         {
            'name':'energy',
            'data': df_ch.to_dict('records'),
            'color':'green',

        },

    ]