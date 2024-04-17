from flask import Flask, request, jsonify
from waitress import serve
import requests

app = Flask(__name__)

cars = [
    { "id": 1, "make": "Lamborghini", "model":"Gallardo", "year":2006, "vin":"JN1BY1PR0FM736887", "color":"Mauve" },
    { "id": 2, "make": "Chevrolet", "model":"Monte Carlo", "year":1996, "vin":"1G4HP54K714224234", "color":"Violet" }
]

fields = ["id", "vin", "make", "model", "year", "color"]

vin_decoder_url = "http://vin-decoder-service:8082/car-info/"  # Kubernetes
#vin_decoder_url = "http://localhost:8082/car-info/"  # Local

## helper functions

def _find_next_id():
    return max(car["id"] for car in cars) + 1

def _find_car_pos(id):
    for pos, car in enumerate(cars):
        if car["id"] == id:
            return pos
    return -1

def _has_all_fields(car):
    return set(car.keys()) == set(fields)

## handlers

@app.get("/cars")
def get_cars():
    return jsonify(cars) # generates JSON from a Python list

@app.get("/cars/<int:id>")
def get_car(id):
    pos = _find_car_pos(id)
    if pos >= 0:
        return cars[pos]
    return {"error": "The requested id was not found"}, 404

@app.post("/cars")
def add_car():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    
    vin = request.get_json()["vin"]

    for car in cars:
        if car["vin"] == vin:
            return {"error": "The requested VIN already exists"}, 409

    response = requests.get(vin_decoder_url + vin)
    
    if response.status_code == 200:
        car_info = response.json()
        car = {
            "id": _find_next_id(),
            "vin": vin,
            "make": car_info["make"],
            "model": car_info["model"],
            "year": car_info["year"],
            "color": car_info["color"]
        }
        if _has_all_fields(car):
            cars.append(car)
            return car, 201
    return {"error": "Request has invalid or missing data"}, 422

@app.delete("/cars/<int:id>")
def delete_car(id):
    pos = _find_car_pos(id)
    if pos >= 0:
        cars.pop(pos)
        return "", 204
    return {"error": "The requested id was not found"}, 404

serve(app, listen='*:8081')

