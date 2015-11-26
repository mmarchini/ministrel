
import os
import logging
import hashlib
from datetime import datetime
from time import sleep

from popgen import composition

from ministrel.model import Session, Musics

log = logging.getLogger(__name__)


def get_hash():
    hasher = hashlib.sha1()
    hasher.update(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    return hasher.hexdigest()


def compose(session, limit):
    composed_songs = session.query(Musics).filter(Musics.status == 'composed')\
        .count()

    if composed_songs < limit:
        log.info("Composing track '01 - Lorem'")
        base_path = "output/%s/" % get_hash()
        os.makedirs(base_path)
        filename = os.path.join(base_path, '01_lorem.midi')
        composer = composition.Composer()

        composer.compose()
        composer.save(filename)
        music = Musics()
        music.name = u"01 - Lorem"
        music.midi_file = filename
        session.add(music)
    else:
        sleep(5)


def convert(session, limit):
    available_songs = session.query(Musics).filter(Musics.status == 'available')\
        .count()

    if available_songs < limit:
        songs = session.query(Musics).filter(Musics.status == 'composed')\
                       .order_by(Musics.creation_date)\
                       .limit(limit - available_songs).all()

        for song in songs:
            song.convert_to_mp3()
            song.status = 'available'
            session.add(song)
    else:
        sleep(5)


def worker(compose_limit=100, convert_limit=10):
    session = Session()

    while True:
        with session.begin():
            compose(session, compose_limit)
            convert(session, convert_limit)


def main():
    worker()

if __name__ == "__main__":
    main()
