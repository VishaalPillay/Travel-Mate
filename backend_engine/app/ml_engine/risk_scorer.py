import joblib
import pandas as pd
import os

class RouteRiskScorer:
    def __init__(self):
        # Path to the trained model
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "trained_models/route_risk_model.pkl")
        
        self.model = None
        try:
            self.model = joblib.load(model_path)
            print("✅ ML Model loaded successfully.")
        except FileNotFoundError:
            print("⚠️ Warning: Model file not found. Please run train_risk_model.py")

    def calculate_risk(self, route_data: dict, weather_data: dict) -> dict:
        if not self.model:
            return {"risk_score": 0, "status": "UNKNOWN", "warnings": ["Model not loaded"]}

        # 1. Prepare Input Vector
        slope = route_data.get('slope_angle', 30) 
        is_night_int = 1 if route_data.get('is_night_travel', False) else 0
        
        input_features = pd.DataFrame([{
            "elevation_gain": route_data.get('elevation_gain', 0),
            "snow_level_cm": weather_data.get('snow_level_cm', 0),
            "wind_speed": weather_data.get('wind_speed', 0),
            "is_night": is_night_int,
            "slope_angle": slope
        }])

        # 2. Predict
        predicted_risk = self.model.predict(input_features)[0]
        
        # 3. Determine Status & Generate Warnings
        final_score = int(predicted_risk)
        status = "SAFE"
        warnings = []

        if final_score > 40: 
            status = "CAUTION"
            warnings.append("Conditions are worsening. Proceed with care.")
            
        if final_score > 70: 
            status = "DANGER"
            warnings.append("High Risk detected by AI Model.")
            warnings.append("Travel is strictly not recommended.")

        # --- THE FIX IS HERE ---
        # We now return 'risk_score' and 'warnings' to match routes.py
        return {
            "risk_score": final_score,   
            "status": status,
            "warnings": warnings 
        }

# Instantiate
risk_engine = RouteRiskScorer()