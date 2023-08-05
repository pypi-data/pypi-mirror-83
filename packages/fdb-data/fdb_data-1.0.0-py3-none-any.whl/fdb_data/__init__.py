# Foton Data Base

import fdb.parser as _parser
import fdb.errors as _errors
from bs4 import BeautifulSoup as BS


class FDB:

    def __init__(self, file='fdb.fdb'):
        self.file_name = file
        self.file = open(file)
        text = self.file.read()
        self.base = _parser.Base(text)
        self.closed = False

    def getv(self, key):
        block = self.base.block(key)
        typev = block.type
        value = block.value
        result = None
        if typev == 'int':
            result = int(value)
        elif typev == 'str':
            result = value
        elif typev == 'float':
            result = float(value)
        else:
            raise _errors.FdbTypeValueError('Unknow type: "' + typev + '".')
        return result

    def addb(self, key, value):
        if self.base.in_block(key):
            raise _errors.FdbAddDataError('The key is already in the database!')
        typev = value.__class__.__name__
        self.base.add_block(key, value, typev)

    def rebl(self, key, value):
        if not self.base.in_block(key):
            raise _errors.FdbAddDataError('This key is not in the database!')
        self.base.delete_block(key)
        self.addv(key, value)

    def delete(self, key):
        self.base.delete_block(key)

    def save(self):
        file = open(self.file_name, 'w+')
        file.write(self.base.upload())
        file.close()

    def close(self):
        file = open(self.file_name, 'w+')
        file.write(self.base.upload())
        file.close()
        del self.file_name
        del self.file
        del self.base
        self.closed = True
