from fakiu import model 
from fakiu.sql_db import db
from flask import url_for
from sqlalchemy import Column, Integer , String , Text , ForeignKey , Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from fakiu.tools.input_tools import Field, Block, Tab , Form

class Team(db.Model ,model.Model,model.Base):
    __tablename__ = 'teams'
    __table_args__ = {'extend_existing': True}
    page_title = 'Equipas'
    model_name = 'Team'
    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    description = Column(Text)
    abbreviation = Column(String(4))
    picture_path = Column(String(255))
    kart_picture_path = Column(String(255))
    primary_color = Column(String(255),default='#000000')
    secondary_color = Column(String(255),default='#000000')
    tertiary_color = Column(String(255),default='#000000')

    racers_relations = relationship('Association_RacerTeam', back_populates='team', cascade="all, delete-orphan")
    championships_relations = relationship('Association_TeamChampionship', back_populates='team', cascade="all, delete-orphan")

    @hybrid_property
    def racers(self):
        return [rel.racer for rel in self.racers_relations]
    
    @hybrid_property
    def championships(self):
        return [rel.championship for rel in self.championships_relations]
    
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
            get_field(name='abbreviation',label='Abreviatura',type='Text'),
            get_field(name='racers_relations',label='Pilotos',type='ManyToMany',related_model='Association_RacerTeam'),
            get_field(name='primary_color',label='Cor principal',type='Color'),
            get_field(name='secondary_color',label='Cor secundária',type='Color'),
            get_field(name='tertiary_color',label='Cor terciária',type='Color'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        # Create Fotografias tab
        fields = [
            get_field(name='kart_picture_path',label='Fotografia do kart',type='Picture'),
        ]
        form.add_tab(Tab(title='Fotografias',fields=fields,orientation='horizontal'))
        
        return form

    def kart_image_full_url(self):
        return url_for('static', filename=f"images/{self.kart_picture_path}")
    
    def logo_full_url(self):
        return url_for('static', filename=f"images/{self.picture_path}")