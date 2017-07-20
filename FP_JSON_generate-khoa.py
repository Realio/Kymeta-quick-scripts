# -*- coding: utf-8 -*-
"""
Created on Fri Oct 07 10:32:46 2016

@author: aguenterberg
"""

import matplotlib.pyplot as plt
import numpy as np
import json
import time
import sys
import os

from PyQt4 import QtGui

def rjson(fpath):
    with open(fpath) as d_file:
        datas = json.load(d_file)
    return datas

def wjson(data,fpath):
    with open(fpath, 'wb') as fid:
        json.dump(data,fid,indent=0)

## Grab all jsons in directory
## For each json generate scan roll off measurement

def get_file(prompt='Select File',*args):
    try:
        app1 = QtGui.QApplication(sys.argv)
        myWidget = QtGui.QWidget() #Generic parent for the file dialog.
        fnames = QtGui.QFileDialog.getOpenFileNames(myWidget, prompt)
        return fnames
    finally:
        pass

def check_dir(dirs):
    if not os.path.exists(dirs):
        os.mkdir(dirs)
    return dirs

d_path = get_file()

try:
    a = [i for i in d_path]
except TypeError:
    d_path = [d_path]

for d_paths in d_path:
    dirpath = (os.path.split(str(d_paths)))
    ndatas = rjson(str(d_paths))
    #Read a json file. Ask if it is a tx json or a Rx json
    bands = [k for k,v in ndatas.items()]#AJ WHY?
    if 'RX' in bands:
        bands = 'RX'
    elif 'TX' in bands:
        bands = 'TX'


    ffreq = ndatas[bands]['Pattern_FREQ']

    ups = {'Pattern_THETA':[0]}
    ups['Pattern_LPA'] = [90,0]
    ups['Pattern_PHI'] = [0]

    if ndatas[bands]['Pattern_PatternType']=='TX':
        ups['Pattern_LPA'] = [90,0]

    if ffreq == 11.8 or ffreq == 14.0:
        ups['Pattern_THETA'] = [0,30,45,60]
        ups['Pattern_PHI'] = [0,45]

    for lpas in ups['Pattern_LPA']:
        for phs in ups['Pattern_PHI']:
            for ths in ups['Pattern_THETA']:
                for band in bands:
                    ndatas[bands]['Pattern_LPA'] = lpas
                    ndatas[bands]['Pattern_THETA'] = ths
                    ndatas[bands]['Pattern_PHI'] = phs
                freq = ndatas[bands]['Pattern_FREQ']
                lpa = ndatas[bands]['Pattern_LPA']
                th = ndatas[bands]['Pattern_THETA']
                ph = ndatas[bands]['Pattern_PHI']
                bnd = ndatas[bands]['Pattern_PatternType']
                time.sleep(1)
                nows = time.strftime("%Y%m%d%H%M%S",time.gmtime())
                fname = 'SN%s_%s_LIN_f=%s_LPA=%s_THETA=%s_PHI=%s.json'%(nows,bnd,freq,lpa,th,ph)
                ndatas[bands]['Pattern_ConfigFile'] = fname

                datadir = dirpath[0]+'\\First Pass JSONS'+time.strftime("%Y%m%d",time.gmtime())
                datadir = check_dir(datadir)

                wjson(ndatas,datadir+'\\%s'%(fname))
