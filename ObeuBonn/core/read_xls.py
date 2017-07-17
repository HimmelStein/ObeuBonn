
import pandas as pd
import datetime
import os
from collections import defaultdict


xlsDFDict = defaultdict()
xlsfNames = ['FISTL inv. 2017.xls',
             'Innenaufträge.xls',
             'Kostenstellen.xls',
             'Produkte 2017.xls',
             'Profitcenter Hierarchie Bundesstadt Bonn.xls']


def xls_tables(fpath):
    """
    a dataframe is constructed by calling <excel stream>.parse(<sheet name>)
    :param fpath: relative path to the xls files
    :return: xlsDF_Dict = {
                'FISTL inv. 2017.xls' : { "df" : <excel stream>
                                          "sheet" : ['Sheet1]
                                        }
                }
    """
    global xls_DF, xlsfNames
    xlsfNames = []
    for xlsFile in os.listdir(fpath):
        fn, ext = os.path.splitext(xlsFile)
        fn = fn[:5]
        if ext == '.xls':
            xlsfNames.append(xlsFile)
            xlsDFDict[fn] = {}
            xlsDFDict[fn]['df'] = pd.ExcelFile(os.path.join(fpath, xlsFile))
            xlsDFDict[fn]['sheet'] = xlsDFDict[fn]['df'].sheet_names
    return xlsDFDict






