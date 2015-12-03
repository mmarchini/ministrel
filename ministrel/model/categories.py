from sqlalchemy import Column, Integer, Unicode, ForeignKey

from ministrel.model.base import Base


class Instrument(Base):
    __tablename__ = 'instruments'
    name = Column(Unicode(255), primary_key=True)


class Style(Base):
    __tablename__ = 'styles'
    name = Column(Unicode(100), primary_key=True)


class Mood(Base):
    __tablename__ = 'moods'
    name = Column(Unicode(100), primary_key=True)


class UsableInstrument(Base):
    __tablename__ = 'usable_instruments'
    instrument = Column(Unicode(255), ForeignKey('instruments.name'),
                        primary_key=True)
    style = Column(Unicode(100), ForeignKey('styles.name'), primary_key=True)
    mood = Column(Unicode(100), ForeignKey('moods.name'), primary_key=True)
    # vocal; chords; bass
    instrument_type = Column(Unicode(100), primary_key=True)
    score = Column(Integer)
