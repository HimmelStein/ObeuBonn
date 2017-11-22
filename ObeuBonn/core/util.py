import pandas as pd
import numpy as np
import math
from pprint import pprint

def get_kostenstellen_dic(ifile):
    rlt = dict()
    xlsDFDict = pd.ExcelFile(ifile)
    dfs = {sheet_name: xlsDFDict.parse(sheet_name) for sheet_name in xlsDFDict.sheet_names}
    for k, v in dfs.items():
        dic = v.to_dict()
        for i, kosten in dic['Kostenart'].items():
            if not math.isnan(kosten):
                rlt[int(kosten)] = dic['Bezeichnung'][i].replace(',', '.')
    return rlt


def get_proficenter_dic(ifile):
    rlt = dict()
    xlsDFDict = pd.ExcelFile(ifile)
    dfs = {sheet_name: xlsDFDict.parse(sheet_name) for sheet_name in xlsDFDict.sheet_names}
    for k, v in dfs.items():
        dic = v.to_dict()
        for i, kosten in dic['Profitcenter'].items():
            if not math.isnan(kosten):
                rlt[int(kosten)] = dic['Betzeichnung'][i].replace(',', '.')
    return rlt


def add_prof_kosten_description(ifile="", pDic=dict(), kDic=dict(), ofile=""):
    headLst =["Profitcenter","Profitcenter Beschreibung", "Kostenstelle", "Kostenstelle Beschreibung",
              "Outlier Betrag", "Outlier Jahr", "Max Betrag", "in Jahr", "Min Betrag", "in Jahr"]
    nLst = [','.join(headLst)]
    with open(ifile, 'r') as ifh:
        for ln in ifh:
            wlst = ln[:-1].split(',')
            pfid,  ktid = int(wlst[0]), int(wlst[1])
            pStr, ktStr = pDic.get(pfid, ""), kDic.get(ktid, "")
            thisLine = ','.join([str(pfid), pStr, str(ktid), ktStr]+wlst[2:-1])
            nLst.append(thisLine)
    with open(ofile, 'w') as ofh:
        ofh.write('\n'.join(nLst))



if __name__ == "__main__":
    iProficenterFile = "/Users/tdong/git/ObeuBonn/data/ProfitcenterHierarchieBonn2016.xlsx"
    iKostenstellenFile = "/Users/tdong/git/ObeuBonn/data/KostenartengruppeBonn2016.xlsx"
    ifiles = ["/Users/tdong/Documents/Bonndatasets/OutlierDetectionResults/fqr_M.csv",
              "/Users/tdong/Documents/Bonndatasets/OutlierDetectionResults/lof_M.csv"]
    ofiles =  ["/Users/tdong/Documents/Bonndatasets/OutlierDetectionResults/fqrX_M.csv",
              "/Users/tdong/Documents/Bonndatasets/OutlierDetectionResults/lofX_M.csv"]

    profDic = get_proficenter_dic(iProficenterFile)
    kostenDic = get_kostenstellen_dic(iKostenstellenFile)
    for f1, fo in zip(ifiles, ofiles):
        add_prof_kosten_description(ifile=f1, pDic=profDic, kDic=kostenDic, ofile=fo)
