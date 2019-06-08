# -*- coding: utf-8


app = None
jinja = None


def init_http_app(app_instance, jinja_instance):
    global app
    global jinja

    app = app_instance
    jinja = jinja_instance
