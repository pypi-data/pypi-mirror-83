#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Associ un "nom de dommaine" raisin, a
un vrai nom de dommaine ou a une ip et un port.
"""
import ipaddress
import os
import socket

import raisin

def get(rais_domain, signature):
    """
    Si le nom de domain est un nom de domaine recence par raisin.
    Les informations permettant de se connecter a ce serveur sont retourne.
    Sinon retourne None.
    L'objet retourne ressemble a ca:
        {
        "ipv4_wan": "37.45.168.54",
        "ipv4_wan": "192.168.1.24",
        "ipv6": "2a01:cb15:829b:c600:4ca7:56b3:fd1e:1719",
        "dns_ipv4": "machin_chose.ddns.net",
        "dns_ipv6": None,
        "port": 16395,
        "port_forwarding": None,
        "last_check": 1602927982.9591131,
        }
    """
    assert type(rais_domain) is str, "Le nom de domaine doit etre une chaine de caractere. Pas %s." % type(rais_domain)
    with raisin.Printer("Recherche du domain %s..." % rais_domain, signature=signature) as p:
        filename = os.path.join(os.path.expanduser("~"), "dns.py")
        if not os.path.exists(filename): # si le fichier n'existe pas
            p.show("File not found.")
            return None
        with open(filename, "r", encoding="utf-8") as f:
            dico = eval(f.read()) # c'est vraiment moche cette ligne niveau complexite!
        if rais_domain not in dico:
            p.show("Domain not present in the database.")
            return None
        infos = dico[rais_domain]
        p.show("Trouve: %s" % repr(infos))
        return infos

def is_ipv4(addr):
    """
    retourne True si il s'agit d'une adresse ipv4
    """
    assert type(addr) is str, "Pour ce test, l'ip doit etre une chaine de caractere."
    try:
        ipaddress.IPv4Address(addr)
        return True
    except ipaddress.AddressValueError:
        return False

def is_ipv6(addr):
    """
    retourne True si il s'agit d'une adresse ipv6
    """
    assert type(addr) is str, "Pour ce test, l'ip doit etre une chaine de caractere."
    try:
        ipaddress.IPv6Address(addr)
        return True
    except ipaddress.AddressValueError:
        return False

def is_domain(domain, signature):
    """
    retourne l'ip du dommaine si il s'agit d'un nom de domaine
    associe a une adresse ip. Retourn False sinon.
    """
    assert type(domain) is str, "Pour ce test, le nom de dommaine doit etre une chaine de caractere."
    with raisin.Printer("Attribution d'un potentiel dns a une ip...", signature=signature):
        if not raisin.re.fullmatch(r"(?!\-)(?:[a-zA-Z\d\-]{0,62}[a-zA-Z\d]\.){1,126}(?!\d+)[a-zA-Z\d]{1,63}", domain):
            return False
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            return False




