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

from lib.Advantech.Automation.BDaq import *
from lib.Advantech.Automation.BDaq.InstantDoCtrl import InstantDoCtrl
from lib.Advantech.Automation.BDaq.InstantDiCtrl import InstantDiCtrl
from lib.Advantech.Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed

# Advantech Digital Output Pinout
class Adv_Pin_DO:
    DO_0 = 0x00
    DO_1 = 0x01
    DO_2 = 0x02
    DO_3 = 0x03
    DO_4 = 0x04
    DO_5 = 0x05
    DO_6 = 0x06
    DO_7 = 0x07

# Instant access digital Input Output
class InstantDigitalIO:
    def __init__(self, configuration:dict) -> None:
        '''
            @brief 
                This class used for accessing instant Input/Output 
            
            @param configuration {dict} 
                Advantech USB-xxxx configuration that contains key-value of:
                "deviceDescription" : "USB-4704,BID#0",
                "profilePath" : <path of profile xml>,
                "startPort" : <int: start point of advantech port>,
                "portCount" : <int: number of device available>
        '''
        self.deviceDescription = configuration['deviceDescription']
        self.profilePath = configuration['profilePath']
        self.startPort = configuration['startPort']
        self.portCount = configuration['portCount']
        
        self.instantDoCtrl = InstantDoCtrl(self.deviceDescription)
        self.instantDiCtrl = InstantDiCtrl(self.deviceDescription)
        self.registerValue = 0x00

    # def __del__(self):
    #     self.instantDoCtrl.dispose()
    #     self.instantDiCtrl.dispose()
    
    def resetDO(self):
        self.AdvInstantDO()
    
    def AdvInstantDO(self, value:int=0x00):
        '''
            Function to execute value
            param:
                value is 8-bit
        '''
        ret = ErrorCode.Success

        # Step 1: Create a instantDoCtrl for DO function.
        # Select a device by device number or device description and specify the access mode.
        # In this example we use ModeWrite mode so that we can fully control the device,
        # including configuring, sampling, etc.
        for _ in range(1):
            self.instantDoCtrl.loadProfile = self.profilePath

            # Step 2: Write DO ports
            dataBuffer = [0] * self.portCount
            for i in range(self.startPort, self.portCount + self.startPort):
                inputVal = value
                dataBuffer[i-self.startPort] = inputVal

            ret = self.instantDoCtrl.writeAny(self.startPort, self.portCount, dataBuffer)
            if BioFailed(ret):
                return 1

        # Step 3: Close device and release any allocated resource. Move to instance delete
        # self.instantDoCtrl.dispose()

        # If something wrong in this execution, print the error code on screen for tracking.
        if BioFailed(ret):
            enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
            print("Some error occurred. And the last error code is %#x. [%s]" % (ret.value, enumStr))
        return 0

    def AdvInstantDI(self):
        ret = ErrorCode.Success

        # Step 1: Create a 'InstantDiCtrl' for DI function.
        # Select a device by device number or device description and specify the access mode.
        # In this example we use ModeWrite mode so that we can fully control the device,
        # including configuring, sampling, etc.
        instantDiCtrl = InstantDiCtrl(self.deviceDescription)
        for _ in range(1):
            instantDiCtrl.loadProfile = self.profilePath

            # Step 2: Read DI ports' status and show.
            # print("Reading ports status is in progress, any key to quit!")
            ret, data = instantDiCtrl.readAny(self.startPort, self.portCount)
            if BioFailed(ret):
                break

            return data

        # If something wrong in this execution, print the error code on screen for tracking.
        if BioFailed(ret):
            enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
            print("Some error occurred. And the last error code is %#x. [%s]" % (ret.value, enumStr))
        return 0

# Example begin
'''
    Running relay :)
    
    This script will shift bit from 0 to 7 and apply the state to the relay 
'''
from time import sleep

with open(f'{ROOT_DIRECTORY}/constant/station_configuration.json', 'r') as f:
    configuration = json.load(f)
    configuration = configuration['Advantech']['USB_4704'] # I am using Advantech USB-USB_4704
adv = InstantDigitalIO(configuration) 
state = 1
for i in range(0,8):
    adv.AdvInstantDO(state)
    state = state << 1
    sleep(2)
adv.AdvInstantDO(0)
    