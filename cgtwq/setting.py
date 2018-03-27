#-*- coding=UTF-8 -*-
"""Settings to connect server."""

SERVER_IP = '192.168.55.55'


def apply_():
    """Apply settings.   """
    from . import database

    database.Database.ip = SERVER_IP
