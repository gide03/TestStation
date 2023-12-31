import requests
import logging
import pathlib
from copy import deepcopy

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()
PROJECT_DIR = CURRENT_DIR.parent.parent
LOG_DATA_DIR = f'{PROJECT_DIR}/logdata'
APP_DATA_DIR = f'{PROJECT_DIR}/appdata'

BACKEND_API = 'http://10.23.40.185/api'

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
logger.setLevel(LEVEL['INFO'])
# Create file handler
file_handler = logging.FileHandler(f'{LOG_DATA_DIR}/lib_CosemObject.log')
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
        self.id = node_ui_state['id']
        logger.debug(f'[AttributeTree::init] Generating node id-{self.id}')
        self.data_structure = None
        self.enumerated_data_structure = None
        self.default_value = None
        self.min_value = None
        self.max_value = None
        self.association  = None
        
        self.render(node_ui_state)
        
    def get_dtype_enum(self, dtype:str)-> int:
        '''
            Get enumerator standard blue book
        '''
        dtype_enum = {
            None:None,
            "NullDTO":0,
            "BooleanDTO":3,
            "BitStringDTO":4,
            "Integer32DTO":5, 
            "Unsigned32DTO": 6,
            "OctetStringDTO":9, 
            "VisibleStringDTO":10,
            "utf8-string":12,
            "bcd":13,
            "Integer8DTO":15,
            "Integer16DTO":16,
            "Unsigned8DTO":17,
            "Unsigned16DTO":18, 
            "Integer64DTO":24,
            "Unsigned64DTO":21, 
            "EnumeratedDTO":22, 
            "Float32DTO":23,
            "Float64DTO":24,
            "DateTime":25,
            "Date":26,
            "Time":27,
            "Array":1,
            "Structure":2,
        }
        if dtype == None:
            return None
        if 'Array' in dtype:
            return 1
        return dtype_enum[dtype]
            
    def flatten_attribute(self, data):
        '''
            
        '''
        def flatten(value_list):
            '''
                Remove dict
            '''
            output = []
            for element in value_list:
                if type(element) == dict:
                    key = list(element.keys())[0]
                    temp = []
                    temp.append(key)
                    temp.extend(flatten(element[key]))
                    output.extend(temp)
                    continue
                output.append(element)
            return output
                
        return [flatten([i]) for i in data]
        
    def extract_value(self, node, key):
        '''
            Walk the structure of attribute/method node.
            Refer to backend documentation
        '''
        dtype = node['_dtype']
        output = node[key]
        if dtype == 'Choice':
            logger.debug(f'[AttributeTree::extract_value] Get choice data type. Get the first child')
            output = self.extract_value(node["children"][0], key)
        
        elif "Array" in dtype and key == '_dtype':
            _key = f'{dtype}-{node["minValue"]}-{node["maxValue"]}'
            output = {_key: [self.extract_value(node['arrayTemplate'], key)]}
            
        elif "Structure" in dtype: # for structure
            output = {}
            output[dtype] = []
            temp = []
            for child in node['children']:
                temp.append(self.extract_value(child, key))
            output[dtype] = temp
        elif "Array" in dtype: # for array
            output = {}
            _key = f'{dtype}-{node["minValue"]}-{node["maxValue"]}'
            output[_key] = []
            temp = []
            for child in node['children']:
                temp.append(self.extract_value(child, key))
            output[_key] = temp
        return output
    
    def render(self, attribute_state):
        '''
            Render attribute_state to object
        '''
        if attribute_state == None: # for some case an attribute is None, which is the attribute is not used
            return None
        
        self.id = attribute_state['id']
        self.data_structure = self.extract_value(attribute_state, '_dtype')
        self.default_value = self.extract_value(attribute_state, 'defaultValue')
        self.min_value = self.extract_value(attribute_state, 'minValue')
        self.max_value = self.extract_value(attribute_state, 'maxValue')
        
        def transform_data_structure(data):
            if type(data) == list:
                output = []
                for value in data:
                    result = transform_data_structure(value)
                    output.append(result)
                return output
                
            elif type(data) == dict:
                output = {}
                _key = list(data.keys())[0]
                _enumerate_key = self.get_dtype_enum("Array" if "Array" in _key else _key)
                output[_enumerate_key] = []
                for value in data[_key]:
                    result = transform_data_structure(value)
                    output[_enumerate_key].append(result)
                return output
            
            output = self.get_dtype_enum(data)
            return output
        self.enumerated_data_structure = transform_data_structure(self.data_structure)
    
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
        
    def flatten_attribute(self, data):
        '''
            Flatten attribute tree
        '''
        if type(data) == dict:
            _key = list(data.keys())[0]
            output = [_key]
            output.extend(self.flatten_attribute(data[_key]))
            
            while True:
                test = [type(i) for i in output]
                if list in test:
                    output = self.flatten_attribute(output)
                else:
                    break
            return output
        elif type(data) == list:
            output = []
            for value in data:
                if type(value) != list:
                    output.append(self.flatten_attribute(value))
                else:
                    output.extend(self.flatten_attribute(value))
            return output
        return data
            
    def render(self, data):
        '''
            Render data from UI state format
        '''
        self.object_name = data['objectName']
        self.logical_name = data['logicalName']
        
        attribute_list = data['attribute']
        method_list = data['method']
        # Render Attribute
        logger.debug('[COSEM:render] rendering attributes')
        for att in attribute_list:
            if att != None:
                Att = AttributeTree(att)
            else:
                Att = None
            self.attributes.append(deepcopy(Att))

        # Render Method
        logger.debug('[COSEM:render] rendering methods')
        for mtd in method_list:
            if mtd != None:
                Mtd = AttributeTree(mtd)
            else:
                Mtd = None
            self.methods.append(deepcopy(Mtd))

