# --*-- coding:utf8 --*--


import os
import unittest
from units.HTMLTestRunner import HTMLTestRunner
from units.config import Report_Path, API_PATH

# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)


if __name__ == "__main__":

    report_file = os.path.join(Report_Path, 'report.html')
    case_path = os.path.join(API_PATH, 'story')
    suite = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(
        case_path, pattern="test*.py", top_level_dir=None)
    suite.addTests(discover)

    with open(report_file, 'wb') as f:
        runner = HTMLTestRunner(stream=f,
                                title='pps test',
                                description='100 times',
                                verbosity=2)
        runner.run(suite)
