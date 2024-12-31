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
    generate_feature_importance_plot,
    generate_prediction_analysis,
    generate_class_distribution_plot,
    generate_confusion_matrix
)

from components import dropdown, p_dropdown, track_genre_drp, mood_options, mood_pd

register_page(__name__, path="/insights", name="Insight Dashboard", order=2)

# Mood Colors
COLOR_MAP = {
    'Happy': 'green',
    'Energetic': 'yellow',
    'Sad': 'orange',
    'Unhealthy': 'red',
    'Calm': 'purple',
}


# Helper Function: Artist Mood Popularity
def artist_mood_popularity(mood_indicator, track_genre):
    filtered_df = df[(df['mood_indicator'] == mood_indicator) & (df['track_genre'] == track_genre)]
    if filtered_df.empty:
        return dmc.Text("No data available for the selected mood and genre.", c="dimmed", ta="center")

    data = filtered_df.groupby('artists')['popularity'].sum().reset_index()
    top_20 = data.nlargest(20, 'popularity')
    least_20 = data.nsmallest(20, 'popularity')
    combined = pd.concat([top_20, least_20])

    return dmc.BarChart(
        id=f'pop_tab_{mood_indicator}',
        datakey='artists',
        data=combined.to_dict('records'),
        orientation='vertical',
        yAxisProps={"width": 80},
        series=[
            {
                "name": "Popularity",
                "data": combined['popularity'].tolist(),
                "color": COLOR_MAP.get(mood_indicator, 'blue'),
            }
        ],
    )


# Helper Function: Tabs for Moods
def create_mood_tabs(track_genre):
    return dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.TabsTab('Happy', value='Happy'),
                    dmc.TabsTab('Energetic', value='Energetic'),
                    dmc.TabsTab('Sad', value='Sad'),
                    dmc.TabsTab('Calm', value='Calm'),
                ]
            ),
            dmc.TabsPanel(artist_mood_popularity('Happy', track_genre), value='Happy'),
            dmc.TabsPanel(artist_mood_popularity('Energetic', track_genre), value='Energetic'),
            dmc.TabsPanel(artist_mood_popularity('Sad', track_genre), value='Sad'),
            dmc.TabsPanel(artist_mood_popularity('Calm', track_genre), value='Calm'),

        ],
        value='Happy',
        id='return_tabs',
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
                dmc.GridCol(p_dropdown,  span=3),
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
                                dmc.Container(
                                    id="artist_popularity",
                                    style={"height": "620px"}
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
                                                dcc.Graph(
                                                    id="mood_analysis",
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
    )
    
    # Update layout to remove margins
    fig.update_layout(margin={'l': 0, 'r': 0, 't': 0, 'b': 0})
    
    return fig



@callback(Output("mood_analysis", "figure"),
           [Input("check_box", "value")])

def update_prediction_chart(selected_mood):
    if not selected_mood:
        raise PreventUpdate
    
    fitt_df = df[df['mood_indicator'].isin(selected_mood)]

    # Drop unnecessary columns and convert categorical features
    X = fitt_df.drop(columns=['popularity', 'track_id', 'artists', 'album_name', 'track_name', 'explicit_flag', 'mood_indicator'])
    y = fitt_df['popularity']
    
    # Handle categorical features (if any remain)
    categorical_cols = X.select_dtypes(include=['category', 'object']).columns
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
    
    # Select only numeric columns
    X = X.select_dtypes(include=['int64', 'float64'])


    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)
    #mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Prepare results for visualization
    results = pd.DataFrame({
        'Track_Name': fitt_df['track_name'].iloc[:len(y_pred)],
        'Predicted_Popularity': y_pred
    }).sort_values(by='Predicted_Popularity', ascending=False)

    # Sort the data for top 10 and least 10
    top_10 = results.nlargest(10, 'Predicted_Popularity')
    least_10 = results.nsmallest(10, 'Predicted_Popularity')

    # Concatenate top 10 and least 10
    combined = pd.concat([top_10, least_10])
    combined['Category'] = ['Top 10'] * len(top_10) + ['Least 10'] * len(least_10)

    fig = px.bar(
        combined,
        x='Track_Name',
        y='Predicted_Popularity',
        title=f"Predicted Popularity of Tracks and it's R2 {r2}",
        labels={'Track_Name': 'Track Name', 'Predicted_Popularity': 'Pred Po'},
        color='Predicted_Popularity',
        color_continuous_scale='Viridis'
    )

    # Update layout to remove margins
    #fig.update_layout(margin={'l': 0, 'r': 0, 't': 4, 'b': 0})
    return fig

@callback(
    [
        Output("dropdown_track_genre", "options"),
        Output("Average_Popularity_Mood", "figure")
    ],
    [
        Input("check_box", "value"),
        Input("dropdown_track_genre", "value")
    ]
)
def update_graph(selected_moods, selected_genres):
    print("Selected Moods:", selected_moods)
    print("Selected Genres:", selected_genres)
    print("Available columns in the DataFrame:", df.columns)

    filtered_data = df

    # Filter by moods
    if selected_moods:
        filtered_data = filtered_data[filtered_data["mood_indicator"].isin(selected_moods)]
    else:
        print("No moods selected; skipping mood filtering.")

    # Ensure selected_genres is a list
    if isinstance(selected_genres, str):
        selected_genres = [selected_genres]  # If it's a single genre, make it a list

    # Filter by genres
    if selected_genres:
        filtered_data = filtered_data[filtered_data["track_genre"].isin(selected_genres)]
    else:
        print("No genres selected; skipping genre filtering.")

    # Handle empty filtered data for dropdown
    if filtered_data.empty:
        dropdown_options = []
    else:
        dropdown_options = [
            {"label": genre, "value": genre} for genre in filtered_data["track_genre"].unique()
        ]

    # Handle empty filtered data for scatter plot
    if filtered_data.empty:
        fig = px.scatter(title="No data available for the selected filters.")
    else:
        fig = px.scatter(
            filtered_data,
            x="duration_min",
            y="popularity",
            color="mood_indicator",
            hover_data=["track_genre"],
            title="Track Popularity vs Duration (Filtered)"
        )
        fig.update_layout(margin={'l': 0, 'r': 0, 't': 4, 'b': 0})

    return dropdown_options, fig

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
