
import logging
from time import sleep

from sqlalchemy import literal
from sqlalchemy.sql.functions import count

from ministrel.model.base import Session
from ministrel.model.music import Musics
from ministrel.model.categories import Style, Mood

log = logging.getLogger(__name__)


def compose(session, limit):
    m = session.query(Musics).filter(Musics.status == 'composed').subquery()
    composed_songs = session.query(Style.name).join(Mood, literal(True))\
        .add_column(Mood.name)\
        .outerjoin(m, (m.c.style == Style.name) & (Mood.name == m.c.mood))\
        .add_column(count(m.c.id))\
        .group_by(Style.name, Mood.name)\
        .all()

    for style, mood, musics in composed_songs:
        if musics < limit:
            Musics.compose(style, mood)
        else:
            sleep(5)


def convert(session, limit):
    m = session.query(Musics).filter(Musics.status == 'available').subquery()
    available_songs = session.query(Style.name).join(Mood, literal(True))\
        .add_column(Mood.name)\
        .outerjoin(m, (m.c.style == Style.name) & (Mood.name == m.c.mood))\
        .add_column(count(m.c.id))\
        .group_by(Style.name, Mood.name)\
        .all()

    for style, mood, musics in available_songs:
        if musics < limit:
            songs = session.query(Musics).filter(Musics.status == 'composed')\
                .filter(Musics.mood == mood).filter(Musics.style == style)\
                .order_by(Musics.creation_date).limit(limit - musics).all()

            for song in songs:
                song.convert_to_mp3()
                song.status = 'available'
                session.add(song)


def worker(compose_limit=20, convert_limit=5):
    session = Session()

    while True:
        with session.begin():
            compose(session, compose_limit)
            convert(session, convert_limit)


def main():
    worker()

if __name__ == "__main__":
    main()
