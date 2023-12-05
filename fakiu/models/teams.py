from fakiu import model 
from fakiu.sql_db import db
from flask import url_for
from sqlalchemy import Column, Integer , String , Text , ForeignKey , Boolean
from sqlalchemy.orm import relationship

from .associations import racer_team, team_championship
from fakiu.tools.input_tools import Field, Block, Tab , Form

class Team(db.Model ,model.Model,model.Base):
    __tablename__ = 'teams'
    __table_args__ = {'extend_existing': True}
    page_title = 'Equipas'
    model_name = 'Team'
    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    description = Column(Text)
    picture_path = Column(String(255))
    primary_color = Column(String(255))
    secondary_color = Column(String(255))

    racers = relationship('Racer',secondary=racer_team, back_populates='teams', cascade="all")
    championships = relationship('Championship',secondary=team_championship, back_populates='teams', cascade="all")

    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
            {'field': 'racers','label':'Pilotos'}
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Picture block

        fields = [get_field(name='picture_path',label='Emblema',type='EditablePicture')]
        picture_block = Block('picture_block',fields)
        form.add_block(picture_block)

        # Create Info block

        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
            get_field(name='racers',label='Pilotos',type='ManyToMany',related_model='Racer'),
            get_field(name='primary_color',label='Cor principal',type='Color'),
            get_field(name='secondary_color',label='Cor secundária',type='Color'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)
        
        return form
