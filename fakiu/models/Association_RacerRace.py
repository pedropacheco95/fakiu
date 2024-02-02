from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Float, Integer, ForeignKey , Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from fakiu.tools.input_tools import Field, Block , Form

from . import Racer , Race

class Association_RacerRace(db.Model ,model.Model, model.Base):
    __tablename__ = 'racers_in_race'
    __table_args__ = (
        db.UniqueConstraint('racer_id', 'race_id', name='_racer_race_uc'),
        {'extend_existing': True}
    )
    page_title = 'Relação de Piloto Corrida'
    model_name = 'Association_RacerRace'

    id = Column(Integer, primary_key=True)

    racer_id = Column(Integer, ForeignKey('racers.id'))
    race_id = Column(Integer, ForeignKey('races.id'))

    qualification_place = Column(Integer)
    qualification_points = Column(Float,default=0)
    place = Column(Integer)
    points = Column(Float,default=0)
    punishments = Column(Float,default=0)
    extras = Column(Float,default=0)
    fastest_lap = Column(Boolean, default=False)
    driver_of_the_day = Column(Boolean, default=False)

    punishment_and_extras_description = Column(Text)

    racer = relationship('Racer', back_populates='races_relations')
    race = relationship('Race', back_populates='racers_relations')

    @hybrid_property
    def name(self):
        return f"{self.racer} in {self.race}"
    
    @hybrid_property
    def total_points(self):
        return self.qualification_points + self.points + self.extras + int(self.fastest_lap) + int(self.driver_of_the_day) - self.punishments

    def __repr__(self):
        try:
            return f"{self.race}: {self.racer}"
        except:
            return f"Empty {self.model_name}"
    
    def __str__(self):
        try:
            return f"{self.race}: {self.racer}"
        except:
            return f"Empty {self.model_name}"

    def create(self,points=False):
        super().create()
        if points:
            if self.place == 0 and self.qualification_place == 0:
                self.punishments = points[self.place]['points']
                self.punishment_and_extras_description = f'Piloto recebeu castigo de {self.punishments} pontos porque faltou à corrida'
            else:
                self.points = points[self.place]['points']
                self.qualification_points = points[self.qualification_place]['qualification_points']
            self.save()
        

    def display_all_info(self):
        searchable_column = {'field': 'racer','label':'Piloto'}
        table_columns = [
            {'field': 'race','label':'Corrida'},
            searchable_column,
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None,options=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model,options=options)
        form = Form()

        # Create Info block
        fields = [
            get_field(name='race',label='Corridas',type='ManyToOne',related_model='Race'),
            get_field(name='racer',label='Piloto',type='ManyToOne',related_model='Racer'),
            get_field(name='qualification_place',label='Lugar na qualificação',type='Integer'),
            get_field(name='qualification_points',label='Pontos na qualificação',type='Float'),
            get_field(name='place',label='Place',type='Integer'),
            get_field(name='points',label='Pontos',type='Float'),
            get_field(name='punishments',label='Pontos de castigo',type='Float'),
            get_field(name='extras',label='Pontos extra',type='Float'),
            get_field(name='fastest_lap',label='Volta mais rápida',type='Boolean'),
            get_field(name='driver_of_the_day',label='Driver of the day',type='Boolean'),
            get_field(name='punishment_and_extras_description',label='Descrição de castigos e extras',type='Text'),
            
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form

    def get_race(self):
        return self.race

    def get_racer(self):
        return self.racer
    