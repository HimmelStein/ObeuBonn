from numpy import mean


def get_all_subgroups(csvFile, outfile=""):
    subgroupsList = []
    with open(csvFile, 'r', encoding='iso-8859-3') as fh:
        for dm in fh.readlines()[1:]:
            wlst = dm.split(',')
            subg = ' '.join(wlst[1:3])
            if subg not in subgroupsList:
                subgroupsList.append(subg)
    print(len(subgroupsList))
    with open(outfile, 'w') as ofh:
        cnt = '\n'.join(subgroupsList)
        ofh.write(cnt)
    return subgroupsList


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


def get_outlier_mm_in_each_group(csvfile, groupfile, outputFile, flag0):
    analst = []
    i = 0
    with open(groupfile, 'r') as gfh:
        for gln in gfh:
            print(i)
            i += 1
            pnum, sachnum = gln[:-1].split()
            rlt = []
            with open(csvfile, 'r') as ifh:
                for iln in ifh:
                    iln = iln.replace(')','').replace('"','').replace('[','').replace(']','')
                    clst = iln[:-1].split(',')

                    if clst[1] == pnum and clst[2] == sachnum:
                        if flag0 == 'lof':
                            rlt.append([float(clst[5])]+[int(clst[4])])
                        else:
                            rlt.append([mean([float(ele) for ele in clst[3:5]])]+[int(clst[5])])

            outlier = sorted(rlt, key=lambda grp: grp[0], reverse=True)[0]
            outlier = [str(ele) for ele in outlier]
            maxEle = sorted(rlt, key=lambda grp:  grp[0], reverse=True)[0]
            maxEle = [str(ele) for ele in maxEle]
            minEle = sorted(rlt, key=lambda grp:  grp[0])[0]
            minEle = [str(ele) for ele in minEle]

            if outlier == maxEle:
                flag = 'M'
            elif outlier == minEle:
                flag = 'I'
            else:
                flag = 'N'
            analst.append(','.join([pnum, sachnum]+outlier+maxEle+minEle+[flag]))
    with open(outputFile, 'w') as ofh:
        cnt = '\n'.join(analst)
        ofh.write(cnt)


if __name__ == "__main__":
    loffile = "/Users/tdong/Documents/Bonndatasets/OutlierDetectionResults/Result_top-1.csv"
    fpifile = "/Users/tdong/Documents/Bonndatasets/OutlierDetectionResults/2013-2024BonnSimple-results.csv"
    subgroupFile = "/Users/tdong/Documents/Bonndatasets/OutlierDetectionResults/all_subgroups.csv"
    analoffile = "/Users/tdong/Documents/Bonndatasets/OutlierDetectionResults/ana_lof_result.csv"
    anafqrfile = "/Users/tdong/Documents/Bonndatasets/OutlierDetectionResults/ana_fqr_result.csv"
    for csvf, outf, flag in zip([fpifile, loffile], [anafqrfile, analoffile], ['fpi', 'lof']):
        get_outlier_mm_in_each_group(csvf, subgroupFile, outf, flag)