import unittest
import requests
from units.config import Config


class test_enum(unittest.TestCase):

    url = Config().get('URL')
    res_enum = Config().get('enum')
    res_enum_error = Config().get('enum_error')
    res_enum_url = url + res_enum
    res_enum_error_url = url + res_enum_error

    @classmethod
    def setUpClass(self):
        pass

    def test_enum_error(self):
        res = requests.get(self.res_enum_error_url)
        result = res.json()
        self.assertEqual(result['9002'], "State error")

    def test_enum_code_null(self):
        res = requests.get(self.res_enum_url+'')
        result = res.status_code
        self.assertEqual(result, 404)

    def test_enum_illegal_str(self):
        res = requests.get(self.res_enum_url + '爱迪生')
        result = res.status_code
        self.assertEqual(result, 400)

    def test_enum_unit_status(self):
        res = requests.get(self.res_enum_url+'1000')
        result = res.json()
        self.assertEqual(result['TestFailed'], u'测试失败')
        self.assertEqual(result['Create'], u'创建')
        self.assertEqual(result['TestSuccess'], u'测试通过')
        self.assertEqual(result['Repair'], u'检修')

    def test_enum_employee_status(self):
        res = requests.get(self.res_enum_url + '1001')
        result = res.json()
        self.assertEqual(result['Hire'], u'入职')
        self.assertEqual(result['Leave'], u'离职')

    def test_enum_errot_type(self):
        res = requests.get(self.res_enum_url + '1002')
        result = res.json()
        self.assertEqual(result['Enable'], u'启用')
        self.assertEqual(result['Disable'], u'禁用')

    def test_enum_testitem_status(self):
        res = requests.get(self.res_enum_url + '1003')
        result = res.json()
        self.assertEqual(result['Enable'], u'启用')
        self.assertEqual(result['Disable'], u'禁用')

    def test_enum_testrecord_status(self):
        res = requests.get(self.res_enum_url + '1004')
        result = res.json()
        self.assertEqual(result['TestFailed'], u'失败')
        self.assertEqual(result['TestSuccess'], u'成功')

    def test_enum_repair_status(self):
        res = requests.get(self.res_enum_url + '1005')
        result = res.json()
        self.assertEqual(result['Repaired'], u'修复')
        self.assertEqual(result['Broken'], u'损坏')

    def test_enum_gender_status(self):
        res = requests.get(self.res_enum_url + '1006')
        result = res.json()
        self.assertEqual(result['Male'], u'男')
        self.assertEqual(result['Female'], u'女')
        self.assertEqual(result['Other'], u'其他')


    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)