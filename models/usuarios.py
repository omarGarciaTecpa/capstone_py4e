from settings import *

class MetaUsuario:
    pass



class Usuario:
    connection: sqlite3.Connection = None
    src_file: str = None
    
    def __init__(self, edad: int ,P6_2_1 : int,P6_2_2: int, P6_2_3: int, P6_3: int, P7_1: int,P7_2: int, id: int = -1):
        self.id = id
        self.edad   = edad
        self.P6_2_1 = P6_2_1
        self.P6_2_2 = P6_2_2
        self.P6_2_3 = P6_2_3
        self.P6_3   = P6_3
        self.P7_1   = P7_1
        self.P7_2   = P7_2
        pass

    def __str__(self):
        msg = ""
        msg += "**********************************************\n"        
        msg += f"id: {self.id}\n"
        msg += f"edad: {self.edad}\n"
        msg += f"P6_2_1: {self.P6_2_1}\n"
        msg += f"P6_2_2: {self.P6_2_2}\n"
        msg += f"P6_2_3: {self.P6_2_3}\n"
        msg += f"P6_3: {self.P6_3}\n"
        msg += f"P7_1: {self.P7_1}\n"
        msg += f"P7_2: {self.P7_2}\n"
        msg += "----------------------------------------------\n"
        return msg
        pass

    @classmethod
    def start(cls, connection, src_file):
        cls.connection = connection
        cls.validate_connection()    
        cls.drop_create_table()   

        cls.src_file = src_file
        pass

    @classmethod
    def validate_connection(cls):
        if cls.connection is None:
            print("Connection is not ready. start() should be run before using the connection")
            quit()


    @classmethod
    def drop_create_table(cls):
        #create table
        cursor = cls.connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS Usuarios")
        cursor.execute("""
        CREATE TABLE Usuarios (
            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            edad INTEGER,
            P6_2_1 INTEGER,
            P6_2_2 INTEGER,	
            P6_2_3 INTEGER,
            P6_3  INTEGER,
            P7_1 INTEGER,
            P7_2 INTEGER           
        )""")
        cls.commit(True)
        cursor.close()
        pass
    

    @classmethod
    def import_from_csv(cls):
        if cls.src_file is None:
            print("The data source file was not opened")
            quit()

        reader = csv.DictReader(cls.src_file)
        counter = 0

        for index, row in enumerate(reader):
            counter += 1
            edad = row['EDAD']
            P6_2_1 = cls.convert_int(row,'P6_2_1') 
            P6_2_2 = cls.convert_int(row,'P6_2_2')  
            P6_2_3 = cls.convert_int(row,'P6_2_3')   
            P6_3 = cls.convert_int(row,'P6_3')            
            P7_1 = cls.convert_int(row,'P7_1')  
            P7_2 = cls.convert_int(row,'P7_2')  
            temp = Usuario(edad, P6_2_1, P6_2_2, P6_2_3, P6_3, P7_1, P7_2)
            temp.create()  

            if counter % INSERT_LOOP_MAX == 0:
                print("Commited:", index)
                cls.connection.commit()

        cls.connection.commit() # final commit
        pass

    @classmethod
    def convert_int(cls, row, column_name: str):
        return int(row[column_name]) if str.isnumeric(row[column_name]) else 0 

    @classmethod
    def commit(cls, auto_commit: bool = False):
        if auto_commit:
            cls.connection.commit()
        pass

    @classmethod
    def list(cls):
        cursor = cls.connection.cursor()
        cursor.execute("SELECT * from Usuarios")
        usuario_list = []
        for row in cursor.fetchall():
            temp = Usuario(
                id=row['id'],
                edad=row['edad'],
                P6_2_1=row['P6_2_1'],
                P6_2_2=row['P6_2_2'],
                P6_2_3=row['P6_2_3'],
                P6_3 = row['P6_3'],
                P7_1= row['P7_1'],
                P7_2= row['P7_2'] )
            

            usuario_list.append(temp)


        cursor.close()
        return usuario_list
        pass

    def create(self, auto_commit: bool = False):
        cursor = self.connection.cursor()
        command = """
        INSERT INTO Usuarios (edad, P6_2_1, P6_2_2, P6_2_3, P6_3, P7_1, P7_2)
        VALUES(?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(command, (self.edad, self.P6_2_1, self.P6_2_2, self.P6_2_3, self.P6_3, self.P7_1, self.P7_2))
  
        id = cursor.lastrowid
        self.id = id
        cursor.close()
        self.commit(auto_commit)
        return id 
        pass

    
    
    
    pass