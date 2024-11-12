from settings import *



class DataDictUsuario:
    src_file = None

    def __init__(self, columna, descripcion, tipo_dato, longitud, codigo_valido, metadatos):
        self.columna = columna
        self.descripcion = descripcion
        self.tipo_dato = tipo_dato  
        self.longitud = longitud   
        self.codigo_valido = codigo_valido 
        self.metadatos = metadatos

        pass

    def __str__(self):
        msg = ""
        msg += "**********************************************\n"        
        msg += f"Columna: {self.columna}\n"
        msg += f"Descripción: {self.descripcion}\n"
        msg += f"Tipo de Dato: {self.tipo_dato}\n"
        msg += f"Longitud: {self.longitud}\n"
        msg += f"Código Válido: {self.codigo_valido}\n"
        msg += f"Metadatos: {self.metadatos}\n"
        msg += "\n\n"
        return msg
        pass

    @classmethod
    def start(cls, src_file):
        """ Setups the class and must be called before any other method.

        Args:
            src_file: File handle to the source csv
        """
        cls.src_file = src_file

    @classmethod
    def import_from_csv(cls)-> dict[str, 'DataDictUsuario']:
        if cls.src_file is None:
            print("The data source file was not opened")
            quit()

        reader = csv.DictReader(cls.src_file)
        datadict = {}
        
        for index, row in enumerate(reader):
            columna = row['COLUMNA']
            descripcion = row['DESCRIPCION']
            tipo_dato = row['TIPO_DATO'] 
            longitud = row['LONGITUD'] 
            codigo_valido = row['CODIGO_VALIDO']
            metadatos = row['METADATOS']

            temp = DataDictUsuario(columna=columna, descripcion=descripcion, tipo_dato=tipo_dato, 
                               longitud=longitud, codigo_valido=codigo_valido, metadatos=metadatos)

            if datadict.get(columna) is not None:
                print("there is a reapeated column in the dictionary")
                quit()
            
            datadict[columna] = temp
        return datadict


