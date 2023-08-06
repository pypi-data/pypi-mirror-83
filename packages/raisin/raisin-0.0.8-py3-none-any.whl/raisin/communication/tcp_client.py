#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import socket
import select
import sys
import threading

import raisin


class ClientIpv4:
    """
    permet d'avoir un dialogue avec un serveur
    """
    def __init__(self, ipv4, port, parallelization_rate, signature):
        assert 0 <= parallelization_rate <= 2
        self.ipv4 = str(ipv4)
        self.port = port
        self.parallelization_rate = parallelization_rate
        self.signature = signature
        self.must_die = False

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # creation d'un TCP/IP socket, SOCK_STREAM=>TCP
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # on tente de reutiliser le port si possible
        self.tcp_socket.connect((self.ipv4, self.port))                       # on etabli la connection

    def send(self, question):
        """
        envoi une question brute, non serialisee.
        ne retourne rien mais cette methode bloque tant que la question n'est pas partie
        """
        with raisin.Printer("Envoi de la question '%s'..." % question, signature=self.signature):
            raisin.communication.tcp_server.send(
                self.tcp_socket,
                raisin.serialize(
                    question,
                    parallelization_rate=self.parallelization_rate,
                    compresslevel=(-1 if self.parallelization_rate else 0),
                    signature=self.signature),
                signature=self.signature)

    def receive(self):
        """
        attend que le serveur reponde.
        retourne la reponsse deserialise du serveur
        """
        with raisin.Printer("Reception de la reponse...", signature=self.signature):
            data = raisin.communication.tcp_server.receive(self.tcp_socket, signature=self.signature)

        is_direct = data[0]
        if is_direct:
            return raisin.deserialize(data[1:], parallelization_rate=self.parallelization_rate, psw=None, signature=self.signature)
        else:
            with open(data[1:].decode("utf-8"), "rb") as f:
                reply = raisin.deserialize(f, parallelization_rate=self.parallelization_rate, psw=None, signature=self.signature)
            os.remove(data[1:].decode("utf-8"))
            return reply

    def close(self):
        self.must_die = True
        self.tcp_socket.close()

    def __del__(self):
        self.close()

class ClientIpv6:
    """
    permet d'avoir un dialogue avec un serveur
    """
    def __init__(self, ipv6, port, parallelization_rate, signature):
        assert 0 <= parallelization_rate <= 2
        self.ipv6 = str(ipv6)
        self.port = port
        self.parallelization_rate = parallelization_rate
        self.signature = signature
        self.must_die = False

        self.tcp_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)
        self.tcp_socket.connect((self.ipv6, self.port))

    def send(self, question):
        """
        envoi une question brute, non serialisee.
        ne retourne rien mais cette methode bloque tant que la question n'est pas partie
        """
        with raisin.Printer("Envoi de la question '%s'..." % question, signature=self.signature):
            raisin.communication.tcp_server.send(
                self.tcp_socket,
                raisin.serialize(
                    question,
                    parallelization_rate=self.parallelization_rate,
                    compresslevel=(-1 if self.parallelization_rate else 0),
                    signature=self.signature),
                signature=self.signature)

    def receive(self):
        """
        attend que le serveur reponde.
        retourne la reponsse deserialise du serveur
        """
        with raisin.Printer("Reception de la reponse...", signature=self.signature):
            data = raisin.communication.tcp_server.receive(self.tcp_socket, signature=self.signature)

        is_direct = data[0]
        if is_direct:
            return raisin.deserialize(data[1:], parallelization_rate=self.parallelization_rate, psw=None, signature=self.signature)
        else:
            with open(data[1:].decode("utf-8"), "rb") as f:
                reply = raisin.deserialize(f, parallelization_rate=self.parallelization_rate, psw=None, signature=self.signature)
            os.remove(data[1:].decode("utf-8"))
            return reply

    def close(self):
        self.must_die = True
        self.tcp_socket.close()

    def __del__(self):
        self.close()


