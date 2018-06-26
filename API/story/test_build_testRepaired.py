# --*-- coding:utf8 --*--

import unittest
import requests
import json

from units.config import Config, Data_API_File
from units.file_reader import Excel_Reader
from units.log import Logger
from units.conn_mysql import Conn_DB


class testRepaired_story(unittest.TestCase):

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

    testrepaired_dict = Config().get('testRepaired')
    testrepaired_build_url = URL + testrepaired_dict.get('build')
    testrepaired_delete_url = URL + testrepaired_dict.get('delete')

    # get test_data
    data_dict = Excel_Reader(Data_API_File, "testrepaired_story").data
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
    repaired_code = None

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        # delete staff
        res = requests.delete(self.staff_delete_url, params={"code": self.staffcode})
        self.log.debug(res.json())

        # delete errortype
        res = requests.delete(self.errortype_delete_url, params={"code": self.errortype_code})
        self.log.debug(res.json())

        # delete smaple
        res = requests.delete(self.sample_delete_url, params={"code": self.samplecode})
        self.log.debug(res.json())

        # delete testoption
        for code in self.testoption_list:
            res = requests.delete(self.testoption_delete_url, params={
                    "sampleCode": self.samplecode, "code": code})
        self.log.debug(res.json())

        # delete testunit
        res = requests.delete(self.testunit_delete_url, params={
                "sampleCode": self.samplecode,
                "sn": self.test_sn,
                "code": self.testunit_code})
        self.log.debug(res.json())

        # delete testrecord
        for record in self.testrecord_list:
            res = requests.delete(self.testrecord_delete_url, params={"code": record})
        self.log.debug(res.json())

        # delete testrepaired
        res = requests.delete(self.testrepaired_delete_url, params={"code": self.repaired_code})
        self.log.debug(res.json())

    def test_01_build_staff(self):
        # call the API and compare the result
        data = eval(self.staff_data)
        res = requests.post(self.staff_build_url, data=data)
        result = res.json()
        self.assertEqual(result["info"], u"创建Staff成功")
        # add static params
        testRepaired_story.jobnumber = result.get('data').get('jobnumber')
        testRepaired_story.staffcode = result.get('data').get('code')
        # write to the log file
        self.log.info(result)

    def test_02_build_errortype(self):
        # call the API and compare the result
        data = eval(self.errortype_data)
        res = requests.post(self.errortype_build_url, data=data)
        result = res.json()
        self.assertEqual(result['info'], u"创建Errortype成功")
        # add static params
        testRepaired_story.errortype_code = result.get('data').get('code')
        # write to the log file
        self.log.info(result)

    def test_03_build_sample(self):
        # call the API and compare the result
        data = eval(self.sample_data)
        res = requests.post(self.sample_build_url, data=data)
        result = res.json()
        self.assertEqual(result['info'], u"创建Sample成功")
        # add static params
        testRepaired_story.samplecode = result.get('data').get('code')
        # write to the log file
        self.log.info(result)

    def test_04_build_testOption(self):
        for value in self.options.values():
            data = {"sampleCode": self.samplecode, "option": value, "code": "pitop{}".format(value)}
            res = requests.post(self.testoption_build_url, data=data)
            result = res.json()
            self.assertEqual(result['info'], "Success")

            # add static params
            testRepaired_story.testoption_list.append(result.get('data').get('code'))

            # write to log file
            self.log.info(result)

    def test_05_build_testUnit(self):
        # call the api and compare the return result
        data = {"sampleCode": self.samplecode, "jobnumber": self.jobnumber, "factorySN": "20180620002",
                "sn": self.test_sn, "mcuSN": "mcu20180620002", "syncState": "Ready"}
        res = requests.post(self.testunit_build_url, data=data)
        result = res.json()
        self.assertEqual(result['info'], u"创建TestUnit成功")

        # add static params
        testRepaired_story.testunit_code = result.get('data').get('code')

        # write to log file
        self.log.info(result)

    def test_06_build_testRecord(self):
        # call the api and compare the return result
        for option in self.testoption_list:
            data = {"jobNumber": self.jobnumber, "testOptionCode": option, "sn": self.test_sn, "state": "TestFailed"}
            res = requests.post(self.testrecord_build_url, data=data)
            result = res.json()
            self.assertEqual(result["info"], u"创建TestRecord成功")
            self.testrecord_list.append(result.get('data').get('code'))
            self.log.info(result)

    def test_07_build_testRepaired(self):
        # call the api and compare the return result
        data = {"testUnitCode": "",  "errorCode": self.errortype_code, "state": "repaired",
                "feedback": "suite has been repaired", "sn": self.test_sn, "jobnumber": self.jobnumber}
        res = requests.post(self.testrepaired_build_url, data=data)
        result = res.json()

        # write to log file
        self.log.info(result)
        self.assertEqual(result['info'], u'创建RepairFeedback成功')

        # add static params
        testRepaired_story.repaired_code = result.get('data').get('code')


if __name__ == "__main__":
    unittest.main(verbosity=2)