import os
import pathlib

CURRENT_PATH = pathlib.Path(__file__).parent.absolute()

MIN_SYSTEM = {
    'directories': [
        f'{CURRENT_PATH}/appdata',
        f'{CURRENT_PATH}/constant',
        f'{CURRENT_PATH}/logdata',
    ]
}


# make system directories
print('Create directories if not exist')
for dir_path in MIN_SYSTEM['directories']:
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        print(f'Create {dir_path}')
        continue
print('Directories creation -- Done')