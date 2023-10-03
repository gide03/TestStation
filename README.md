# TestStation

> This environment is an expansion, and it is designed to adapts with my customized Cosem Management System (CMS) with the mechanical hardware of the test station itself.

Python package for electric metering device test station, DLMS based for RS232/RS485/Optical, using NAVDAQ data acuisition hardware.

The packages will connect us to main develoopment frameworks, it will make us develop test scripts faster by reducing repeatition task. For the advance purpose, this project will used in pipeline for Continuous Integration process. 

## How to working with this framework
> This project designed to run in fresh device (tested on Windows). Thus, after you clone/fork this project, you need to configure the environment first.
1. Install python
2. Create virtual environment `python -m venv <environment name>`
3. Enter the virtual environment, then install package requirements `pip install -r requirements.txt`
4. Run initialization `python project_init.py`, This python script will add folders that will be used by the frame work. (It is ignored by git)
5. Done!!. You can run the example on test station.

Tips: You could make this project as a pakcage for your testing agent
