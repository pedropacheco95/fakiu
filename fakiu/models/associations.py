from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

racer_championship = db.Table('racers_in_championships',
    Column('racer_id', Integer, ForeignKey('racers.id'), primary_key=True),
    Column('championship_id', Integer, ForeignKey('championships.id'), primary_key=True)
)

racer_race = db.Table('racers_in_race',
    Column('racer_id', Integer, ForeignKey('racers.id'), primary_key=True),
    Column('race_id', Integer, ForeignKey('races.id'), primary_key=True)
)

racer_track = db.Table('racers_in_tracks',
    Column('racer_id', Integer, ForeignKey('racers.id'), primary_key=True),
    Column('track_id', Integer, ForeignKey('tracks.id'), primary_key=True)
)

racer_restaurant = db.Table('racers_in_restaurants',
    Column('racer_id', Integer, ForeignKey('racers.id'), primary_key=True),
    Column('restaurant_id', Integer, ForeignKey('restaurants.id'), primary_key=True)
)

racer_team = db.Table('racers_in_teams',
    Column('racer_id', Integer, ForeignKey('racers.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True)
)

team_championship = db.Table('teams_in_championship',
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True),
    Column('championship_id', Integer, ForeignKey('championships.id'), primary_key=True)
)
