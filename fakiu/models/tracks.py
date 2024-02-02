from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer , String , Text , ForeignKey , Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from flask import url_for

from fakiu.tools.input_tools import Field, Block, Tab , Form

class Track(db.Model ,model.Model,model.Base):
    __tablename__ = 'tracks'
    __table_args__ = {'extend_existing': True}
    page_title = 'Pistas'
    model_name = 'Track'
    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    description = Column(Text)
    address = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255))
    website = Column(String(255))
    picture_path = Column(String(255))

    races = relationship('Race', back_populates='track', cascade="all, delete-orphan")

    racers_relations = relationship('Association_RacerTrack', back_populates='track', cascade="all, delete-orphan")
    
    @hybrid_property
    def racers(self):
        return [rel.race for rel in self.racers_relations]
    
    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
            {'field': 'name','label':'Nome'}
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Picture block

        fields = [get_field(name='picture_path',label='Imagem',type='EditablePicture')]
        picture_block = Block('picture_block',fields)
        form.add_block(picture_block)

        # Create Info block

        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
            get_field(name='description',label='Descrição',type='Text'),
            get_field(name='address',label='Morada',type='Text'),
            get_field(name='phone',label='Telemovel',type='Text'),
            get_field(name='email',label='Email',type='Text'),
            get_field(name='website',label='Website',type='Text'),
            get_field(name='racers_relations',label='Pilotos',type='ManyToMany',related_model='Association_RacerTrack'),
            get_field(name='races',label='Pistas',type='ManyToMany',related_model='Race'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)
        
        return form
    
    def full_image_url(self):
        return url_for('static', filename=f"images/{self.picture_path}")