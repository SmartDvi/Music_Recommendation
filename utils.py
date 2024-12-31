import pandas as pd
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
from dash.exceptions import PreventUpdate
from sklearn.metrics import confusion_matrix, accuracy_score, r2_score

df = pd.read_csv('C:\\Users\\Moritus Peters\\Downloads\\dataset.csv')
#df = pd.read_csv('https://raw.githubusercontent.com/SmartDvi/Music_Recommendation/main/dataset.csv')

# Convert duration to minutes
df['duration_min'] = df['duration_ms'] / 60000

# Categorize loudness_level
df['loudness_level'] = pd.cut(
    df['loudness'], 
    bins=[-100, -40, -20, -10, -5, 0], 
    labels=['Very Quiet', 'Quiet', 'Moderate', 'Loud', 'Very Loud'], 
    include_lowest=True
)

# Categorize energy_level
df['energy_level'] = pd.cut(
    df['energy'], 
    bins=[0, 0.33, 0.66, 1], 
    labels=['Low', 'Medium', 'High'], 
    include_lowest=True
)

# Categorize danceability_level
df['danceability_level'] = pd.cut(
    df['danceability'], 
    bins=[0, 0.33, 0.66, 1], 
    labels=['Low', 'Medium', 'High'], 
    include_lowest=True
)

# Categorize tempo_category
df['tempo_category'] = pd.cut(
    df['tempo'], 
    bins=[0, 60, 120, 180, 300], 
    labels=['Slow', 'Medium', 'Fast', 'Very Fast'], 
    include_lowest=True
)

# Categorize explicit_flag
df['explicit_flag'] = df['explicit'].replace({True: 'Explicit', False: 'Non-Explicit'})

# Categorize popularity_level
df['popularity_level'] = pd.cut(
    df['popularity'], 
    bins=[0, 50, 75, 100], 
    labels=['Low', 'Medium', 'High'], 
    include_lowest=True
)

# Define mood_indicator using valence and energy
conditions = [
    (df['valence'] > 0.5) & (df['energy'] > 0.5),
    (df['valence'] > 0.5) & (df['energy'] <= 0.5),
    (df['valence'] <= 0.5) & (df['energy'] > 0.5),
    (df['valence'] <= 0.5) & (df['energy'] <= 0.5)
]
choices = ['Happy', 'Calm', 'Energetic', 'Sad']
df['mood_indicator'] = np.select(conditions, choices, default='Unknown')


color_mapping1 = {
    'Low' : 'red',
    'Medium': 'yellow',
    'High' : 'green'
}




def generate_prediction_chart(df, selected_mood):
    """
    Generate a bar chart showing predicted popularity of tracks based on selected mood.
    
    Parameters:
        df (pd.DataFrame): The dataframe containing track data.
        selected_mood (list): List of moods to filter the dataframe.
        
    Returns:
        fig (plotly.graph_objects.Figure): The generated bar chart.
    """
    if not selected_mood:
        raise PreventUpdate

    # Filter dataframe based on selected moods
    filtered_df = df[df['mood_indicator'].isin(selected_mood)]

    # Drop unnecessary columns and convert categorical features
    X = filtered_df.drop(columns=['popularity', 'track_id', 'artists', 'album_name', 'track_name', 'explicit_flag', 'mood_indicator'])
    y = filtered_df['popularity']
    
    # Handle categorical features
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
    r2 = r2_score(y_test, y_pred)

    # Prepare results for visualization
    results = pd.DataFrame({
        'Track_Name': filtered_df['track_name'].iloc[:len(y_pred)],
        'Predicted_Popularity': y_pred
    }).sort_values(by='Predicted_Popularity', ascending=False)

    # Generate bar chart
    fig = px.bar(
        results,
        x='Track_Name',
        y='Predicted_Popularity',
        title=f"Predicted Popularity of Tracks (R² = {r2:.2f})",
        labels={'Track_Name': 'Track Name', 'Predicted_Popularity': 'Predicted Popularity'},
        color='Predicted_Popularity',
        color_continuous_scale='Viridis'
    )
    return fig




def generate_feature_importance_plot(model, feature_names):
    """
    Generate a Plotly bar chart showing the feature importance of a trained model.
    
    Parameters:
        model: Trained RandomForest model.
        feature_names (list): List of feature names.
        
    Returns:
        fig: Plotly bar chart showing feature importance.
    """
    importances = model.feature_importances_
    sorted_indices = importances.argsort()[::-1]
    sorted_features = [feature_names[i] for i in sorted_indices]
    sorted_importances = importances[sorted_indices]
    
    fig = px.bar(
        x=sorted_importances,
        y=sorted_features,
        orientation="h",
        labels={"x": "Importance", "y": "Feature"},
        title="Feature Importance"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig


def generate_prediction_analysis(y_test, y_pred, model_type="regression"):
    """
    Generate prediction analysis using Plotly visualizations.
    
    Parameters:
        y_test (pd.Series or np.ndarray): True values.
        y_pred (pd.Series or np.ndarray): Predicted values.
        model_type (str): Type of model ('regression' or 'classification').
        
    Returns:
        dict: Metrics like R² for regression or accuracy for classification.
        fig: Plotly visualization.
    """
    if model_type == "regression":
        r2 = r2_score(y_test, y_pred)
        metrics = {"R² Score": r2}
        
        # Create scatter plot for actual vs predicted
        fig = px.scatter(
            x=y_test,
            y=y_pred,
            labels={"x": "Actual", "y": "Predicted"},
            title=f"Actual vs Predicted Values (R² = {r2:.2f})"
        )
        fig.add_trace(go.Scatter(x=y_test, y=y_test, mode="lines", name="Ideal Line"))
    
    elif model_type == "classification":
        acc = accuracy_score(y_test, y_pred)
        metrics = {"Accuracy": acc}
        
        # Create confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        fig = px.imshow(
            cm,
            text_auto=True,
            labels={"x": "Predicted", "y": "True"},
            title=f"Confusion Matrix (Accuracy = {acc:.2f})",
            color_continuous_scale="Viridis"
        )
    
    return metrics, fig


def generate_class_distribution_plot(df, target_column):
    """
    Generate a Plotly bar chart showing the distribution of classes in the target column.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the target column.
        target_column (str): Name of the target column.
        
    Returns:
        fig: Plotly bar chart showing class distribution.
    """
    class_counts = df[target_column].value_counts()
    fig = px.bar(
        x=class_counts.index,
        y=class_counts.values,
        labels={"x": "Class", "y": "Count"},
        title=f"Class Distribution for {target_column}"
    )
    return fig


def generate_confusion_matrix(y_test, y_pred):
    """
    Generate a confusion matrix heatmap using Plotly.
    
    Parameters:
        y_test (pd.Series or np.ndarray): True labels.
        y_pred (pd.Series or np.ndarray): Predicted labels.
        
    Returns:
        fig: Plotly heatmap of the confusion matrix.
    """
    cm = confusion_matrix(y_test, y_pred)
    fig = px.imshow(
        cm,
        text_auto=True,
        labels={"x": "Predicted", "y": "True"},
        title="Confusion Matrix",
        color_continuous_scale="Blues"
    )
    return fig
