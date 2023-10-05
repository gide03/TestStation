'''
    This script adapted to control test station. 
    Please refer test station scematic documents on docs.
'''

import pathlib
import json
import site

CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
ROOT_DIRECTORY = CURRENT_PATH.parent
site.addsitedir(ROOT_DIRECTORY)

from lib.Advantech.advantech_helper import InstantDigitalIO
from lib.DLMS_Client.DlmsCosemClient import DlmsCosemClient


with open(f'{ROOT_DIRECTORY}/constant/station_configuration.json', 'r') as f:
    configuration = json.load(f)

# Define advantech hardwares
advantech_4704 = InstantDigitalIO(
    deviceDescription = configuration['Advantech']['USB_4704']['deviceDescription'],
    profilePath = configuration['Advantech']['USB_4704']['profilePath'],
    startPort = configuration['Advantech']['USB_4704']['startPort'],
    portCount = configuration['Advantech']['USB_4704']['portCount']
)
advantech_4761 = InstantDigitalIO(
    deviceDescription = configuration['Advantech']['USB_4704']['deviceDescription'],
    profilePath = configuration['Advantech']['USB_4761']['profilePath'],
    startPort = configuration['Advantech']['USB_4761']['startPort'],
    portCount = configuration['Advantech']['USB_4761']['portCount']
)

'''
    This example will use communication probe such as RS232, RS485, and Optical
'''
import serial
from time import perf_counter

METER_BOOT_TIME = 50

advantech_4704.setAdvInstantDO(0x1) # Toggle D0 to HIGH to supply meter
advantech_4761.setAdvInstantDO(0x4) # Toggle D3 to HIGH to supply 12V iso to serial IC
optical_client = DlmsCosemClient(
   port = configuration['FW_download']['CommunicationPorts']['OPTICAL'],
   baudrate = 9600,
   parity = serial.PARITY_NONE,
   bytesize = serial.EIGHTBITS,
   stopbits = serial.STOPBITS_ONE,
   timeout = 0.1,
   inactivity_timeout = 60,
   login_retry = 3,
   meter_addr = 16,
   client_nb = 16
)

rs232_client = DlmsCosemClient(
    port = configuration['FW_download']['CommunicationPorts']['RS232'],
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    bytesize = serial.EIGHTBITS,
    stopbits = serial.STOPBITS_ONE,
    timeout = 0.1,
    inactivity_timeout = 60,
    login_retry = 3,
    meter_addr = 16,
    client_nb = 16
)

rs485_client = DlmsCosemClient(
    port = configuration['FW_download']['CommunicationPorts']['RS485'],
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    bytesize = serial.EIGHTBITS,
    stopbits = serial.STOPBITS_ONE,
    timeout = 0.1,
    inactivity_timeout = 60,
    login_retry = 3,
    meter_addr = 16,
    client_nb = 16
)

t = perf_counter()
while perf_counter() - t < METER_BOOT_TIME:
    print(f'Wait meter for booting {perf_counter() - t:.2f}/{METER_BOOT_TIME:.2f}s',end='\r')
print()

print('Login OPTICAL')
login_result = optical_client.client_login_optic()
print(f'Login result: {login_result}')
datetime = optical_client.get_cosem_data(8, '0;0;1;0;0;255', 2) # read clock NOTE: firmware using INAT2
print(f'Datetime: {datetime}')
optical_client.client_logout

print('Login RS232')
login_result = rs232_client.client_login()
print(f'Login result: {login_result}')
datetime = rs232_client.get_cosem_data(8, '0;0;1;0;0;255', 2) # read clock NOTE: firmware using INAT2
print(f'Datetime: {datetime}')
rs232_client.client_logout

# DEVICE NOT READY
    # print('Login RS485') 
    # login_result = rs485_client.client_login()
    # print(f'Login result: {login_result}')
    # datetime = rs485_client.get_cosem_data(8, '0;0;1;0;0;255', 2)
    # print(f'Datetime: {datetime}')
    # rs485_client.client_logout
# DEVICE NOT READY

advantech_4704.setAdvInstantDO(0x0) # turn of supply
advantech_4761.setAdvInstantDO(0x0) # turn of 12V iso