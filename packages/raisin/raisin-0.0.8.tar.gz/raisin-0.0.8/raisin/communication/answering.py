#!/usr/bin/env python3
#-*- coding: utf-8 -*-


"""
Ce module est charge de repondre aux clients.
Il permet aussi la gestion bas niveau des sockets TCP
afin de serialiser/deserialiser les requettes et les reponsses.
"""

import raisin

def send_data(s, generator, signature):
    """
    permet d'envoyer des donnees
    'generator' est la sortie d'une fonctions de serialisation
    """
    def standardize_generator_sizes(generator, buff_size):
        """
        'generator' est un generateur qui cede des paquets de taille tres variable
        les paquets doivent etre de type 'bytes'
        le but est ici, d'uniformiser la taille des packets afin de renvoyer des packets de 
        'buff_size' octets
        cede donc les paquets au fure et a meusure
        """
        pack = b""
        for data in generator:                                          # on va lentement vider le generateur
            pack += data                                                # pour stocker peu a peu les paquets dans cette variable
            while len(pack) >= buff_size:                               # si le packet est suffisement gros
                yield pack[:buff_size]                                  # on le retourne avec la taille reglementaire
                pack = pack[buff_size:]                                 # puis on le racourci et on recomence le test
        if pack:
            yield pack       
    
    def anticipator(generator):
        """
        cede les packets du generateur accompagne d'un boolean
        qui vaut True si l'element itere est le dernier
        et false sinon. Le generateur doit donc etre capable de ceder au moin un paquet
        """
        actuel = next(generator)
        for pack in generator:
            yield False, actuel
            actuel = pack
        yield True, actuel
    
    with raisin.Printer("Envoi des donnees...", signature=signature) as p:
        for is_end, data in anticipator(standardize_generator_sizes(generator, 1024*1024 -1)):
            p.show("Contenu: %s" % (bytes([is_end]) + data))
            s.send(bytes([is_end]) + data)

def send_object(s, obj, signature):
    """
    fonctionne comme send_data
    mais prend un objet en entree
    n'est efficace que pour les petits objets
    """
    with raisin.Printer("Envoi d'un objet...", signature=signature):
        return send_data(s,
            raisin.serialize(
                obj,
                compresslevel=0,
                parallelization_rate=0,
                copy_file=False,
                signature=self.signature),
            signature=signature)

def receive_data(s, signature, timeout=None):
    """
    permet de receptionner les donnees,
    meme si elle sont nombreuses
    retourne soit directement les donnees soit le nom du fichier qui les contients
    ce qui permet de distinguer les 2, c'est le premier octet qui vaut 1 si les donnees sont directement recuperee
    ou 0 si ce qui suit est le nom de fichier
    """
    with raisin.Printer("Reception des donnees brutes...", signature=signature) as p:
        default_timeout = s.getdefaulttimeout()
        s.settimeout(timeout)
        data = s.recv(1024*1024)
        is_end = data[0]
        if is_end:
            p.show("Contenu: %s" % (b"\x01" + data[1:]))
            s.setdefaulttimeout(default_timeout)
            return b"\x01" + data[1:]
        filename = os.path.join(str(raisin.temprep), str(uuid.uuid4()))
        with open(filename, "wb") as f:
            f.write(data[1:])
            while not is_end:
                data = s.recv(1024*1024)
                f.write(data[1:])
                is_end = data[0]
        p.show("Contenu: %s" % (b"\x00" + filename.encode("utf-8")))
        s.setdefaulttimeout(default_timeout)
        return b"\x00" + filename.encode("utf-8")

def receive_object(s, signature, timeout=None):
    """
    fonction comme receive_data mais retourne directement l'objet
    deserialise
    """
    with raisin.Printer("Reception et mise en forme des donnees...", signature=signature):
        data = receive_data(s, signature, timeout=None)
        if data[0] == 1: # dans le cas ou les donnees sont toute presentes
            return raisin.deserialize(data[1:], parallelization_rate=0, signature=signature)
        elif data[0] == 0: # si c'est ecrit dans un fichier
            with open(data[1:].decode("utf-8")) as f:
                obj = raisin.deserialize(f, parallelization_rate=0, signature=signature)
            os.remove(data[1:].decode("utf-8"))
            return obj



def answering(data, signature):
	"""
	permet de traiter une question
	Pour une question de paralelisation, la requette 'data'
	doit etre etre serialise et commencer par b'\x01'
	ou bien doit etre serialise dans un fichier accessible
	retourne le resultat serialise sous la forme d'un generateur
	affin d'offir la possibilite d'une compression dynamique
	"""
	assert type(data) is bytes, "'data' doit etre de type bytes, pas %s." % type(data)
	
	# deserialisation de la requete
	is_direct = data[0]
	if is_direct:
		request = raisin.deserialize(data[1:], parallelization_rate=0, psw=None, signature=signature)
	else:
		with open(data[1:].decode("utf-8"), "rb") as f:
			request = raisin.deserialize(f, parallelization_rate=0, psw=None, signature=signature)
		os.remove(data[1:].decode("utf-8"))

	# traitement de la requette
	reply = "Tiens! voila ta reponse!"

	# emission de la reponsse
	return raisin.serialize(reply, signature=None, buff=1048576, compresslevel=0, copy_file=True, parallelization_rate=0, psw=None)


