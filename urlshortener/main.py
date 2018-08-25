import falcon
from routes import setup_routes
from models import setup_models
from middleware import dbconnection, formatter

api = falcon.API(middleware=[dbconnection.PeeweeConnectionMiddleware(),
                 formatter.JSONFormatterMiddleware()])
setup_routes(api)
setup_models()
