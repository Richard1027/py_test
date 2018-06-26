# --*-- coding:utf8 --*--

import unittest
from units.file_reader import Excel_Reader
from units.config import Config, Base_Path
import os,sys, time
sys.path.append(os.getcwd())
from WebUI.cases.test_learn.open_baidu import open
from WebUI.common.BasePage import BasePage



class Test_baidu(unittest.TestCase):

    url = 'https://www.baidu.com'
    excel_file = os.path.join(Base_Path, 'data', 'UIelements.xlsx')
    test_elements = Excel_Reader(excel_file, 'login').data
    value_loc = test_elements['value_loc']
    submit_loc = test_elements['submit_loc']
    result_loc = test_elements['result_loc']
    tianqi_loc = test_elements['tianqi_loc']
    today_loc = test_elements['today_value']
    page = open().get(url)



    @classmethod
    def setUpClass(self):
        self.page.search_value()

    def test_01(self):
        self.page.find_element(self.today_loc).click()
        title = self.page.find_element(('css'))
        time.sleep(2)
        self.page.find_element(self.result_loc).click()

    def test_02(self):
        self.page.switch_window()
        self.page.find_element(self.tianqi_loc).click()

    @classmethod
    def tearDownClass(cls):
        cls.page.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)