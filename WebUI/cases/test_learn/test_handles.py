# --*-- coding:utf8 --*--


import sys
sys.path.append(r"D:\Richard\python\unit_test")

from WebUI.common.BasePage import BasePage
from units.config import Data_UI_File
from units.file_reader import Excel_Reader


elements = Excel_Reader(Data_UI_File, 'login').data
value_loc = elements["value_loc"]
submit_loc = elements["submit_loc"]
result_loc = elements["result_loc"]
area_loc = elements["area_loc"]
result2_loc = elements["result2_loc"]
move_loc = elements["move_loc"]

search_tool = elements["search_tool"]
search_time = elements["search_time"]
time_loc = elements["time_loc"]

page = BasePage()
page.get("https://www.baidu.com")
page.send_values(value_loc, "天气")
page.click(submit_loc)
assign_window = page.get_current_page()
page.click(result_loc)
page.switch_window()
print(page.get_text(area_loc))
page.close()
page.switch_assign_handle(assign_window)
page.get_current_page()
page.click(result2_loc)
page.switch_window()
page.mouse_move(move_loc)
page.close()
page.switch_assign_handle(assign_window)



# page.click(result2_loc)
# page.switch_window()
# page.mouse_move(move_loc)
# page.close()
# page.switch_assign_handle(assign_window)


page.set_sleep_time(10)
page.click(search_tool)
page.click(time_loc)
page.click(search_time)
page.set_sleep_time(5)
page.quit()
