from mlflow import MlflowClient
import mlflow
from flask import Flask, request, jsonify
from flasgger import Swagger
import pandas as pd

app = Flask(__name__)
app.config["SWAGGER"] = {"title": "Apartment webdev API", "uiversion": 3}
swagger = Swagger(app)


mlflow.set_tracking_uri("http://135.181.85.42:5000")

client = MlflowClient()
model_version = client.get_latest_versions(
    "champion-model", stages=["Production"])[0]

model_uri = f"mlflow-artifacts:/2/{model_version.run_id}/artifacts/predict_model/"
model = mlflow.sklearn.load_model(model_uri)


@app.route("/predict", methods=["GET"])
def predict():
    """
    Predict apartment price
    ---
    tags:
      - Prediction
    summary: Predict apartment price
    description: Predict the price of an apartment.
    parameters:
      - name: plz
        in: formData
        type: integer
        required: true
      - name: space
        in: formData
        type: number
        required: true
      - name: rooms
        in: formData
        type: number
        required: true
    responses:
      200:
        description: Predicted price
        content:
          text/plain:
            schema:
              type: string
    """
    plz = request.args.get("plz", type=int)
    space = request.args.get("space", type=float)
    rooms = request.args.get("rooms", type=float)

    if None in [plz, space, rooms]:
        return jsonify({"error": "Missing required parameters"}), 400

    input_features = pd.DataFrame(
        [{"plz": str(
            plz), "space": space, "rooms": rooms}]
    )

    prediction = model.predict(input_features)

    return jsonify({"prediction": prediction.tolist()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
