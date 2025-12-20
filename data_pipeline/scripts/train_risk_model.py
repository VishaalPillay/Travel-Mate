import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import os

# Paths
DATA_PATH = "../raw_data/accident_history.csv"
MODEL_PATH = "../../backend_engine/app/ml_engine/trained_models/route_risk_model.pkl"

def train_model():
    print("🚀 Starting Model Training...")
    
    # 1. Load Data
    if not os.path.exists(DATA_PATH):
        print("❌ Error: Data file not found. Run generate_fake_data.py first.")
        return

    df = pd.read_csv(DATA_PATH)
    
    # 2. Split Features (X) and Target (y)
    X = df[["elevation_gain", "snow_level_cm", "wind_speed", "is_night", "slope_angle"]]
    y = df["risk_score"]
    
    # 3. Split into Train/Test sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train Random Forest (The Machine Learning part)
    # n_estimators=100 means we use 100 decision trees
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Evaluate Accuracy
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"📊 Model Trained. Mean Absolute Error: {mae:.2f} (Lower is better)")
    
    # 6. Save the Model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()