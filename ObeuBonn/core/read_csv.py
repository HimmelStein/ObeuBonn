
import codecs
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


def get_all_bonn_budget_files(fPath, pattern='PlandatenErgebnisplan', end='csv'):
    """
    get all Bonn budget datasets
    :param fPath: search path
    :return: a list of csv filenames with absolute file name
    """
    rlt = []
    for f in os.listdir(fPath):
        if f.startswith(pattern) and f.endswith(end):
            rlt.append(os.path.abspath(os.path.join(fPath, f)))
    return rlt


def get_all_columns_from_csv(csvFile):
    """
    return all dimensions from a csv file
    :param csvFile:
    :return:
    """
    dmlst = []
    with open(csvFile, 'r', encoding='iso-8859-3') as fh:
        for dm in fh.readline().split(';'):
            dmlst.append(dm.strip())
    return dmlst


def get_all_pockets_in_budgets(outFile):
    """
    a pocket is Product center + Konto
    110200126;503200
    :param csvFile:
    :return:
    """
    opath = ''
    for csvFile in get_all_bonn_budget_files('data'):
        if opath == '':
            opath, file = os.path.split(csvFile)
        ofh = open(os.path.join(opath, outFile), 'w')
        dmlst = []
        with open(csvFile, 'r', encoding='iso-8859-3') as fh:
            fh.readline()
            for ln in fh.readlines():
                pocket=''
                for ele in ln.split(';')[:2]:
                    pocket +=ele
                if pocket not in dmlst:
                    print(pocket)
                    ofh.write(pocket+'\n')
                    dmlst.append(pocket)
    ofh.close()
    return dmlst


def collect_values_for_each_pocket(csvpath):
    """
    collect all budgets for a pocket in one csv file.
    :param csvFile: input budget csv file
    :param outFile: output json file
    :return: json structure, which is also stored in outFile
    """
    opath = ''
    for csvFile in get_all_bonn_budget_files(csvpath):
        opath, file = os.path.split(csvFile)
        outFile = os.path.basename(file).split('.')[0] + '.json'
        ofh = open(os.path.join(opath, outFile), 'w')
        rlt = defaultdict((lambda : 0.0))
        with open(csvFile, 'r', encoding='iso-8859-3') as fh:
            fh.readline()
            for ln in fh.readlines():
                lst = ln.split(';')
                pocket = lst[0]+lst[1]
                rlt[pocket] += float(lst[3].replace('.','').replace(',','.'))
                #print(lst[3], pocket, float(lst[3].replace('.','').replace(',','.')))
                if pocket=='':
                    print(csvFile, lst[3], pocket, float(lst[3].replace('.','').replace(',','.')))
        json.dump(rlt, ofh)
        ofh.close()
    return rlt


def normalize_pockets_distribution(jsonPath, end='json'):
    """
    '':<sum> in the json file
    remove no-named pocket
    sum all the value of the pockets
    devide each pocket value by the sum
    :param jsonFile:
    :return:
    """
    for jsonFile in get_all_bonn_budget_files(jsonPath, end=end):
        print(jsonFile)
        opath, file = os.path.split(jsonFile)
        outFile = os.path.basename(file).split('.')[0] + '_norm.json'
        ofh = open(os.path.join(opath, outFile), 'w')
        rlt = defaultdict((lambda: 0.0))
        with open(jsonFile, 'r', encoding='iso-8859-3') as fh:
            dic = json.load(fh)
            sum = dic['']
            for key in dic.keys():
                if key == '':
                    continue
                else:
                    rlt[key] = dic[key]/sum
        json.dump(rlt, ofh)
        ofh.close()
    return rlt


def visualize_patterns(jsonPath, subplotN=7, end='_norm.json', minusFlag=1, low = 0e+16, up = 10.905e+16):
    """
    to do: separate positive value and negative value
    :param jsonPath:
    :param subplotN:
    :param end:
    :param minusFlag:
    :param low:
    :param up:
    :return:
    """
    keys = []
    with open('/Users/tdong/git/ObeuBonn/data/pockets.csv', 'r') as kfh:
        for key in kfh.readlines():
            keys.append(key.strip('\n'))
    i = 0
    subplosts = [711,712,713,714,715,716,717]
    colors=['bo', 'go', 'ro', 'mo', 'yo', 'ko','co']
    fig = plt.figure(1)
    lowStr, lowVal ='', up
    upStr, upVal = '', low
    vv= {}
    for jsonFile in get_all_bonn_budget_files(jsonPath, end=end):
        print(jsonFile)
        subTitel = jsonFile.split('_')[0][-4:]
        plt.subplot(subplosts[i])
        plt.ylabel('Plan'+subTitel)
        vv['Plan'+subTitel] = []
        x = []
        y = []
        dic = json.load(open(jsonFile, 'r', encoding='iso-8859-3'))
        for keyStr in keys:
            if keyStr == '':
                continue
            xv = int(keyStr)
            if xv < low or xv > up:
                continue

            if lowVal > xv:
                lowVal = xv
                lowStr = keyStr
            if upVal < xv:
                upVal = xv
                upStr = keyStr

            x.append(xv)
            if keyStr in dic:
                y.append(dic[keyStr])
            else:
                y.append(0)
        plt.plot(x,y, colors[i])
        i += 1

    fig.suptitle(lowStr+"----"+upStr)
    plt.show()
    return vv

