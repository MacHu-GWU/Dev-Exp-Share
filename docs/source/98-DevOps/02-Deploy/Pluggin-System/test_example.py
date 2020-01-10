# -*- coding: utf-8 -*-

import pluggy

hookspec = pluggy.HookspecMarker("crawlib")
hookimpl = pluggy.HookimplMarker("crawlib")






class OrmModelSpec(object):
    @hookspec
    def build_request(self):
        """
        """

    @hookspec
    def send_request(self, request):
        """
        """

    @hookspec
    def parse_response(self, request, response):
        """
        """

    @hookspec
    def process_result(self, parse_result):
        """
        """

class Plug1(object):
    @hookimpl
    def build_request(self):
        url = "http://{domain}/{id}".format(self.domain, self.id)
        return url


def get_plugin_manager():
    pm = pluggy.PluginManager("crawlib")
    pm.add_hookspecs(OrmModelSpec)
    pm.register(Plug1())
    return pm

pm = get_plugin_manager()


class OrmModel(object):
    def build_request(self):
        return pm.hook.build_request()

class Movie(OrmModel):
    domain = "www.imdb.com"
    def __init__(self, id):
        self.id = id

movie = Movie(id=1)
print(movie.build_request())