# coding=utf-8

'''Bard is a server for popge'''

import tornado.ioloop
import tornado.web
from tornado.web import template

from ministrel import model


class Generate(tornado.web.RequestHandler):
    def get(self):
        style = self.get_query_argument('style')
        mood = self.get_query_argument('mood')
        print style, mood
        self.set_header('Content-Type', 'audio/mp3')
        with open(model.Musics.get_next_song()) as mp3_file:
            self.write(mp3_file.read())


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
