from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer , Float , ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from fakiu.tools.input_tools import Field, Block, Form

class RacePointDistribution(db.Model ,model.Model,model.Base):
    __tablename__ = 'race_point_distribution'
    __table_args__ = {'extend_existing': True}
    page_title = 'Distribuições de pontos'
    model_name = 'RacePointDistribution'
    id = Column(Integer, primary_key=True)

    place = Column(Integer)
    points = Column(Float,default=1)
    qualification_points = Column(Float,default=0)

    championship_id = Column(Integer, ForeignKey('championships.id'))

    championship = relationship('Championship', back_populates='race_point_distributions')

    @hybrid_property
    def name(self):
        return f"Place {self.place} in {self.championship}"

    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
            {'field': 'championship','label':'Campeonato'}
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Info block

        fields = [
            get_field(name='championship',label='Campeonato',type='ManyToOne',related_model='Championship'),
            get_field(name='place',label='Lugar',type='Integer'),
            get_field(name='points',label='Pontos na corrida',type='Float'),
            get_field(name='qualification_points',label='Pontos na qualificação',type='Float'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form

    def get_points_dict(self):
        return {self.place:{'points':self.points,'qualification_points':self.qualification_points}}