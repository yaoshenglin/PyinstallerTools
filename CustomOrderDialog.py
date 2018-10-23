#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'YSL-PC'

import FileO
import wx
#(self, parent=None, id=None, title=None, pos=None, size=None, style=None, name=None)
class MyTextDialog(wx.Dialog):
    def __init__(self,value=''):
        wx.Dialog.__init__(self, None, -1, '自定义',size=(500, 200),style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.SetMinSize((500,200))

        panel = wx.Panel(self, -1)  #父容器
        label = wx.StaticText(panel, -1, '输入命令', pos=(100, 60), size=wx.DefaultSize)
        self.textOut = wx.TextCtrl(panel, -1, value, pos=(0, 0), size=wx.DefaultSize, style=wx.TE_MULTILINE | wx.TE_RICH2)
        line = wx.StaticLine(panel, -1)

        fullBox = wx.BoxSizer(wx.VERTICAL) # 垂直布局
        fullBox.Add(label, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM |wx.TOP, border=10)  #信息提示label
        fullBox.Add(self.textOut, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=15)   #输入框
        fullBox.Add(line, flag=wx.ALL | wx.EXPAND, border=10)    #线条

        btnBox = wx.BoxSizer(wx.HORIZONTAL) # 水平布局
        tLabel = wx.StaticText(panel, label='')
        # tLabel.SetBackgroundColour('red')
        btnBox.Add(tLabel, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)  #用来挤占下边左边区域
        btnOK = wx.Button(panel, wx.ID_OK, "确定", pos=(100, 120))
        btnCancel = wx.Button(panel, wx.ID_CANCEL, "取消", pos=(100, 120))
        btnBox.Add(btnOK, proportion=0,flag=wx.RIGHT, border=10)         #OK按钮
        btnBox.Add(btnCancel, proportion=0,flag=wx.RIGHT, border=10)    #Cancel按钮

        fullBox.Add(btnBox, flag=wx.BOTTOM | wx.RIGHT|wx.EXPAND, border=10)

        panel.SetSizer(fullBox)
    def GetValue(self):
        return self.textOut.GetValue()