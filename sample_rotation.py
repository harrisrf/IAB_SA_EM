ids = []
month = []

def importer(yyyy, mm):
    with open('D:\\Users\\F3879852\\Documents\\Telmar\\'+ str(yyyy) + '-' + str(mm) + '\\data_demo_c1_' + str(yyyy) + str(mm) +'0100_30') as demo:
        for line in demo:
            ids.append(line[0: 31])
            month.append(str(yyyy) + str(mm))
    return
            
if __name__ == '__main__':
    importer('2016', '07')
    importer('2016', '08')
