from settings import *
from models.usuarios import Usuario, DataDictUsuario

class DataImporter:   
    """Imports and cleans data from the datasources

    Attributes:
        connection: connection to the database
        usuario_datadict: contains the Data Dictionary info for Usuarios
        usuario_list: usuarios in the dabatase
    """
    def __init__(self,  db_connection: sqlite3.Connection):
        self.connection: sqlite3.Connection  = db_connection
        self.usuario_datadict: dict[str,'DataDictUsuario'] = None
        self.usuario_list: list['Usuario'] = None


    def import_datadict_usuario(self)-> dict[str, 'DataDictUsuario']:        
        """Create the DataDictionary for Usuario.

        It's main use is getting the text labels for the questions
        and answers. It uses the value in DATA_DICT['usuario'] from
        settings as path for the csv file.

        Returns:
            Data Dictionary of Users
        """
        try:
            src_file = open(DATA_DICT['usuario'], encoding='utf-8-sig')
        except:
            print(f"Couldn't open the file for Usuario datasource")
            quit()
        DataDictUsuario.start(src_file)
        self.usuario_datadict = DataDictUsuario.import_from_csv()
         
        print(f"Usuario Data Dictionary items: {len(self.usuario_datadict.keys())}")
        src_file.close()
        return self.usuario_datadict
        

    def import_usuarios(self) -> list['Usuario']:
        """Add Usuarios to the database.
        
        Reads users from the source csv file described in DATA_SOURCES['usuario']
        present in settings.py; then it saves these users in the database.

        Returns:
        List of Usuarios
        """
        try:
            src_file = open(DATA_SOURCES['usuario'], encoding="utf-8")
        except:
            print(f"Couldn't open the file for Usuario datasource")
            quit()

        Usuario.start(self.connection, src_file)
        Usuario.import_from_csv()
        self.usuario_list = Usuario.list()
        print(f"Imported {Usuario.count()} Usuario(s) in total.")        
        src_file.close()
        return self.usuario_list
        

   


# MAIN APP LOOP -------------------------------------------------------
# create the database connection
try:
    conn = sqlite3.connect(DATA_BASES['content'])
    # Establish a row factory so we can reference columns by 
    # name instead of index
    conn.row_factory = sqlite3.Row 

except:
    print("Could not connect to database. Quitting app")
    quit()

#create importer and import the data
importer = DataImporter(conn)
importer.import_usuarios()
importer.import_datadict_usuario() # this function is only called here for testing purposes
conn.close()
