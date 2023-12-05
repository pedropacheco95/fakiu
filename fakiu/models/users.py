from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer , String , Text , ForeignKey , Boolean
from sqlalchemy.orm import relationship

class User(db.Model ,model.Model,model.Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    is_admin = Column(Boolean, default=False)
    generated_code = Column(Integer)

    racer_id = Column(Integer, ForeignKey('racers.id'))

    racer = relationship('Racer', back_populates="user")
    