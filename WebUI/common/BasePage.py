# --*-- coding: utf8 --*--

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

# Temporarily add system path
import os
import time
from units.config import Pictures_Path
from units.crack import build_vector
import sys
sys.path.append(os.getcwd())
from .browser import Browser


class BasePage(Browser):

    def __init__(self, page=None, web_type='chrome'):
        if page:
            self.driver = page.driver
        else:
            super(BasePage, self).__init__(web_type=web_type)

    def on_page(self, title):
        return title in self.driver.title

    def _open(self, url, title):
        self.driver.get(url)
        assert self.on_page(title), u'open the page error %s' % url

    def switch_frame(self, loc):
        return self.driver.switch_to.frame(loc)

    def switch_default_frame(self):
        return self.driver.switch_to.default_content()

    def get_current_page(self):
        return self.driver.current_window_handle

    def switch_assign_handle(self, handle):
        self.driver.switch_to.window(handle)

    def switch_window(self):
        handles = self.driver.window_handles
        current_handle_id = handles.index(self.driver.current_window_handle)
        switch_handle_id = (current_handle_id + 1) % len(handles)
        self.driver.switch_to.window(handles[switch_handle_id])

    def find_element(self, *loc):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
        except BaseException:
            print(u"%s page can not find %s element" % (self, loc))
        else:
            return self.driver.find_element(*loc)

    def find_elements(self, *loc):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
        except BaseException:
            print(u"%s page can not find %s element" % (self, loc))
        else:
            table_list = self.driver.find_elements(*loc)
            return table_list

    def send_values(self, loc, value, clear_first=True, click_first=True):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
        except BaseException:
            print(u"%s page can not find %s element" % (self, loc))
        else:
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
            self.find_element(*loc).send_keys(value)

    # Mouse Events
    def click(self, loc):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
        except BaseException:
            print(u"%s page can not find %s element" % (self, loc))
        else:
            self.driver.find_element(*loc).click()

    def double_click(self, loc):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
        except NoSuchElementException:
            print(u"%s page can not find %s element" % (self, loc))
        else:
            element = self.driver.find_element(*loc)
            ActionChains(self.driver).double_click(element).perform()

    def context_click(self, loc):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
        except NoSuchElementException:
            print(u"%s page can not find %s element" % (self, loc))
        else:
            element = self.driver.find_element(*loc)
            ActionChains(self.driver).double_click(element).perform()

    def mouse_move(self, loc):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
        except NoSuchElementException:
            print(u"%s page can not find %s element" % (self, loc))
        else:
            element = self.driver.find_element(*loc)
            ActionChains(self.driver).move_to_element(element).perform()

    def mouse_drag(self,loc1, loc2):
        try:
            WebDriverWait(self.driver).until(EC.visibility_of_element_located(loc1))
            WebDriverWait(self.driver).until(EC.visibility_of_element_located(loc2))
        except NoSuchElementException:
            print(u"%s page can not find %s or %s element" % (self, loc1, loc2))
        else:
            element1 = self.find_element(*loc1)
            element2 = self.find_element(*loc2)
            ActionChains(self.driver).drag_and_drop(element1, element2).perform()

    # get_screenshot
    def save_screen_shot(self, name='screen_shot'):
        day = time.strftime("%Y%m%d")
        screen_path = os.path.join(Pictures_Path, day)
        if os.path.exists(screen_path):
            os.makedirs(screen_path)
        day_time = time.strftime("%Y%m%d%H%M%S")
        screen_name = screen_path + day_time + ".png"
        pic_file = os.path.join(Pictures_Path, screen_name)
        st = self.driver.get_screenshot_as_file(pic_file)
        return st

    def web_back(self):
        self.driver.back()

    def web_forward(self):
        self.driver.forward()

    def set_sleep_time(self, second):
        time.sleep(second)

    def get_text(self, loc):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
            element = self.driver.find_element(*loc)
            return element.text
        except NoSuchElementException:
            print(u"%s page can not find %s element" % (self, loc))

    def get_attr(self, loc, attr):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
            atrr_text = self.driver.find_element(*loc).get_attribute(attr)
            return atrr_text
        except NoSuchElementException:
            print(u"%s page can not find %s element" % (self, loc))

    def script(self, script):
        try:
            return self.driver.execute_script(script)
        except JavascriptException:
            print("Execute js failure ： %s" % script)

    def scroll_top_script(self):
        js = "window.scrollTo(0,0)"
        try:
            self.script(js)
        except JavascriptException:
            print("Execute js failure ： %s" % js)

    def scroll_bottom_script(self):
        js = "window.scrollTo(0, document.body.scrollHeight)"
        try:
            self.script(js)
        except JavascriptException:
            print("Execute js failure ： %s" % js)

    # selector

    def select_by_index(self, loc, index):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
            element = self.driver.find_element(*loc)
        except NoSuchElementException:
            print(u"%s page can not find %s element" % (self, loc))
        else:
            try:
                Select(element).select_by_index(index)
            except InvalidSelectorException:
                print("Select index-%d in the element-%s  failed" % (self, index, loc))

    def select_by_attr(self, loc, attr):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
            element = self.driver.find_element(*loc)
        except NoSuchElementException:
            print(u"%s page can not find %s element" % (self, loc))
        else:
            try:
                Select(element).select_by_index(attr)
            except InvalidSelectorException:
                print("Select index-%d in the element-%s  failed" % (self, attr, loc))

    def select_by_text(self, loc, text):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
            element = self.driver.find_element(*loc)
        except NoSuchElementException:
            print(u"%s page can not find %s element" % (self, loc))
        else:
            try:
                Select(element).select_by_index(text)
            except InvalidSelectorException:
                print("Select index-%d in the element-%s  failed" % (self, text, loc))

    # assert text in element
    def asser_text_in_elementvalue(self, loc, attr):
        try:
            result = WebDriverWait(self.driver).until(EC.text_to_be_present_in_element_value(loc),u'{s}'.format(attr))
            return result
        except NoSuchAttributeException:
            print(u"%s page can not find %s element" % (self, loc))

    def asser_text_in_element(self, loc, text):
        try:
            result = WebDriverWait(self.driver).until(EC.text_to_be_present_in_element(loc),u'{s}'.format(text))
            return result
        except NoSuchAttributeException:
            print(u"%s page can not find %s element" % (self, loc))

    # assert element_status
    def get_element_status(self, loc):
        try:
            result = WebDriverWait(self.driver).until(EC.element_located_to_be_selected(loc))
            return result
        except ElementNotSelectableException:
            print(u"%s page can not find %s element" % (self, loc))

    # 获取验证码图片
    def get_crack(self, element, filepath):
        crack = build_vector(filepath, element)
        crack_str = crack.store_letters()
        return crack_str

