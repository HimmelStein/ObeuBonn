
import random

def create_column(cfile, newFile, column, refCol, rate):
    """
    create a new column, the value is reference to refCol, with a random update within rate
    :param cfile:
    :param newFile
    :param column:
    :param refCol:
    :param rate:
    :return:
    """
    nln = []
    with open(cfile, 'r', encoding='iso-8859-3') as ifh:
        header = ifh.readline()[:-1].split(";")
        header.append(column)
        nln.append(';'.join(header)+'\n')
        for ln in ifh.readlines():
            cells = ln[:-1].split(';')
            sval = cells[-1]
            if sval:
                sval=sval.replace('.','').replace(',','.')
                val = float(sval) * (1 + random.uniform(-1,1) * rate)
                cells.append(str(val).replace('.',','))
            else:
                cells.append(str(random.uniform(-100000,100000) * rate).replace('.',','))
            print(cells)
            nln.append(';'.join(cells)+'\n')
    with open(newFile, 'w') as ofh:
        ofh.writelines(nln)


if __name__ == "__main__":
    csvFile = "/Users/tdong/Downloads/Plan2017Zeilenebene.csv"
    create_column(csvFile, "/Users/tdong/Downloads/Plan2017ZeilenebeneX.csv",
                  "Executed2017", "Plan2017", 0.1)
