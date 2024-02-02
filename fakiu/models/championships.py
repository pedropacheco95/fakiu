from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer , String , Text , ForeignKey , Boolean , Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from fakiu.tools.input_tools import Field, Block, Form

class Championship(db.Model ,model.Model,model.Base):
    __tablename__ = 'championships'
    __table_args__ = {'extend_existing': True}
    page_title = 'Campeonatos'
    model_name = 'Championship'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    number_of_racers = Column(Integer,default=12)

    races = relationship('Race', back_populates='championship', cascade="all, delete-orphan")
    race_point_distributions = relationship('RacePointDistribution', back_populates='championship', cascade="all, delete-orphan")

    racers_relations = relationship('Association_RacerChampionship', back_populates='championship', cascade="all, delete-orphan")
    teams_relations = relationship('Association_TeamChampionship', back_populates='championship', cascade="all, delete-orphan")

    @hybrid_property
    def racers(self):
        return [rel.racer for rel in self.racers_relations]
    
    @hybrid_property
    def teams(self):
        return [rel.team for rel in self.teams_relations]
    
    def create(self):
        super().create()
        from fakiu.models import RacePointDistribution
        for i in range(self.number_of_racers+1):
            rpd = RacePointDistribution(place=i,championship_id=self.id)
            rpd.create()
    
    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
            {'field': 'description','label':'Descrição'},
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()

        # Create Info block

        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
            get_field(name='number_of_racers',label='Número de pilotos',type='Integer'),
            get_field(name='racers_relations',label='Pilotos',type='ManyToMany',required=True,related_model='Association_RacerChampionship'),
            get_field(name='teams_relations',label='Equipas',type='ManyToMany',required=True,related_model='Association_TeamChampionship'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)
        
        return form
    
    def get_championship_table(self):
        championship_table = [{'racer':racer,'points':sum([rel.total_points for rel in racer.races_relations if rel.race.championship.id == self.id])} for racer in self.racers]
        championship_table_sorted = sorted(championship_table, key=lambda x: x['points'], reverse=True)
        for index, entry in enumerate(championship_table_sorted, start=1):
            entry['place'] = index
        return championship_table_sorted
    
    def get_championship_table_teams(self):
        championship_table = [{
            'team': team,
            'points': sum(sum(rel.total_points for rel in racer.races_relations if rel.race.championship.id == self.id) for racer in team.racers)
        } for team in self.teams]
        championship_table_sorted = sorted(championship_table, key=lambda x: x['points'], reverse=True)
        for index, entry in enumerate(championship_table_sorted, start=1):
            entry['place'] = index
        return championship_table_sorted
    
    def get_championship_table_last_race(self):
        last_race = None
        for race in sorted(self.races, key=lambda x: x.datetime, reverse=True):
            if race.results_added:
                last_race = race
                break
        
        if not last_race:
            return []

        championship_table = [{
            'racer': racer,
            'points': sum(rel.total_points for rel in racer.races_relations if rel.race == last_race)
        } for racer in self.racers]
        championship_table_sorted = sorted(championship_table, key=lambda x: x['points'], reverse=True)
        for index, entry in enumerate(championship_table_sorted, start=1):
            entry['place'] = index
        return championship_table_sorted