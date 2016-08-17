import shlex

results = []
fieldStart = []
fieldEnd = []
fieldName = []
d = {}
with open('D:\\Users\\F3879852\\Documents\\Telmar\\2016-07\\decode_demo_c1_2016070100_30') as demoDecode:
    for line in demoDecode:
        fieldStart.append(int(line[7 : line.find('-')]))
        fieldEnd.append(int(line[line.find('-') + 1 : line.find('=') - 1]))
        if line.find(':') > 1:
            fieldName.append(line[line.find(':') + 2 : line.find('/') - 1])
        else:
            fieldName.append(line[line.find('=') + 2:].strip())
        if line.find('/') > 1:
            valueList = shlex.split(line[line.find('/') + 2 : ].strip())
            for i in valueList:
                d[i.split('=')[0]] = i.split('=')[1]
demoDecode.close()
