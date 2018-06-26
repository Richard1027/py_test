import unittest
import requests
from units.config import Config, Data_API_File
from units.file_reader import Excel_Reader
from units.log import Logger

class test_account(unittest.TestCase):

    # get API URL
    url = Config().get('URL')
    account_dict = Config().get('account')
    modify_passwd = account_dict.get('modify_passwd')
    account_modify_passwd_url = url + modify_passwd

    # get API Test Element
    data_dict = Excel_Reader(Data_API_File, "account").data
    value_null = data_dict.get('all_null')[0]
    value_token_null = data_dict.get('token_null')[0]
    value_password_null = data_dict.get('password_null')[0]
    value_password_token = data_dict.get('token_password')[0]

    @classmethod
    def setUpClass(cls):
        pass

    def test_account_modify_all_null(self):
        res = requests.put(self.account_modify_passwd_url, data=self.value_null)
        result = res.json()
        Logger.Debug(result)
        self.assertEqual(result['info'], u'注册失败')

    def test_account_modify_token__null(self):
        res = requests.put(self.account_modify_passwd_url, data= self.value_token_null)
        result = res.json()
        Logger.Debug(result)
        self.assertEqual(result['info'], u'注册失败')

    def test_account_modify_passwd_null(self):
        res = requests.put(self.account_modify_passwd_url, data= self.value_password_null)
        result = res.json()
        Logger.Debug(result)
        self.assertEqual(result['info'], u'注册失败')

    @unittest.skip("sdjkfjsdkf")
    def test_account_modify_passwd(self):
        res = requests.put(self.account_modify_passwd_url, data= self.value_password_token)
        result = res.json()
        Logger.Debug(result)
        self.assertEqual(result['info'], u'注册成功')

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)