#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


@app.get("/restaurants")
def all_restaurants():
    return [restaurant.to_dict(rules=("-restaurant_pizzas",)) for restaurant in Restaurant.query.all()], 200

@app.get("/restaurants/<int:id>")
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id ==id).first()
    if restaurant:
        return restaurant.to_dict(), 200
    else:
        return{'error':'Restaurant not found'}, 404
    
@app.delete("/restaurants/<int:id>")
def delete_restaurant(id):
    restaurant=Restaurant.query.filter(Restaurant.id==id).first()
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return{}, 204
    else:
        return {
         "error": "Restaurant not found"
        }, 404
    
@app.get("/pizzas")
def get_pizzas():
    return [pizza.to_dict(rules=("-restaurant_pizzas",)) for pizza in Pizza.query.all()], 200

@app.post("/restaurant_pizzas")
def post_restaurant_pizza():
    try:
        restaurant_pizza=RestaurantPizza(
            price=request.json.get('price'),
            restaurant_id=request.json.get('restaurant_id'),
            pizza_id=request.json.get('pizza_id'),
        )
        db.session.add(restaurant_pizza)
        db.session.commit()
        return restaurant_pizza.to_dict(),201
    except ValueError as error:
        return {"errors": ["validation errors"]}, 400
   

    
    #     data = request.json

    # # Validation checks
    #     if 'price' not in data or data['price'] <= 0:
    #         return {'error': 'Invalid price'}, 400
    #     if 'restaurant_id' not in data or 'pizza_id' not in data:
    #         return {'error': 'Missing restaurant_id or pizza_id'}, 400

    #     # Create new RestaurantPizza instance
    #     restaurant_pizza = RestaurantPizza(
    #         price=data['price'],
    #         restaurant_id=data['restaurant_id'],
    #         pizza_id=data['pizza_id']
    #     )
    #     db.session.add(restaurant_pizza)
    #     db.session.commit()
    #     return restaurant_pizza.to_dict(),201

if __name__ == "__main__":
    app.run(port=5555, debug=True)
