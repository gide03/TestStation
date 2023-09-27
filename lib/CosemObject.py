import requests
import logging
import pathlib
from copy import deepcopy

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()
PROJECT_DIR = CURRENT_DIR.parent
LOG_DATA_DIR = f'{PROJECT_DIR}/log_data'

BACKEND_API = 'http://10.23.40.185/api'
PROJECT_NAME = 'RUBY'
VERSION = '0.04_20230922'
OBJECT_NAME = 'PRMNumber'

LEVEL = {
    "NOTSET" : logging.NOTSET,
    "DEBUG" : logging.DEBUG,
    "INFO" : logging.INFO,
    "WARNING" : logging.WARN,
    "ERROR" : logging.ERROR,
    "CRITICAL" : logging.CRITICAL
}

# LOGGER

# Create a logger
logger = logging.getLogger(__name__)
# Set the log level
logger.setLevel(LEVEL['DEBUG'])
# Create file handler
file_handler = logging.FileHandler(f'{LOG_DATA_DIR}/CosemObject.log')
# Create a console handler
console_handler = logging.StreamHandler()
# Set the log format
console_handler.setFormatter(logging.Formatter('[%(asctime)s - %(name)s] - %(levelname)s - %(message)s'))
file_handler.setFormatter(logging.Formatter('[%(asctime)s - %(name)s] - %(levelname)s - %(message)s'))
# Add the console handler to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

class Node:
    def __init__(self, id:str) -> None:
        '''
           Attribute/Method presentation of COSEM
        '''
        self.id = id
        self.data_structure = None
        self.default_value = None
        self.min_value = None
        self.max_value = None
        self.association  = None
    
    # @property
    # def data_structure(self, flatten:bool = False) -> list:
    #     '''
    #         Data structure getter
    #     '''
    #     if flatten:
    #         pass
    #     return self.data_structure
    # @data_structure.setter
    # def data_structure(self, new_value) -> None:
    #     self.data_structure = new_value
    
    # @property
    # def min_value(self, flatten:bool = True) -> list:
    #     '''
    #         Minimum value getter
    #     '''
    #     if flatten:
    #         pass
    #     return self.min_value
    # @min_value.setter
    # def min_value(self, new_value) -> None:
    #     self.min_value = new_value
    
    # @property
    # def max_value(self, flatten:bool = True) -> list:
    #     '''
    #         Maximum value getter
    #     '''
    #     if flatten:
    #         pass
    #     return self.max_value
    # @max_value.setter
    # def max_value(self, new_value):
    #     self.max_value = new_value
    
    # @property
    # def association(self, flatten:bool = True) -> list:
    #     '''
    #         Default value getter
    #     '''
    #     if flatten:
    #         pass
    #     return self.association
    # @max_value.setter
    # def association(self, new_value):
    #     self.association = new_value
    
class COSEM:
    def __init__(self, ui_state) -> None:
        '''
            UI State stored in database. The us_state itself represent COSEM object 
            Refer to backend documentation
        '''
        self.object_name = ''
        self.logical_name = ''
        self.attributes = []
        self.methods = []
        
        self.render(ui_state)
        
    def walk(self, node, key):
        '''
            Walk the structure of attribute/method nodes. NOTE: Attribute and method represented list of "Tree" structure of Nodes.
            Refer to backend documentation
        '''
        # dtype = node['_dtype']
        # output = node[key]
        # if "Array" in dtype and key == '_dtype':
        #     output = ({dtype: [self.walk(node['arrayTemplate'], key)]})
            
        # elif "Array" in dtype or "Structure" in dtype:
        #     output = {}
        #     output[dtype] = []
        #     temp = []
        #     for child in node['children']:
        #         temp.append(self.walk(child, key))
        #     output[dtype] = temp
        return None
    
    def render(self, data):
        '''
            Render data from UI state format
        '''
        self.object_name = data['objectName']
        self.logical_name = data['logicalName']
        
        attribute_list = data['attribute']
        method_list = data['method']
        # Render Attribute
        for att in attribute_list:
            Att = Node(att['id'])
            Att.data_structure = self.walk(att, '_dtype')
            Att.default_value = self.walk(att, 'defaultValue')
            Att.min_value = self.walk(att, 'minValue')
            Att.max_value = self.walk(att, 'maxValue')
            self.attributes.append(deepcopy(Att))

        # Render Method
        for mtd in method_list:
            Mtd = Node(att['id'])
            Mtd.data_structure = self.walk(mtd, '_dtype')
            Mtd.default_value = self.walk(mtd, 'defaultValue')
            Mtd.min_value = self.walk(mtd, 'minValue')
            Mtd.max_value = self.walk(mtd, 'maxValue')
            self.attributes.append(deepcopy(Mtd))

def get_data_structure(cosem):
    def walk(attribute):
        pass
    pass    

def get_cosem_list(projectname, version):
    cosem_list = requests.get(f'{BACKEND_API}/project/getcosemlist/{projectname}/{version}')
    return cosem_list.json()

def fetch_cosem(projectname, version):
    logger.info('Fetch all cosem data')
    cosem_list = get_cosem_list(PROJECT_NAME, VERSION)    
    cosem_list_out = []
    for cosem in cosem_list:
        cosem_data = requests.get(f'{BACKEND_API}/project/get/{projectname}/{version}/{cosem}').json()
        object = COSEM(cosem_data)
        break

    return cosem_list_out
        

fetch_cosem(PROJECT_NAME, VERSION)