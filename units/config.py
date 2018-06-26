# --*-- coding:utf-8 --*--

import os
from units.file_reader import Yaml_Reader


print(os.path.dirname(__file__))
Base_Path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
Config_API_File = os.path.join(Base_Path, 'Config', 'config_api')
Config_UI_File = os.path.join(Base_Path, 'Config', 'config_ui')
Data_API_File = os.path.join(Base_Path, 'data', 'Interface.xlsx')
Data_UI_File = os.path.join(Base_Path, 'data', 'UIelements.xlsx')
Driver_Path = os.path.join(Base_Path, 'drivers')
Log_Path = os.path.join(Base_Path, 'log')
Report_Path = os.path.join(Base_Path, 'report')
Pictures_Path = os.path.join(Base_Path, 'pictures')
API_PATH = os.path.join(Base_Path, 'API')


class Config:

    def __init__(self, config=Config_API_File):
        self.config = Yaml_Reader(config).data

    def get(self, element, index=0):
        return self.config[index].get(element)
