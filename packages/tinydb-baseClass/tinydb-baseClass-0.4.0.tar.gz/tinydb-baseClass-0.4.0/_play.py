from tinydb_base.getSet import GetSet, futureTimeStamp

obj = GetSet('test.ds.json', table='getSetTest')
# obj.set('testTimeOut', 'this is a thing', timeout=futureTimeStamp(second=1))
# obj.set('testlog', 'battle')
x = obj.get('testTimeOut')
print(x)
