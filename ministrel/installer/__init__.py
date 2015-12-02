from mingus.containers.instrument import MidiInstrument

from ministrel.model.base import Base, engine, session
from ministrel.model.categories import Instrument, Mood, Style
from ministrel.model.categories import UsableInstrument

Base.metadata.create_all(engine)

usable_instruments = [
    # Rock happy
    ('rock', 'happy', 'vocal', "Harmonica"),
    ('rock', 'happy', 'chords', "Electric Guitar (clean)"),
    ('rock', 'happy', 'bass', "Electric Bass (finger)"),
    # Rock serene
    ('rock', 'serene', 'vocal', "Sitar"),
    ('rock', 'serene', 'chords', "Electric Guitar (clean)"),
    ('rock', 'serene', 'bass', "Electric Bass (finger)"),
    # Rock angry
    ('rock', 'angry', 'vocal', "Lead1 (square)"),
    ('rock', 'angry', 'chords', "Overdriven Guitar"),
    ('rock', 'angry', 'bass', "Slap Bass 1"),
    # Rock melancholic
    ('rock', 'melancholic', 'vocal', "Violin"),
    ('rock', 'melancholic', 'chords', "Electric Guitar (jazz)"),
    ('rock', 'melancholic', 'bass', "Electric Bass (finger)"),

    # Pop happy
    ('pop', 'happy', 'vocal', "English Horn"),
    ('pop', 'happy', 'chords', "Pad1 (new age)"),
    ('pop', 'happy', 'bass', "Lead8 (bass + lead)"),
    # Pop serene
    ('pop', 'serene', 'vocal', "Lead2 (sawtooth)"),
    ('pop', 'serene', 'chords', "Honky-tonk Piano"),
    ('pop', 'serene', 'bass', "Electric Bass (finger)"),
    # Pop angry
    ('pop', 'angry', 'vocal', "Lead1 (square)"),
    ('pop', 'angry', 'chords', "Pad1 (new age)"),
    ('pop', 'angry', 'bass', "Lead8 (bass + lead)"),
    # Pop melancholic
    ('pop', 'melancholic', 'vocal', "Violin"),
    ('pop', 'melancholic', 'chords', "Acoustic Grand Piano"),
    ('pop', 'melancholic', 'bass', "Contrabass"),

    # EDM happy
    ('edm', 'happy', 'vocal', "Lead4 (chiff)"),
    ('edm', 'happy', 'chords', "Pad3 (polysynth)"),
    ('edm', 'happy', 'bass', "Lead8 (bass + lead)"),
    # EDM serene
    ('edm', 'serene', 'vocal', "Lead6 (voice)"),
    ('edm', 'serene', 'chords', "Pad1 (new age)"),
    ('edm', 'serene', 'bass', "Synth Bass 1"),
    # EDM angry
    ('edm', 'angry', 'vocal', "Lead1 (square)"),
    ('edm', 'angry', 'chords', "Pad6 (metallic)"),
    ('edm', 'angry', 'bass', "Lead8 (bass + lead)"),
    # EDM melancholic
    ('edm', 'melancholic', 'vocal', "Lead7 (fifths)"),
    ('edm', 'melancholic', 'chords', "Pad4 (choir)"),
    ('edm', 'melancholic', 'bass', "Synth Bass 1"),

    # Jazz happy
    ('jazz', 'happy', 'vocal', "Soprano Sax"),
    ('jazz', 'happy', 'chords', "Electric Guitar (jazz)"),
    ('jazz', 'happy', 'bass', "Acoustic Bass"),
    # Jazz serene
    ('jazz', 'serene', 'vocal', "Harpsichord"),
    ('jazz', 'serene', 'chords', "Glockenspiel"),
    ('jazz', 'serene', 'bass', "Electric Bass (finger)"),
    # Jazz angry
    ('jazz', 'angry', 'vocal', "Tenor Sax"),
    ('jazz', 'angry', 'chords', "Overdriven Guitar"),
    ('jazz', 'angry', 'bass', "Electric Bass (pick)"),
    # Jazz melancholic
    ('jazz', 'melancholic', 'vocal', "Trumpet"),
    ('jazz', 'melancholic', 'chords', "Bright Acoustic Piano"),
    ('jazz', 'melancholic', 'bass', "Contrabass"),
]

with session.begin():
    for style in ['rock', 'pop', 'edm', 'jazz']:
        session.add(Style(name=style))

    for mood in ['happy', 'serene', 'angry', 'melancholic']:
        session.add(Mood(name=mood))

    for instrument in MidiInstrument.names:
        session.add(Instrument(name=instrument))

    session.flush()
    for style, mood, instrument_type, instrument in usable_instruments:
        session.add(UsableInstrument(
            style=style,
            mood=mood,
            instrument=instrument,
            instrument_type=instrument_type,
            score=100
        ))
