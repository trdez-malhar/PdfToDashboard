import joblib

# Load new table data

def predict_table_names(new_df):
    # Load trained RandomForest model from pickle file
    model_path = r"C:\Users\malhar.yadav\scripts\PdfToDashboard\model\ecas_model.pkl"
    rf_model = joblib.load(model_path)

    # Load LabelEncoder from pickle file
    encoder_path = r"C:\Users\malhar.yadav\scripts\PdfToDashboard\model\label_encoder.pkl"
    label_encoder = joblib.load(encoder_path)
# Ensure only trained features are used
    trained_features = rf_model.feature_names_in_
    new_df = new_df[trained_features]

# Predict table type using RandomForest
    rf_preds = rf_model.predict(new_df)


# Convert predictions from numbers to table names
    rf_predicted_labels = label_encoder.inverse_transform(rf_preds)


# Add predictions to DataFrame
    new_df["table_name"] = rf_predicted_labels
    new_df = new_df[["table_no", "page_no", "table_name"]].copy()
    return new_df

# new_df = predict_table_names(rf_model, label_encoder)

# # Display results
# print("🔹 Final Predictions:\n", new_df[["table_no", "page_no", "RandomForest Prediction"]])
