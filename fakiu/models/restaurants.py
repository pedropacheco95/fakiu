from fakiu import model 
from fakiu.sql_db import db
from sqlalchemy import Column, Integer , String , Text , ForeignKey , Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from fakiu.tools.input_tools import Field, Block, Tab , Form

class Restaurant(model.Imageable, db.Model ,model.Model, model.Base):
    __tablename__ = 'restaurants'
    __table_args__ = {'extend_existing': True}
    page_title = 'Restaurantes'
    model_name = 'Restaurant'
    id = Column(Integer, primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': model_name,
    }

    imageable_id = Column(Integer, ForeignKey('imageables.imageable_id'))
    imageable = relationship('Imageable', backref=db.backref('restaurants', uselist=False, cascade='all,delete-orphan'),post_update=True)

    name = Column(String(255))
    description = Column(Text)
    address = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255))
    website = Column(String(255))

    races = relationship('Race', back_populates='restaurant', cascade='all, delete')

    racers_relations = relationship('Association_RacerRestaurant', back_populates='restaurant', cascade="all, delete-orphan")

    @hybrid_property
    def racers(self):
        return [rel.race for rel in self.racers_relations]
    
    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Picture block

        fields = [get_field(name='imageable',label='Fotografia',type='MultiplePictures')]
        picture_block = Block('picture_block',fields)
        form.add_block(picture_block)

        # Create Info block

        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
            get_field(name='description',label='Descrição',type='Text'),
            get_field(name='address',label='Morada',type='Text'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        # Create Contactos tab
        fields = [
            get_field(name='phone',label='Telefone',type='Text'),
            get_field(name='email',label='Email',type='Text'),
            get_field(name='website',label='Website',type='Text'),
        ]
        form.add_tab(Tab(title='Contactos',fields=fields,orientation='vertical'))

        return form
