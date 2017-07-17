
import datetime
import pandas as pd

xlsFile="Kostenstellen.xls"

xls_file = pd.ExcelFile(xlsFile)

xls_file.sheet_names

table = xls_file.parse('Sheet1')

table.irow(0)
table.icol(0)

table.ix[table['Kostenstelle'] == 100001]

# view a column
table.ix[:,'Kostenstelle']


date0 = datetime.date(2017, 5,1)
table.ix[table['Erfaßt am'] > date0]


dict = table.to_dict()
