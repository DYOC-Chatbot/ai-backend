import joblib

joblib_file = "classifier.pkl"
pipeline = joblib.load(joblib_file)


def predict_message(new_message):
    prediction = pipeline.predict([new_message])
    return "Request" if prediction[0] == 0 else "Query"
