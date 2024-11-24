import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from dash import *

from utils import df, generate_plotly_colors
from components import dropdown, p_dropdown

register_page(__name__, path="/insights", name="insight", order=2)


# Reusable function for metric cards
def create_metric_card(title, value, color):
    return dmc.Card(
        dmc.Group(
            [
                dmc.Text(title, size="sm", c="dimmed"),
                dmc.Text(value, size="xl", c=color, fw=700),
            ],
            justify="center",
        ),
        withBorder=True,
        shadow="sm",
        radius="md",
        p="lg",
    )

layout = dmc.MantineProvider(
    [
        # Header
        dmc.Container(
            dmc.Text(
                "Insight Dashboard",
                tt="uppercase",
                size="xl",
                c="indigo",
                ta="center",
                td="underline",
                fw=700,
                py=20,
            ),
            fluid=True,
        ),
        # Key Insight Section
        dmc.Container(
            dmc.Grid(
                [
                    dmc.GridCol(create_metric_card("Total Track", "1,300", "blue"), span=3),
                    dmc.GridCol(create_metric_card("Average Popularity", "68%", "green"), span=3),
                    dmc.GridCol(create_metric_card("Top Genre", "Acoustic", "purple"), span=3),
                    dmc.GridCol(create_metric_card("Average Duration (min)", "3.5", "teal"), span=3),
                ],
                gutter="xl",
            ),
            fluid=True,
            py=20,
        ),
        # Main Section
        dmc.Container(
            dmc.Grid(
                [
                    # Left Section: Popularity
                    dmc.GridCol(
                        dmc.Paper(
                            [
                                dmc.Text(
                                    "Popularity prediction",
                                    size="md",
                                    fw=600,
                                    ta="center",
                                    mt="10",
                                ),
                                dmc.Container(
                                    id="popularity", style={"height": "600px"}
                                ),
                            ],
                            p="sm",
                            shadow="sm",
                            radius="md",
                            withBorder=True,
                        ),
                        span=3,
                    ),
                    # Right Section: Nested GridCols for Average Popularity and Duration
                    dmc.GridCol(
                        [
                            # First Row of Right Section
                            dmc.Grid(
                                [
                                    dmc.GridCol(
                                        dmc.Paper(
                                            [
                                                dmc.Text(
                                                    "Average Popularity by Mood",
                                                    size="sm",
                                                    fw=600,
                                                    mb=10,
                                                ),
                                                dmc.Container(
                                                    id="Average_Popularity_Mood",
                                                    style={"height": "255px"},
                                                ),
                                            ],
                                            p="md",
                                            shadow="md",
                                            withBorder=True,
                                        ),
                                        span=5,
                                    ),
                                    dmc.GridCol(
                                        dmc.Paper(
                                            [
                                                dmc.Text(
                                                    "Duration vs Danceability",
                                                    size="sm",
                                                    fw=600,
                                                    mb=10,
                                                ),
                                                dmc.Container(
                                                    id="duration_vs_danceability",
                                                    style={"height": "255px"},
                                                ),
                                            ],
                                            p="md",
                                            shadow="md",
                                            withBorder=True,
                                        ),
                                        span=7,
                                    ),
                                ],
                                gutter="sm",
                            ),
                            # Second Row of Right Section
                            dmc.Grid(
                                [
                                    dmc.GridCol(
                                        dmc.Paper(
                                            [
                                                dmc.Text(
                                                    "Genre Distribution",
                                                    size="sm",
                                                    fw=600,
                                                    mb=10,
                                                ),
                                                dmc.Container(
                                                    id="genre_distribution",
                                                    style={"height": "250px"},
                                                ),
                                            ],
                                            p="md",
                                            shadow="md",
                                            withBorder=True,
                                        ),
                                        span=6,
                                    ),
                                    dmc.GridCol(
                                        dmc.Paper(
                                            [
                                                dmc.Text(
                                                    "Mood Analysis",
                                                    size="sm",
                                                    fw=600,
                                                    mb=10,
                                                ),
                                                dmc.Container(
                                                    id="mood_analysis",
                                                    style={"height": "250px"},
                                                ),
                                            ],
                                            p="md",
                                            shadow="md",
                                            withBorder=True,
                                        ),
                                        span=6,
                                    ),
                                ],
                                gutter="sm",
                            ),
                        ],
                        span=9,  # Right section spans the remaining space
                    ),
                ],
                gutter="sm",
            ),
            fluid=True,
            py=15,
        ),
    ],
)



@callback(
    Output("Average_Popularity_Mood", "children"),
    Input("dropdown_popularity_level", "value")  
)
def update_mood_analysis(selected_mood):
    if not selected_mood:
        raise PreventUpdate

    # Filter data for the selected mood
    filtered_data = df[df["popularity_level"] == selected_mood]

    if filtered_data.empty:
        return dmc.Text("No data available for the selected mood.")

    # Group data and aggregate energy values
    grouped_data = filtered_data.groupby("energy_level")["energy"].sum().reset_index()
    print(grouped_data)

    # Prepare data for the Donut Chart
    donut_data = [
       {"name": row["energy_level"], "value": row["energy"], "color": "indigo.6" if row["energy_level"] == "Low" else "yellow.6" if row["energy_level"] == "Medium" else "teal.6"}
        for _, row in grouped_data.iterrows()
    ]

    # Create the Donut Chart
    return dmc.DonutChart(
        data=donut_data,
        thickness=30,
        size=300,
       withLabels=True,
       tooltipDataSource="segment"
    )


@callback(Output("duration_vs_danceability", "children"),
          Input('dropdown_danceability_level', "value"),
          )

def po_da(selceted_dance_level):
    f_data = df[df['danceability_level'] == selceted_dance_level]

    if f_data.empty:
        return dmc.Text('No data avaliable for the analysis')
    
    unique_genres = df["track_genre"].unique()
    genre_color_mapping = generate_plotly_colors(unique_genres)
    
    f_data["color"] = f_data["track_genre"].map(genre_color_mapping)

    print(f_data["color"])

    
    t_data = [
        {
            'name': 'popularity',
            'data' : f_data.to_dict('records'),
            'color': 'orange'
        },
        {
            'name': 'danceability',
            'data' : f_data.to_dict('records'),
           'color': 'green'
        }
    ]

    return dmc.ScatterChart(
        id='popularity_dancibility',
        h=300,
        data=t_data,
        dataKey = {'x':"danceability", 'y':"Popularity"},
        xAxisLabel="danceability",
        yAxisLabel="Popularity"

    )

    

    
