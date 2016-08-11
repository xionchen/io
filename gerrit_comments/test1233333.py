import datetime

start_time = datetime.datetime.now()
lista = []
for i in range(100):
    listb = []
    for j in range(100):
        listb.append(j)
    lista.append(listb)
end_time = datetime.datetime.now()
print '==================================='
print (end_time - start_time).seconds

start_time = datetime.datetime.now()
for x in lista:
    for haha in x:
        print haha,

end_time = datetime.datetime.now()
print '==================================='
print (end_time - start_time).seconds

start_time = datetime.datetime.now()

dicta = {}
for i in range(100):
    dictb = {}
    for j in range(100):
        dictb['%d' % j] = j
    dicta['%d' % i] = dictb

end_time = datetime.datetime.now()
print '==================================='
print (end_time - start_time).seconds

start_time = datetime.datetime.now()

for keys in dicta.keys():
    for keys2 in dicta[keys].keys():
        print dicta[keys][keys2],


end_time = datetime.datetime.now()
print '==================================='
print (end_time - start_time).seconds


