import os
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


if os.path.exists("test.db"):
    os.remove("test.db")


# Строка подключения
engine = create_engine("sqlite:///test.db", echo=True)    # Все операции логируются на консоль


class Base(DeclarativeBase):
    pass


class Cultures(Base):
    """Культура"""
    __tablename__ = 'culture'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(27))
    description = Column(Text)
    period = Column(String(27))


class Materials(Base):
    """Материал"""
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(25))
    description = Column(Text)


class Locations(Base):
    """Локация"""
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(27))
    description = Column(Text)
    coordinates = Column(Text)


class Excavations(Base):
    """Раскопки"""
    __tablename__ = 'excavation'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(27))
    description = Column(Text)
    location_id = Column(Integer, ForeignKey('location.id'), comment='На какой локации проводили раскопки')
    location = relationship('Locations', backref='excavation_location', lazy='subquery')


class Researchers(Base):
    """Исследователь"""
    __tablename__ = 'researcher'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String(27))
    firstname = Column(String(27))
    specialization = Column(Text)
    organization = Column(Text)


class ArchaeologicalFindings(Base):
    """Археологические находки"""
    __tablename__ = "finding"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(27))
    description = Column(Text)
    Date_finding = Column(Date)
    location_id = Column(Integer, ForeignKey('location.id'), comment='На каких локациях найдены находки')
    researcher_id = Column(Integer, ForeignKey('researcher.id'), comment='Какой исследователь')
    location = relationship('Locations', backref='finding_location', lazy='subquery')
    researcher = relationship('Researchers', backref='finding_researcher', lazy='subquery')


class ResearcherPaper(Base):
    """Исследовательская работа"""
    __tablename__ = 'reswork'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(27))
    description = Column(Text)
    researcher_id = Column(Integer, ForeignKey('researcher.id'), comment='Указываем исследователя')
    researcher = relationship('Researchers', backref='reswork_researcher', lazy='subquery')


class Exhibitions(Base):
    """Выставка"""
    __tablename__ = 'exhibition'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(27))
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    location_id = Column(Integer, ForeignKey('location.id'), comment='В какой локации выставка')
    location = relationship('Locations', backref='exhibition_location', lazy='subquery')


class Exhibits(Base):
    """Экспонат"""
    __tablename__ = 'exhibit'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(27))
    description = Column(Text)
    exhibition_id = Column(Integer, ForeignKey('exhibition.id'), comment='обозначаем выставку')
    exhibition = relationship('Exhibitions', backref='exhibit_exhibition', lazy='subquery')


class Artifacts(Base):
    __tablename__ = 'actifact'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(27))
    description = Column(Text)
    date = Column(Date, comment='Дата находки артефакта')
    culture_id = Column(Integer, ForeignKey('culture.id'), comment='Что за культура использовала')
    location_id = Column(Integer, ForeignKey('location.id'), comment='На какой локации найдено')
    material_id = Column(Integer, ForeignKey('material.id'), comment='Из какого материала состоит')
    exhibit_id = Column(Integer, ForeignKey('exhibit.id'), comment='Название экспоната')
    culture = relationship('Cultures', backref='artifact_culture', lazy='subquery')
    location = relationship('Locations', backref='artifact_location', lazy='subquery')
    material = relationship('Materials', backref='artifact_material', lazy='subquery')
    exhibit = relationship('Exhibits', backref='artifact_material', lazy='subquery')

    def __repr__(self):
        return f'{self.title}, {self.description}, {self.date}'


Base.metadata.create_all(engine)