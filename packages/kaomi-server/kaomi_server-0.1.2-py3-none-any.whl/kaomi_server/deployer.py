"""
File/modulo contenente la classe "Deployer"
"""
import os
import stat
import shutil
import subprocess
from tempfile import NamedTemporaryFile


class ActionNotFoundError(Exception):
    """ Eccezione sollevata quando viene richiesta un'azione non esistente """
    pass


class Deployer:
    """
    Classe che si occupa del deployment sul server
    """
    __config = {}
    __placeholder_format = '##{}##'
    __default_actions_shell = '/bin/bash'       # shell da utilizzare di default nel caso non venga comunicata nella config
    __default_actions_timeout = 180             # timeout in secondi da utilizzare nel caso che non venga specificato niente nella config
    __permission_mask = 0o777

    def __init__(self, configuration):
        """
        Inizializzazione dello stato interno
        :param configuration:          configurazione del deployer
        """
        self.__config = configuration

    def __run(self, bash_string):
        """
        Funzione che esegue i comandi specificati in bash_string e ritorna il loro output
        :param bash_string:         stringa contente i comandi (attenzione ai new_line)
        :return:                    output dei comandi
        """

        # ottengo la shell da utilizzare per le azioni
        actions_shell = self.__config.get('DEFAULT', {}).get('actions-shell', self.__default_actions_shell)
        actions_timeout = self.__config.get('DEFAULT', {}).get('actions-timeout', self.__default_actions_timeout)

        # si deve crare un file bash contenente tutti i comandi in modo che vengano eseguiti nello stesso enviroment
        # creo un file temporaneo in /tmp
        bash_script = NamedTemporaryFile(mode='w', delete=False)
        # scrivo i comandi sul file
        bash_script.write(bash_string)
        bash_script.close()

        # modifico i permessi del file in modo che sia eseguibile
        os.chmod(bash_script.name, stat.S_IEXEC | stat.S_IREAD)
        # eseguo lo script chiamandolo utilizzando la shell specificata e ridirigo:
        # il suo stderr verso lo stdout, poichè voglio avere entrambi gli stream assieme, nell'ordine dei messaggi giusto
        # il suo stdin verso /dev/null, poichè se qualcuno nello script cerca di chiamare un programma che legge dallo standard input qui hanga forever
        proc_handle = subprocess.Popen([actions_shell, bash_script.name], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # leggo lo standard output del processo, tenendo conto del timeout
        try:
            stdout, _ = proc_handle.communicate(timeout=actions_timeout)
        except subprocess.TimeoutExpired:
            # se il timeout del processo scade, lo killo e leggo il suo stdout
            proc_handle.kill()
            # qui si può piantare solo nel caso che il processo stia eseguendo una system call piantata a causa di un fattore esterno.
            # un esempio è la lettura da un disco rimovibile rotto, o un modulo kernel buggato
            stdout, _ = proc_handle.communicate()

        # elimino il file
        os.unlink(bash_script.name)

        return stdout.decode()

    @staticmethod
    def __get_common_prefix_len(path, directory):
        """
        Funzione che controlla se un path ricade all'interno di una directory
        Non è riflessiva, quindi una cartella non è all'interno di se stessa
        :param path:                path che deve ricadere
        :param directory:           directory nella quale deve ricadere
        :return:                    la lunghezza del prefisso comune tra il path e la cartella
        """
        # realpath elimina i link simbolici all'interno del path
        directory = os.path.realpath(directory).rstrip('/') + '/'
        path = os.path.realpath(path)

        # controllo se il prefisso comune ai due path
        if os.path.commonprefix([directory, path]) == directory:
            return len(directory)
        else:
            return 0

    def __resolve_path_aliases(self, path):
        """
        Funzione che dato un path risolve eventuali alias al suo interno e restituisce il path assoluto
        Se il path passato non dovesse contenere aliases allora viene restituito invariato
        :param path:                path nel quale risolvere gli aliases
        :return:                    path con gli aliases risolti
        """
        # aliases => dizionario con chiave = nome placeholder, valore = valore da sostituire
        for alias in self.__config.get('aliases', {}):
            # per ogni alias definito nel dizionario degli aliases verifico se è presente nel path e in caso lo sostituisco
            # il formato del placeholder è definito come variabile privata della classe
            placeholder = self.__placeholder_format.format(alias)
            path = path.replace(placeholder, self.__config['aliases'][alias])

        return os.path.abspath(path)

    def __get_root_folder(self, path):
        """
        Funzione che verifica se un path ricade tra quelli che sono modificabili e restituisce la directory che matcha
        in modo più specifico
        :param path:            path da verificare
        :return:                il path all'interno del quale ricade
        """

        max_common_prefix_len = 0
        best_matching_folder = None

        # scorro tutte le cartelle che sono modificabili da questo deployer
        for directory in self.__config['folder']:
            common_prefix_len = self.__get_common_prefix_len(path=path, directory=directory)
            if common_prefix_len > max_common_prefix_len:
                max_common_prefix_len = common_prefix_len
                best_matching_folder = directory

        return best_matching_folder

    def __validate_permissions(self, permissions):
        """
        Funzione di controllo dei permessi passati
        Viene controllato che siano del tipo giusto e viene applicata la maschera
        :param permissions:  valore passato come argomento del parametro indicante i permessi
        :return:             permessi
        """

        if not isinstance(permissions, int):
            raise RuntimeError('Permissions must be specified as an octal number (eg. 0o777, 0o0777, 0777, 777, etc.')

        # maschero i permessi per eliminare configurazioni non ammissibili
        perms = permissions & self.__permission_mask

        # controllo se i permessi sono stati modificati dalla maschera
        if perms != permissions:
            raise RuntimeError('Permissions have been modified by the mask. Please change your permissions.')

        return perms

    def execute_action(self, action_name):
        """
        Esecuzione dell'azione specificata
        :param action_name:     nome dell'azione che si vuole eseguire
        :throw ActionNotFoundError:  nel caso non venga trovata l'azione richiesta
        :throw RuntimeError:    nel caso ci siano problemi con l'esecuzione
        :retrun:                lista degli outputs dei singoli comandi che fanno parte dell'azione
        """
        # controllo se l'azione esiste per questo deployer
        if action_name not in self.__config['action']:
            raise ActionNotFoundError("Cannot find action \"{}\"".format(action_name))

        # ottengo la lista di comandi da eseguire per questa azione
        commands = self.__config['action'][action_name]

        # eseguo i comandi
        try:
            results = self.__run(commands)
        except RuntimeError as e:
            raise RuntimeError('Something went wrong running action "{}". {}.'.format(action_name, e))

        # ritorno la lista degli output dei comandi
        return results

    def delete_filesystem_node(self, to_delete_path):
        """
        Funzione che dato un path elimina il nodo del filesystem corrispondente
        :param to_delete_path:      path del nodo da eliminare
        :throw PermissionError:     nel caso il nodo non rientri in un path modificabile dal deployer
        :throw RuntimeError:        nel ci siano dei problemi con l'eliminazione del nodo
        :throw FileNotFoundError:   nel caso il nodo non venga trovato
        """
        # ottengo il path pulito (rimuovo gli alias e risolvo i link)
        to_delete_path = self.__resolve_path_aliases(path=to_delete_path)

        # controllo se il path è accessibile
        if self.__get_root_folder(path=to_delete_path) is None:
            # il path non è modificabile, quindi restituisco errore
            raise PermissionError('Target file is located in a not reachable path!')

        # se il path ricade tra quelli modificabili, eseguo l'azione
        try:
            if os.path.isfile(to_delete_path):
                # se il path punta a un file allora rimuovo il file
                os.remove(to_delete_path)
            elif os.path.isdir(to_delete_path):
                # se il path punta a una directory allora rimuovo ricorsivamente tutto il suo contenuto
                shutil.rmtree(to_delete_path)
            else:
                # la tipologia non è tra quelle eliminabili
                raise FileNotFoundError('Path given as argument "{}" is not a file and not a directory!'.format(to_delete_path))
        except OSError as e:
            # errore durante l'eliminazione
            raise RuntimeError('An error occurred deleting file or directory "{}". OSError: {}.'.format(to_delete_path, e))

    def __get_perms_of_root_folder(self, root_folder):
        """
        Funzione che ritorna i permessi definiti per una cartella root presente nella config di questo deployer
        :param root_folder:         cartella root della quale si vogliono ottenere i permessi
        :return:                    permessi cartelle, permessi files, uid, gid
        """
        dir_perms = self.__config['folder'][root_folder]['dir-perms']
        file_perms = self.__config['folder'][root_folder]['file-perms']

        # ottengo l'uid dell'owner e il gid del group
        uid = self.__config['folder'][root_folder]['owner']
        gid = self.__config['folder'][root_folder]['group']

        return dir_perms, file_perms, uid, gid

    def create_folder(self, folderpath, overwrite=False, permissions=None):
        """
        Funzione che dato il path di una cartella la crea
        :param folderpath:              path della cartella da creare
        :param overwrite:               flag che indica se la cartella deve essere sovrascritta
        :param permissions:             permessi da assegnare alla cartella
        :throw PermissionError:         nel caso la cartella non rientri in un path modificabile dal deployer
        :throw FileExistsError:         nel caso la cartella esista già (per poter gestire/skippare il problema dal chiamante)
        :throw RuntimeError:            nel caso ci siano problemi con la creazione della cartella
        """
        # ottengo il path pulito (rimuovo gli alias e risolvo i link)
        folderpath = self.__resolve_path_aliases(path=folderpath)

        # ottengo la cartella parent definita nella configurazione per sapere che permessi applicare
        root_folder = self.__get_root_folder(path=folderpath)

        if root_folder is None:
            # il path non è modificabile, quindi restituisco errore
            raise PermissionError('Target folder is located in a not reachable path!')

        # controllo se la cartella esiste già
        if os.path.isdir(folderpath) and not overwrite:
            raise FileExistsError('Folder "{}" already exists!'.format(folderpath))
        elif os.path.isdir(folderpath) and overwrite:
            # la cartella esiste e il flag overwrite è attivo, quindi elimino la vecchia cartella
            try:
                shutil.rmtree(folderpath)
            except Exception as e:
                # c'è stato un errore nell'eliminazione, lo segnalo al chiamante
                raise RuntimeError(e)
        elif not os.path.isdir(os.path.dirname(folderpath)):
            # la cartella nella quale si vuole creare la cartella non esiste
            raise RuntimeError('Parent folder "{}" does not exist.'.format(os.path.dirname(folderpath)))

        # ottengo i permessi
        dir_perms, _, uid, gid = self.__get_perms_of_root_folder(root_folder=root_folder)

        perms = dir_perms if permissions is None else self.__validate_permissions(permissions=permissions)

        # effettuo le modifiche all'umask per poter impostare in modo corretto i permessi
        umask = 0o777 ^ perms
        umask_original = os.umask(umask)

        try:
            # creo la cartella specificandone i vari permessi
            os.mkdir(path=folderpath, mode=perms)
            os.chown(path=folderpath, uid=uid, gid=gid)
        except OSError as e:
            raise RuntimeError('An error occurred creating folder "{}". OSError: {}.'.format(folderpath, e))
        finally:
            # sia che la creazione abbia avuto successo o meno, ripristino l'umask al suo stato iniziale
            os.umask(umask_original)

    def get_file_uploader(self, filepath, overwrite=False, permissions=None):
        """
        Funzione per la creazione di un uploader di files
        :param filepath:            path del file che si vuole creare
        :param overwrite:           indica se nel caso il file esista già debba venire sovrascritto
        :param permissions:         permissions da assegnare al file
        :throw PermissionError:     se la cartella in cui si vuole creare il file non è accessibile
        :throw FileExistsError:     nel caso il file esista già e overwrite è impostato a False
        :throw RuntimeError:        nel caso ci siano dei problemi con la creazione del file
        :return: handle, str        handle del file sul quale poter chiamare le operazioni di scrittura, path effettivo del file aperto
        """
        # ottengo il path pulito (rimuovo gli alias e risolvo i link)
        new_file = self.__resolve_path_aliases(path=filepath)

        # ottengo la cartella parent definita nella configurazione per sapere che permessi applicare
        root_folder = self.__get_root_folder(path=new_file)

        if root_folder is None:
            # il path non è modificabile, quindi restituisco errore
            raise PermissionError('File to be created is located in a not reachable path!')

        if not os.path.isdir(os.path.dirname(new_file)):
            # la cartella nella quale si vuole creare il file non esiste
            raise RuntimeError('Parent folder "{}" does not exist.'.format(os.path.dirname(new_file)))

        if os.path.isfile(new_file) and overwrite:
            # il file esiste già ed overwrite è attivo, allora cancello il vecchio file
            try:
                os.remove(new_file)
            except OSError as e:
                # segnalo il problema con l'eliminazione del file
                raise RuntimeError("An exception occurred removing old file: (OSError) {}".format(e))
        elif os.path.isfile(new_file) and not overwrite:
            # segnalo che il file esisteva
            raise FileExistsError("File already exists and overwrite is set to False.")

        # ottengo i permessi della cartella nella quale verrà posizionato il file
        _, file_perms, uid, gid = self.__get_perms_of_root_folder(root_folder=root_folder)

        perms = file_perms if permissions is None else self.__validate_permissions(permissions=permissions)

        # importazione di alcuni flag utili
        # il file viene creato se non esiste già (O_CREAT) se esiste già viene sollevata un'eccezione (O_EXCL)
        flags = os.O_CREAT | os.O_WRONLY | os.O_TRUNC | os.O_EXCL

        # modifico l'umask a seconda dei permessi che ho intenzione di impostare al nuovo file
        umask = 0o777 ^ perms
        umask_original = os.umask(umask)

        try:
            # creo il file e imposto immediatamente l'owner e il group
            file_descriptor = os.open(new_file, flags, perms)
            os.fchown(fd=file_descriptor, uid=uid, gid=gid)
        except Exception as e:
            raise RuntimeError('An error occurred opening file: {}'.format(e))
        finally:
            # torno a ripristinare l'umask in ogni caso
            os.umask(umask_original)

        return os.fdopen(file_descriptor, 'wb'), new_file