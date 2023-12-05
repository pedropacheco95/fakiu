from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer , String , Text , ForeignKey , Boolean , Date
from sqlalchemy.orm import relationship

from .associations import team_championship , racer_championship
from fakiu.tools.input_tools import Field, Block, Tab , Form

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

    teams = relationship('Team', secondary=team_championship, back_populates='championships', cascade="all")
    racers = relationship('Racer', secondary=racer_championship, back_populates='championships', cascade="all")
    races = relationship('Race', back_populates='championship', cascade="all, delete-orphan")

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
            get_field(name='racers',label='Pilotos',type='ManyToMany',required=True,related_model='Racer'),
            get_field(name='teams',label='Equipas',type='ManyToMany',required=True,related_model='Team'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)
        
        return form