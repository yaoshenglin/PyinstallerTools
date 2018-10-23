#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'YSL-PC'

import FileO
import os

def ConvertParam(param):
    if param == '单个文件':
        return '-F'
    elif param == '显示命令行窗口':
        return '-c'     # 与-w相反，默认含有此参数
    elif param == '生成log文件':
        return '-d'
    elif param == '显示帮助':
        return '-h'
    elif param == '显示版本号':
        return '-v'
    elif param == '覆盖原文件':
        return '-y'
    elif param == '编译前清理':
        return '--clean'
    else:
        return None
    pass


'''
dicData = {
        "Order":"pyinstaller -F -w",
        "Version": "file_version_info.txt",
        "Icon": "icon\\bitbug_favicon.ico",
        "Dir": "E:\\程序目录\\界面跳转",
        "Main":"Main.py"
    }
'''
def GetShellCode(dicData):
    Order = dicData.get("Order")
    ExeName = dicData.get("Name")
    Version = dicData.get("Version")
    Icon = dicData.get("Icon")
    fileDir = dicData.get("Dir")
    fileName = dicData.get("Main")
    if os.path.isdir(fileDir):
        listResult = []
        listResult.append(Order)
        listResult.append('-n ' + ExeName)
        listResult.append('--specpath ' + os.path.join(fileDir, 'dist'))
        FileO.CreateDir(os.path.join(fileDir, 'dist'))  #避免目录不存在
        if Version != None and len(Version):
            listResult.append('--version-file=' + Version)
        if Icon != None and len(Icon):
            listResult.append('-i ' + Icon)
        content = " ".join(listResult)
        strCommand = "%s %s" % (content,fileName)
        tDrive = os.path.splitdrive(fileDir)[0]  # 获得磁盘盘符(切换盘符用用盘符号加冒号，例如:d:)
        # python pyinstaller.py - -version - file = file_version_info.txt - -icon = ico.ico - -onefile - -windowed target.py
        listCommand = [tDrive, 'cd ' + fileDir, strCommand]
        strCommand = " && ".join(listCommand)  # 组合命令
        # self.ExecuteCommand(strCommand)
        # self.textOut.Show(True)
        # strCommand = 'echo E:\PyProgramPack>test.txt'   # 测试命令的有效性
        return strCommand

'''
dicData = {
        "Order":"pyinstaller -F -w",
        "Version": "file_version_info.txt",
        "Icon": "icon\\bitbug_favicon.ico",
        "Dir": "E:\\程序目录\\界面跳转",
        "list":listFile
        "Main":"Main.py"
    }
'''
# 目录
def ExtendShell(dicData):
    Order = dicData.get("Order")
    ExeName = dicData.get("Name")
    Version = dicData.get("Version")
    Icon = dicData.get("Icon")
    mainFile = dicData.get("Main")
    fileDir = dicData.get("Dir")
    listFile = [] + dicData.get("list")
    # FileO.List.RemoveObj(listValue, mainFile)
    if len(listFile) > 0:
        listResult = []
        listResult.append(Order)
        listResult.append('-n ' + ExeName)
        listResult.append('--specpath ' + os.path.join(fileDir, 'dist'))
        FileO.CreateDir(os.path.join(fileDir, 'dist'))  #避免目录不存在
        if Version != None and len(Version):
            listResult.append('--version-file=' + Version)
        if Icon != None and len(Icon):
            listResult.append('-i ' + Icon)

        # 更正主文件顺序
        FileO.List.RemoveObj(listFile, mainFile)
        listFile.insert(0,mainFile)
        content = " -p ".join(listFile)
        # print(content)
        listResult.append(content)
        # FileO.List.RemoveObj(listFile,mainFile)
        # content = " --hidden-import ".join(listFile)
        # content = "--hidden-import " + content
        # print(content)
        # listResult.append(content)
        content = " ".join(listResult)

        tDrive = os.path.splitdrive(fileDir)[0]  # 获得磁盘盘符(切换盘符用用盘符号加冒号，例如:d:)
        listCommand = [tDrive, 'cd ' + fileDir, content]
        strCommand = " && ".join(listCommand)  # 组合命令
        # print(strCommand)
        return strCommand

def GetPyFile(path):
    listResult = []
    if os.path.isdir(path):
        listFile = os.listdir(path)
        if len(listFile)>0:
            for name in listFile:
                if name.endswith('.py'):
                    listResult.append(name)
    elif path.endswith('.py'):
        listResult.append(path)
    return listResult

def DeleteEndFile(content,fileDir,MainObj,EName):
    # 产生三个文件夹(__pycache__,build,dist)，一个单独文件(.spec)
    print('end',fileDir,MainObj,EName)
    path1 = os.path.join(fileDir, "__pycache__")
    path2 = os.path.join(fileDir, "build")
    path3 = os.path.join(fileDir, EName + ".spec")
    # oldPath = os.path.join(fileDir,"dist",os.path.splitext(MainObj)[0]+".exe")
    # ExePath = os.path.join(fileDir,"dist",EName+".exe")
    listPath = [path1, path2, path3]
    for i in range(len(listPath)):
        path = listPath[i]
        FileO.DeleteFile(path)

    if content == "操作失败":
        fileName = 'error_log.txt'
        excuPath = os.getcwd()
        strPath = os.path.join(excuPath, fileName)
        FileO.AddWriteFile(strPath,fileDir)
        FileO.AddWriteFile(strPath,"\n" + os.path.join(fileDir, fileName))
        FileO.DeleteFile(os.path.join(fileDir, "dist"))