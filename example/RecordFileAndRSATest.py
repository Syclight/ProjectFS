from clazz.RSA import rsaEncrypt
from clazz.RecordFile import RecordFile
import json

# m = {'DATE': '2020-3-22', 'TIME': '12:00:00', 'HP': '98', 'MP': '22'}
m = ['2020-3-22', '12:00:00', '98', '22', 'AR56']
rf = RecordFile('/', 'ss')
rf.create(m)
print(rf.getList())

# s = '[FS-RECORDHEAD]\nTime&2020-3-2212:00:00\nHP&98 MP&22\nEquip&OBJ_ARMOR_0'
# rsaEncrypt(s)
