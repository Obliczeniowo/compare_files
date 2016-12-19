#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bez nazwy.py
#  
#  Copyright 2016 Krzysztof Zajączkowski (obliczeniowo.com.pl/?id=579
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os
from PIL import Image as im

path = input("Podaj ścieżkę do folderu, który ma być przeszukany: ")

def compareFile(file1, file2, maxdiff):
    if os.path.getsize(file1) != os.path.getsize(file2):
        return 100000
    img1 = im.open(file1)
    img2 = im.open(file2)
    
    img1.resize((500,500))
    img2.resize((500,500))
    
    data1 = list(img1.getdata())
    data2 = list(img2.getdata())
    
    diff = 0;
    
    if (not isinstance(data1[0], tuple)) and isinstance(data2[0], tuple):
        return 10000
    if isinstance(data1[0], tuple) and (not isinstance(data2[0], tuple)):
        return 10000        
    if isinstance(data1[0], tuple):
        for i in zip(data1, data2):
            for j in zip(list(i[0]), list(i[1])):
                diff += abs(j[0] - j[1])
            if diff > maxdiff:
                return diff
    else:
        for i in zip(data1, data2):
            diff += abs(i[0] - i[1])
            if diff > maxdiff:
                return diff
    return 0

if os.path.exists(path) and os.path.isdir(path):
    
    if not path.endswith("/") or not path.endswith("\\"):
        path += "/";
    
    fl = list(os.walk(path))

    filelist = files = [i for i in list(os.walk(path))[0][2] if i.lower().endswith(".jpg")]

    filelist.sort()

    k = 0

    nr = 1
    filelists = []
    for file1 in filelist[:-1]:
        if os.path.exists(path + file1):
            cmplist = []
            print("compare " + file1)
            for file2 in filelist[nr:]:
                if os.path.exists(path + file2):
                    if compareFile(path + file1, path + file2, 0) == 0:
                        print("\npowtarza sie " + file2 + " z " + file1 + "\n")
                        cmplist += [("powtarza sie " + file2 + " z " + file1, file2)];
            if len(cmplist):
                filelists += [cmplist.copy()];
            nr += 1
    
    delete = False
    
    if len(filelists):
        data = open(path + "files.txt", "w", -1, "utf-8")
        for i in filelists:
            for j in i:
                data.write(str(j) + "\n")
            if delete:
                for j in i:
                    if os.path.exists(path + j[1]):
                        os.remove(path + j[1])
        data.write(str(filelists))
        data.close()
        print("\nWykryto {nr} powtarzających się plików, ktore usunięto\n")
    else:
        print("\nNie wykryto powtarzających się plików\n")
else:
    print("Podana ścieżka nie istnieje lub nie jest ścieżką do folderu")
