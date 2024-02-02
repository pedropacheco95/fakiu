from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer, ForeignKey , Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from fakiu.tools.input_tools import Field, Block , Form

from . import Racer , Restaurant

class Association_RacerRestaurant(db.Model ,model.Model, model.Base):
    __tablename__ = 'racers_in_restaurants'
    __table_args__ = (
        db.UniqueConstraint('racer_id', 'restaurant_id', name='_racer_restaurant_uc'),
        {'extend_existing': True}
    )
    page_title = 'Relação de Piloto Restaurante'
    model_name = 'Association_RacerRestaurant'

    id = Column(Integer, primary_key=True)

    racer_id = Column(Integer, ForeignKey('racers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    racer = relationship('Racer', back_populates='restaurants_relations')
    restaurant = relationship('Restaurant', back_populates='racers_relations')

    @hybrid_property
    def name(self):
        return f"{self.racer} in {self.restaurant}"

    def __repr__(self):
        try:
            return f"{self.restaurant}: {self.racer}"
        except:
            return f"Empty {self.model_name}"
    
    def __str__(self):
        try:
            return f"{self.restaurant}: {self.racer}"
        except:
            return f"Empty {self.model_name}"


    def display_all_info(self):
        searchable_column = {'field': 'racer','label':'Piloto'}
        table_columns = [
            {'field': 'restaurant','label':'Restaurante'},
            searchable_column,
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None,options=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model,options=options)
        form = Form()

        # Create Info block
        fields = [
            get_field(name='restaurant',label='Restaurante',type='ManyToOne',related_model='Restaurant'),
            get_field(name='racer',label='Piloto',type='ManyToOne',related_model='Racer'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form

    def get_restaurant(self):
        return self.restaurant

    def get_racer(self):
        return self.racer