class Usuario:
    """ Representation of Usuarios from the survey.

    Attributes:
        connection: Connection to the sqlite database [class attribute]
        src_file: File handle for the source file [class attribute]
        id: id after insertion
        edad: Age of the surveyed person
        P6_1: PC, laptop or tablet usage question   
        P6_2_1: PC, laptop or tablet usage question 
        P6_2_2: PC, laptop or tablet usage question
        P6_2_3: PC, laptop or tablet usage question
        P6_3: PC, laptop or tablet usage question
        P7_1: Internet usage question
        P7_2: Internet usage question
    """
    connection: sqlite3.Connection = None
    src_file = None
    
    def __init__(self, edad: int ,P6_1,P6_2_1 : int,P6_2_2: int, P6_2_3: int, 
                 P6_3: int, P7_1: int,P7_2: int, id: int = -1):
        self.id = id
        self.edad   = edad
        self.P6_1 = P6_1
        self.P6_2_1 = P6_2_1
        self.P6_2_2 = P6_2_2
        self.P6_2_3 = P6_2_3
        self.P6_3   = P6_3
        self.P7_1   = P7_1
        self.P7_2   = P7_2
        

    def __str__(self):
        msg = ""
        msg += "**********************************************\n"        
        msg += f"id: {self.id}\n"
        msg += f"edad: {self.edad}\n"
        msg += f"P6_1: {self.P6_1}\n"
        msg += f"P6_2_1: {self.P6_2_1}\n"
        msg += f"P6_2_2: {self.P6_2_2}\n"
        msg += f"P6_2_3: {self.P6_2_3}\n"
        msg += f"P6_3: {self.P6_3}\n"
        msg += f"P7_1: {self.P7_1}\n"
        msg += f"P7_2: {self.P7_2}\n"
        msg += "\n\n"
        return msg
        

    @classmethod
    def start(cls, connection, src_file):
        """ Setups the class and must be called before any other method.

        Args:
            connection: Sqlite connection to the database
            src_file: File handle to the source csv
        """
        cls.connection = connection
        cls.validate_connection()    
        cls.drop_create_table()   

        cls.src_file = src_file
        

    @classmethod
    def validate_connection(cls):
        """ Closes the app if the connection does not exist.
        """
        if cls.connection is None:
            print("Connection is not ready. start() should be run before using the connection")
            quit()


    @classmethod
    def drop_create_table(cls):
        """ Erases the table from the database and then recreates it. 
        """

        cls.validate_connection()
        #create table
        cursor = cls.connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS Usuarios")
        cursor.execute("""
        CREATE TABLE Usuarios (
            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            edad INTEGER,
            P6_1 INTEGER,
            P6_2_1 INTEGER,
            P6_2_2 INTEGER,	
            P6_2_3 INTEGER,
            P6_3  INTEGER,
            P7_1 INTEGER,
            P7_2 INTEGER           
        )""")
        cls.commit(True)
        cursor.close()
        
    

    @classmethod
    def import_from_csv(cls):
        """Reads the CSV source file and imports it into the database."""

        cls.validate_connection()

        if cls.src_file is None:
            print("The data source file was not opened")
            quit()

        reader = csv.DictReader(cls.src_file)

        for index, row in enumerate(reader):
            edad = row['EDAD']
            P6_1 = cls.convert_int(row,'P6_1') 
            P6_2_1 = cls.convert_int(row,'P6_2_1') 
            P6_2_2 = cls.convert_int(row,'P6_2_2')  
            P6_2_3 = cls.convert_int(row,'P6_2_3')   
            P6_3 = cls.convert_int(row,'P6_3')            
            P7_1 = cls.convert_int(row,'P7_1')  
            P7_2 = cls.convert_int(row,'P7_2')  
            temp = Usuario(edad, P6_1, P6_2_1, P6_2_2, P6_2_3, P6_3, P7_1, P7_2)
            temp.save()  

            # commit only every X insertions, based on INSERT_LOOP_MAX
            if (index + 1) % INSERT_LOOP_MAX == 0:
                print("Commited:", index + 1)
                cls.connection.commit()

        cls.connection.commit() # final commit
        

    @classmethod
    def convert_int(cls, row, column_name: str) -> int:
        """Checks if the values is a number otherwise returns 0.
        
        Since many of the values in the survey are empty, we need to validate
        whether the value will cause an error when convertint into an int.
        
        Args:
            row: Row we are currently reading
            column_name: Name of the column. Case Sensitive.

        Returns:
            The int version of the value
        """
        return int(row[column_name]) if str.isnumeric(row[column_name]) else 0 


    @classmethod
    def commit(cls, auto_commit: bool = False):
        """Will commit the connection based on auto commit.
        
        Args:
            auto_commit: Whether the connection should commit. Default False
        """
        cls.validate_connection()
        if auto_commit:
            cls.connection.commit()
        

    @classmethod
    def list(cls) -> list['Usuario']: 
        """Gets all the Usuarios from database.
        
        Returns:
            A list of all the Usuarios
        """
        cls.validate_connection()

        cursor = cls.connection.cursor()
        cursor.execute("SELECT * from Usuarios")
        usuario_list = []

        for row in cursor.fetchall():
            temp = Usuario(
                id=row['id'],
                edad=row['edad'],
                P6_1=row['P6_1'],
                P6_2_1=row['P6_2_1'],
                P6_2_2=row['P6_2_2'],
                P6_2_3=row['P6_2_3'],
                P6_3 = row['P6_3'],
                P7_1= row['P7_1'],
                P7_2= row['P7_2'] )
            

            usuario_list.append(temp)


        cursor.close()
        return usuario_list
      

    def save(self, auto_commit: bool = False):
        """ Saves the current Ususario into the database. 
        
        WARNING: Does not include the update part!!!

        Args:
            auto_commit: If True commits the connection 
        
        Returns:
            Returns the Id of the created Usuario
        """
        self.validate_connection()

        cursor = self.connection.cursor()
        command = """
        INSERT INTO Usuarios (edad, P6_1, P6_2_1, P6_2_2, P6_2_3, P6_3, P7_1, P7_2)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(command, (self.edad, self.P6_1, self.P6_2_1, self.P6_2_2, self.P6_2_3, self.P6_3, self.P7_1, self.P7_2))
  
        id = cursor.lastrowid
        self.id = id
        cursor.close()
        self.commit(auto_commit)
        return id 
        

