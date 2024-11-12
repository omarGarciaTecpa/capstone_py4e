from settings import *
from models.usuarios import Usuario, DataDictUsuario

class DataImporter:   
    """Imports and cleans data from the datasources

    Attributes:
        connection: connection to the database
    """
    def __init__(self,  db_connection: sqlite3.Connection):
        self.connection = db_connection
        self.usuario_datadict = None
        self.usuario_list = None
        pass
    pass


    def import_datadict_usuario(self):        
        """Create the DataDictUsuario
        """
        try:
            src_file = open(DATA_DICT['usuario'], encoding='utf-8-sig')
        except:
            print(f"Couldn't open the file for Usuario datasource")
            quit()
        DataDictUsuario.start(src_file)
        self.usuario_datadict = DataDictUsuario.import_from_csv()

        # for item in self.usuario_datadict.values(): print(item)
        
        src_file.close()
        pass

    def import_usuarios(self):
        """Add Usuarios to the database."""

        try:
            src_file = open(DATA_SOURCES['usuario'], encoding="utf-8")
        except:
            print(f"Couldn't open the file for Usuario datasource")
            quit()

        Usuario.start(self.connection, src_file)
        Usuario.import_from_csv()
        src_file.close()
        pass

    def import_all(self):
        """Import All data into the database or dictionaries"""
        #import Data Dictionary of Usuarios and Usuarios
        self.import_datadict_usuario()
        self.import_usuarios()
    


# MAIN APP LOOP -------------------------------------------------------
try:
    conn = sqlite3.connect(DATA_BASES['content'])
    conn.row_factory = sqlite3.Row
except:
    print("Could not connect to database. Quitting app")
    quit()



importer = DataImporter(conn)
importer.import_all()
conn.close()
