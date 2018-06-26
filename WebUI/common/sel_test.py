from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(r"D:\Richard\python\unit_test\drivers\chromedriver.exe")
driver.current_window_handle
driver.get("https://www.baidu.com")
time.sleep(5)
driver.find_element(By.ID, 'kw').send_keys("天气")
driver.find_element(By.ID, 'su').click()
time.sleep(5)
driver.find_element(By.XPATH, "//div[@id='content_left']/div[1]/h3/a").click()
cur_handle = driver.current_window_handle
handles = driver.window_handles
for handle in handles:
    if handle != cur_handle:
        driver.switch_to.window(handle)
time.sleep(5)
# content = driver.find_element(By.XPATH, "//div[@class='crumbs fl']/a[2]").text()
# print(content)
print("1`2312312")
print(driver.current_window_handle)
driver.close()
driver.switch_to.window(cur_handle)
print(driver.current_window_handle)
time.sleep(5)
driver.find_element(By.XPATH, "//div[@id='content_left']/div[1]/h3/a").click()