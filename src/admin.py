import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, People, Planet

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(Planet, db.session))

    if os.getenv("SEED") == "1":
        seed_data(app)

def seed_data(app):
    with app.app_context():
        if not User.query.first():
            db.session.add(User(email="test@sw.com", password="123", is_active=True))
        if not People.query.first():
            db.session.add_all([
                People(name="Luke Skywalker"),
                People(name="Leia Organa"),
            ])
        if not Planet.query.first():
            db.session.add_all([
                Planet(name="Tatooine"),
                Planet(name="Alderaan"),
            ])
        db.session.commit()
