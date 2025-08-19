"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, FavoritePeople, FavoritePlanet

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

CURRENT_USER_ID = 1

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {"msg": "Hello, this is your GET /user response "}
    return jsonify(response_body), 200


@app.get("/people")
def list_people():
    people = People.query.all()
    return jsonify([p.serialize() for p in people]), 200


@app.get("/people/<int:people_id>")
def get_person(people_id):
    p = People.query.get(people_id)
    if not p:
        return jsonify({"msg": "people not found"}), 404
    return jsonify(p.serialize()), 200


@app.get("/planets")
def list_planets():
    planets = Planet.query.all()
    return jsonify([pl.serialize() for pl in planets]), 200


@app.get("/planets/<int:planet_id>")
def get_planet(planet_id):
    pl = Planet.query.get(planet_id)
    if not pl:
        return jsonify({"msg": "planet not found"}), 404
    return jsonify(pl.serialize()), 200


@app.get("/users")
def list_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200


@app.get("/users/favorites")
def list_my_favorites():
    fav_people = FavoritePeople.query.filter_by(user_id=CURRENT_USER_ID).all()
    fav_planets = FavoritePlanet.query.filter_by(user_id=CURRENT_USER_ID).all()
    return jsonify({
        "people": [fp.people.serialize() for fp in fav_people],
        "planets": [fp.planet.serialize() for fp in fav_planets],
    }), 200


@app.post("/favorite/people/<int:people_id>")
def add_fav_person(people_id):
    if not People.query.get(people_id):
        return jsonify({"msg": "people not found"}), 404
    exists = FavoritePeople.query.filter_by(user_id=CURRENT_USER_ID, people_id=people_id).first()
    if exists:
        return jsonify({"msg": "favorite already exists"}), 409
    db.session.add(FavoritePeople(user_id=CURRENT_USER_ID, people_id=people_id))
    db.session.commit()
    return jsonify({"done": True}), 201


@app.post("/favorite/planet/<int:planet_id>")
def add_fav_planet(planet_id):
    if not Planet.query.get(planet_id):
        return jsonify({"msg": "planet not found"}), 404
    exists = FavoritePlanet.query.filter_by(user_id=CURRENT_USER_ID, planet_id=planet_id).first()
    if exists:
        return jsonify({"msg": "favorite already exists"}), 409
    db.session.add(FavoritePlanet(user_id=CURRENT_USER_ID, planet_id=planet_id))
    db.session.commit()
    return jsonify({"done": True}), 201


@app.delete("/favorite/people/<int:people_id>")
def delete_fav_person(people_id):
    fav = FavoritePeople.query.filter_by(user_id=CURRENT_USER_ID, people_id=people_id).first()
    if not fav:
        return jsonify({"msg": "favorite not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"done": True}), 200


@app.delete("/favorite/planet/<int:planet_id>")
def delete_fav_planet(planet_id):
    fav = FavoritePlanet.query.filter_by(user_id=CURRENT_USER_ID, planet_id=planet_id).first()
    if not fav:
        return jsonify({"msg": "favorite not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"done": True}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
