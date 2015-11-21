#_*_encoding=utf8_*_
'''
Created on 2015年11月20日

@author: 15361
'''
import re
m = re.match("4.4", "4 4");
if m is not None: m.group()
print m.group()

patten = re.compile("\d*\d*\d");
li = re.findall(patten,"9dd0kk00kk00ee00ii00ii0jj0k0k0k0")
print li
tu = ('测试','ee')
print tu[0].decode("utf-8")
t = "总过"
print t
