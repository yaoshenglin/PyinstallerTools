#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'YSL-PC'

import os
import sys
import chardet  #编码相关
import shutil   #目录操作相关

def CreateDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def GetCurDir():
    return os.getcwd()

def GetListFiles(path):
    if os.path.exists(path):
        return os.listdir(path)
    return None

def GetTextEncod(path):
    if not os.path.exists(path):
        return None
    f = open(path, "rb")
    data = f.read()
    f.close()
    code = chardet.detect(data)['encoding']
    return code

def readFile(path):
    if not os.path.exists(path):
        return None
    f = open(path, "r",encoding='UTF-8')
    value = f.read()
    f.close()
    return value

def readBinData(path):
    if not os.path.exists(path):
        return None
    f = open(path, "rb")
    value = f.read()
    f.close()
    return value

def readFileByEncode(path):
    if not os.path.exists(path):
        return None
    f = open(path, "rb")
    data = f.read()
    f.close()
    code = chardet.detect(data)['encoding']
    value = data.decode(code)
    return value

def writeFile(path, value,encodint='utf-8'):
    f = open(path, "w",encoding=encodint)
    f.write(value)
    f.close()

def AddWriteFile(path,value):
    if not os.path.exists(path):
        writeFile(path,value)
        return
    encode = GetTextEncod(path)
    if encode == None or len(encode) < 1:encode='utf-8'
    f = open(path, mode='a', encoding=encode)
    f.write(value)
    f.close()

def MoveFile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname = os.path.split(dstfile)    #分离文件名和路径
        oldPath = os.path.join(dstfile,os.path.basename(srcfile))   #旧文件路径
        if os.path.isfile(oldPath):
            print(oldPath)
            os.remove(oldPath)                     # 先删除旧文件
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #如果不存在，则创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print("move %s -> %s"%( srcfile,dstfile))

def CopyFile(srcfile,dstfile):
    if os.path.exists(srcfile) and os.path.isdir(dstfile):
        shutil.copy(srcfile, dstfile)

# 根据路径删除文件
def DeleteFile(path):
    if os.path.exists(path):
        print("删除 --> "+path)
        if os.path.isfile(path):
            os.remove(path) #文件
        elif os.path.isdir(path):
            shutil.rmtree(path) #目录

# def GetBmpFromExe(path):
#     if path.lower().endswith('.exe'):
#         large, small = win32gui.ExtractIconEx(r"C:/Windows/regedit.exe",0)
#         win32gui.DestroyIcon(small[0])
#         hdc = win32ui.CreateDCFromHandle( win32gui.GetDC(0) )
#         hbmp = win32ui.CreateBitmap()
#         hbmp.CreateCompatibleBitmap( hdc, 32, 32 )
#         hdc = hdc.CreateCompatibleDC()
#         hdc.SelectObject( hbmp )
#         hdc.DrawIcon( (0,0), large[0] )
#         hbmp.SaveBitmapFile( hdc, "save.bmp" )
#
# def ImgConvertIcon(infile,outfile):
#     if len(outfile) < 1:
#         outfile = os.path.splitext(infile)[0] + ".ico"
#     if infile != outfile:
#         try:
#             img = PythonMagick.Image(infile)
#             img.sample(img.size())
#             img.write(outfile)
#             # img = Image.open(infile)
#             # img.thumbnail(img.size)
#             # img.save(outfile, "ico")
#         except IOError:
#             print("cannot create thumbnail for", infile)
#
# def GetIconFromExe(path):
#     GetBmpFromExe(path)
#     ImgConvertIcon('save.bmp')
#     os.remove('save.bmp')

def GetExecuteExt():
    listData = sys.argv
    if isinstance(listData, list) and len(listData) > 0:
        name = listData[0]
        ext = os.path.splitext(name)[1]
        return ext
    return None

class Obj(object):
    def cN(self):
        return self.__class__.__name__

class List(list):
    def GetObjByType(self,A_tuple):
        result = None
        for x in self:
            if Obj.cN(x) == A_tuple:
                result = x
                break
        return result
    def RemoveObj(self,Obj):
        if Obj in self:
            self.remove(Obj)
    def RemoveGroup(self,group):
        for value in group:
            if value in self:
                self.remove(value)

if __name__ == '__main__':
    path = "file_version_info.txt"
    isExist = False
    with open(path,'r',encoding='utf-8') as f:
        content = f.read()
        while '\n\n' in content:
            isExist = True
            content = content.replace('\n\n','\n')
    if True :
        with open(path,'w',encoding='utf-8') as f:
            f.write(content)
            print(content)