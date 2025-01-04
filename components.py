
import dash_mantine_components as dmc
from dash import *

from utils import df


dropdown = dmc.Select(
                id='dropdown_danceability_level',
                label='Select danceabile Music Level',
                data=[{'label': danceability_level, 'value': danceability_level} for danceability_level in df['danceability_level'].dropna().unique()],
                value=df['danceability_level'].dropna().iloc[0],
                clearable=True,
                style={'marginBottom': "20px"}
        )

track_genre_drp = dmc.Select(
            id='dropdown_track_genre',
            label='Select track_genre Music',
            data=[{'label': track_genre, 'value': track_genre} for track_genre in df['track_genre'].dropna().unique()],
            value=df['track_genre'].dropna().iloc[0],
            clearable=True,
            style={'marginBottom': "20px"}
        )



p_check =dmc.Group( [
    dmc.Checkbox(
        label=mood,  
        value=mood  
    )
    for mood in df['mood_indicator'].unique()
],
justify='center',
grow=True)

# Create the checkbox group
mood_check = dmc.CheckboxGroup(
    id="genre-select",
    label="Check fot mood Indication",
    withAsterisk=True,
    mb=10,
    children=p_check,  
    value=["Calm"]  
)


mood_options =dmc.Group( [
    dmc.Checkbox(
        label=mood,  
        value=mood  
    )
    for mood in df['mood_indicator'].unique()
],
justify='center',
grow=True)

# Create the checkbox group
mood_pd = dmc.CheckboxGroup(
    id="check_box",
    label="Check mood to predict",
    withAsterisk=True,
    mb=10,
    children=mood_options,  
    value=["Calm"]  
)



#print("Available columns in df:", df.columns)
#print("Sample rows in df:")
#print(df.head())
#print(df.info())
#print(f"the cplumn: {df['mood_indicator'].value_counts()}")
#print(f"the cplumn: {df['track_name'].value_counts()}")
grouped_data = df.groupby("energy_level")["energy"].sum().reset_index()
print(grouped_data)

# Tabs Helper Function
def create_insights_tabs():
    return dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.TabsTab("Prediction Chart", value="generate_prediction_chart"),
                    dmc.TabsTab("Feature Importance", value="feature_importance"),
                    dmc.TabsTab("Prediction Analysis", value="prediction_analysis"),
                    dmc.TabsTab("Class Distribution", value="class_distribution"),
                    dmc.TabsTab("Confusion Matrix", value="confusion_matrix"),
                ]
            ),
            dmc.TabsPanel(
                dcc.Graph(
                    id="generate_prediction_chart",
                    style={"height": "450px"},
                    config={"displayModeBar": True, "responsive": True},
                ),
                value="generate_prediction_chart",
            ),
            dmc.TabsPanel(
                dcc.Graph(
                    id="feature_importance",
                    style={"height": "450px"},
                    config={"displayModeBar": True, "responsive": True},
                ),
                value="feature_importance",
            ),
            dmc.TabsPanel(
                dcc.Graph(
                    id="prediction_analysis",
                    style={"height": "450px"},
                    config={"displayModeBar": True, "responsive": True},
                ),
                value="prediction_analysis",
            ),
            dmc.TabsPanel(
                dcc.Graph(
                    id="class_distribution",
                    style={"height": "450px"},
                    config={"displayModeBar": True, "responsive": True},
                ),
                value="class_distribution",
            ),
            dmc.TabsPanel(
                dcc.Graph(
                    id="confusion_matrix",
                    style={"height": "450px"},
                    config={"displayModeBar": True, "responsive": True},
                ),
                value="confusion_matrix",
            ),
        ],
        value="generate_prediction_chart",
        id="insights_tabs",
    )


