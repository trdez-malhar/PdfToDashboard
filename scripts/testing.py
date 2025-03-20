import joblib
import pandas as pd

# Load trained RandomForest model from pickle file
model_path = "/content/sample_data/ecas_model.pkl"
rf_model = joblib.load(model_path)

# Load LabelEncoder from pickle file
encoder_path = "/content/sample_data/label_encoder.pkl"
label_encoder = joblib.load(encoder_path)
# Load new table data
new_data_path = "/content/sample_data/1742362287902937500_cell_level.csv"
new_df = pd.read_csv(new_data_path)

# Ensure only trained features are used
trained_features = rf_model.feature_names_in_
new_df = new_df[trained_features]

# Predict table type using RandomForest
rf_preds = rf_model.predict(new_df)


# Convert predictions from numbers to table names
rf_predicted_labels = label_encoder.inverse_transform(rf_preds)


# Add predictions to DataFrame
new_df["RandomForest Prediction"] = rf_predicted_labels

# Display results
print("🔹 Final Predictions:\n", new_df[["table_no", "page_no", "RandomForest Prediction"]])
