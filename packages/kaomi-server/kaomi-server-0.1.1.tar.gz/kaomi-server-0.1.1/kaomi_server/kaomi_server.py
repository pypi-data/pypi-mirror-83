import logging
import cherrypy
import logging.config

from .views_files import File
from .views_alive import Alive
from .views_actions import Action
from . import globals
from .functions import load_apikey_configs


def setup_logging():
    """
    Procdeura di inizializzazione e setup del logging in base alle configurazioni
    """
    # imposto i nomi dei file di logging come sono scritti nella configurazione di cherrypy
    globals.LOG_CONF['handlers']['cherrypy_access']['filename'] = cherrypy.config.get('lisp.logging.cherrypy_access.file', 'server_access.log')
    globals.LOG_CONF['handlers']['cherrypy_error']['filename'] = cherrypy.config.get('lisp.logging.cherrypy_error.file', 'server_error.log')

    # imposto i livelli di logging in base alla configurazione
    globals.LOG_CONF['handlers']['cherrypy_access']['level'] = cherrypy.config.get('lisp.logging.cherrypy_access.level', 'INFO')
    globals.LOG_CONF['handlers']['cherrypy_error']['level'] = cherrypy.config.get('lisp.logging.cherrypy_error.level', 'INFO')
    globals.LOG_CONF['handlers']['cherrypy_console']['level'] = cherrypy.config.get('lisp.logging.cherrypy_console.level', 'INFO')
    globals.LOG_CONF['handlers']['default']['level'] = cherrypy.config.get('lisp.logging.default.level', 'INFO')

    # setup del logging utilizzando la configurazione su file
    logging.config.dictConfig(globals.LOG_CONF)


def start_server(config_file, apikey_folder):
    """
    Procedura per l'avvio del server
    :param config_file:         path del file di configurazione del server
    :param apikey_folder:       path della cartella in cui sono presenti le configurazioni delle apikey
    """
    # ottengo la configurazione del server dal file passato
    cherrypy.config.update(config_file)

    # faccio il setup del logging
    setup_logging()

    try:
        globals.DEPLOYERS = load_apikey_configs(apikey_folder=apikey_folder)
    except RuntimeError as e:
        print('Something went wrong loading configs. {}'.format(e))

    # mounting classes
    cherrypy.tree.mount(Alive(), '/', config_file)
    cherrypy.tree.mount(File(), '/api/v1/files/', config_file)
    cherrypy.tree.mount(Action(), '/api/v1/actions/', config_file)

    signal_handler = cherrypy.process.plugins.SignalHandler(bus=cherrypy.engine)
    signal_handler.subscribe()

    # starting server
    cherrypy.engine.start()
    cherrypy.engine.block()
