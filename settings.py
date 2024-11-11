import sqlite3
from os.path import join
import csv

INSERT_LOOP_MAX = 200

DATA_META = {
    "usuario": join("datasources", "diccionario_de_datos", "diccionario_de_datos_tr_endutih_usuarios_anual_2022.csv")
}


DATA_SOURCES = { 
    "usuario": join("datasources", "conjunto_de_datos", "tr_endutih_usuarios_anual_2022.csv")
}


DATA_BASES = {
    "content": join("databases", 'content.sqlite')
}

