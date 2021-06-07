from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound

from app_base.app import app as app1
from app_tei.app import app as app2


application = DispatcherMiddleware(app1, {
    '/tei_viewer': app2
})