#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:03:44 2020

@author: nick
"""
import mysql.connector
import numpy as np
import os, glob, re

def local(cfg):
    
    files = np.array(glob.glob(os.path.join(cfg.scc['input-dir'],'*')))
    
    exts = np.array([re.split('[.]', x)[-2] for x in files])
    
    sel = np.array([f'b{x}' for x in cfg.scc['wave']])
    
    files_b = []
    label_w = []
    for ext in sel:
        files_b.extend(files[exts == ext])
        label_w.extend(exts[exts == ext])
        
    files = np.array(files_b)
    exts = np.array(label_w)
        
    return(files, exts)