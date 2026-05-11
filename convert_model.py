import joblib

model = joblib.load(
    "models/best_delivery_model_after_tuning.pkl"
)

joblib.dump(
    model,
    "models/final_streamlit_model.pkl"
)

print("Model converted successfully")