import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import *

from utils import (
    df,
    generate_prediction_chart,
    generate_feature_importance_plot,
    generate_prediction_analysis,
    generate_class_distribution_plot,
    generate_confusion_matrix,
)

from components import (dropdown,
                        mood_check, 
                        track_genre_drp, 
                        mood_options, 
                        mood_pd
                        )

register_page(__name__, path="/insights", name="Insight Dashboard", order=2, allow_duplicate=True)

# Mood Colors
COLOR_MAP = {
    'Happy': 'green',
    'Energetic': 'yellow',
    'Sad': 'orange',
    'Unhealthy': 'red',
    'Calm': 'purple',
}

# Tabs Helper Function
def create_insights_tabs():
    return dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.TabsTab("Prediction", value="generate_prediction_chart"),
                    dmc.TabsTab("Feature Importance", value="feature_importance"),
                    dmc.TabsTab("Prediction Analysis", value="prediction_analysis"),
                    dmc.TabsTab("Class Distribution", value="class_distribution"),
                    dmc.TabsTab("Confusion Matrix", value="confusion_matrix"),
                ]
            ),
            dmc.TabsPanel(
                dcc.Graph(
                    id="generate_prediction_chart",
                    style={"height": "250px"},
                    config={"displayModeBar": True, "responsive": True},
                ),
                value="generate_prediction_chart",
            ),
            dmc.TabsPanel(
                dcc.Graph(
                    id="feature_importance",
                    style={"height": "250px"},
                    config={"displayModeBar": True, "responsive": True},
                ),
                value="feature_importance",
            ),
            dmc.TabsPanel(
                dcc.Graph(
                    id="prediction_analysis",
                    style={"height": "250px"},
                    config={"displayModeBar": True, "responsive": True},
                ),
                value="prediction_analysis",
            ),
            dmc.TabsPanel(
                dcc.Graph(
                    id="class_distribution",
                    style={"height": "250px"},
                    config={"displayModeBar": True, "responsive": True},
                ),
                value="class_distribution",
            ),
            dmc.TabsPanel(
                dcc.Graph(
                    id="confusion_matrix",
                    style={"height": "250px"},
                    config={"displayModeBar": True, "responsive": True},
                ),
                value="confusion_matrix",
            ),
        ],
        value="generate_prediction_chart",
        id="insights_tabs",
    )


# Metric Card Helper Function
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
        style={"background": "#f5f5f5"},
    )


