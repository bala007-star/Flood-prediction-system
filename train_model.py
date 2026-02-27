import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib # Used to save the model for later use

# --- 1. Load Data ---
df = pd.read_csv('C:\\Users\\balan\Final_Flood_Prediction\\final_flood_training_data.csv')

# Define Features (X) and Target (y)
# Ensure these column names match your CSV exactly
X = df[['Temperature', 'Rainfall', 'WindSpeed']] 
y = df['Flood_Risk']

# --- 2. Split Data ---
# 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 3. Train the Model ---
# We use class_weight='balanced' to handle the small number of flood cases
print("Training Random Forest Model... (this may take a moment)")
model = RandomForestClassifier(
    n_estimators=100, 
    random_state=42, 
    class_weight='balanced'  # CRITICAL: Fixes the imbalance problem
)

model.fit(X_train, y_train)

# --- 4. Evaluate ---
y_pred = model.predict(X_test)

print("\n--- Model Performance ---")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nDetailed Report:\n", classification_report(y_test, y_pred))

# --- 5. Save the Model ---
# We save the trained model to a file so the Live App can load it instantly
joblib.dump(model, 'flood_model.pkl')
print("\n✅ Model saved as 'flood_model.pkl'. Ready for the App!")

# --- 6. Quick Test ---
# Let's test it with a fake "Heavy Rain" scenario
print("\n--- Manual Test ---")
# Example: 25°C Temp, 150mm Rain (Heavy), 15km/h Wind
test_input = [[25, 150, 15]] 
prediction = model.predict(test_input)

risk_map = {0: "Low Risk", 1: "Moderate Risk", 2: "High Risk"}
print(f"Test Input: 150mm Rain -> Prediction: {risk_map[prediction[0]]}")



