from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer, ForeignKey , Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from fakiu.tools.input_tools import Field, Block , Form

from . import Championship , Team

class Association_TeamChampionship(db.Model ,model.Model, model.Base):
    __tablename__ = 'teams_in_championship'
    __table_args__ = (
        db.UniqueConstraint('championship_id', 'team_id', name='_team_championship_uc'),
        {'extend_existing': True}
    )
    page_title = 'Relação de Campeonato Equipa'
    model_name = 'Association_TeamChampionship'

    id = Column(Integer, primary_key=True)

    championship_id = Column(Integer, ForeignKey('championships.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))

    championship = relationship('Championship', back_populates='teams_relations')
    team = relationship('Team', back_populates='championships_relations')

    @hybrid_property
    def name(self):
        return f"{self.team} in {self.championship}"

    def __repr__(self):
        try:
            return f"{self.championship}: {self.team}"
        except:
            return f"Empty {self.model_name}"
    
    def __str__(self):
        try:
            return f"{self.championship}: {self.team}"
        except:
            return f"Empty {self.model_name}"


    def display_all_info(self):
        searchable_column = {'field': 'championship','label':'Corrida'}
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
            get_field(name='championship',label='Campeonato',type='ManyToOne',related_model='Championship'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form

    def get_team(self):
        return self.team

    def get_championship(self):
        return self.championship