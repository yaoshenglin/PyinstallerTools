#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'YSL-PC'

import UIExtend
import FileBoxDialog
import PyinstallerPack
import FileO
import os
import wx
import sys

class ButtonFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'PyInstaller打包工具', size=(350, 500))
        self.Center()
        if UIExtend.GetIcon():
            self.SetIcon(UIExtend.GetIcon())

        panel = wx.Panel(self, -1)

        self.isEndTask = True

        self.label1 = wx.StaticText(panel, -1, '文件路径', pos=(100, 60), size=wx.DefaultSize)
        self.label2 = wx.StaticText(panel, -1, '', pos=(100, 30), size=wx.DefaultSize)

        self.textCtrl = wx.TextCtrl(panel, -1, '', pos=(200, 10), size=wx.DefaultSize)
        self.fileDrop = UIExtend.FileDrop(self.textCtrl)  # 第1步，创建FileDrop对象，并把grid传给初始化函数
        self.textCtrl.SetDropTarget(self.fileDrop)  # 第2步，调用grid的SetDropTarget函数，并把FileDrop对象传给它
        self.textCtrl.SetHelpText("帮助")

        self.button = wx.Button(panel, -1, "下一步", pos=(100, 120))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()

        row = 2
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(row, 2, 10, 10)    #5行，列，垂直间距，水平间距

        fgs.AddMany([(self.label1), (self.textCtrl, 1, wx.EXPAND), self.label2, self.button])
        fgs.AddGrowableRow(row-1, 1)
        fgs.AddGrowableCol(1, 1)
        hbox.Add(fgs, proportion=2, flag=wx.ALL | wx.EXPAND, border=15)
        panel.SetSizer(hbox)

    def OnClick(self, event):
        strPath = self.textCtrl.GetValue()
        if len(strPath) == 0 :
            self.ShowMessage("路径不能为空")
        elif not (os.path.exists(strPath)):
            self.ShowMessage("文件不存在")
        elif os.path.isdir(strPath):
            # 目录
            WxFrame = FileBoxDialog.ButtonFrame()
            WxFrame.InitUI(strPath)
            WxFrame.SetDelegate(self)
            center = UIExtend.GetCenter(self)
            UIExtend.SetCenter(WxFrame,center)
            WxFrame.ShowModal()
            WxFrame.Destroy()
        else:
            # 单个文件
            (strDir,MainObj) = os.path.split(strPath)
            frame = PyinstallerPack.ButtonFrame()
            frame.Show()
            frame.UpdateUI({'isDir':False,'Dir': strDir, "Main": MainObj})
            frame.SetDelegate(self)
            self.Hide()
            center = UIExtend.GetCenter(self)
            UIExtend.SetCenter(frame, center)

    def ShowMessage(self, content):
        wx.MessageBox(content, "提示", wx.OK | wx.ICON_INFORMATION)
        pass

    def SetShow(self,isShow):
        # print('isShow',isShow)
        self.Show(isShow)

if __name__ == '__main__':
    app = wx.App()
    frame = ButtonFrame()
    frame.Show()
    if FileO.GetExecuteExt() == '.py':
        path = 'E:\\Python工程\\测试工程\\PyInstaller打包工具'
        frame.textCtrl.SetLabel("E:\\Python工程\\测试工程\\PyInstaller打包工具")
        # frame.textCtrl.SetLabel("E:\\Python工程\\测试工程\\实时监控指定股票价格.py")
        curPath = FileO.GetCurDir()
        if os.path.split(curPath)[1] == os.path.split(path)[1]:
            listFile = os.listdir(curPath)
            for fileName in listFile:
                if fileName.endswith('.py'):
                    curFilePath = os.path.join(curPath,fileName)
                    tarFilePath = os.path.join(path,fileName)
                    if not os.path.exists(tarFilePath) or os.stat(curFilePath).st_mtime != os.stat(tarFilePath).st_mtime:
                        FileO.CopyFile(curFilePath,path)
    # os.system('cls')
    # os.system('cmd.exe')
    app.MainLoop()