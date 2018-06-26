# --*-- coding:utf8 --*--

from WebUI.common.BasePage import BasePage
from units.file_reader import Excel_Reader
from units.config import Config, Base_Path
import os, time

class open(BasePage):

    url = 'https://www.baidu.com'
    excel_file = os.path.join(Base_Path, 'data', 'UIelements.xlsx')
    test_elements = Excel_Reader(excel_file, 'login').data
    value_loc = test_elements['value_loc']
    submit_loc = test_elements['submit_loc']

    def open(self):
        self._open(self.url)

    def search_value(self, value="天气"):
        self.find_element(self.value_loc).send_keys(value)

    def submit_button(self):
        self.find_element(self.value_loc).click()