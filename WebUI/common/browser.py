# --*-- coding: utf8 --*--

import os, time
from selenium import webdriver

from units.config import Config, Config_UI_File, Driver_Path


# get web types
web_types = {'chrome': webdriver.Chrome, 'firefox': webdriver.Firefox}

# get webdriver for Chrome
Chromdriver = os.path.join(Driver_Path, 'chromedriver.exe')

# set webdriver execute path
Executeable_path = {'chrome': Chromdriver}


class UnsupportBrowserTypeError(Exception):
    pass


class Browser:

    def __init__(self, web_type='Chrome'):
        self._type = web_type.lower()
        if self._type in web_types:
            self.browser = web_types[self._type]
        else:
            raise UnsupportBrowserTypeError('only support %s !' % ','.join(web_types.keys()))

        self.driver = None

    def get(self, url, maximize_window=True, implicitly_wait=10):
        self.driver = self.browser(executable_path=Executeable_path[self._type])
        self.driver.get(url)
        if maximize_window:
            self.driver.maximize_window()
        self.driver.implicitly_wait(implicitly_wait)
        return self

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()






