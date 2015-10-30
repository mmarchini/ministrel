# coding=utf-8

'''Bard is a server for popge'''

from tempfile import NamedTemporaryFile

import tornado.ioloop
import tornado.web
from tornado.web import template
from pydub import AudioSegment
from popgen import composition


def generate(mp3_file):
    c = composition.Composition()
    c.compose()
    with NamedTemporaryFile(suffix='.wav') as wav_file:
        c.play(wav_file.name)
        AudioSegment.from_wav(wav_file).export(mp3_file)
    return mp3_file


class Generate(tornado.web.RequestHandler):
    def get(self):
        style = self.get_query_argument('style')
        mood = self.get_query_argument('mood')
        print style, mood
        self.set_header('Content-Type', 'audio/mp3')
        with NamedTemporaryFile(suffix='.wav') as mp3_file:
            self.write(generate(mp3_file).read())


class Page(tornado.web.RequestHandler):

    def get(self):
        loader = template.Loader('ministrel/templates/')
        self.write(loader.load('index.html').generate())


application = tornado.web.Application([
    (r"/", Page),
    (r"/generate", Generate),
], static_path='ministrel/static', debug=True)


def main():
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
