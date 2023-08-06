import re
from bs4 import BeautifulSoup as BS
import fdb_data.errors as _errors
import lxml

class Block:
    
    def __init__(self,key,value,typev):
        self.key=key
        self.value=value
        self.type=typev
    def __str__(self):
        return 'Key: '+self.key+'\nValue: '+self.value+'\nType: '+self.type

class Base:
    
    def __init__(self,code):
        self.code=code

    def in_block(self,key):
        return BS(self.code,'lxml').find('block',key=key)!=None
    def delete_block(self,key):
        delb=BS(self.code,'lxml').find('block',key=key)
        if delb==None:
            raise _errors.FdbNoKeyError('This key is not in database!')
        self.code=self.code.replace(str(delb),'')
        
    def add_block(self,key,value,typev):
        block=f'\n<block key="{key}" value="{value}" type="{typev}"></block>'
        self.code+=block
        
    def block(self,key):
        block=BS(self.code,'lxml').find('block',key=key)
        if block==None:
            raise _errors.FdbNoKeyError('This key is not in database!')
        block=str(block)
        typev=re.search(r'type="[^"]*"',block)
        try: typev=typev.group(0)
        except: raise _errors.FdbCodeError('Invalid Syntax!')
        typev=typev[6:-1:]
        value=re.search(r'value="[^"]*"',block)
        try: value=value.group(0)
        except: raise _errors.FdbCodeError('Invalid Syntax!')
        value=value[7:-1:]
        return Block(key,value,typev)
    
    def upload(self):
        return self.code
    
if __name__=='__main__':
    b=Base('''
<block key="earth" value="moon" type="str"></block>
<block key="mars" value="phobos, deimos" type="str"></block>''')
    print(b.block('mars'))
