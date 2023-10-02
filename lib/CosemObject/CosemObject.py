import requests
import logging
import pathlib
from copy import deepcopy

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()
PROJECT_DIR = CURRENT_DIR.parent.parent
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

class AttributeTree:
    def __init__(self, node_ui_state) -> None:
        '''
           @brief - Attribute/Method presentation of COSEM
           @param - (node_ui_state str)
                    json string of ui state
        '''
        self.id = id
        self.data_structure = None
        self.default_value = None
        self.min_value = None
        self.max_value = None
        self.association  = None
        
        self.render(node_ui_state)
    
    def walk(self, node, key):
        '''
            Walk the structure of attribute/method node.
            Refer to backend documentation
        '''
        dtype = node['_dtype']
        output = node[key]
        if "Array" in dtype and key == '_dtype':
            _key = f'{dtype}-{node["minValue"]}-{node["maxValue"]}'
            output = ({_key: [self.walk(node['arrayTemplate'], key)]})
            
        elif "Structure" in dtype: # for structure
            output = {}
            output[dtype] = []
            temp = []
            for child in node['children']:
                temp.append(self.walk(child, key))
            output[dtype] = temp
        elif "Array" in dtype: # for array
            output = {}
            _key = f'{dtype}-{node["minValue"]}-{node["maxValue"]}'
            output[_key] = []
            temp = []
            for child in node['children']:
                temp.append(self.walk(child, key))
            output[_key] = temp
        return output
    
    def render(self, attribute_state):
        '''
            Render attribute_state to object
        '''
        self.id = attribute_state['id']
        self.data_structure = self.walk(attribute_state, '_dtype')
        self.default_value = self.walk(attribute_state, 'defaultValue')
        self.min_value = self.walk(attribute_state, 'minValue')
        self.max_value = self.walk(attribute_state, 'maxValue')
    
class   COSEM:
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
            Att = AttributeTree(att)
            self.attributes.append(deepcopy(Att))

        # Render Method
        for mtd in method_list:
            Mtd = AttributeTree(mtd)
            self.methods.append(deepcopy(Mtd))

def get_cosem_list(projectname, version):
    cosem_list = requests.get(f'{BACKEND_API}/project/getcosemlist/{projectname}/{version}')
    return cosem_list.json()

def fetch_cosem(projectname, version):
    logger.info('Fetch all cosem data')
    cosem_list = get_cosem_list(PROJECT_NAME, VERSION)    
    cosem_list_out = []
    
    # Iterate cosem 
    for cosem in cosem_list:
        cosem_data = requests.get(f'{BACKEND_API}/project/get/{projectname}/{version}/{cosem}').json()
        object = COSEM(cosem_data)
        for att in object.attributes:
            print(att.data_structure)
            print(att.default_value)
            print(att.min_value)
            print(att.max_value)
        break

    return cosem_list_out
        

fetch_cosem(PROJECT_NAME, VERSION)