class CosemWrapper:
    def __init__(self, projectname, version):
        '''
            Generate wrapper that wrap cosem objects based on project name and version
            @param - projectname {str} the project will be used
            @param - version {str} the version of database inside the project
        '''
        self.projectname = projectname
        self.version = version
        self.cosem_list = self.fetch_cosem()
    
    def get_cosem_list(self):
        '''
            GET cosem list inside database
        '''
        cosem_list = requests.get(f'{BACKEND_API}/project/getcosemlist/{self.projectname}/{self.version}')
        return cosem_list.json()

    def fetch_cosem(self):
        '''
            Based on project name and version, it will fetch cosem object inside a file or fetch from server. If the file doen't exist, the file will genereate after fetching data.
        '''
        import os
        import pickle
        filename = f'objectlist_{self.projectname}_{self.version}'
        if filename in os.listdir(APP_DATA_DIR): # LOAD COSEM_PROJECT
            logger.info(f'[CosemWrapper::fetch_cosem] FOUND COSEM list file: {filename}!!')
            with open(f'{APP_DATA_DIR}/{filename}', 'rb') as f:
                logger.info(f'[CosemWrapper::fetch_cosem] loading file')
                cosem_list_out = pickle.load(f)
                return cosem_list_out
        
        # else:  # INITIALIZE COSEM_PROJECT
        logger.info('[CosemWrapper::fetch_cosem] First synchronize, fetch all cosem data')
        cosem_list = self.get_cosem_list()    
        cosem_list_out = []
        
        # Iterate cosem 
        for cosem in cosem_list:
            logger.debug(f'[fetch_cosem] fetching {cosem}')
            cosem_data = requests.get(f'{BACKEND_API}/project/get/{self.projectname}/{self.version}/{cosem}').json()
            object = COSEM(cosem_data)
            cosem_list_out.append(object)
                
        logger.info(f'[CosemWrapper::fetch_cosem] Store cosem list in {APP_DATA_DIR}/{filename}')
        with open(f'{APP_DATA_DIR}/{filename}', 'wb') as f:
            pickle.dump(cosem_list_out, f)        
        return cosem_list_out

# EXAMPLE
# PROJECT_NAME = 'RUBY'
# VERSION = '0.04_20230922'
# cosemWrapper = CosemWrapper(PROJECT_NAME, VERSION)
