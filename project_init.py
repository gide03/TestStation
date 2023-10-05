import os
import pathlib

CURRENT_PATH = pathlib.Path(__file__).parent.absolute()

MIN_SYSTEM = {
    'directories': [
        f'{CURRENT_PATH}/appdata', # general purpose storage for applications
        f'{CURRENT_PATH}/appdata/fw_images', # used by tool/fw_download.py
        f'{CURRENT_PATH}/constant', # used to store all contants
        f'{CURRENT_PATH}/logdata', # used to store files about process log
    ]
}

# CREATE SYSTEM DIRECTORIES
print('Create directories if not exist')
for dir_path in MIN_SYSTEM['directories']:
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        print(f'Create {dir_path}')
        continue
print('Directories creation -- Done')