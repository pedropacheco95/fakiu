from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer, ForeignKey , Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from fakiu.tools.input_tools import Field, Block , Form

from . import Racer , Championship

class Association_RacerChampionship(db.Model ,model.Model, model.Base):
    __tablename__ = 'racers_in_championships'
    __table_args__ = (
        db.UniqueConstraint('racer_id', 'championship_id', name='_racer_championship_uc'),
        {'extend_existing': True}
    )
    page_title = 'Relação de Piloto Campeonato'
    model_name = 'Association_RacerChampionship'

    id = Column(Integer, primary_key=True)

    racer_id = Column(Integer, ForeignKey('racers.id'))
    championship_id = Column(Integer, ForeignKey('championships.id'))

    racer = relationship('Racer', back_populates='championships_relations')
    championship = relationship('Championship', back_populates='racers_relations')

    @hybrid_property
    def name(self):
        return f"{self.racer} in {self.championship}"

    def __repr__(self):
        try:
            return f"{self.championship}: {self.racer}"
        except:
            return f"Empty {self.model_name}"
    
    def __str__(self):
        try:
            return f"{self.championship}: {self.racer}"
        except:
            return f"Empty {self.model_name}"


    def display_all_info(self):
        searchable_column = {'field': 'racer','label':'Piloto'}
        table_columns = [
            {'field': 'championship','label':'Campeonato'},
            searchable_column,
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None,options=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model,options=options)
        form = Form()

        # Create Info block
        fields = [
            get_field(name='championship',label='Campeonatos',type='ManyToOne',related_model='Championship'),
            get_field(name='racer',label='Piloto',type='ManyToOne',related_model='Racer'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form

    def get_championship(self):
        return self.championship

    def get_racer(self):
        return self.racer