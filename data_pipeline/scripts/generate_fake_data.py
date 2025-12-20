import pandas as pd
import numpy as np
import random
import os

# Define constants
NUM_SAMPLES = 5000
OUTPUT_FILE = "../raw_data/accident_history.csv"

def generate_data():
    data = []
    
    print(f"Generating {NUM_SAMPLES} synthetic records...")
    
    for _ in range(NUM_SAMPLES):
        # 1. Generate Random Features
        elevation = random.randint(500, 4500)   # Meters (Srinagar to Glaciers)
        snow_level = random.randint(0, 150)     # cm
        wind_speed = random.randint(0, 80)      # km/h
        is_night = random.choice([0, 1])        # 0=Day, 1=Night
        slope_angle = random.randint(0, 60)     # Degrees
        
        # 2. Calculate "Ground Truth" Risk (The Logic we want the AI to learn)
        # Base risk
        risk = 10 
        
        # Add risk factors
        if elevation > 2500: risk += 20
        if slope_angle > 35: risk += 15
        if snow_level > 30: risk += 25
        if wind_speed > 40: risk += 20
        if is_night == 1 and elevation > 2000: risk += 15
        
        # 3. Add "Noise" (Randomness) so the model doesn't just memorize rules
        # Real life is messy. Sometimes safe routes have accidents.
        noise = random.randint(-5, 15)
        risk += noise
        
        # Cap risk between 0 and 100
        risk = max(0, min(100, risk))
        
        # Append to list
        data.append([elevation, snow_level, wind_speed, is_night, slope_angle, risk])

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=[
        "elevation_gain", "snow_level_cm", "wind_speed", 
        "is_night", "slope_angle", "risk_score"
    ])
    
    # Save to CSV
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Success! Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_data()