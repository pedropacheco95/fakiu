from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer , String , Text , ForeignKey , Boolean , Date
from sqlalchemy.orm import relationship

from .associations import racer_race

class Race(db.Model ,model.Model,model.Base):
    __tablename__ = 'races'
    __table_args__ = {'extend_existing': True}
    page_title = 'Corridas'
    model_name = 'Race'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    date = Column(Date)

    track_id = Column(Integer, ForeignKey('tracks.id'), primary_key=True)
    championship_id = Column(Integer, ForeignKey('championships.id'), primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), primary_key=True)

    track = relationship('Track', back_populates='races')
    championship = relationship('Championship', back_populates='races')
    restaurant = relationship('Restaurant', back_populates='races')
    
    racers = relationship('Racer',secondary=racer_race, back_populates='races', cascade="all")

