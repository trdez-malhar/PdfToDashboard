import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
# Load dataset
df = pd.read_csv("/content/sample_data/cell_level_train.csv")  # Change to your file path if needed
df = df.drop_duplicates(keep="first")
label_encoder = LabelEncoder()
df["table_name"] = label_encoder.fit_transform(df["table_name"])  # Encode table types
# Save label mappings for debugging
label_mapping = dict(zip(label_encoder.transform(label_encoder.classes_), label_encoder.classes_))
print("🔹 LabelEncoder Mapping (Train):", label_mapping)

# Define features (X) and target (y)
X = df.drop(columns=["table_name", 'coord_origin','row_section', 'text'])  # Features (excluding target)
y = df["table_name"]  # Target variable

# Split dataset into Training & Testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RandomForest Classifier
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_split=5, random_state=42)
rf_model.fit(X_train, y_train)

# Make Predictions
rf_preds = rf_model.predict(X_test)

# Evaluate RandomForest
print("🔹 RandomForest Accuracy:", accuracy_score(y_test, rf_preds))
print("🔹 RandomForest Classification Report:\n", classification_report(y_test, rf_preds))
# Save LabelEncoder to avoid refitting later
# Save trained RandomForest model as a pickle file
model_path = "/content/sample_data/ecas_model.pkl"
joblib.dump(rf_model, model_path)

# Save trained LabelEncoder as a pickle file
encoder_path = "/content/sample_data/label_encoder.pkl"
joblib.dump(label_encoder, encoder_path)
print("✅ Model & LabelEncoder saved successfully using joblib!")
