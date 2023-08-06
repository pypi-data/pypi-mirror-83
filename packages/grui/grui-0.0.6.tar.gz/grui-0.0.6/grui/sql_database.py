from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Boolean, Integer, Float, String, JSON
from sqlalchemy.ext.declarative import declarative_base

from typing import *

from .typing import GruiModel, GruiTypeModelAttribute


class DataBase:

    def __init__(self, engine):
        self.__engine = engine
        self.__db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        self.__Base = declarative_base()
        self.__mapped_classes = {}

    def bind_class(self, model_class: Type[GruiModel]):

        def init(s, model_instance: GruiModel):
            for attr in model_instance.__class__.grui_attributes:
                s.__setattr__(attr, model_instance.__getattribute__(attr))

        def repr_(s):
            return '<%s %r>' % (s.__class__.__name__, s.id)

        name = "%s.%s" % (model_class.__module__, model_class.__name__)
        attributes = {
            '__tablename__': name,
            '__init__': init,
            '__repr__': repr_
        }
        for attr_name, grui_attr in model_class.grui_attributes.items():
            grui_type = grui_attr.type
            attributes[attr_name] = {
                'nullable': grui_type.nullable,
                'default': grui_attr.default_value
            }
            if attr_name == "id":
                attributes[attr_name]['primary_key'] = True
                attributes[attr_name]['nullable'] = False
                # The following line is done by default by sqlalchemy
                # attributes[attr_name]['autoincrement'] = True
            if grui_type.name == "__bool__":
                return Column(Boolean, **argument)
            elif grui_type.name == "__int__":
                return Column(Integer, **argument)
            elif grui_type.name == "__float__":
                return Column(Float, **argument)
            elif grui_type.name == "__str__":
                return Column(String(150), **argument)
            else:
                return Column(JSON(500), **argument)

        self.__mapped_classes[model_class] = type(name + "Mapped", (self.__Base,), attributes)

    def bind(self):
        self.__Base.query = self.__db_session.query_property()
        self.__Base.metadata.create_all(bind=self.__engine)

    def select_all(self, model_class: Type[GruiModel]):
        return self.__mapped_classes[model_class].query.all()

    def add(self, model_instance: GruiModel):
        mapped_class = self.__mapped_classes[model_instance.__class__]

        mapped_instance = mapped_class(model_instance)
        self.__db_session.add(mapped_instance)

    def commit(self):
        self.__db_session.commit()

    @staticmethod
    def sqlite_engine(file_path):
        return create_engine('sqlite:///'+file_path, convert_unicode=True)
