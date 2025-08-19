from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, BigInteger, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self) -> dict:
        return {"id": self.id, "email": self.email}

class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    height: Mapped[int | None] = mapped_column(nullable=True)
    mass: Mapped[int | None] = mapped_column(nullable=True)
    hair_color: Mapped[str | None] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str | None] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str | None] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str | None] = mapped_column(String(20), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)

    favorites: Mapped[list["FavoritePeople"]] = relationship(
        back_populates="people",
        cascade="all, delete-orphan"
    )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }

class Planet(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    climate: Mapped[str | None] = mapped_column(String(80), nullable=True)
    terrain: Mapped[str | None] = mapped_column(String(80), nullable=True)
    population: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    diameter: Mapped[int | None] = mapped_column(nullable=True)
    gravity: Mapped[str | None] = mapped_column(String(30), nullable=True)

    favorites: Mapped[list["FavoritePlanet"]] = relationship(
        back_populates="planet",
        cascade="all, delete-orphan"
    )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "diameter": self.diameter,
            "gravity": self.gravity,
        }

class FavoritePeople(db.Model):
    __tablename__ = "favorite_people"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "people_id", name="uq_user_people"),)

    people: Mapped["People"] = relationship(back_populates="favorites")

    def serialize(self) -> dict:
        return {"id": self.id, "user_id": self.user_id, "people_id": self.people_id}

class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "planet_id", name="uq_user_planet"),)

    planet: Mapped["Planet"] = relationship(back_populates="favorites")

    def serialize(self) -> dict:
        return {"id": self.id, "user_id": self.user_id, "planet_id": self.planet_id}
