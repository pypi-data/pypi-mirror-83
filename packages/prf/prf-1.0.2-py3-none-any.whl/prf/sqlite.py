import sqlite3
from slovar import slovar

def includeme(config):
    Settings = slovar(config.registry.settings)
    sqlite3.connect()