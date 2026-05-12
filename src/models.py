import os
from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er

db = SQLAlchemy()


class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))

    def serialize(self):
        return {"id": self.id, "name": self.name}


class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    climate: Mapped[Optional[str]] = mapped_column(String(100))

    def serialize(self):
        return {"id": self.id, "name": self.name}


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return {"id": self.id, "email": self.email}


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("character.id"))
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"))

    user: Mapped["User"] = relationship(back_populates="favorites")
    character: Mapped[Optional["Character"]] = relationship()
    planet: Mapped[Optional["Planet"]] = relationship()

    def serialize(self):
        return {"id": self.id, "user_id": self.user_id}
