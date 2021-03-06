# --*-- coding:utf8 --*--

import unittest
import requests
import json

from units.config import Config, Data_API_File
from units.file_reader import Excel_Reader
from units.log import Logger
from units.conn_mysql import Conn_DB


class testRecord_story(unittest.TestCase):

    # get URL List
    URL = Config().get('URL')

    staff_dict = Config().get('staff')
    staff_build_url = URL + staff_dict.get('build')
    staff_delete_url = URL + staff_dict.get('delete')

    errortype_dict = Config().get('errortype')
    errortype_build_url = URL + errortype_dict.get('build')
    errortype_delete_url = URL + errortype_dict.get('delete')

    sample_dict = Config().get('sample')
    sample_build_url = URL + sample_dict.get('build')
    sample_delete_url = URL + sample_dict.get('delete')

    testoption_dict = Config().get('testoption')
    testoption_build_url = URL + testoption_dict.get('build')
    testoption_delete_url = URL + testoption_dict.get('delete')

    testunit_dict = Config().get('testunit')
    testunit_build_url = URL + testunit_dict.get('build')
    testunit_delete_url = URL + testunit_dict.get('delete')

    testrecord_dict = Config().get('testRecord')
    testrecord_build_url = URL + testrecord_dict.get('build')
    testrecord_delete_url = URL + testrecord_dict.get('delete')

    # get test_data
    data_dict = Excel_Reader(Data_API_File, "testrecord_story").data
    staff_data = data_dict.get('staff_build')[0]
    errortype_data = data_dict.get('errortype_build')[0]
    sample_data = data_dict.get('sample_build')[0]
    test_sn = data_dict.get('test_sn')[0]
    options = Config().get("options")

    # get log object
    log = Logger().get_logger()

    # get conn mysql object
    conn = Conn_DB()

    # class params
    jobnumber = None
    staffcode = None
    errortype_code = None
    samplecode = None
    testoption_list = []
    testunit_code = None
    testrecord_list = []

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):

        # delete staff
        res = requests.delete(cls.staff_delete_url, params={"code": cls.staffcode})
        cls.log.debug(res.json())

        # delete errortype
        res = requests.delete(cls.errortype_delete_url, params={"code": cls.errortype_code})
        cls.log.debug(res.json())

        # delete smaple
        res = requests.delete(cls.sample_delete_url, params={"code": cls.samplecode})
        cls.log.debug(res.json())

        # delete testoption
        for code in cls.testoption_list:
            res = requests.delete(cls.testoption_delete_url, params={
                    "sampleCode": cls.samplecode, "code": code})
            cls.log.debug(res.json())

        # delete testunit
        res = requests.delete(cls.testunit_delete_url, params={
                "sampleCode": cls.samplecode, "sn": cls.test_sn, "code": cls.testunit_code})
        cls.log.debug(res.json())

        # delete testrecord
        for record in cls.testrecord_list:
            res = requests.delete(cls.testrecord_delete_url, params={"code": record})
            cls.log.debug(res.json())

    def test_01_build_staff(self):

        # call the API and compare the result
        data = eval(self.staff_data)
        res = requests.post(self.staff_build_url, data=data)
        result = res.json()
        self.assertEqual(result["info"], u"创建Staff成功")

        # add static params
        testRecord_story.jobnumber = result.get('data').get('jobnumber')
        testRecord_story.staffcode = result.get('data').get('code')

        # write to the log file
        self.log.info(result)

    def test_02_build_errortype(self):

        # call the API and compare the result
        data = eval(self.errortype_data)
        res = requests.post(self.errortype_build_url, data=data)
        result = res.json()
        self.assertEqual(result['info'], u"创建Errortype成功")

        # add static params
        testRecord_story.errortype_code = result.get('data').get('code')

        # write to the log file
        self.log.info(result)

    def test_03_build_sample(self):

        # call the API and compare the result
        data = eval(self.sample_data)
        res = requests.post(self.sample_build_url, data=data)
        result = res.json()
        self.assertEqual(result['info'], u"创建Sample成功")

        # add static params
        testRecord_story.samplecode = result.get('data').get('code')

        # write to the log file
        self.log.info(result)

    def test_04_build_testOption(self):
        for value in self.options.values():
            data = {"sampleCode": testRecord_story.samplecode,
                    "option": value, "code": "pitop{}".format(value)}
            res = requests.post(self.testoption_build_url, data=data)
            result = res.json()
            self.assertEqual(result['info'], "Success")

            # add static params
            testRecord_story.testoption_list.append(result.get('data').get('code'))

            # write to log file
            self.log.info(result)

    def test_05_build_testUnit(self):

        # call the api and compare the return result
        data = {"sampleCode": self.samplecode, "jobnumber": self.jobnumber, "factorySN": "20180620001",
                "sn": self.test_sn, "mcuSN": "mcu20180620001", "syncState": "Ready"}
        res = requests.post(self.testunit_build_url, data=data)
        result = res.json()
        self.assertEqual(result['info'], u"创建TestUnit成功")

        # add static params
        testRecord_story.testunit_code = result.get('data').get('code')

        # write to log file
        self.log.info(result)

    def test_06_build_testRecord(self):
        # call the api and compare the return result
        for option in testRecord_story.testoption_list:
            data = {"jobNumber": self.jobnumber, "testOptionCode": option, "sn": self.test_sn, "state": "TestSuccess"}
            res = requests.post(self.testrecord_build_url, data=data)
            result = res.json()
            self.assertEqual(result["info"], u"创建TestRecord成功")
            self.testrecord_list.append(result.get('data').get('code'))
            self.log.info(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)