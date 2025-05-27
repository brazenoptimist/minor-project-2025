import joblib


pkg = joblib.load("depression_model.pkl")
proba = pkg["model"].predict_proba(new_df)[:,1]
pred  = (proba >= pkg["threshold"]).astype(int)