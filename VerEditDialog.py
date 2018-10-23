#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'YSL-PC'

import FileO
import wx
import re
import os
import win32api

class ButtonFrame(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '版本编辑',size=(500, 480),style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.SetMinSize((500, 480))
        self.SetMaxSize((1000,480))
        self.Center()

        panel = wx.Panel(self, -1)

        self.path = ''
        self.dictData = {}
        self.listItems = []
        self.listKeys = ['FileDescription','fileType','FileVersion','ProductName','ProductVersion','LegalCopyright','LegalTrademarks','OriginalFilename','CompanyName','InternalName','Comments']
        dictKeys = {'FileDescription': '描述', 'fileType': '类型', 'FileVersion': '文件版本', 'ProductName': '产品名称',
                    'ProductVersion': '产品版本',
                    'LegalCopyright': '版权', 'LegalTrademarks': '合法商标', 'OriginalFilename': '原始文件名', 'CompanyName': '公司',
                    'InternalName': '内部名称',
                    'Comments': '备注'}
        for i in range(len(self.listKeys)):
            tID = i + 1
            key = self.listKeys[i]
            key = dictKeys.get(key)
            if not isinstance(key,str) or len(key)<1:
                key = self.listKeys[i]
            label = wx.StaticText(panel,tID,key,pos=(10,10),size=wx.DefaultSize)
            textCtrl = wx.TextCtrl(panel, tID, '', pos=(10, 10), size=wx.DefaultSize)
            self.listItems.append(label)
            self.listItems.append((textCtrl,1,wx.EXPAND))

        self.label = wx.StaticText(panel,-1,'',pos=(10,10),size=wx.DefaultSize)
        self.button = wx.Button(panel, 1, "保存", pos=(100, 120))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.listItems.append((self.label,1,wx.EXPAND))
        self.listItems.append(self.button)

        row = int(len(self.listItems)/2)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(row, 2, 10, 10)    #5行，列，垂直间距，水平间距

        fgs.AddMany(self.listItems)
        fgs.AddGrowableRow(row-1, 1)
        fgs.AddGrowableCol(1, 1)
        hbox.Add(fgs, proportion=2, flag=wx.ALL | wx.EXPAND, border=15)
        panel.SetSizer(hbox)


    def GetTextValue(self,key):
        if self.listKeys.count(key) > 0:
            index = self.listKeys.index(key)
            textCtrl = self.listItems[index * 2 + 1][0]
            if FileO.Obj.cN(textCtrl) == 'TextCtrl':
                return textCtrl.GetValue()
        return None

    def SetTextValue(self,key,value):
        if self.listKeys.count(key) > 0:
            index = self.listKeys.index(key)
            textCtrl = self.listItems[index * 2 + 1][0]
            if FileO.Obj.cN(textCtrl) == 'TextCtrl':
                if value == None:value = ''
                textCtrl.SetLabel(value)
                # 设置插入点
                wx.CallAfter(textCtrl.SetInsertionPoint,0)
            else:
                print(FileO.Obj.cN(textCtrl), textCtrl)

    def UpdateUI(self,args=None):
        self.path = args
        content = FileO.readFileByEncode(args)

        # 分割
        listValue = re.findall('StringStruct\((.+)\)',content)
        # print(listValue)
        pattern = re.compile('u\'(.+)\', u\'(.*)\'')
        for x in listValue:
            tMatch = pattern.search(x)
            if tMatch != None and len(tMatch.groups())>0:
                key = tMatch.group(1)
                value = tMatch.group(2)
                # print(tMatch.groups())
                self.dictData[key] = value
                if key == 'FileVersion':
                    value = GetVerFromStr(content,'filevers')
                    # value = value.replace(' ', '')
                    # value = value.replace(',', '.')
                    # listMatch = re.findall('[\.0-9]+', content) #部分文件可能有后续部分，需要分割掉
                    # if len(listMatch) > 0:
                    #     value = listMatch[0]
                self.SetTextValue(key,value)
        tMatch = re.search('fileType=(.+)\,',content)
        if tMatch != None and len(tMatch.groups())>0:
            value = tMatch.group(1)
            self.dictData['fileType'] = value
            value = str(int(value, 16))
            self.SetTextValue('fileType',value)

    def OnClick(self,event=None):
        # print(self.dictData)
        isMatch = False
        content = self.GetTextValue('FileVersion')
        if not content.startswith('.') and len(content.split('.')) < 5:
            content = content.replace('.', '')
            tMatch = re.match("[0-9]*", content)
            if tMatch != None and tMatch.span()[1] == len(content):
                # print('OK')
                isMatch = True
        if not isMatch:
            wx.MessageBox("文件版本格式不正确", "提示", wx.OK | wx.ICON_WARNING)
            return
        content = FileO.readFileByEncode(self.path)
        for key in self.listKeys:
            oldValue = self.dictData.get(key)
            newValue = self.GetTextValue(key)
            if key == 'fileType':
                newValue = str(hex(int(newValue)))
                content = content.replace('fileType='+oldValue,'fileType='+newValue)
            else:
                oldValue = "StringStruct(u\'%s\', u\'%s\')"%(key,oldValue)
                rpValue = "StringStruct(u\'%s\', u\'%s\')" % (key, newValue)
                # print(oldValue,rpValue)
                content = content.replace(oldValue, rpValue)
                if key == 'FileVersion':
                    listVer = newValue.split('.')
                    tMatch = re.search('filevers=\((.+)\),', content)
                    if len(tMatch.groups())>0 and len(listVer)>0:
                        value = tMatch.group(1)
                        oldValue = 'filevers=(' + value + '),'
                        if len(listVer) < 4:
                            for i in range(4 - len(listVer)):
                                listVer.append('0')
                        newValue = ', '.join(listVer)
                        newValue = 'filevers=(' + newValue + '),'
                        # print(oldValue,newValue)
                        content = content.replace(oldValue, newValue)
            # print(oldValue,newValue)
        FileO.writeFile(self.path,content)
        wx.MessageBox('修改完成','提示',wx.OK|wx.ICON_INFORMATION)
        self.EndModal(wx.ID_OK)

def CustomVerText():
    content = "# UTF-8\n#\n# For more details about fixed file info 'ffi' see:\n# http://msdn.microsoft.com/en-us/library/ms646997.aspx\nVSVersionInfo(\n  ffi=FixedFileInfo(\n    # filevers and prodvers should be always a tuple with four items: (1, 2, 3)\n    # Set not needed items to zero 0.\n    filevers=(1, 0, 0, 0),\n    prodvers=(3, 0, 0, 0),\n    # Contains a bitmask that specifies the valid bits 'flags'r\n    mask=0x3f,\n    # Contains a bitmask that specifies the Boolean attributes of the file.\n    flags=0x0,\n    # The operating system for which this file was designed.\n    # 0x4 - NT and there is no need to change it.\n    OS=0x4,\n    # The general type of file.\n    # 0x1 - the file is an application.\n    fileType=0x1,\n    # The function of the file.\n    # 0x0 - the function is not defined for this fileType\n    subtype=0x0,\n    # Creation date and time stamp.\n    date=(0, 0)\n    ),\n  kids=[\n    StringFileInfo(\n      [\n      StringTable(\n        u'080904E4',\n        [StringStruct(u'CompanyName', u'华夏大地有限公司'),\n        StringStruct(u'FileDescription', u'Python打包工具'),\n        StringStruct(u'FileVersion', u'1.0'),\n        StringStruct(u'InternalName', u'config.exe'),\n        StringStruct(u'LegalCopyright', u'Copyright 2018'),\n        StringStruct(u'LegalTrademarks', u'YSL'),\n        StringStruct(u'OriginalFilename', u'config.exe'),\n        StringStruct(u'ProductName', u'Py生成器'),\n        StringStruct(u'ProductVersion', u'1.00'),\n        StringStruct(u'Comments', u'一个用来将py文件打包成exe文件的工具')])\n      ]), \n    VarFileInfo([VarStruct(u'Translation', [2057, 1252])])\n  ]\n)\n"
    return content

def GetVerFromStr(cString,key):
    tMatch = re.search('%s=\((.+)\),' % key, cString)
    value = ''
    if tMatch != None:
        value = tMatch.group(1)
        value = value.replace(' ','').replace(',', '.')
        # print(value)
    tMatch = re.search('items: \((.+)\)\n',cString)
    if tMatch != None:
        countStr = tMatch.group(1)
        if len(countStr) > 0:
            c = len(countStr.split(', '))
            if c < len(value.split('.')):
                listC = value.split('.')[0:c]
                value = '.'.join(listC)
        # print(tMatch.groups())
    return value

def getFileProperties(path):
    """
    读取给定文件的所有属性, 返回一个字典.
    """

    props = {'FixedFileInfo': None, 'StringFileInfo': None}

    # A = None
    try:
        fixedFileInfo = {'FixedFileInfo': None, 'StringFileInfo': {}}
        fixedInfo = win32api.GetFileVersionInfo(path, '\\')
        # print(fixedInfo.get('StrucVersion'))
        # print(fixedInfo.get('Signature'))

        struc = 65536
        fixedFileInfo['filevers'] = "%d.%d.%d.%d" % (
            fixedInfo.get('FileVersionMS') / struc, fixedInfo.get('FileVersionMS') % struc,
            fixedInfo.get('FileVersionLS') / struc, fixedInfo.get('FileVersionLS') % struc)
        fixedFileInfo['prodvers'] = "%d.%d.%d.%d" % (
            fixedInfo.get('ProductVersionMS') / struc, fixedInfo.get('ProductVersionMS') % struc,
            fixedInfo.get('ProductVersionLS') / struc, fixedInfo.get('ProductVersionLS') % struc)
        fixedFileInfo['mask'] = fixedInfo.get('FileFlagsMask')
        fixedFileInfo['flags'] = fixedInfo.get('FileFlags')
        fixedFileInfo['OS'] = fixedInfo.get('FileOS')
        fixedFileInfo['fileType'] = fixedInfo.get('FileType')
        fixedFileInfo['subtype'] = fixedInfo.get('FileSubtype')
        fixedFileInfo['date'] = fixedInfo.get('FileDate')
        props['FixedFileInfo'] = fixedFileInfo
        print(fixedFileInfo)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(path, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        propNames = ('Comments', 'InternalName', 'ProductName',
                     'CompanyName', 'LegalCopyright', 'ProductVersion',
                     'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                     'FileVersion', 'OriginalFilename', 'SpecialBuild',)
        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            ## print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(path, strInfoPath)

        props['StringFileInfo'] = strInfo
        print(strInfo)
    except Exception as e:
        print(e.__dict__)
        props['code'] = e.winerror
        props['msg'] = e.strerror

    return props

def GetFileInfo(path):
    content = CustomVerText()
    distData = getFileProperties(path)
    FixedFileInfo = distData.get('FixedFileInfo')
    StringFileInfo = distData.get('StringFileInfo')
    if not isinstance(FixedFileInfo,dict) or not isinstance(StringFileInfo,dict):
        dictResult = {'result': False}
        dictResult.update(distData)
        return (dictResult, content)
    verCount = 0
    for key in FixedFileInfo:
        value = FixedFileInfo.get(key)
        if key == 'filevers' or key == 'prodvers':
            tMatch = re.search('%s=\((.+)\),' % key, content)
            listVer = value.split('.')
            verCount = len(listVer)
            if tMatch != None and len(tMatch.groups()) > 0 and len(listVer) > 0:
                value = tMatch.group(1)
                oldValue = '%s=(' % key + value + '),'
                if len(listVer) < 4:
                    for i in range(4 - len(listVer)):
                        listVer.append('0')
                newValue = ', '.join(listVer)
                newValue = '%s=(' % key + newValue + '),'
                # print(oldValue, newValue)
                content = content.replace(oldValue, newValue)
        elif key != 'date':
            tMatch = re.search('%s=(.+),' % key, content)
            if tMatch != None and len(tMatch.groups()) > 0:
                oldValue = tMatch.group(1)
                oldValue = '%s=' % key + oldValue + ','
                newValue = str(hex(int(value)))
                newValue = '%s=' % key + newValue + ','
                # print(key,oldValue, newValue)
                content = content.replace(oldValue, newValue)
        else:
            tMatch = re.search('%s=\((.+)\)' % key, content)
            if tMatch != None and len(tMatch.groups())>0:
                print(tMatch.groups())
    if verCount > 0:
        oldValue = 'items: (1, 2, 3)\n'
        tList = []
        for i in range(verCount):
            tList.append('%d'%(i+1))
        newValue = 'items: (' + ', '.join(tList) + ')\n'
        # print(oldValue,newValue)
        content = content.replace(oldValue,newValue)
    for key in StringFileInfo:
        tMatch = re.search('StringStruct\(u\'%s\', u\'(.+)\'\)' % key, content)
        # print(tMatch)
        if tMatch != None and len(tMatch.groups()) > 0:
            value = StringFileInfo.get(key)
            if value == None : value = ''
            # print(tMatch.groups())
            oldValue = tMatch.group(1)
            oldValue = "StringStruct(u\'%s\', u\'%s\')" % (key, oldValue)
            newValue = "StringStruct(u\'%s\', u\'%s\')" % (key, value)
            # print(key, oldValue, newValue)
            content = content.replace(oldValue, newValue)

    dictResult = {'result': True, 'Path': path}
    return (dictResult,content)

def SaveFileInfo(path):
    dictResult,content = GetFileInfo(path)
    # print(content)
    if dictResult.get('result'):
        path = os.path.join(os.getcwd(),'file_version_info.txt')
        if FileO.GetExecuteExt() == '.py':
            path = 'E:\\PyProgramPack111\\Test.txt'
        # FileO.writeFile(path, content)
        dictResult = {'result': True,'content':content, 'Path': path}
    return dictResult

if __name__ == '__main__':
    app = wx.App()
    frame = ButtonFrame()
    # path = 'E:\\Python工程\\file_version_info.txt'
    path = 'E:\\PyProgramPack111\\Test.txt'
    frame.UpdateUI(path)
    frame.ShowModal()
    frame.Destroy()
    app.MainLoop()