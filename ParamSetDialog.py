#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'YSL-PC'

import CCommand
import FileO
import wx

class ParamFrame(wx.Dialog):
    def __init__(self,args):
        wx.Dialog.__init__(self, None, -1, '参数', size=(250, 200),style=wx.CAPTION|wx.CLOSE_BOX)
        self.Center()

        panel = wx.Panel(self, -1)
        self.listParam = args

        listItems = []
        listItemNames = ['单个文件','显示命令行窗口','生成log文件','编译前清理']
        for i in range(len(listItemNames)):
            Id = i + 1
            name = listItemNames[i]
            self.btn_Cb = wx.CheckBox(panel, Id, name, pos=wx.DefaultPosition, size=wx.DefaultSize)
            self.btn_Cb.Bind(wx.EVT_CHECKBOX, self.OnClick)
            # self.btn_Cb.SetValue(0)
            listItems.append(self.btn_Cb)
            value = CCommand.ConvertParam(name)
            isExist = value in self.listParam
            if value == '-c':
                value = '-w'
                isExist = not value in self.listParam
            self.btn_Cb.SetValue(isExist)

        row = int(len(listItems)/2)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(row, 2, 10, 10)    #3行，列，垂直间距，水平间距

        fgs.AddMany(listItems)
        fgs.AddGrowableRow(row-1, 1)
        fgs.AddGrowableCol(1, 1)
        hbox.Add(fgs, proportion=2, flag=wx.ALL | wx.EXPAND, border=15)
        panel.SetSizer(hbox)

    def SetDelegate(self,args):
        self.delegate = args
        pass
    def OnClick(self, event):   #开始执行
        Object = event.GetEventObject()
        name = Object.GetLabel()
        state = Object.GetValue()
        value = CCommand.ConvertParam(name)
        if value == '-c':
            value = '-w'
            state = not state
        if state:
            self.listParam.append(value)
        else:
            FileO.List.RemoveObj(self.listParam, value)
        # print(self.listParam)

    def UpdateUI(self, args):
        print(args)
        pass

if __name__ == '__main__':
    listFile = ['contentFrame.py', 'wx_main.py', 'xDialog.py', 'utils.py', 'guiManager.py', 'loginFrame.py']
    strPath = "E:\\Python工程\\wxPyFrame"
    MainObj = 'wx_main.py'
    # strPath = "E:\\Python工程\\wxPyFrame\\wx_main.py"
    # MainObj = os.path.split(strPath)[1]
    app = wx.App()
    frame = ParamFrame(['-F','-w'])
    frame.Show()
    frame.UpdateUI({'path': strPath, "main": MainObj,'list':listFile})
    # frame.UpdateUI({'path': strPath, "main": MainObj})
    app.MainLoop()
    print(frame.listParam)