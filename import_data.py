from settings import *
from models.usuarios import Usuario, MetaUsuario

class DataImporter:   
    """Imports and cleans data from the datasources

    Attributes:
        connection: connection to the database
    """
    def __init__(self,  db_connection: sqlite3.Connection):
        self.connection = db_connection
        self.meta_usuario_dict = None
        self.usuario_list = None
        pass
    pass


    def import_meta_usuario(self):        
        """Create Dictionary with MetaUsuario
        """

        pass

    def import_usuarios(self):
        """Add Usuarios to the database
        """

        try:
            src_file = open(DATA_SOURCES['usuario'], encoding="utf-8")
        except:
            print(f"Couldn´t open the file for Usuario datasource")
            quit()

        Usuario.start(self.connection, src_file)
        Usuario.import_from_csv()
        src_file.close()
        pass

    def import_all(self):
        #import Meta of Usuarios and Usuarios
        self.import_meta_usuario()
        self.import_usuarios()
        pass


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
