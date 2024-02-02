from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer, ForeignKey , Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from fakiu.tools.input_tools import Field, Block , Form

from . import Racer , Team

class Association_RacerTeam(db.Model ,model.Model, model.Base):
    __tablename__ = 'racers_in_team'
    __table_args__ = (
        db.UniqueConstraint('racer_id', 'team_id', name='_racer_team_uc'),
        {'extend_existing': True}
    )
    page_title = 'Relação de Piloto Equipa'
    model_name = 'Association_RacerTeam'

    id = Column(Integer, primary_key=True)

    racer_id = Column(Integer, ForeignKey('racers.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))

    racer = relationship('Racer', back_populates='teams_relations')
    team = relationship('Team', back_populates='racers_relations')

    @hybrid_property
    def name(self):
        return f"{self.racer} in {self.team}"

    def __repr__(self):
        try:
            return f"{self.team}: {self.racer}"
        except:
            return f"Empty {self.model_name}"
    
    def __str__(self):
        try:
            return f"{self.team}: {self.racer}"
        except:
            return f"Empty {self.model_name}"


    def display_all_info(self):
        searchable_column = {'field': 'racer','label':'Piloto'}
        table_columns = [
            {'field': 'team','label':'Equipa'},
            searchable_column,
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None,options=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model,options=options)
        form = Form()

        # Create Info block
        fields = [
            get_field(name='team',label='Equipa',type='ManyToOne',related_model='Team'),
            get_field(name='racer',label='Piloto',type='ManyToOne',related_model='Racer'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form

    def get_team(self):
        return self.team

    def get_racer(self):
        return self.racer