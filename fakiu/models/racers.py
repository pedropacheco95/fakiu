from fakiu import model 
from fakiu.sql_db import db
from flask import url_for
from sqlalchemy import Column, Integer , String , Float , Boolean
from sqlalchemy.orm import relationship

from .associations import racer_championship, racer_race, racer_restaurant, racer_team, racer_track
from fakiu.tools.input_tools import Field, Block, Tab , Form

class Racer(db.Model ,model.Model, model.Base):
    __tablename__ = 'racers'
    __table_args__ = {'extend_existing': True}
    page_title = 'Pilotos'
    model_name = 'Racer'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    surname = Column(String(255))
    nickname = Column(String(255))
    height = Column(Float,default=1.80)
    weight = Column(Float,default=75)
    was_born = Column(Boolean,default=False)

    picture = Column(String(255))
    winner_picture = Column(String(255))
    serious_picture = Column(String(255))
    kart_picture = Column(String(255))

    championships = relationship('Championship', secondary=racer_championship, back_populates='racers', cascade="all")
    races = relationship('Race',secondary=racer_race, back_populates='racers', cascade="all")
    restaurants = relationship('Restaurant',secondary=racer_restaurant, back_populates='racers', cascade="all")
    teams = relationship('Team',secondary=racer_team, back_populates='racers', cascade="all")
    tracks = relationship('Track',secondary=racer_track, back_populates='racers', cascade="all")

    user = relationship('User',back_populates='racer', uselist=False, cascade="all, delete-orphan")

    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
            {'field': 'team','label':'Equipa'}
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Picture block

        fields = [get_field(name='picture',label='Fotografia',type='EditablePicture')]
        picture_block = Block('picture_block',fields)
        form.add_block(picture_block)

        # Create Info block

        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
            get_field(name='surname',label='Apelido',type='Text',required=True),
            get_field(name='was_born',label='Nasceu',type='Boolean'),
            get_field(name='nickname',label='Alcunha',type='Text'),
            get_field(name='teams',label='Equipas',type='ManyToMany',related_model='Team'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        # Create Caracteristicas Físicas tab
        fields = [
            get_field(name='height',label='Altura',type='Float'),
            get_field(name='weight',label='Peso',type='Float'),
        ]
        form.add_tab(Tab(title='Caracteristicas Físicas',fields=fields,orientation='vertical'))

        # Create Fotografias tab
        fields = [
            get_field(name='winner_picture',label='Fotografia de vencedor',type='EditablePicture'),
            get_field(name='serious_picture',label='Fotografia séria',type='EditablePicture'),
            get_field(name='kart_picture',label='Fotografia do kart',type='EditablePicture'),
        ]
        form.add_tab(Tab(title='Fotografias',fields=fields,orientation='horizontal'))

        return form
    
    def get_basic_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()

        # Create Info block
        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
            get_field(name='surname',label='Apelido',type='Text',required=True),
            get_field(name='nickname',label='Alcunha',type='Text'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form
