import os
import sys
import logging
from .kaomi_client import ServerError
from .globals import EXIT_STATUS_RESOLVER


def display_output_and_exit(client_output, verbose_flag=False):
    """
    Dato un dizionario rappresentante lo stato di uscita del server, costruisce lo stato di uscita del client ed esce dallo script
    :param client_output:       dizionario che contiene le informazioni sull'output
    :param verbose_flag:        flag che indica se l'output deve essere verbose, nei casi di errore viene sempre considerato (True)

    WARNING: la funzione termina lo script

    """

    # ottengo il significato dell'exit status del client, per poterlo stampare all'utente nel caso l'output sia verbose
    status = client_output.get('status', -1)
    status_meaning = EXIT_STATUS_RESOLVER.get(status, '{}: Unknown'.format(status))

    # ottengo il flag che indica se ci sono stati errori
    error_flag = client_output.get('error', True)           # se non esiste il campo, c'è stato un errore

    # ottengo il message d'uscita e i dati
    message = client_output.get('message', '')
    data = client_output.get('data', '')

    # stampo l'output e stampo nel logging

    # si è verificato un errore
    if error_flag:
        # stampo gli errori sia sui log che sul
        print('{} \nError: {} \nData: {}'.format(status_meaning, message, data))
        logging.error('{}. --- Error: {}. --- Data: {}'.format(status_meaning, message, data))

    # non si è verificato un errore
    elif not error_flag:
        # scrivo sui log che è stata eseguita questa operazione con successo
        logging.info('{}. --- Output: {}. --- Data: {}'.format(status_meaning, message, data))

        if verbose_flag:
            # nel caso lo script sia stato chiamato con verbose, mostro anche l'output sul terminale
            print('{} \nOutput: {} \nData: {}'.format(status_meaning, message, data))

    # esco dallo script con l'exit status specificato
    sys.exit(status)


def upload_directory(kaomi_client, local_dir, remote_dir, dir_perms=None, file_perms=None, verbose=False):
    """
    Funzione per il caricamento di una directory
    Nota: all'interno della funzione non mi devo preoccupare dell'overwrite perché so che remote_dir è vuota
    :param kaomi_client:        client da utilizzare per l'upload
    :param local_dir:           cartella da uploadare
    :param remote_dir:          posizione di upload per la cartella specificata
    :param dir_perms:           permessi da assegnare alle cartelle
    :param file_perms:          permessi da assegnare ai file
    :param verbose:             indica se l'output deve essere verbose
    :throw RuntimeError:        (anche dal kaomi-client) per problemi generici della funzione o delle operazione di uplaod
    :throw ConnectionError:     (re-raise dalle operazioni del kaomi-client) per problemi di comunicazione con il server
    """
    if verbose: print('Local folder "{}" is being uploading in "{}"'.format(local_dir, remote_dir))

    if not os.path.isdir(local_dir) or os.path.islink(local_dir):
        # la cartella passata non è una cartella o è un link ad una cartella
        raise RuntimeError('Wrong argument: "{}" is not a valid directory'.format(local_dir))

    for entry in os.listdir(local_dir):
        # scorro tutte le entry presenti all'interno della cartella

        # ottengo il path assoluto dell'entry
        entry_abs_path = os.path.join(local_dir, entry)

        # salto le entry che non mi interessano
        if os.path.islink(entry_abs_path) or os.path.ismount(entry_abs_path):
            # tipologie di entry che non ci interessano, le saltiamo
            continue

        if os.path.isdir(entry_abs_path):
            # LA ENTRY È UNA DIRECTORY

            # ottengo la nuova cartella di destinazione per la dir considerata
            new_remote_dir = os.path.join(remote_dir, entry)

            # come prima cosa devo creare la cartella, i vari catch ad eccezioni vengono fatti dal chiamante
            server_resp = kaomi_client.create_directory(dest_dir=new_remote_dir, perms=dir_perms)
            if server_resp.get('status') != 0:
                # controllo se l'azione ha avuto successo, altrimenti sollevo un'eccezione
                raise ServerError(server_resp)

            # arrivato qui sono sicuro che la creazione ha avuto successo
            # allora posso chiamare ricorsivamente la funzione di upload sulla cartella
            upload_directory(kaomi_client=kaomi_client, local_dir=entry_abs_path, remote_dir=new_remote_dir, dir_perms=dir_perms,
                             file_perms=file_perms, verbose=verbose)

        elif os.path.isfile(entry_abs_path):
            # LA ENTRY È UN FILE

            # ottengo il path del file di destinazione
            new_remote_file = os.path.join(remote_dir, entry)

            # procedo con l'upload del file, i vari catch ad eccezioni vengono fatti dal chiamante
            server_resp = kaomi_client.upload_file(local_file=entry_abs_path, dest_file=new_remote_file, perms=file_perms)
            if server_resp.get('status') != 0:
                # controllo se l'azione ha avuto successo, altrimenti sollevo un'eccezione
                raise ServerError(server_resp)

            # se è impostato il verbose, segnalo il successo dell'operazione
            if verbose: print('Local file "{}" uploaded in "{}"'.format(entry_abs_path, new_remote_file))

    # ho terminato di caricare la cartella, segnalo il successo se verbose è attivo
    if verbose: print('Local folder "{}" uploaded in "{}"'.format(local_dir, remote_dir))


def get_client_output(server_output):
    """
    Funzione che dato il dizionario ottenuto come risposta, ne ricava le informazioni da fornire in output al client
    :param server_output:       dizionario ottenuto dal server come risposta
    :return:                    dizionario con la risposta del server
    """
    requested_fields = ['status', 'substatus', 'message', 'data']
    if not all(k in server_output for k in requested_fields):
        # non ci sono le chiavi che ci aspetteremmo nel dizionario del server, quindi errore nel client
        return {'status': 1, 'error': True, 'message': 'Missing fields in server response: {}'.format(list(server_output.keys())), 'data': ''}

    # ottengo i campi dal dizionario del server
    status, substatus, message, data = server_output.get('status'), server_output.get('substatus'), server_output.get('message'), server_output.get('data')

    # analizzo lo stato di uscita del server e converto il valore di uscita in quello del client
    if status == 0:
        # il comando ha avuto successo
        return {'status': 0, 'error': False, 'message': '(server {}:{}) {}'.format(status, substatus, message), 'data': data}
    elif status == 1:
        # problema di connessione
        return {'status': 2, 'error': True, 'message': '(server error {}:{}) {}'.format(status, substatus, message), 'data': data}
    elif status == 2 and (substatus == 1 or substatus == 2):
        # problema di autorizzazioni
        return {'status': 3, 'error': True, 'message': '(server error {}:{}) {}'.format(status, substatus, message), 'data': data}
    else:
        # problema applicativo
        return {'status': 4, 'error': True, 'message': '(server error {}:{}) {}'.format(status, substatus, message), 'data': data}