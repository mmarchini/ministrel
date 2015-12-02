import os
from datetime import datetime
from tempfile import NamedTemporaryFile

from sqlalchemy import Column, Integer, Unicode, UnicodeText, DateTime
from pydub import AudioSegment

from ministrel.model.base import Base, session
from ministrel import utils


class Musics(Base):
    __tablename__ = 'musics'

    id = Column(Integer, primary_key=True)

    name = Column(Unicode(255))
    creation_date = Column(DateTime, default=datetime.now)
    # composed; available; played;
    status = Column(Unicode(255), default='composed')
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
    def get_next_song(cls):
        next_song = session.query(Musics).filter(Musics.status == 'available')\
            .order_by(Musics.creation_date).first()

        with session.begin():
            next_song.status = 'played'
            session.add(next_song)

        return next_song.mp3_filename