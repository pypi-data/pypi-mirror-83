import os
import json
import argparse
import cherrypy
from .example_files import APIKEY_CONF_FOLDER, SERVER_CONF_EXAMPLE, APIKEY_CONF_EXAMPLE
from .deployer import Deployer
from .config_file import ConfigFile

def folder_check(path):
    """ Funzione di controllo delle cartelle passate via linea di comando """
    if not os.path.isabs(path):
        # path non assoluto
        raise argparse.ArgumentTypeError('The path must be absolute')
    if not os.path.isdir(path):
        # file non trovato
        raise argparse.ArgumentTypeError('Cannot find specified folder {}'.format(path))
    return path


def file_check(path):
    """ Funzione di controllo dei file passati via linea di comando """
    if not os.path.isabs(path):
        # path non assoluto
        raise argparse.ArgumentTypeError('The path must be absolute')
    if not os.path.isfile(path):
        # file non trovato
        raise argparse.ArgumentTypeError('Cannot find specified file {}'.format(path))
    return path


def get_payload_data(request, requested_fields):
    """
    Funzione che data la richiesta restituisce il dizionario contenente il payload parsato
    :param request:             richiesta
    :param requested_fields:    campi che devono essere presenti
    :throw RuntimeError:        nel caso si verificasse qualche problema con la richiesta
                                nel caso venga sollevata un'eccezione, conterrà una stringa contenente il dizionario da restituire al chiamante
    :return:                    dizionario contenente i dati
    """
    try:
        # ottengo la dimensione del payload
        content_length = int(request.headers['Content-Length'])

        # ottengo la dimensione massima ammissibile (definita ad hoc) dalla configurazione
        max_request_size = cherrypy.config.get('lisp.request.max_size_mb') * 1000**2

        # controllo sulla dimensione massima ammissibile
        if content_length > max_request_size:
            # la dimensione della richiesta supera la dimensione massima consentita
            raise RuntimeError(build_response(status=1, substatus=1, message="Payload content-length greater than maximum allowed", data=max_request_size))

        # per ovviare al fatto che la grandezza del payload potrebbe non coincidere con quella dichiarata nel content-length,
        # andiamo a leggere solo content_length dati
        payload = json.loads(request.body.read(content_length))
    except json.JSONDecodeError:
        # errore nella decodifica del json
        raise RuntimeError(build_response(status=1, substatus=2, message="Json content cannot be parsed"))
    except ValueError:
        # errore nel casting per il content_length
        raise RuntimeError(build_response(status=1, substatus=3, message="Content-length not specified or not valid integer"))

    # controllo che tutti i campi richiesti siano presenti nel payload
    if not all(k in payload for k in requested_fields):
        raise RuntimeError(build_response(status=1, substatus=4, message="Missing fields in JSON", data=requested_fields))

    return payload


def build_response(status, substatus, message="", data=None):
    """
    Funzione per la creazione della risposta del server
    :param status:      stato della richiesta (int)
    :param substatus:   sotto-stato della richiesta (int)
    :param message:     messaggio descrittivo del sottostato
    :param data:        eventuali dati di output
    """
    return json.dumps({
        "status": status,
        "substatus": substatus,
        "message": message,
        "data": data
    })


def create_config_dir(path):
    """
    Funzione per la creazione dei file di configurazione di esempio del server e delle apikey
    :param path:            cartella nella quale vengono creati gli esempi
    :throw RuntimeError:    nel caso si verifichi un errore
    """
    if not os.path.isdir(path):
        # la cartella non si trova
        raise RuntimeError('Cannot find specified directory "{}".'.format(path))

    # creo la directory per le configurazioni dell'apikey
    apikey_conf_folder = os.path.join(path, APIKEY_CONF_FOLDER)
    try:
        # la cartella non viene sovrascritta, nel caso esista si deve eliminarla
        os.mkdir(apikey_conf_folder)
    except (OSError, FileExistsError) as e:
        raise RuntimeError('Something went wrong creating folder {}. Error: {}'.format(apikey_conf_folder, e))

    # ottengo i path dei file di esempio
    server_conf_path = os.path.join(path, 'server.conf.example')
    apikey_conf_path = os.path.join(apikey_conf_folder, 'dashboard.ini.example')

    # scrivo i file di esempio
    try:
        # i file nel caso dovessero esistere vengono sovrascritti

        with open(server_conf_path, 'w') as fh:
            # file conf server
            fh.write(SERVER_CONF_EXAMPLE)
        with open(apikey_conf_path, 'w') as fh:
            # file conf apikey
            fh.write(APIKEY_CONF_EXAMPLE)
    except OSError as e:
        # nel caso qualcosa vada storto con la scrittura dei file segnalo il problema al chiamante
        raise RuntimeError('Something went wrong trying to create example files. Error: {}'.format(e))


def handle_error():
    """
    Funzione per la mascheratura degli errori non previsti del server
    Questa funzione serve ad evitare che venga ritornato un 500 al client
    """
    # gli errori vengono loggati in automatico da cherrypy

    # imposto lo stato della risposta
    cherrypy.response.status = 500

    # imposto il contenuto della risposta
    cherrypy.response.body = [
        bytes(json.dumps({'status': 2, 'substatus': 0, 'message': 'Oops, something went wrong'}), encoding='utf-8')
    ]
    # volendo si possono fare altre azioni come inviare un email


def load_apikey_configs(apikey_folder):
    """
    Procedura per l'ottenimento del dizionario
    :param apikey_folder:   cartella in cui sono presenti le configs
    :throw RuntimeError:    cartella non esiste, errore nel parse delle config, etc.
    :return:                dizionario con i deployers { 'apikey' : <Deployer> }
    """
    # dizionario che verrà restituito come output
    deployers_dict = {}

    try:
        print('\n--- Loading api key configs ---')
        # lettura delle configurazioni dalla cartella delle config
        for config_file in os.listdir(apikey_folder):
            # controllo che la configurazione abbia il formato corretto
            if os.path.splitext(config_file)[-1].lower() == '.ini':
                # inizializzo un oggetto configurazione
                this_config = ConfigFile(os.path.join(apikey_folder, config_file))
                this_config_dict = this_config.to_dict()

                this_apikey = this_config_dict['default']['key']

                # creo il deployer per questa configurazione
                deployers_dict[this_apikey] = Deployer(configuration=this_config_dict), this_config_dict['default'].get('allow-ip', None)

                # il caricamento ha avuto successo
                print('"{}" OK'.format(os.path.basename(config_file), this_apikey))
            else:
                # altrimenti ignoro il file
                continue
        print('-------------------------------\n')
        # finito il caricamento di tutte le config, restituisco il dizionario con i deployer
        return deployers_dict
    except (ValueError, FileNotFoundError, RuntimeError) as e:
        # try/except esterno al for in modo da bloccare il funzionamento se esiste anche un'unica config errata
        raise RuntimeError('An error occurred loading api key configs. Error {}: {}'.format(type(e), e))