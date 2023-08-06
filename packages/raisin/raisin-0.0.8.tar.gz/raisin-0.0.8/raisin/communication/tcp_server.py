#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import multiprocessing
import os
import socket
import threading
import uuid

import raisin


"""
un lien interressant:
https://www.neuralnine.com/tcp-chat-in-python/
"""

class _Receiver(threading.Thread):
    """
    Permet d'etre en ecoute sans bloquer le fil principal.
    Permet donc d'ecouter plusieurs ip a la fois
    """
    def __init__(self, tcp_socket):
        threading.Thread.__init__(self)
        self.tcp_socket = tcp_socket
        self.queue = [] # c'est la fifo des clients en attente
        self.must_die = False

    def run(self):
        """
        fonction appellee par self.start()
        c'est ici que l'on ajoute les nouveaux clients a la file
        """
        while not self.must_die:
            self.queue.append(self.tcp_socket.accept())

    def stop(self):
        """
        demande gentiment au server de s'arretter
        """
        self.must_die = True

    def kill(self):
        """
        arrete le serveur imediatement, meme si une opperation est en cours
        """
        if self.is_alive():
            self.join(timeout=0)

    def __iter__(self):
        """
        c'est ici que l'on vide la file
        """
        while self.queue:
            yield self.queue.pop(0)

