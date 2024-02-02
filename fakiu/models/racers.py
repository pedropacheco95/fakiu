from fakiu import model 
from fakiu.sql_db import db
from flask import url_for
from sqlalchemy import Column, Integer , String , Float , Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from fakiu.tools.input_tools import Field, Block, Tab , Form

class Racer(db.Model ,model.Model, model.Base):
    __tablename__ = 'racers'
    __table_args__ = {'extend_existing': True}
    page_title = 'Pilotos'
    model_name = 'Racer'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    surname = Column(String(255))
    nickname = Column(String(255))
    abbreviation = Column(String(4))
    height = Column(Float,default=1.80)
    weight = Column(Float,default=75)

    picture = Column(String(255))
    winner_picture = Column(String(255))
    serious_picture = Column(String(255))
    kart_picture = Column(String(255))

    championships_relations = relationship('Association_RacerChampionship', back_populates='racer', cascade="all, delete-orphan")
    races_relations = relationship('Association_RacerRace', back_populates='racer', cascade="all, delete-orphan")
    tracks_relations = relationship('Association_RacerTrack', back_populates='racer', cascade="all, delete-orphan")
    restaurants_relations = relationship('Association_RacerRestaurant', back_populates='racer', cascade="all, delete-orphan")
    teams_relations = relationship('Association_RacerTeam', back_populates='racer', cascade="all, delete-orphan")

    @hybrid_property
    def name(self):
        return f"{self.first_name} {self.surname}"
    
    @hybrid_property
    def championships(self):
        return [rel.championship for rel in self.championships_relations]
    
    @hybrid_property
    def races(self):
        return [rel.race for rel in self.races_relations]
    
    @hybrid_property
    def tracks(self):
        return [rel.track for rel in self.tracks_relations]
    
    @hybrid_property
    def restaurants(self):
        return [rel.restaurant for rel in self.restaurants_relations]
    
    @hybrid_property
    def teams(self):
        return [rel.team for rel in self.teams_relations]
    
    @hybrid_property
    def team(self):
        if self.teams:
            return self.teams[-1]
        return None

    def display_all_info(self):
        searchable_column = {'field': 'first_name','label':'Nome'}
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
            get_field(name='first_name',label='Primeiro nome',type='Text',required=True),
            get_field(name='surname',label='Apelido',type='Text',required=True),
            get_field(name='nickname',label='Alcunha',type='Text'),
            get_field(name='abbreviation',label='Abreviatura',type='Text'),
            get_field(name='teams_relations',label='Equipas',type='ManyToMany',related_model='Association_RacerTeam'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        # Create Caracteristicas Físicas tab
        fields = [
            get_field(name='height',label='Altura (m)',type='Float'),
            get_field(name='weight',label='Peso (kg)',type='Float'),
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
            get_field(name='first_name',label='Primeiro nome',type='Text',required=True),
            get_field(name='surname',label='Apelido',type='Text',required=True),
            get_field(name='nickname',label='Alcunha',type='Text'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form

    def full_image_url(self):
        return url_for('static', filename=f"images/{self.picture}")
    
    def racer_url(self):
        return  url_for('main.racer', id=self.id)
    
    def total_points(self):
        return  sum([rel.total_points for rel in self.races_relations])
    
    def best_result(self):
        return  min([rel.place for rel in self.races_relations])
    
    def worst_result(self):
        return  max([rel.place for rel in self.races_relations])