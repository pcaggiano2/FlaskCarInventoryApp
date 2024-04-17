from flask import Flask
from waitress import serve
import random

app = Flask(__name__)

fields = ["make", "model", "year", "color"]

def _generate_car_info():
    car_info = {}
    for field in fields:
        if field == "make":
            car_info[field] = random.choice(["Audi", "BMW", "Chevrolet", "Ford", "Honda", "Hyundai", "Kia", "Mazda", "Mercedes-Benz", "Nissan", "Toyota", "Volkswagen", "Volvo"])
        elif field == "model":
            car_info[field] = random.choice(["A4", "A6", "A8", "Coupe", "Convertible", "Electric", "Hatchback", "Limousine", "Minivan", "Pickup", "Sedan", "SUV", "Wagon"])
        elif field == "year":
            car_info[field] = random.randint(1900, 2022)
        else:
            car_info[field] = random.choice(["Red", "Blue", "Green", "Yellow", "Black", "White", "Pink", "Orange", "Purple", "Brown", "Gray", "Cyan", "Magenta", "Gold", "Silver", "Platinum", "Copper", "Titanium", "Bronze", "Steel", "Aluminum", "Lead", "Zinc", "Nickel", "Cobalt", "Manganese", "Iron", "Copper", "Tin", "Silver", "Gold", "Platinum", "Diamond", "Ruby", "Sapphire", "Emerald", "Amethyst", "Topaz", "Opal", "Jade"])
    return car_info
## handlers
@app.get("/car-info/<string:vin>")
def get_car(vin):
    if len(vin)!=17:
        return {"error": "Request has invalid or missing data"}, 422
    return _generate_car_info(), 200
    
serve(app, listen='*:8082')