class Client(threading.Thread):
    """
    Unique client TCP.
    Unique car il faut creer un objet par connection,
    chaque client est associe a un serveur.
    """
    def __init__(self, ip, port=0, signature=None):
        assert type(ip) is str, "L'ip doit etre une chaine de caractere."
        assert type(port) is int, "Le port doit etre un entier."
        assert port >= 0, "Le port doit etre positif ou nul."

        threading.Thread.__init__(self)
        self.signature = signature          # c'est la signature pour l'imprimente
        self.server_infos = {               # les informations concernant le serveur
            "ipv4_wan": None,
            "ipv4_wan": None,
            "ipv6": None,
            "dns_ipv4": None,
            "dns_ipv6": None,
            "port": None,
            "port_forwarding": None,
            "last_check": None,
        }
        self.server_in_lan = None           # booleen qui permet de dire si le serveur que l'on cherche a joindre est sur le meme reseau local que ce client

        with raisin.Printer("Initialisation of client from %s..." % repr(server_name), signature=signature) as p:
            # recherche des informations permetant de creer une connection
            
            # cas d'un nom de domaine raisin
            infos = raisin.communication.dns.get(ip, signature=self.signature)
            if infos: # si le serveur est deja recence par raisin
                self.server_infos = infos
                if infos["ipv4_wan"] != None and infos["ipv4_wan"] == str(raisin.Id().ipv4_wan): # si ce serveur a la meme ip publique
                    self.server_in_lan = True # c'est qu'il fait parti du meme reseau local
                elif infos["port_forwarding"]: # si il est de toute facon accessible depuis l'exterieur
                    self.server_in_lan = False # on considere que le serveur est dehors
                else:
                    raise RuntimeError("Serveur non local, son port externe est inconu.")

            else:
                # cas d'un vrai nom de dommaine
                dns = ip
                ip_dns = raisin.communication.dns.is_domain(ip, signature=signature)
                if ip_dns:
                    ip = ip_dns

                # cas d'une ipv6 ou d'une ipv4
                if raisin.communication.dns.is_ipv6(ip):
                    self.server_infos["ipv6"] = ip
                    if ip_dns:
                        self.server_infos["dns_ipv6"] = dns
                elif raisin.communication.dns.is_ipv4(ip):
                    if ip_dns:
                        self.server_infos["dns_ipv4"] = dns
                else:
                    raise RuntimeError("Entree incorecte, ce n'est ni une ip, ni un nom de domaine.")
                self.server_in_lan = ipadress.ip_address(ip).is_private
                if not self.server_infos["ipv6"]:
                    if self.server_in_lan:
                        self.server_infos["ipv4_lan"] = ip
                    else:
                        self.server_infos["ipv4_wan"] = ip

                # le port
                if 0 == port:
                    raise RuntimeError("Le port doit etre precise.")
                if self.server_in_lan:
                    self.server_infos["port"] = port
                else:
                    self.server_infos["port_forwarding"] = port



            # creation de la connection
            try: # on tente d'abord en ipv6
                self.tcp_socket_ipv6 = socket.socket(
                    socket.AF_INET6,        # socket internet en ipv6
                    socket.SOCK_STREAM)     # creation d'un TCP/IP socket, SOCK_STREAM=>TCP
                self.tcp_socket_ipv6.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)
            except Exception as e: # si la connection en ipv6 a echouee
                self.tcp_socket_ipv6 = None
            try: # allors on essay en ipv4
                self.tcp_socket_ipv4 = socket.socket(
                    socket.AF_INET,         # socket internet plutot qu'un socket unix
                    socket.SOCK_STREAM)     # creation d'un TCP/IP socket, SOCK_STREAM=>TCP
                self.tcp_socket_ipv4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # on tente de reutiliser le port si possible
            except Exception as e:
                self.tcp_socket_ipv4 = None
            if self.tcp_socket_ipv6 == None and self.tcp_socket_ipv4 == None:
                raise RuntimeError("Impossible de creer un socket TCP, peut etre n'y a-t-il pas internet?")

    def run(self):
        """
        Methode special appelle par la classe parente.
        Au moment ou l'on fait: self.start()
        """
        pass


"""
copier coller du site
"""

def example():
    # Choosing Nickname
    nickname = input("Choose your nickname: ")

    # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 55555))

    # Listening to Server and Sending Nickname
    def receive():
        while True:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    print(message)
            except:
                # Close Connection When Error
                print("An error occured!")
                client.close()
                break

    # Sending Messages To Server
    def write():
        while True:
            message = '{}: {}'.format(nickname, input(''))
            client.send(message.encode('ascii'))

    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()




