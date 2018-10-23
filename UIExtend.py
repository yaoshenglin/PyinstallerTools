#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'YSL-PC'

import wx
import os
import win32api #获取执行文件情况

# 文件拖动操作
class FileDrop(wx.FileDropTarget):
    def __init__(self, object):
        wx.FileDropTarget.__init__(self)
        self.textCtrl = object

    def OnDropFiles(self, x, y, filePath):  # 当文件被拖入后，会调用此方法
        # print(filePath)
        if len(filePath) > 0:
            strPath = filePath[0]
            self.textCtrl.SetLabelText(strPath)
        else:
            print("文件路径不存在")
        return 0

def Dialog():
    listData = ["Alpha", "Baker", "Charlie", "Delta"]
    dialog = wx.SingleChoiceDialog(None, "选择一个值", "标题", listData)
    if dialog.ShowModal() == wx.ID_OK:
        print("You selected: %s\n" % dialog.GetStringSelection())
    dialog.Destroy()

    dlg = wx.TextEntryDialog(None, "请输入姓名:", "文本框标题", "")
    if dlg.ShowModal() == wx.ID_OK:
        message = dlg.GetValue()  # 获取文本框中输入的值
        print(message)
    dlg.Destroy()

def GetCenter(Obj):
    pos = Obj.GetPosition()
    size = Obj.GetSize()
    center = wx.Point()
    center.x = pos.x + size.Width/2
    center.y = pos.y + size.Height/2
    return center

def SetCenter(Obj,center):
    size = Obj.GetSize()
    pos = wx.Point()
    pos.x = center.x - size.Width/2
    pos.y = center.y - size.Height/2
    Obj.SetPosition(pos)

def GetIcon():
    exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
    Icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
    return Icon

def SetIcon(Object,path=None):
    if isinstance(path,str) and os.path.exists(path):
        Icon = wx.Icon(path, wx.BITMAP_TYPE_ICO)
    else:
        exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
        Icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
    Object.SetIcon(Icon)

if __name__ == '__main__':
	pass