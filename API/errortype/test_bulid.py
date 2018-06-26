# --*-- coding: utf8 --*--

import unittest
import requests

from units.config import Config, Data_API_File
from units.file_reader import Excel_Reader
from units.log import Logger


class test_error_bulid(unittest.TestCase):

    # get URL
    url = Config().get('URL')
    errortype = Config().get('errortype')
    build_value = errortype.get('build')
    delete_value = errortype.get('delete')
    list_value = errortype.get('list')
    modify_value = errortype.get('modify')
    errortype_build_url = url + build_value
    errortype_delete_url = url + delete_value
    errortype_list_url = url + list_value
    errortype_modify_url = url + modify_value

    # get log object
    log = Logger().get_logger()

    # get API Data
    data_dict = Excel_Reader(Data_API_File, "errortype").data
    build_name_null = data_dict.get('build_name_null')[0]
    build_name = data_dict.get('build_name')[0]
    build_name_disable = data_dict.get('build_name_disable')[0]
    modify_all_null = data_dict.get('modify_all_null')[0]
    list_all_null = data_dict.get('list_all_null')
    delete_code_null = data_dict.get('delete_code_null')

    # class params
    errortype_code = None
    errortype_name = None
    modify_errortype_name = "keyboard broken"

    @classmethod
    def setUpClass(cls):
        pass

    def test_001_build_errortype_null(self):
        data = eval(self.build_name_null)
        res = requests.post(self.errortype_build_url, data= data)
        result = res.json()
        # write to log
        self.log.info(data)
        self.log.info(result)
        self.assertEqual(result['info'], 'Parameter is empty')

    def test_002_build_errortype_success(self):
        data = eval(self.build_name)
        res = requests.post(self.errortype_build_url, data= data)
        result = res.json()
        # write to log
        self.log.info(data)
        self.log.info(result)
        test_error_bulid.errortype_code = result['data']['code']
        test_error_bulid.errortype_name = result['data']['name']
        self.assertEqual(result['info'], u'创建Errortype成功')

    def test_003_build_errortype_failure_repeat(self):
        data = eval(self.build_name)
        res = requests.post(self.errortype_build_url, data= data)
        result = res.json()
        # write to log
        self.log.info(data)
        self.log.info(result)
        self.assertEqual(result['info'], u'创建Errortype不成功,name已存在')

    # def test_004_build_errortype_success(self):
    #
    #     data = json.loads()
    #     res = requests.post(
    #         self.errortype_build_url, data={
    #             "name": self.init_errortype})
    #     result = res.json()
    #     self.init_errortype_id = result['data']['id']
    #     self.init_errortype_code = result['data']['code']
    #     self.assertEqual(result['data']['name'], 'error operate')
    #     self.assertEqual(result['info'], u'创建Errortype成功')
    #
    def test_101_errortype_modify_all_null(self):
        data = {"id": "", "code": "", "name": "", "state": ""}
        res = requests.put(self.errortype_modify_url, data=data)
        result = res.json()
        self.assertEqual(result["code"], "9999")

    def test_102_errortype_modify_code_notexist(self):
        data = {"code": self.error_type_01_code, "name": self.errortype_name, "state": "enable"}
        res = requests.put(self.errortype_modify_url, data=data)
        result = res.json()
        self.assertEqual(result["code"], '9999')

    def test_103_errortype_modify_code_exist(self):
        data = {"code": self.errortype_code, "name": self.modify_errortype_name, "state": "enable"}
        res = requests.put(self.errortype_modify_url, data=data)
        result = res.json()
        self.assertEqual(result['info'], u'修改Errortype成功')
        self.assertEqual(result['data']['name'], self.modify_errortype)


    def test_104_errortype_modify_state_disable(self):
        data = {"code": self.errortype_code, "name": self.modify_errortype_name, "state": "disable"}
        res = requests.put(self.errortype_modify_url, data=data)
        result = res.json()
        self.assertEqual(result['data']['state'], u'Disable')
        self.assertEqual(result['info'], u'修改Errortype成功')

    def test_201_errortype_list_all_null(self):
        data = {"code": "", "name": "", "state": ""}
        res = requests.get(self.errortype_list_url, params=data)
        result = res.json()
        errortype_dict = result['voList']
        self.assertTrue(len(errortype_dict) > 1)

    def test_202_errortype_list_name_not_exist(self):
        data = {"code": "", "name": "error operate not exist", "state": ""}
        res = requests.get(self.errortype_list_url, params=data)
        result = res.json()
        self.assertEqual(len(result['voList']), 0)

    def test_203_errortype_list_name_exist(self):
        data = {"code": self.errortype_code, "name": self.modify_errortype_name, "state": "disable"}
        res = requests.get(self.errortype_list_url, params=data)
        result = res.json()
        errortype_dict = result['voList'][0]
        self.errorcode = errortype_dict['code']
        self.assertEqual(errortype_dict['name'], self.modify_errortype_name)
    #
    # def test_204_errortype_list_code_not_exist(self):
    #     res = requests.get(
    #         self.errortype_list_url,
    #         params={
    #             "code": self.errorcode +
    #             '01010',
    #             "name": '',
    #             "state": ''})
    #     result = res.json()
    #     self.assertEqual(len(result['voList']), 0)
    #
    # def test_205_errortype_list_code_exist(self):
    #     res = requests.get(
    #         self.errortype_list_url,
    #         params={
    #             "code": self.errorcode,
    #             "name": '',
    #             "state": ''})
    #     result = res.json()
    #     errortype_dict = result['voList'][0]
    #     self.assertEqual(errortype_dict['code'], self.errorcode)
    #
    # def test_206_errortype_list_state_enable(self):
    #     res = requests.get(
    #         self.errortype_list_url,
    #         params={
    #             "code": '',
    #             "name": '',
    #             "state": 'enable'})
    #     test_result = False
    #     result = res.json()
    #     errortype_dict = result['voList']
    #
    #     # 判断errorcode是否存在
    #     for dict in errortype_dict:
    #         if self.errorcode == dict['code']:
    #             test_result = True
    #             return test_result
    #
    #     self.assertTrue(test_result)
    #
    # def test_207_errortype_list_state_disable(self):
    #     res = requests.get(
    #         self.errortype_list_url,
    #         params={
    #             "code": '',
    #             "name": '',
    #             "state": 'Disable'})
    #     test_result = False
    #     result = res.json()
    #     errortype_dict = result['voList']
    #
    #     # 判断errorcode是否存在
    #     for dict in errortype_dict:
    #         if self.modify_errortype == dict['name']:
    #             test_result = True
    #             return test_result
    #
    #     self.assertTrue(test_result)
    #
    # def test_301_errortype_delete_null(self):
    #     res = requests.delete(self.errortype_delete_url, data={"code": ''})
    #     result = res.json()
    #     self.assertEqual(result['info'], u'操作失败')
    #
    # def test_302_errortype_delete_code_not_exist(self):
    #
    #     data = {"code": self.errortype_code}
    #     res = requests.delete(self.errortype_delete_url, data=data)
    #     result = res.json()
    #     self.assertEqual(result['info'], u'删除Errortype不成功')
    #
    def test_303_errortype_delete_code_success(self):
        data = {"code": self.errortype_code}
        res = requests.delete(self.errortype_delete_url, params= data)
        result = res.json()
        self.assertEqual(result['info'], u'删除Errortype成功')
    #
    # def test_304_errortype_delete_code_success(self):
    #     res = requests.delete(
    #         self.errortype_delete_url, data={
    #             "code": self.error_type_01_code})
    #     result = res.json()
    #     self.assertEqual(result['info'], u'删除Errortype成功')

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
