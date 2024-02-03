from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer , String , Text , ForeignKey , Boolean , DateTime
from sqlalchemy.orm import relationship
from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property
import calendar

from fakiu.tools.input_tools import Field, Block, Tab , Form

class Race(db.Model ,model.Model,model.Base):
    __tablename__ = 'races'
    __table_args__ = {'extend_existing': True}
    page_title = 'Corridas'
    model_name = 'Race'
    id = Column(Integer, primary_key=True)
    
    description = Column(Text)
    datetime = Column(DateTime)
    results_added = Column(Boolean,default=False) 

    track_id = Column(Integer, ForeignKey('tracks.id'))
    championship_id = Column(Integer, ForeignKey('championships.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    track = relationship('Track', back_populates='races')
    championship = relationship('Championship', back_populates='races')
    restaurant = relationship('Restaurant', back_populates='races')
    
    racers_relations = relationship('Association_RacerRace', back_populates='race', cascade="all, delete-orphan")

    @hybrid_property
    def name(self):
        formatted_date = self.datetime.strftime("%B %Y")
        return f"{self.track.name} in {formatted_date}"
    
    @hybrid_property
    def racers(self):
        return [rel.racer for rel in self.racers_relations]

    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
            {'field': 'track','label':'Pista'}
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Info block

        fields = [
            get_field(name='championship',label='Campeonato',type='ManyToOne',related_model='Championship'),
            get_field(name='track',label='Pista',type='ManyToOne',related_model='Track'),
            get_field(name='datetime',label='Data',type='DateTime'),
            get_field(name='restaurant',label='Restaurante',type='ManyToOne',related_model='Restaurant'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form
    
    def get_display_data(self):
        data = super().get_display_data()
        action = {'url':url_for('editor.create_race_results', model_name=self.model_name, model_id=self.id),'name':'Adicionar resultados'}
        data['extra_actions'] =  [action]
        return data
    
    def get_month_name(self):
        return calendar.month_abbr[self.datetime.month].upper()