import json
import pathlib
import subprocess
import zipfile
import os
from time import sleep, perf_counter

def download_fw(advantech, image_directory):
    advantech.AdvInstantDO(0)
    # extract image
    print('[extract image] Scan for image')
    image_path = image_directory + os.listdir(image_directory)[-1]
    with zipfile.ZipFile(image_path, 'r') as zip_ref:
        # Extract all the contents to the specified directory
        print('[extract image] Extracting image')
        zip_ref.extractall(image_directory)
        print('[extract image] Extract file completed')


    # Detecting DFU devices
    # Power up USB
    print('Power up board to DFU mode')
    advantech.AdvInstantDO(0x40)
    sleep(1)
    try:
        shell_output = subprocess.run(["STM32_Programmer_CLI", '-l'], shell=True, stdout=subprocess.PIPE, text=True)
    except:
        pass

    # Detecting DFU devices
    num_of_DFU_device = 0
    usb_address = None
    if 'No STM32 device in DFU mode connected' in shell_output.stdout:
        print('No device detected')
        exit(1)
    lines = shell_output.stdout.splitlines()
    for line in lines:
        if 'Total number of available STM32 device in DFU mode' in line:
            num_of_DFU_device = int(line.split(' ')[-1])
            continue
        if 'USB Address Number' in line:
            usb_address = int(line.split(':')[-1])
            continue
    if usb_address == None:
        print('TEST ABORTED, NO DFU FOUND')
        exit(1)

    # execute flash script
    print(f'DFU device found at address: {usb_address}')
    sleep(2)
    batch_file_path = image_path.replace('.zip','')
    t_download_start = perf_counter()
    command = ['powershell.exe', f"./02-fw_download.ps1 {usb_address} VT"]
    print(f'[execute_script] start execute script at: {t_download_start}')
    try:
        # sleep(5)
        shell_output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True, cwd=batch_file_path)
    except:
        pass
    print(shell_output.stdout)
    t_download_finish = perf_counter()
    print(f'Download firmware finish. Time est: {(t_download_finish-t_download_start):.3f}ms')
    advantech.AdvInstantDO(0)


def start_download():
    import site
    import zipfile
    CURRENT_DIR = pathlib.Path(__file__).parent.absolute()
    ROOT_DIR = CURRENT_DIR.parent
    site.addsitedir(ROOT_DIR)
    
    from lib.Advantech.advantech_helper import InstantDigitalIO
    
    with open(f'{ROOT_DIR}/constant/station_configuration.json','r') as f:
        m_config = json.load(f)
        
        advantech_configuration = m_config['Advantech']
        deviceDescription = advantech_configuration['USB_4704']['deviceDescription']
        profilePath = advantech_configuration['USB_4704']['profilePath']
        startPort = advantech_configuration['USB_4704']['startPort']
        portCount = advantech_configuration['USB_4704']['portCount']
        
        fw_images_path = m_config['FW_download']['FirmwareImagesPath']
    
    advantech = InstantDigitalIO(deviceDescription, f'{profilePath}', startPort, portCount)
    
    FW_IMAGE_DIR = f'{ROOT_DIR}/{fw_images_path}'
    print(f'Scan for firmware image at {FW_IMAGE_DIR}')
    if not os.path.exists(FW_IMAGE_DIR):
        os.mkdir(FW_IMAGE_DIR)
        print('')
        
    image_list = os.listdir(FW_IMAGE_DIR)
    for idx, img in enumerate(image_list):
        if ".zip" in img:
            continue
        else:
            image_list.pop(idx)
    
    # Protection if multiple image found in images directory
    if len(image_list)>1:
        print('Found some images')
        for img_name in image_list:
            print(img_name)
        exit(f'System terminated. Make sure only an image stored in {fw_images_path}')
    
    # Unzip selected image
    selected_image = image_list[0]
    print(f'Found image will be install: {selected_image}')
    with zipfile.ZipFile(f'{FW_IMAGE_DIR}/{selected_image}', 'r') as zip_ref:
        # Extract all the contents to the specified directory
        print('[extract image] Extracting image')
        zip_ref.extractall(FW_IMAGE_DIR)
        print('[extract image] Extract file completed')
    
    # DFU device detection
    print('Power up board with USB (USB-4704 D6 HIGH)')
    advantech.InstantDO( 1<<6 ) # turn on D6 (download firmware)
    
    sleep(3) # give a chace for computer to detect DFU
    try:
        shell_output = subprocess.run(["STM32_Programmer_CLI", '-l'], shell=True, stdout=subprocess.PIPE, text=True)
    except:
        pass
    
    # Detecting DFU devices
    num_of_DFU_device = 0
    usb_address = None
    if 'No STM32 device in DFU mode connected' in shell_output.stdout:
        print('No device detected')
        exit(1)
    lines = shell_output.stdout.splitlines()
    for line in lines:
        if 'Total number of available STM32 device in DFU mode' in line:
            num_of_DFU_device = int(line.split(' ')[-1])
            continue
        if 'USB Address Number' in line:
            usb_address = int(line.split(':')[-1])
            continue
    if usb_address == None:
        print('TEST ABORTED, NO DFU FOUND')
        exit(1)
    print(f'DFU device found at address: {usb_address}')
    
    # Download FW
    batch_file_dir = selected_image.replace('.zip','')    
    t_download_start = perf_counter()
    command = ['powershell.exe', f"./02-fw_download.ps1 {usb_address} VT"]
    print(f'[execute_script] start execute script at: {t_download_start}')
    try:
        shell_output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True, cwd=f'{FW_IMAGE_DIR}/{batch_file_dir}')
    except:
        pass
    print(shell_output.stdout)
    t_download_finish = perf_counter()
    print(f'Download firmware finish. Time est: {(t_download_finish-t_download_start):.3f}ms')
    
    # DONE. Turn off board
    print('Power down board')
    advantech.InstantDO( 0 ) # turn on D6 (download firmware)
