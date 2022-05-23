import os

import joblib
import pandas as pd


lgbm_model = joblib.load(os.getcwd() + "/model/lgbm_model.joblib")
enc = joblib.load(os.getcwd() + "/model/encoder.joblib")
team_dict = {0: "CT", 1: "T"}


def welcome_message() -> dict:
    """Welcome message to test the API."""
    return {"message": "Hello World!"}


def return_prediction(payload) -> dict:
    """Return a prediction for a single example from the testset with our own ML model.

    Args:
        - payload: a json string with data for a single example
    """
    try:
        # load data in correct format
        data = pd.read_json(payload, typ="series").to_frame()
        data = data.T

        # transform categorical data with one-hot encoder saved during training process
        enc_df = pd.DataFrame(enc.transform(data[["map"]]).toarray())
        data = data.join(enc_df)
        data = data.drop("map", axis=1)
        data = data.astype("float")

        # Get prediction
        pred = lgbm_model.predict(data)
        predicted_proba = lgbm_model.predict_proba(data)[0][pred]
        pred_desc = team_dict[pred[0]]

        return {
            "message": f"Lgbm model predicts '{pred_desc}' with a probability of {predicted_proba}",
        }

    except Exception as e:
        raise Exception(f"Something went wrong, please check your request. Error: {e}")
