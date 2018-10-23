#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'YSL-PC'

import wx
import os
import FileO
import UIExtend
import PyinstallerPack

class ButtonFrame(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '选择文件', size=(500, 300),style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.SetMinSize((500, 300))
        self.Center()

    def InitUI(self,path):
        panel = wx.Panel(self)

        self.delegate = None
        self.path = path
        self.MainObj = None

        font = wx.Font()
        # wx.Font(wx.SYS_SYSTEM_FONT)
        titleFont = font
        font.SetPointSize(9)
        titleFont.SetPointSize(12)

        # 间隙
        hvGap = 10;

        # 主布局、水平
        mainHBox = wx.BoxSizer(wx.HORIZONTAL)

        # 左侧布局、垂直
        leftVBox = wx.BoxSizer(wx.VERTICAL)

        # leftVBox.Add((-1, 10))

        # 案例标题
        st1 = wx.StaticText(panel, label=u'文件列表')
        st1.SetFont(titleFont)
        leftVBox.Add(st1, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=hvGap)

        # 案例列表
        listFile = os.listdir(path)
        self.checkListBox = wx.CheckListBox(panel, choices=listFile)
        self.Bind(wx.EVT_CHECKLISTBOX, self.onCheckListBoxSelect, self.checkListBox)
        leftVBox.Add(self.checkListBox, proportion=1, flag=wx.EXPAND | wx.ALL, border=hvGap)

        # 全选
        self.selectAllCheckBox = wx.CheckBox(panel, label=u'全选', style=wx.CHK_3STATE)
        self.selectAllCheckBox.SetFont(font)
        self.Bind(wx.EVT_CHECKBOX, self.onCheckBoxSelectAll, self.selectAllCheckBox)
        leftVBox.Add(self.selectAllCheckBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=hvGap)

        mainHBox.Add(leftVBox, proportion=3, flag=wx.EXPAND, border=hvGap)

        # 右侧布局、垂直
        rightVBbox = wx.BoxSizer(wx.VERTICAL)

        # 日志标题
        st2 = wx.StaticText(panel, label=u'选择主文件')
        st2.SetFont(titleFont)
        # st2.SetBackgroundColour('red')
        rightVBbox.Add(st2, flag= wx.RIGHT, border=hvGap)


        # 串口选择(下拉列表)
        self.ComChoice = wx.Choice(panel, choices=[], size=(100, 30))
        self.Bind(wx.EVT_CHOICE, self.onClickedChoice, self.ComChoice)
        rightVBbox.Add(self.ComChoice, flag=wx.RIGHT|wx.TOP|wx.EXPAND, border=10)

        rightVBbox.Add((-1, 10), proportion=1)

        # 刷新串口按钮
        self.refreshBtn = wx.Button(panel, label=u'下一步', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.onClickedRefreshBtn, self.refreshBtn)
        rightVBbox.Add(self.refreshBtn, proportion=0, flag=wx.BOTTOM, border=-5)

        mainHBox.Add(rightVBbox, proportion=2, flag=wx.EXPAND|wx.ALL, border=hvGap)

        panel.SetSizer(mainHBox)

        # 默认只选.py文件
        listCheckItems = []
        for i in range(len(listFile)):
            name = listFile[i]
            ext = os.path.splitext(name)[1]
            if ext.lower() == '.py':
                listCheckItems.append(i)
            else:
                FileO.List.RemoveObj(listCheckItems, i)
        self.checkListBox.SetCheckedItems(listCheckItems)   #设置勾选项目
        self.onCheckListBoxSelect()     #设置全选按钮状态
        if len(listCheckItems)>0:
            for i in listCheckItems:
                Obj = listFile[i]
                if Obj.lower() == 'main.py':
                    index = listCheckItems.index(i)
                    self.ComChoice.SetSelection(index)
                    self.MainObj = Obj

    def GetSelectedFiles(self):
        listItems = []
        for i in self.checkListBox.GetCheckedItems():
            Item = self.checkListBox.GetItems()[i]
            listItems.append(Item)
        return listItems

    def SetDelegate(self,args):
        self.delegate = args
        pass

    # check列表 是否选中
    def onCheckListBoxSelect(self,event=None):
        # 选中个数
        selectCount = len(self.checkListBox.GetCheckedItems())
        listItems = self.GetSelectedFiles()
        # print(listItems)
        self.ComChoice.SetItems(listItems)

        # 全不选
        if selectCount == 0:
            self.selectAllCheckBox.Set3StateValue(wx.CHK_UNCHECKED)
            pass
        # 全选
        elif selectCount == self.checkListBox.GetCount():
            self.selectAllCheckBox.Set3StateValue(wx.CHK_CHECKED)
            pass
        # 未全选
        else:
            self.selectAllCheckBox.Set3StateValue(wx.CHK_UNDETERMINED)
            pass
        pass

    # 全选按钮
    def onCheckBoxSelectAll(self, event):
        # self.selectListAll(self.selectAllCheckBox.Get3StateValue() == wx.CHK_CHECKED)
        if self.selectAllCheckBox.Get3StateValue() == wx.CHK_CHECKED:
            self.checkListBox.SetCheckedItems(range(0, self.checkListBox.GetCount()))
        else:
            self.checkListBox.SetCheckedItems([])
        listItems = self.GetSelectedFiles()
        self.ComChoice.SetItems(listItems)

    # 下拉列表
    def onClickedChoice(self, event):
        Object = event.GetEventObject()
        Item = Object.GetItems()[Object.GetSelection()]
        self.MainObj = Item
        # print(self.ComChoice.GetItems())
        # print(self.ComChoice.GetSelection())
        pass

    # 下一步
    def onClickedRefreshBtn(self, event):
        index = self.ComChoice.GetSelection()
        if index >= 0:
            if self.delegate != None:
                self.delegate.Hide()
            listFiles = self.GetSelectedFiles()
            frame = PyinstallerPack.ButtonFrame()
            frame.Show()
            frame.UpdateUI({'isDir': True, 'list': listFiles, 'Dir': self.path, "Main": self.MainObj})
            frame.SetDelegate(self.delegate)

            center = UIExtend.GetCenter(self)
            UIExtend.SetCenter(frame, center)
            self.EndModal(wx.ID_OK)
        else:
            wx.MessageBox('必须选择一个主文件才能进行下一步', '提示', wx.OK|wx.ICON_WARNING)

#--------------- end of class Frame1 --------------------
# program entry point ...
if __name__ == '__main__':
    app = wx.App()
    path = "E:\\Python工程\\测试工程\\PyInstaller打包工具"
    frame = ButtonFrame()
    frame.InitUI(path)
    frame.ShowModal()
    frame.Destroy()
    app.MainLoop()


