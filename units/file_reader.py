# --*-- coding:utf8 --*--

import yaml
import openpyxl
import os


class Yaml_Reader:

    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError(u'文件不存在')
        self._data = None

    @property
    def data(self):
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))
        return self._data


class Excel_Reader:

    def __init__(self, excelf, sheetname):
        if os.path.exists(excelf):
            self.excelf = excelf
            self.sheetname = sheetname
        else:
            raise FileNotFoundError

        self._data = {}

    @property
    def data(self):
        if not self._data:
            wb = openpyxl.load_workbook(self.excelf, 'r')
            table = wb[self.sheetname]
            max_rows = table.max_row

            for row in range(0,max_rows):
                row_num = row +1
                loc_name = table['A%s' %row_num].value
                by = table['B%s' % row_num].value
                val = table['C%s' % row_num].value
                self._data[loc_name] = by, val
        return self._data