# Layout
layout = dmc.MantineProvider(
    [
        # Header Section
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
                    dmc.GridCol(create_metric_card("Total Tracks", "1,300", "blue"), span=3),
                    dmc.GridCol(create_metric_card("Average Popularity", "68%", "green"), span=3),
                    dmc.GridCol(create_metric_card("Top Genre", "Acoustic", "purple"), span=3),
                    dmc.GridCol(create_metric_card("Average Duration (min)", "3.5", "teal"), span=3),
                ],
                gutter="xl",
            ),
            fluid=True,
            py=20,
        ),

        # Filters Section
        dmc.Grid(
            [
                dmc.GridCol(dropdown, span=3),
                dmc.GridCol(mood_check,  span=3),
                dmc.GridCol(track_genre_drp, span=3),
            ],
            gutter="xl",
            justify='center'
        ),

        # Main Data and Insights Section
        dmc.Container(
            dmc.Grid(
                [
                    # Left Section: Popularity Graph
                    dmc.GridCol(
                        dmc.Paper(
                            [
                                dmc.Text(
                                    "Artist Popularity by Mood",
                                    size="md",
                                    fw=600,
                                    ta="center",
                                    mt="10",
                                ),
                                dcc.Graph(
                                                    id="Aartist_popularity",
                                                    style={"height": "680px"},
                                                    config={"displayModeBar": True, "responsive": True},
                                                ),
                            ],
                            p="sm",
                            shadow="sm",
                            radius="md",
                            withBorder=True,
                        ),
                        span=3,
                    ),

                    # Right Section: Nested Grids for Various Insights
                    dmc.GridCol(
                        [
                            # First Row of Right Section
                            dmc.Grid(
                                [
                                    dmc.GridCol(
                                        dmc.Paper(
                                            [
                                                dmc.Text("Track Popularity vs Duration", size="sm", fw=600, ta="center", mb=10),
                                                dcc.Graph(
                                                    id="Average_Popularity_Mood",
                                                    style={"height": "255px"},
                                                    config={"displayModeBar": True, "responsive": True},
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
                                                dmc.Text("Popularity vs Danceability by Genre", size="sm", ta="center", fw=600, mb=10),
                                                dcc.Graph(
                                                    id="duration_vs_danceability",
                                                    style={"height": "255px"},
                                                    config={"displayModeBar": True, "responsive": True},
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

                            dmc.Grid(
                                dmc.GridCol(dmc.Paper(
                                    [
                                        mood_pd
                                    ],
                                     p="md",
                                        shadow="md",
                                        withBorder=True,
                                ))
                                
                            ),

                            # Second Row of Right Section
                            dmc.Grid(
                                [
                                    dmc.GridCol(
                                        dmc.Paper(
                                            [
                                                dmc.Text("Popularity by Tempo Category", size="sm", ta="center", fw=600, mb=10),
                                                dcc.Graph(
                                                    id="genre_distribution",
                                                    style={"height": "255px"},
                                                    config={"displayModeBar": True, "responsive": True},
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
                                                dmc.Text("Popularity Prediction and model Evaluation", size="sm", ta="center", fw=600, mb=10),
                                               create_insights_tabs(),
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
                        span=9,
                    ),
                ],
                gutter="sm",
            ),
            fluid=True,
            py=15,
        ),
    ],
)



# Callbacks
@callback(
    Output("duration_vs_danceability", "figure"),
    Input("dropdown_danceability_level", "value"),
)
def pop_dan(selected_dan_level):
    # Filter the dataframe based on the selected danceability level
    filtered_df = df if not selected_dan_level else df[df['danceability_level'] == selected_dan_level]

    # List of relevant genres you want to keep
    relevant_genres = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'blues', 
                       'classical', 'dance', 'disco', 'electronic', 'indie', 'jazz', 'metal', 'pop', 
                       'rock', 'soul', 'techno', 'trance']
    
    # Filter the dataframe to only include rows where track_genre is in the relevant genres list
    filtered_df = filtered_df[filtered_df['track_genre'].isin(relevant_genres)]
    
    # Create the scatter plot
    fig = px.scatter(
        filtered_df,
        x="danceability",
        y="popularity",
        color="track_genre",
        size="energy",
        hover_data=["track_name", "artists"],
        labels={"danceability": "Danceability", "popularity": "Popularity"},
        template="plotly_white"
    )
    
    # Update layout to remove margins
    fig.update_layout(margin={'l': 0, 'r': 0, 't': 0, 'b': 0})
    
    return fig

@callback(
    [
        Output("generate_prediction_chart", "figure"),
        Output("feature_importance", "figure"),
        Output("prediction_analysis", "figure"),
        Output("class_distribution", "figure"),
        Output("confusion_matrix", "figure"),
    ],
    Input("insights_tabs", "value"),
)
def update_tab_content(active_tab):
    if active_tab == "generate_prediction_chart":
        fig = generate_prediction_chart(df, ["Happy", "Sad", "Calm"])
        return fig, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    elif active_tab == "feature_importance":
        model = RandomForestRegressor(random_state=42)
        X = df.select_dtypes(include=["float64", "int64"])
        y = df["popularity"]
        model.fit(X, y)
        fig = generate_feature_importance_plot(model, X.columns)
        return dash.no_update, fig, dash.no_update, dash.no_update, dash.no_update
    elif active_tab == "prediction_analysis":
        X_train, X_test, y_train, y_test = train_test_split(
            df.select_dtypes(include=["float64", "int64"]),
            df["popularity"],
            test_size=0.2,
            random_state=42,
        )
        model = RandomForestRegressor(random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metrics, fig = generate_prediction_analysis(y_test, y_pred, model_type="regression")
        return dash.no_update, dash.no_update, fig, dash.no_update, dash.no_update
    elif active_tab == "class_distribution":
        fig = generate_class_distribution_plot(df, "popularity_level")
        return dash.no_update, dash.no_update, dash.no_update, fig, dash.no_update
    elif active_tab == "confusion_matrix":
        y_test = [0, 1, 0, 1]
        y_pred = [0, 1, 1, 1]
        fig = generate_confusion_matrix(y_test, y_pred)
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, fig
    else:
        raise PreventUpdate

@callback(
    [
        Output("dropdown_track_genre", "options"),
        Output("Average_Popularity_Mood", "figure"),
        Output("Aartist_popularity", "figure"),
    ],
    [
        Input("genre-select", "value"),
        Input("dropdown_track_genre", "value"),
    ]
)
def update_combined_graphs(selected_moods, selected_genres):
    filtered_data = df

    # Filter by moods
    if selected_moods:
        filtered_data = filtered_data[filtered_data["mood_indicator"].isin(selected_moods)]
    else:
        print("No moods selected; skipping mood filtering.")

    # Ensure selected_genres is a list
    if isinstance(selected_genres, str):
        selected_genres = [selected_genres] 
    # Filter by genres
    if selected_genres:
        filtered_data = filtered_data[filtered_data["track_genre"].isin(selected_genres)]
    else:
        print("No genres selected; skipping genre filtering.")

    # Handle empty filtered data for dropdown
    if filtered_data.empty:
        dropdown_options = []
        fig_avg_popularity = px.scatter(title="No data available for the selected filters.")
        fig_artist_popularity = px.bar(title="No data available for the selected filters.")
    else:
        dropdown_options = [
            {"label": genre, "value": genre} for genre in filtered_data["track_genre"].unique()
        ]

        # Average Popularity Figure
        fig_avg_popularity = px.scatter(
            filtered_data,
            x="duration_min",
            y="popularity",
            color="mood_indicator",
            hover_data=["track_genre"],
            template="plotly_white"
        )
        fig_avg_popularity.update_layout(margin={'l': 0, 'r': 0, 't': 4, 'b': 0})
       



        # Artist Popularity Figure with Vertical Orientation
    top_artists = filtered_data.nlargest(10, 'popularity')
    fig_artist_popularity = px.bar(
        top_artists,
        y="artists",  
        x="popularity",  
        color="popularity_level",  
        text="popularity",  
        title="Top 10 Artists by Popularity Score on the Platform",
        labels={
            "artists": "Artists",
            "popularity": "Popularity Score",
            "popularity_level": "Popularity Level",
        },
        hover_data=["track_name", "album_name"],  # Additional details on hover
        orientation="h"  
    )

    # Sort bars by popularity
    fig_artist_popularity.update_yaxes(categoryorder="total ascending")  # Reverse for vertical orientation

    # Enhance visuals
    fig_artist_popularity.update_traces(texttemplate='%{text}', textposition='outside')
    fig_artist_popularity.update_layout(
    title={
        'text': "Top 10 Artists by Popularity Score",
        'x': 0.5,  # Center align title
        'xanchor': 'center'
    },
    xaxis=dict(title="Popularity Score"),  
    yaxis=dict(title="Artists"),
    showlegend=True,
    legend_title="Popularity Level",
    legend=dict(
        orientation="h", 
        x=0.5,  
        y=1.1,  
        xanchor="center",  
        yanchor="bottom"  
    ),
    plot_bgcolor="rgba(0,0,0,0)" )
    fig_artist_popularity.update_layout(margin={'l': 0, 'r': 0, 't': 4, 'b': 0})

    return dropdown_options, fig_avg_popularity, fig_artist_popularity

@callback(
    Output("genre_distribution", "figure"),
    Input("dropdown_track_genre", "value")

)

def update_chart(selected_track_genre):
    if not selected_track_genre:
        raise PreventUpdate
    
    # Ensure selected_track_genre is a list-like object
    if isinstance(selected_track_genre, str):
        selected_track_genre = [selected_track_genre]

    fit_df = df[df['track_genre'].isin(selected_track_genre)]

    fig = px.box(
        fit_df,
        x="tempo_category",
        y="popularity",
        color="tempo_category",
        title="Popularity by Tempo Category",
        labels={
            "tempo_category": "Tempo Category",
            "popularity": "Popularity (Popularity Score)"
        },
        template="plotly_white"
    )

    # Customizing the box plot for better insights
    fig.update_traces(
        marker=dict(size=10, opacity=0.6),
        boxmean="sd",  
        jitter=0.05,   
        pointpos=-1.8  
    )

    # Adding title, axis labels, and annotations for better understanding
    fig.update_layout(
        title={
            'text': "Popularity by Tempo Category (Understanding the Distribution)",
            'x': 0.5,  
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Tempo Category (Speed of the Track)",
        yaxis_title="Popularity Score (Measure of Track's Popularity)",
        showlegend=False,  
        annotations=[
            dict(
                x=0,  
                y=fit_df['popularity'].min(),
                xref="x",
                yref="y",
                text="Low Tempo: Slow-paced tracks.",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                ax=-60,
                ay=-50,
                font=dict(size=12, color="blue")
            ),
            dict(
                x=2,  # Positioning annotation for 'high tempo'
                y=fit_df['popularity'].max(),
                xref="x",
                yref="y",
                text="High Tempo: Fast-paced tracks.",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                ax=-60,
                ay=-50,
                font=dict(size=12, color="red")
            ),
            dict(
                x=1,  
                y=fit_df['popularity'].mean(),
                xref="x",
                yref="y",
                text="Medium Tempo: Moderately-paced tracks.",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                ax=30,
                ay=0,
                font=dict(size=12, color="green")
            )
        ]
    )
    fig.update_layout(margin={'l': 0, 'r': 0, 't': 4, 'b': 0})

    return fig













