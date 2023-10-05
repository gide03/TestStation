from .Automation.BDaq import *
from .Automation.BDaq.InstantDoCtrl import InstantDoCtrl
from .Automation.BDaq.InstantDiCtrl import InstantDiCtrl
from .Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed

class InstantDigitalIO:
    def __init__(self, deviceDescription:str, profilePath:str, startPort:int, portCount:int) -> None:
        self.deviceDescription = deviceDescription
        self.profilePath = profilePath
        self.startPort = startPort
        self.portCount = portCount

        self.instantDoCtrl = InstantDoCtrl(deviceDescription)
        self.instantDiCtrl = InstantDiCtrl(deviceDescription)
        self.registerValue = 0x00

    def __del__(self):
        self.instantDoCtrl.dispose()
        self.instantDiCtrl.dispose()
    
    def resetDO(self):
        self.InstantDO()
    
    def InstantDO(self, value:int=0x00):
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

    def InstantDI(self):
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
