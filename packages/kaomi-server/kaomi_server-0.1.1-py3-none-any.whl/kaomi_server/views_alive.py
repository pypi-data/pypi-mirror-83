import logging
import cherrypy
from .functions import build_response, handle_error


class Alive(object):
    """
    Classe contenitore di viste che danno informazioni di stato ai client
    """

    # imposto l'handler di errori del server
    _cp_config = {'request.error_response': handle_error}

    @cherrypy.expose()
    def index(self):
        """
        Utilizzato per indicare se il kaomi deployer è up
        """
        return build_response(status=0, substatus=0, message="Ready to deploy!")
