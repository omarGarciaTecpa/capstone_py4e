from os.path import join
from models.usuarios import Usuario, DataDictUsuario
from settings import *
import json


class DataBuilder:
    def read_file(self):
        ''' Open and print the data json file.
        '''
        file_r = open(CHART_FILES['main'], 'r')
        print(f"Opening file: {file_r}")
        for line in file_r:
            print(line)



    def build_file(self, dict):
        '''Builds the json file that feeds the visualization.
        
        It gets the path of the file from CHART_FILES['main']
        present in setting.py
        '''
        file_w = open(CHART_FILES['main'], 'w', encoding='utf8') 
        file_dict = {
            "name": "Usage of computing devices in households in Mexico (2022)", 
            "children": [
                dict
            ]
        }

        json.dump(dict, file_w, ensure_ascii=False)

        file_w.close()

    
    def get_p6_1_dict(self, list: list['Usuario'], data_dict: dict['DataDictUsuario']):
        '''
        Build the dictionary to answer the P6_1 question:

        The question to answer reads as follows:
            "6.1 En los últimos tres meses, ¿utilizó computadora, laptop o tablet en este hogar o fuera de él?"
        Args:
            list: the list of all the usuarios
            data_dict: the data dictionary for usuario
        
        Returns: 
            A dict contanining the answer's data and related answers
        '''
        dict_item = data_dict['P6_1']
        print(dict_item.descripcion)     
        children6_1 = []
        
        r_yes = [item for item in list if item.P6_1 == 1]   


        truthy = [(1,1,1),(1,1,2),(1,2,1),(1,2,2),(2,1,1),(2,1,2),(2,2,1),(2,2,2)] 
        children6_2 = []
        for row in truthy:
            children6_2.append(self.get_p6_2_dict(row,list, data_dict))
        

        children6_1.append({"name":"Sí", "children": children6_2})
        
        r_no = [item for item in list if item.P6_1 == 2]
        children6_1.append(self.get_p6_3_dict(r_no, data_dict))

        result = {
            "name": dict_item.descripcion,
            "children": children6_1
        }
        
        return result
    

    
    def get_p6_2_dict(self, truthy_row, list, data_dict: dict['DataDictUsuario']):
        '''
        Build the dictionary to answer the P6_2_1 question:

        The questions to answer read as follows:
            - "6.2.1 ¿Usted usa… computadora de escritorio?"
            - "6.2.2 ¿Usted usa… computadora portátil (laptop, notebook)?"
            - "6.2 ¿Usted usa… tablet?"

        These answers only apply to those who answered "Yes/Si" at question P6_1
            
        Args:
            list: the list of all the usuarios who said "Yes"
            data_dict: the data dictionary for usuario
        
        Returns: 
            A dict contanining the answer's data and related answers
        '''
        dict_items = []
        dict_items.append(data_dict[f'P6_2_1'])
        dict_items.append(data_dict[f'P6_2_2'])
        dict_items.append(data_dict[f'P6_2_3'])

        res = [item for item in list if getattr(item, f"P6_2_1") == truthy_row[0] and getattr(item, f"P6_2_2") == truthy_row[1] and getattr(item, f"P6_2_3") == truthy_row[2]] 
        
        label = ""
        for index in range(0,3):
            if truthy_row[index] == 1:
                if ("escritorio" in dict_items[index].descripcion):
                    label += f"Escritorio, "
                if ("laptop" in dict_items[index].descripcion):
                    label += f"Laptop, "
                if ("tablet" in dict_items[index].descripcion):
                    label += f"Tablet, "

        if len(label) == 0:
            label = "No usa ninguna"
        print(label, len(res))

        return {"name": label, "value": len(res)}

  
 


    def get_p6_3_dict(self, list, data_dict: dict['DataDictUsuario']):
        '''
        Build the dictionary to answer the P6_3 question:

        The question to answer reads as follows:
            "6.3 ¿Por qué no utiliza computadora, laptop o tablet?"

        This answer only applies to those who answered "No" at question P6_1
            
        Args:
            list: the list of all the usuarios who said "No"
            data_dict: the data dictionary for usuario
        
        Returns: 
            A dict contanining the answer's data and related answers
        '''
        dict_item = data_dict['P6_3']
        dict_meta = dict_item.metadatos

        children = []

        # Aggregate each question that was answered
        for index, item in enumerate(dict_meta):            
            temp_list = [answer for answer in list if answer.P6_3 == (index + 1)]
            children.append({"name": item, "value": len(temp_list)})
            print(f"[{index}]: {item}")

        # Aggregate the case where the question was not answered
        no_res = [answer for answer in list if answer.P6_3 == 0]
        children.append({"name":"No respondió", "value": len(no_res)})

        for res in children:
            print(res)

        return {"name":"No", "children": children}

        pass


# MAIN APP LOOP -------------------------------------------------------
try:
    conn = sqlite3.connect(DATA_BASES['content'])
    conn.row_factory = sqlite3.Row
except:
    print("Could not connect to database. Quitting app")
    quit()

try:
    src_file = open(DATA_DICT['usuario'], encoding='utf-8-sig')
except:
    print(f"Couldn't open the file for Usuario datasource")
    quit()


# Read the usuario list
Usuario.start(connection=conn, src_file=None)
usuario_list = Usuario.list()
print("Total user answers in DB:" , len(usuario_list))

#create the data dict
DataDictUsuario.start(src_file)
data_dict = DataDictUsuario.import_from_csv()

# start the builder
builder = DataBuilder()
data = builder.get_p6_1_dict(usuario_list, data_dict)
builder.build_file(data)


conn.close()