class Server:
    """
    c'est un serveur ipv4 et ipv6
    qui permet de gerer plein de clients.
    Il comunique avec un orchestrateur pour gerer les differentes taches demandees par
    les clients
    """
    def __init__(self, signature=None):
        self.signature = signature
        with raisin.Printer("Initialisation of TCP servers...", signature=self.signature) as p:
            
            # partie serveur
            self.port = raisin.worker.configuration.load_settings()["server"]["port"]
            self.listen = raisin.worker.configuration.load_settings()["server"]["listen"]
            myid = raisin.Id()
            self.ipv4 = myid.ipv4_lan
            self.ipv6 = myid.ipv6
            if self.ipv4 == None and self.ipv6 == None:
                raise RuntimeError("Impossible de detecter l'ip, peut etre n'y a-t-il pas internet?")

            if self.ipv4:
                self.tcp_socket_ipv4 = socket.socket(
                    socket.AF_INET,         # socket internet plutot qu'un socket unix
                    socket.SOCK_STREAM)     # creation d'un TCP/IP socket, SOCK_STREAM=>TCP
                self.tcp_socket_ipv4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # on tente de reutiliser le port si possible
                self.tcp_socket_ipv4.bind((str(self.ipv4), self.port))
                self.tcp_socket_ipv4.listen()
                self.receiver_ipv4 = _Receiver(self.tcp_socket_ipv4)
            else:
                self.tcp_socket_ipv4 = None
                self.receiver_ipv4 = None
            if self.ipv6:
                self.tcp_socket_ipv6 = socket.socket(
                    socket.AF_INET6,        # socket internet en ipv6
                    socket.SOCK_STREAM)     # creation d'un TCP/IP socket, SOCK_STREAM=>TCP
                self.tcp_socket_ipv6.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
                self.tcp_socket_ipv6.bind((str(self.ipv6), self.port))
                self.tcp_socket_ipv6.listen()
                self.receiver_ipv6 = _Receiver(self.tcp_socket_ipv6)
            else:
                self.tcp_socket_ipv6 = None
                self.rceiver_ipv6 = None
            
            # partie environement
            self.clients = {}               # c'est tous les clients connectes

    def is_accepted(self, public_key):
        """
        renvoi True si ce client a le droit de se connecter
        retourne False si il n'a pas le droit.
        retourne None si on doit demander l'avis de l'utilisateur 
        Ne pose aucune question a l'utilisateur, retourne sans attendre
        """
        with raisin.Printer("Testing if a pecific client is accepted...", signature=self.signature) as p:
            blacklisted = os.path.join(os.path.expanduser("~"), ".raisin/blacklisted.py")
            if os.path.exists(blacklisted):
                with open(blacklisted, "r", encoding="utf-8") as f:
                    if public_key.replace(b"\n", b"") in eval(f.read()):
                        p.show("It is accepted.")
                        return False
            whitelisted = os.path.join(os.path.expanduser("~"), ".raisin/whitelisted.py")
            if os.path.exists(whitelisted):
                with open(whitelisted, "r", encoding="utf-8") as f:
                    if public_key.replace(b"\n", b"") in eval(f.read()):
                        p.show("It is refoule.")
                        return True
            if raisin.worker.configuration.load_settings()["server"]["accept_new_client"]:
                p.show("It is accepted.")
                return True
            p.show("Maybe, we must ask the question.")
            return None

    def accept(self, identity, signature):
        """
        ajoute le client passe en parametre dans la liste blanche
        ou a la liste noir si l'utilisateur le veut
        Si il faut attendre l'approbation de l'utilisateur,
        cette fonction est bloquante.
        retourne True si au final le client est accepte, et False sinon
        """
        with raisin.Printer("Ask to user for accept a new client...", signature=signature) as p:
            is_a = self.is_accepted(identity["public_key"])
            if is_a == True:
                p.show("The client is already accepted.")
                return True
            if is_a == False:
                p.show("This client is already baned.")
                return False
            question =  "'%s' client shouaite se connecter.\n" % identity["username"] \
                        + "Il travail sur l'os '%s' sur le PC %s.\n" % (identity["os_version"], identity["hostname"]) \
                        + "Il est localise en %s a %s.\n" % (identity["country"], identity["city"]) \
                        + "Il pretend avoir l'adresse mac %s.\n" % identity["mac"]
            rep = raisin.worker.configuration.question_binaire(question, default=None, existing_window=None)
            listed = "whitelisted.py" if rep else "blacklisted.py"
            path = os.path.join(os.path.expanduser("~"), ".raisin", listed)
            data = set()
            with raisin.Lock(id="listed", timeout=30, signature=signature, locality_degrees=2):
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        data = eval(f.read())
                data.add(identity["public_key"].replace(b"\n", b""))
                with open(path, "w", encoding="utf-8") as f:
                    f.write(repr(data))
            if rep:
                p.show("The client is desormais accepted.")
            else:
                p.show("This client is desormais baned.")
            return rep

    def close(self):
        """
        permet de fermer proprement les sockets
        """
        with raisin.Printer("Close connection...", signature=self.signature):
            if self.tcp_socket_ipv4:
                self.receiver_ipv4.kill()
                self.tcp_socket_ipv4.close()
            if self.tcp_socket_ipv6:
                self.receiver_ipv4.kill()
                self.tcp_socket_ipv6.close()
            for client in self.clients:
                client["socket"].close()

    def receive(self):
        """
        generateur qui cede les variables:
        client_socket, (ip_client, port_client)
        des l'ors qu'un client tente de se connecter, que se soit en ipv4
        ou en ipv6
        """
        if self.ipv4 and self.ipv6:
            message = "aux adresses '%s' et '%s'" % (self.ipv4, self.ipv6)
        else:
            message = "a l'adresse '%s'" % (self.ipv4 if self.ipv4 else self.ipv6)
        with raisin.Printer("En ecoute sur le port %d %s..." % (self.port, message), signature=self.signature) as p:
            if self.receiver_ipv4:
                self.receiver_ipv4.start()
            if self.receiver_ipv6:
                self.receiver_ipv6.start()
            while 1:
                if self.receiver_ipv4:
                    yield from self.receiver_ipv4
                if self.receiver_ipv6:
                    yield from self.receiver_ipv6

    def handle(self, client_socket, key, signature):
        """
        cette methode doit etre lancee dans un thread
        c'est ici que l'on interragit avec un client
        """
        while 1:
            try:
                # Traitement des messages
                with raisin.Printer("Waiting for a reponse...", signature=signature) as p:
                    data = raisin.communication.answering.receive_data(client_socket, signature=signature)
                    if data[0] == 0: # si ce qui suit est un nom de ficher
                        p.show("Reception d'un gros message.")
                        pass
                    elif data[0] == 1: # si ce qui suit et un objet serialise
                        p.show("Reception d'un petit message.")
                        request = raisin.deserialize(
                            data[1:],
                            parallelization_rate=0,
                            psw=None,
                            signature=signature)
                        pass
                    else: # ce cas ne devrai jamais arriver
                        p.show("Le message recut ne respecte pas la norme.")
                        raise ValueError("Le message recut ne respecte pas la norme.")
            except Exception as e:
                # Suppresion est extermination du client
                client_socket.close()
                del self.clients[key]
                break

    def select(self):
        """
        Gere l'acceptation des nouveau clients.
        Si le client est accepte, il est ajouter dans les clients connectes
        et un nouveau thread apparait rien que pour lui
        """
        for client_socket, (ip_client, port_client) in self.receive():
            p.show("Un client d'ip %s tente de se connecter via le port %d." % (ip_client, port_client))
            if len(self.clients) >= raisin.worker.configuration.load_settings()["server"]["listen"]: # si il y a deja trop de monde
                p.show("Client expulse car il y a deja trop de monde connecte.")
                answer = {"type": "error", "message": "Desole, il y a deja trop de monde."}
                raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                continue
            with raisin.Printer("Demande de plus amples informations...", signature=self.signature):
                question1 = {"type": "question", "question": "How are you?"}
                raisin.communication.answering.send_object(client_socket, question1, signature=self.signature)
                try:
                    identity = raisin.communication.answering.receive_object(client_socket, signature=self.signature, timeout=30)
                except socket.timeout:
                    p.show("Client expulse car il met trop de temps a repondre.")
                    answer = {"type": "error", "message": "Tu es trop lent a repondre."}
                    raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                    continue
                with raisin.Printer("Verification de la reponse...", signature=self.signature):
                    champs = {
                        "type": str,
                        "public_key": bytes,
                        "username": str,
                        "os_version": str,
                        "hostname": str,
                        "country": str,
                        "city": str,
                        "mac": str,
                        }
                    for clef, genre in champs.items():
                        if clef not in identity:
                            p.show("Client expulse car il n'y a pas de champs '%s' dans sa reponse." % clef)
                            answer = {"type": "error", "message": "Il doit y avoir un champs '%s', ce n'est pas le cas." % clef}
                            raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                            continue
                        if type(identity[clef]) is not genre:
                            p.show("Client expulse car la valeur associee au champs '%s' n'est pas de type '%s'." % (clef, genre))
                            answer = {"type": "error", "message": "N'essai meme pas de hacker le champs '%s'"}
                            raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                            continue
                    if type(identity) is not dict:
                        p.show("Client expulse car il n'a pas repondu avec un dictionaire.")
                        answer = {"type": "error", "message": "Vous devez envoyer un dictionnaire, pas un %s." % type(identity)}
                        raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                        continue
                    if identity["type"] != "identity":
                        p.show("Client expulse car il ne veut pas donner son identite.")
                        answer = {"type": "error", "message": "Le type de reponse atendu est 'identity', pas %s." % str(identity["type"])}
                        raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                        continue
                    if not raisin.re.search(r"-----BEGIN PUBLIC KEY-----(.|\n)+-----END PUBLIC KEY-----", identity["public_key"].decode()):
                        p.show("Client expulse car la clef publique n'est pas au format 'PEM'.")
                        answer = {"type": "error", "message": "La clef publique n'est pas au format 'PEM'."}
                        raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                        continue
                    p.show("Le client a livre son identite.")
                if raisin.worker.configuration.load_settings()["server"]["force_authentication"]:
                    with raisin.Printer("Envoi d'un challenge pour confirmer l'identite...", signature=self.signature):
                        challenge = uuid.uuid4().bytes   # creation aleatoire d'une phrase 
                        question2 = {                    # on chiffre cette phrase avec la clef publique du client
                            "type":"challenge",
                            "challenge":raisin.worker.security.encrypt_rsa(
                                challenge,
                                identity["public_key"],
                                parallelization_rate=0,
                                signature=self.signature)}
                        answer_challenge = raisin.communication.answering.send_object(client_socket, question2, signature=self.signature) # on demande au client de la dechiffrer
                        if type(answer_challenge) is not dict:
                            p.show("Client expulse car il n'a pas repondu au challenge avec un dictionaire.")
                            answer = {"type":"error", "message":"Vous devez envoyer un dictionnaire, pas un %s." % type(answer_challenge)}
                            raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                            continue
                        if "type" not in answer_challenge:
                            p.show("Client expulse car il n'y a pas de champ 'type' dans ca reponse.")
                            answer = {"type":"error", "message":"Il doit y avoir un champs 'type' dans votre reponse."}
                            raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                            continue
                        if answer_challenge["type"] != "challenge_back":
                            p.show("Client expulse car ca reponse n'est pas un retour de challenge.")
                            answer = {"type":"error", "message":"Le type de reponse atendu est 'challenge_back', pas %s." % str(answer_challenge["type"])}
                            raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                            continue
                        if "challenge" not in answer_challenge:
                            p.show("Client expulse car il n'a pas voulut repondre au challenge.")
                            answer = {"type":"error", "message":"Il doit y avoir un champs 'challenge' dans votre reponse."}
                            raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                        if type(answer_challenge["challenge"]) is not bytes: # cela evite de pouvoir hacker la methode compare
                            p.show("Client expulse car il a tente de hacker la reponse du chalenge.")
                            answer = {"type":"error", "message":"Cherche pas a me hacker!"}
                            raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                        if answer_challenge["challenge"] != challenge:
                            p.show("Client expulse car il n'a pas reussi le defit.")
                            answer = {"type":"error", "message":"Vous etes un escrot, vous n'avez pas reussi le defit!"}
                            raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                            continue
                        p.show("Le client a reussi le defit.")
                autorization = self.is_accepted(identity["public_key"])
                if autorization == None: # si il faut demander l'avis
                    threading.Thread(target=self.accept, args=(identity.copy(), uuid.uuid4().hex)).start() # on pose la question a l'utilisateur
                    p.show("Client expulse car l'utilisateur n'a pas encore donne son accord.") # mais on attend pas qu'il reponde
                    answer = {"type": "error", "message": "Il faut attendre l'avis de l'utilisateur."}
                    raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                    continue
                elif autorization == False:  # si il faut le virer
                    p.show("Client expulse car il n'a pas le droit de metre les pieds ici!")
                    answer = {"type": "error", "message": "Tu n'a pas le droit de metre les pieds ici!"}
                    raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                    continue
                if identity["public_key"].replace(b"\n", b"") in self.clients:
                    p.show("Client expulse car il est deja connecte.")
                    answer = {"type": "error", "message": "Tu es deja connecte."}
                    raisin.communication.answering.send_object(client_socket, answer, signature=self.signature)
                    continue
                p.show("Client accepte.")
            with raisin.Printer("Ajout de ce client dans le serveur...", signature=self.signature):
                key = identity["public_key"].replace(b"\n", b"")
                self.clients[key] = {
                    "username": identity["username"],
                    "os_version": identity["os_version"],
                    "hostname": identity["hostname"],
                    "country": identity["counrty"],
                    "city": identity["city"],
                    "mac": identity["mac"],
                    "ip": ip_client,
                    "port": port,
                    "socket": client_socket,
                    "thread": threading.thread(
                        target=self.handle,
                        args=(client_socket, key, uuid.uuid4().hex)),
                }
                self.clients[key]["thread"].start()

    def start(self):
        """
        c'est la premiere methode qui doit
        etre appelle apres la creation de l'objet
        """
        return self.select()

    def __del__(self):
        self.close()

