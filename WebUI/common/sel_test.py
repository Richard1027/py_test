from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image

driver = webdriver.Chrome(r"D:\Richard\python\py_test\drivers\chromedriver.exe")
driver.get("https://www.baidu.com")
time.sleep(1)
#driver.find_element_by_id("kw").send_keys("tianqi")
time.sleep(1)
driver.maximize_window()
time.sleep(1)
element1 = driver.find_element_by_xpath("//div[@class='head_wrapper']")
print(element1.location)
print(element1.size)
time.sleep(2)
driver.save_screenshot("button.png")
#driver.fullscreen_window()
time.sleep(1)

element = driver.find_element_by_xpath("//div[@id='lg']/img[1]")
time.sleep(2)
print(element.location)
print(element.size)
left = element.location['x']
top = element.location['y']
right = left + element.size['width']
bottom = top + element.size['height']
# left = 1040
# top = 260
# right = 270 + 1187
# bottom = 129 + 320
print(left, top, right, bottom)

im = Image.open("button.png")
print(im.size)
# im2 = Image.open("test.png")
# im2.paste(im, "11.png", (left, top, right, bottom))
# im2.save("button.png")
im = im.crop((left, top, right, bottom))
im.show()
im.save("button.png")
driver.quit()