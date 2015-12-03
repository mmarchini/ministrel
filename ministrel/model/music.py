# coding=utf-8

import os
import logging
from datetime import datetime
from tempfile import NamedTemporaryFile

from sqlalchemy import Column, Integer, Unicode, UnicodeText, DateTime
from sqlalchemy import ForeignKey
from popgen import composition
from pydub import AudioSegment

from ministrel import utils
from ministrel.model.base import Base, session
from ministrel.model.categories import UsableInstrument

log = logging.getLogger(__name__)


class Musics(Base):
    __tablename__ = 'musics'

    id = Column(Integer, primary_key=True)

    name = Column(Unicode(255))
    creation_date = Column(DateTime, default=datetime.now)
    # composed; available; played;
    status = Column(Unicode(255), default='composed')

    style = Column(Unicode(100), ForeignKey('styles.name'))
    mood = Column(Unicode(100), ForeignKey('moods.name'))

    midi_file = Column(UnicodeText, unique=True)

    @property
    def mp3_filename(self):
        return os.path.splitext(self.midi_file)[0] + '.mp3'

    def convert_to_mp3(self):
        mp3_filename = None
        with NamedTemporaryFile(suffix='.wav') as wav_file:
            utils.play(self.midi_file, 'arachno.sf2', wav_file.name)
            mp3_filename = self.mp3_filename
            with open(mp3_filename, 'w') as mp3_file:
                AudioSegment.from_wav(wav_file).export(mp3_file, format="mp3")

        return mp3_filename

    @classmethod
    def get_next_song(cls, style, mood):
        next_song = session.query(Musics).filter(Musics.status == 'available')\
            .filter(Musics.style == style.lower())\
            .filter(Musics.mood == mood.lower())\
            .order_by(Musics.creation_date).first()

        with session.begin():
            next_song.status = 'played'
            session.add(next_song)

        return next_song.mp3_filename

    @classmethod
    def compose(cls, style, mood):
        log.info("Composing a %s %s track" % (style, mood))
        base_path = "output/%s/" % utils.get_hash()
        os.makedirs(base_path)
        filename = '01_lorem_%s_%s.midi' % (style, mood)
        filename = os.path.join(base_path, filename)
        composer = composition.Composer()
        instrument_query = session.query(UsableInstrument.instrument)\
                                  .filter(UsableInstrument.style == style)\
                                  .filter(UsableInstrument.mood == mood)
        instrument = instrument_query.filter(UsableInstrument.instrument_type == 'vocal').scalar()
        composer.instrument('melody', instrument)
        instrument = instrument_query.filter(UsableInstrument.instrument_type == 'chords').scalar()
        composer.instrument('chord', instrument)
        instrument = instrument_query.filter(UsableInstrument.instrument_type == 'bass').scalar()
        composer.instrument('bass', instrument)

        composer.compose()
        composer.save(filename)
        music = cls()
        music.name = u"01 - Lorem %s %s" % (style.title(), mood.title())
        music.style = style
        music.mood = mood
        music.midi_file = filename
        session.add(music)
