import os
import gzip

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None

def read(file):
    with gzip.open(file, 'rt') as f:
       csv_file = pd.read_csv(f)
    return csv_file # A user-uploaded zipped data file from IPUMS

def createCodeFrame(input_text, inds):
    with open(input_text) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    c = [x for x in content if "\t\t" in x]
    codes = []
    for i in c:
        if i[0].isupper():
            key = i.split()[0]
            header = " ".join(i.split()[1:])
            continue
        else:
            codeNum = int(i.split()[0])
            label = " ".join(i.split()[1:])
            codeOut={
                "code":codeNum,
                "key":key,
                "label":label,
                "header":header
            }
            codes.append(codeOut)

    outdf = pd.DataFrame(codes)

    dir = os.path.dirname(os.path.abspath(__file__))
    with open(inds) as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    indcodes=[]
    inddesc=[]
    for i in range(len(content)):
        if i % 2 == 0:
            indcodes.append(int(content[i]))
        else:
            inddesc.append(content[i])

    codes2 = pd.DataFrame({"code":[int(x) for x in indcodes],"key":"IND","label":inddesc,"header":"Industry"})
    outdf = outdf.append(codes2)
    return outdf

def decodeIpums(df, code):
    nullReplace = ['NIU', 99, 999, 99.0, 99.0]
    for n in nullReplace:
        df=df.replace(n,np.nan)
    checks = [x for x in list(df) if x in list(code['key'])]
    for check in checks:
        # print ("Running " + check)
        xcode = code[code['key']==check].reset_index(drop=True)
        codeDict = dict(zip(xcode['code'],xcode['label']))
        targetList = list(df[check])
        newName = xcode['header'][0]
        newList = []
        for i in targetList:
            try:
                newList.append(codeDict[i])
            except:
                newList.append(i)
                pass
        df[check] = newList
        df=df.rename(columns={check:newName})
    return df
