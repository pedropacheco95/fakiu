from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer , String , Text , ForeignKey , Boolean
from sqlalchemy.orm import relationship

from .associations import racer_track

class Track(db.Model ,model.Model,model.Base):
    __tablename__ = 'tracks'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    description = Column(Text)
    address = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255))
    website = Column(String(255))
    picture_path = Column(String(255))

    racers = relationship('Racer',secondary=racer_track, back_populates='tracks', cascade="all")
    races = relationship('Race', back_populates='track', cascade="all, delete-orphan")
    