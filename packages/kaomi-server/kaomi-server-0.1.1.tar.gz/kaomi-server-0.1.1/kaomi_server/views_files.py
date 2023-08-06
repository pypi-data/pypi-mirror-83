import os
import json
import logging
import cherrypy

from . import globals
from .functions import build_response, get_payload_data, handle_error


class File(object):
    """
    Api server per il deployment
    """

    # imposto l'handler di errori del server
    _cp_config = {'request.error_response': handle_error}

    @staticmethod
    def __get_and_validate_perms(value):
        """
        Funzione di controllo dei permessi ottenuti via POST e ritorna i permessi utilizzabili dal deployer
        :param value:                   permessi indicati come stringa contenente un numero ottale
        :throw ValueError:              nel caso il permesso non sia un numero ottale
        :return:                        valore dei permessi come intero decimale
        """
        try:
            permissions = int(value, 8)
        except ValueError as e:
            # il numero passato non è convertibile
            raise ValueError('Permissions must be specified as an octal number (eg. 0o777, 0o0777, 0777, 777, etc.). ValueError: {}'.format(e))

        return permissions

    @cherrypy.expose(['upload'])
    def upload_file(self, *args, **kargs):
        """
        Vista per il caricamento di un file a chunk
        Sono ammesse solo chiamate POST
        :POST param apikey:     apikey che vuole effettuare l'azione
        :POST param file:       file da caricare
        :POST param dest_path:  destinazione del file (comprensiva del nome)
        :POST param perms:      permessi da impostare sul file (default = None)
        :POST param overwrite:  indica se eliminare il file nel caso esistesse (default = False)
        """
        if cherrypy.request.method != 'POST':
            # controllo se è una chiamata GET, in tal caso specifico che sono ammesse solo chiamate POST
            return build_response(status=1, substatus=0, message="Only POST admitted")

        # controllo la presenza di tutti i campi necessari
        requested_fields = ['apikey', 'file', 'dest_path']
        if not all(k in kargs for k in requested_fields):
            return build_response(status=1, substatus=4, message="Missing fields in JSON", data=requested_fields)

        apikey = kargs['apikey']
        input_handle = kargs['file'].file
        dest_path = kargs['dest_path']
        overwrite_flag = kargs['overwrite'].lower() == 'true' if 'overwrite' in kargs else False

        # provo ad ottenere i permessi dalla richiesta, mi arrivano come stringa contenente un ottale
        if 'perms' in kargs and kargs['perms'] is not None and len(kargs['perms']) > 0:
            try:
                # provo ad ottenere i permessi
                perms = self.__get_and_validate_perms(kargs['perms'])
            except ValueError as e:
                # nel caso non riesca ad ottenere i permessi ma questi ci siano, segnalo l'errore al client
                return build_response(status=1, substatus=5, message="ValueError in request data", data="{}".format(e))
        else:
            # non sono stati specificati dei permessi, o sono vuoti
            perms = None

        # ottengo il file handle per poter scrivere il file sul server
        try:
            deployer, allowed_ips = globals.DEPLOYERS.get(apikey, (None, None))
            if deployer is None:
                return build_response(status=2, substatus=1, message="Invalid Apikey")

            if allowed_ips is not None:
                if cherrypy.request.remote.ip not in allowed_ips:
                    return build_response(status=2, substatus=6, message="Client ip not allowed")

            output_handle, output_file_path = deployer.get_file_uploader(filepath=dest_path, overwrite=overwrite_flag, permissions=perms)
        except PermissionError as e:
            return build_response(status=2, substatus=2, message="Action not permitted", data='PermissionError: {}'.format(e))
        except RuntimeError as e:
            return build_response(status=2, substatus=3, message="A RuntimeError occurred", data='RuntimeError: {}'.format(e))
        except FileExistsError as e:
            return build_response(status=2, substatus=4, message="File already exists", data='FileExistsError: {}'.format(e))

        # se sono arrivato qua sono sicuro che il file handle di output è valido

        # caricamento del file per chunk

        # inizializzo i valori per la massima dimensione del file e il chunk utilizzato
        max_size_mbytes = cherrypy.config.get('lisp.file_upload.max_size_mb', 100)
        max_size_bytes = max_size_mbytes * 1000 * 1000
        chunk_size = cherrypy.config.get('lisp.file_upload.chunk_size_mb', 5) * 1024 * 1024

        while True:
            # leggo un chunk alla volta
            data = input_handle.read(chunk_size)
            if not data:
                # non ci sono più dati da scrivere, ho finito
                break
            # scrivo il file
            output_handle.write(data)

            if output_handle.tell() > max_size_bytes:
                # il file ha sforato la dimensione massima

                # chiudo gli handle aperti dei file
                input_handle.close()
                output_handle.close()

                try:
                    # provo a rimuovere il file scritto parzialmente
                    os.remove(output_file_path)
                except (OSError, Exception) as e:
                    logging.error('Something went wrong deleting partial uploaded file "{}". Exception: {}'.format(output_file_path, e))

                # ritorno l'errore al chiamante
                return build_response(status=2, substatus=5, message="File exceed maximum dimension", data=max_size_mbytes)

        # arrivato qua il file è stato completamente caricato
        # chiudo i descrittori
        input_handle.close()
        output_handle.close()

        return build_response(status=0, substatus=0, message="File uploaded correctly")

    @cherrypy.expose(['mkdir'])
    def create_directory(self):
        """
        creazione di una cartella
        Sono ammesse solo chiamate POST
        :POST param apikey:     apikey che vuole effettuare l'azione
        :POST param path:       path della cartella da creare
        :POST param perms:      permessi della cartella da creare (default = None)
        :POST param overwrite:  indica se sovrascrivere la cartella nel caso esistesse (default = False)
        """
        if cherrypy.request.method != 'POST':
            # controllo se è una chiamata GET, in tal caso specifico che sono ammesse solo chiamate POST
            return build_response(status=1, substatus=0, message="Only POST admitted")

        try:
            # ottengo i dati della richiesta
            requested_fields = ['apikey', 'path']
            payload = get_payload_data(request=cherrypy.request, requested_fields=requested_fields)
        except RuntimeError as e:
            return '{}'.format(e)

        apikey = payload['apikey']
        path = payload['path']
        overwrite = payload['overwrite'].lower() == 'true' if 'overwrite' in payload else False

        # provo ad ottenere i permessi dalla richiesta, mi arrivano come stringa contenente un ottale
        if 'perms' in payload and payload['perms'] is not None and len(payload['perms']) > 0:
            try:
                # provo ad ottenere i permessi
                perms = self.__get_and_validate_perms(payload['perms'])
            except ValueError as e:
                # nel caso non riesca ad ottenere i permessi ma questi ci siano, segnalo l'errore al client
                return build_response(status=1, substatus=5, message="ValueError in request data", data="{}".format(e))
        else:
            # non sono stati specificati dei permessi, o sono vuoti
            perms = None

        try:
            deployer, allowed_ips = globals.DEPLOYERS.get(apikey, (None, None))
            if deployer is None:
                return build_response(status=2, substatus=1, message="Invalid Apikey")

            if allowed_ips is not None:
                if cherrypy.request.remote.ip not in allowed_ips:
                    return build_response(status=2, substatus=6, message="Client ip not allowed")

            deployer.create_folder(folderpath=path, overwrite=overwrite, permissions=perms)
        except PermissionError as e:
            return build_response(status=2, substatus=2, message="Action not permitted", data='PermissionError: {}'.format(e))
        except RuntimeError as e:
            return build_response(status=2, substatus=3, message="A RuntimeError occurred", data='RuntimeError: {}'.format(e))
        except FileExistsError as e:
            return build_response(status=2, substatus=4, message="Folder already exists", data='FileExistsError: {}'.format(e))

        return build_response(status=0, substatus=0, message="Folder created")

    @cherrypy.expose('delete_node')
    def delete_filesystem_node(self):
        """
        eliminazione di un nodo del filesystem
        Sono ammesse solo chiamate POST
        :POST param apikey:     apikey che vuole effettuare l'azione
        :POST param path:       path del nodo da eliminare
        """
        if cherrypy.request.method != 'POST':
            # controllo se è una chiamata GET, in tal caso specifico che sono ammesse solo chiamate POST
            return json.dumps({"status": "1", "message": "Only POST admitted", "data": None})

        try:
            # ottengo i dati della richiesta
            requested_fields = ['apikey', 'path']
            payload = get_payload_data(request=cherrypy.request, requested_fields=requested_fields)
        except RuntimeError as e:
            return '{}'.format(e)

        apikey, path = payload['apikey'], payload['path']

        try:
            deployer, allowed_ips = globals.DEPLOYERS.get(apikey, (None, None))
            if deployer is None:
                return build_response(status=2, substatus=1, message="Invalid Apikey")

            if allowed_ips is not None:
                if cherrypy.request.remote.ip not in allowed_ips:
                    return build_response(status=2, substatus=6, message="Client ip not allowed")

            deployer.delete_filesystem_node(to_delete_path=path)
        except PermissionError as e:
            return build_response(status=2, substatus=2, message="Action not permitted", data='PermissionError: {}'.format(e))
        except RuntimeError as e:
            return build_response(status=2, substatus=3, message="A RuntimeError occurred", data='RuntimeError: {}'.format(e))
        except FileNotFoundError:
            return build_response(status=0, substatus=1, message="Filesystem node not found")

        return build_response(status=0, substatus=0, message="Filesystem node deleted")
