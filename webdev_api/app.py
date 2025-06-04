import requests
from flask import Flask, request
from flasgger import Swagger

from db.model import Apartment
from db.functions import get_repository

predict_url = "http://135.181.85.42:3000/predict"

app = Flask(__name__)
app.config["SWAGGER"] = {"title": "Apartment webdev API", "uiversion": 3}
swagger = Swagger(app)

repo = get_repository()


@app.route("/add_apartments", methods=["POST"])
def add_apartments():
    """
    Add multiple apartments
    ---
    tags:
      - Apartments
    summary: Add multiple apartments
    description: Add multiple apartment entries to the database.
    parameters:
      - name: apartments
        in: body
        description: List of apartments to add
        required: true
        schema:
          type: array
          items:
            type: object
            properties:
              plz:
                type: integer
              space:
                type: number
              rooms:
                type: number
            required:
              - plz
              - space
              - rooms
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: array
            items:
              type: object
              properties:
                plz:
                  type: integer
                space:
                  type: number
                rooms:
                  type: number
              required:
                - plz
                - space
                - rooms
    responses:
      200:
        description: Apartments stored successfully!
    """
    apartments: list[Apartment] = [
        Apartment(**apartment) for apartment in request.get_json()
    ]

    repo.add_apartments(apartments)

    return "Apartments stored successfully!"


@app.route("/add_apartment", methods=["POST"])
def add_apartment():
    """
    Add a single apartment
    ---
    tags:
      - Apartments
    summary: Add a single apartment
    description: Add one apartment entry to the database.
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
      - name: price
        in: formData
        type: number
        required: true
    responses:
      200:
        description: Apartment stored successfully!
    """
    apartment: Apartment = Apartment(**request.form.to_dict())

    repo.add_apartment(apartment)

    return "Apartment stored successfully!"


@app.route("/get_apartments", methods=["GET"])
def get_apartments():
    """
    Get all apartments
    ---
    tags:
      - Apartments
    summary: Get all apartments
    description: Retrieve a list of all apartments stored in the database.
    responses:
      200:
        description: List of apartments
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  plz:
                    type: integer
                  space:
                    type: number
                  rooms:
                    type: number
    """
    apartments: list[Apartment] = repo.get_apartments()

    return apartments


@app.route("/predict_price", methods=["POST"])
def predict_price():
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
    plz: int = int(request.form["plz"])
    space: float = float(request.form["space"])
    rooms: float = float(request.form["rooms"])

    url = (
        f"{predict_url}"
        f"?plz={plz}"
        f"&space={space}"
        f"&rooms={rooms}"
    )

    response = requests.get(url).text
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
