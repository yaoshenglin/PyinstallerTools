#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'YSL-PC'

import UIExtend
import CCommand
import FileO
import ShellScript
import CustomOrderDialog
import ParamSetDialog
import VerEditDialog
import wx
import os
import threading

class ButtonFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'PyInstaller打包工具', size=(350, 500))
        self.SetMinSize((350,255))
        self.Center()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        if UIExtend.GetIcon():
            self.SetIcon(UIExtend.GetIcon())

        panel = wx.Panel(self, -1)

        # self.p = None
        self.isKill = False
        self.isTasking = False
        self.delegate = None
        self.listParam = ['-F','-w']
        self.dictParam = {}
        self.dictParam['type'] = 'dir'

        self.label1 = wx.StaticText(panel, -1, '版本', size=wx.DefaultSize)
        self.label2 = wx.StaticText(panel, -1, '图标', size=wx.DefaultSize)
        self.label3 = wx.StaticText(panel, -1, '主文件', size=wx.DefaultSize)
        self.label4 = wx.StaticText(panel, -1, 'EXE名字', size=wx.DefaultSize)
        self.label5 = wx.StaticText(panel, -1, '', size=wx.DefaultSize)
        self.label6 = wx.StaticText(panel, -1, '', size=wx.DefaultSize)

        self.textCtrlVer = wx.TextCtrl(panel, -1, '', size=wx.DefaultSize)
        self.textCtrlVer.SetDropTarget(UIExtend.FileDrop(self.textCtrlVer))
        self.textCtrlIcon = wx.TextCtrl(panel, -1, '', size=wx.DefaultSize)
        self.textCtrlIcon.SetDropTarget(UIExtend.FileDrop(self.textCtrlIcon))
        self.textCtrlMain = wx.TextCtrl(panel, -1, '', size=wx.DefaultSize)
        self.textCtrlName = wx.TextCtrl(panel, -1, '', size=wx.DefaultSize)
        self.fileDrop = UIExtend.FileDrop(self.textCtrlName)  # 第1步，创建FileDrop对象，并把grid传给初始化函数
        self.textCtrlName.SetDropTarget(self.fileDrop)  # 第2步，调用grid的SetDropTarget函数，并把FileDrop对象传给它
        self.textCtrlMain.Disable()
        # textCtrl.SetHelpText("帮助")

        self.button = wx.Button(panel, -1, "开始", pos=(100, 120))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)

        self.textOut = wx.TextCtrl(panel, -1, '', pos=(200, 300), size=wx.DefaultSize, style = wx.TE_MULTILINE|wx.TE_RICH2|wx.TE_READONLY)
        self.textOut.SetEditable(False)
        self.textOut.Hide()

        listItems = [self.label1, (self.textCtrlVer, 1, wx.EXPAND), self.label2, (self.textCtrlIcon, 1, wx.EXPAND), self.label3, (self.textCtrlMain, 1, wx.EXPAND), self.label4,(self.textCtrlName, 1, wx.EXPAND),self.label5, self.button,self.label6,(self.textOut, 1, wx.EXPAND)]
        row = int(len(listItems)/2)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(row, 2, 10, 10)  # 3行，列，垂直间距，水平间距
        fgs.AddMany(listItems)
        fgs.AddGrowableRow(row-1, 1)
        fgs.AddGrowableCol(1, 1)
        hbox.Add(fgs, proportion=2, flag=wx.ALL | wx.EXPAND, border=15)
        panel.SetSizer(hbox)

        menuBar = wx.MenuBar()
        funcMenu = wx.Menu()
        # fileMenu.Title = "A"
        listMenuItems = ['参数设置','自定义','结束任务','删除pyo文件','删除多余文件夹']
        for i in range(len(listMenuItems)):
            mItem = listMenuItems[i]
            newItem = wx.MenuItem(funcMenu, id=i+1, text=mItem, kind=wx.ITEM_NORMAL)
            funcMenu.Append(newItem)
        menuBar.Append(funcMenu, title="功能")

        verMenu = wx.Menu()
        newItem = wx.MenuItem(funcMenu, id=11, text='生成版本文件', kind=wx.ITEM_NORMAL)
        verMenu.Append(newItem)
        newItem = wx.MenuItem(funcMenu, id=12, text='修改版本文件', kind=wx.ITEM_NORMAL)
        verMenu.Append(newItem)
        menuBar.Append(verMenu, title="版本")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.MenuEvents)

        self.funcMenu = funcMenu
        self.verMenu = verMenu
        self.funcMenu.Enable(3, False)

    def GetStrCommand(self):
        dicData = {}
        strCommand = ''
        Order = 'pyinstaller ' + ' '.join(self.listParam)
        dicData['Order'] = Order
        dicData['Name'] = self.textCtrlName.GetValue()
        dicData['Version'] = self.textCtrlVer.GetValue()
        dicData['Icon'] = self.textCtrlIcon.GetValue()
        dicData['Dir'] = self.dictParam.get('Dir')
        dicData['list'] = None
        dicData['Main'] = self.textCtrlMain.GetValue()
        if self.dictParam['type'] == 'dir':
            dicData['list'] = self.dictParam.get('list')
            strCommand = CCommand.ExtendShell(dicData=dicData)
        elif self.dictParam['type'] == 'file':
            strCommand = CCommand.GetShellCode(dicData)
        return strCommand

    def SetDelegate(self,args):
        self.delegate = args
        pass

    def EnableUI(self,enable=True):
        self.textCtrlVer.Enable(enable)
        self.textCtrlIcon.Enable(enable)
        self.textCtrlName.Enable(enable)
        self.button.Enable(enable)
        self.funcMenu.Enable(3, not enable)
        self.verMenu.Enable(11, enable)
        self.verMenu.Enable(12, enable)

    # 菜单栏操作事件
    def MenuEvents(self,event):
        EventId = event.GetId()
        if EventId == 1:
            # 参数设置
            ParamFrame = ParamSetDialog.ParamFrame(self.listParam)
            center = UIExtend.GetCenter(self)
            UIExtend.SetCenter(ParamFrame,center)
            ParamFrame.ShowModal()
            ParamFrame.Destroy()
        elif EventId == 2:
            # 自定义命令
            if not self.isTasking:
                strCommand = self.GetStrCommand()
                # dlg = wx.TextEntryDialog(None,'自定义命令','输入',strCommand)
                # dlg = UIExtend.MyTextDialog(None,'自定义命令','输入',strCommand)
                dlg = CustomOrderDialog.MyTextDialog(strCommand)
                if dlg.ShowModal() == wx.ID_OK:
                    message = dlg.GetValue()  # 获取文本框中输入的值
                    self.StartThreadint(message)
                    # print(message)
                dlg.Destroy()
                # dig = wx.TextEntryDialog(None, '自定义命令', '输入', '')
                # dig = wx.DirDialog(None, '', '', wx.DD_DEFAULT_STYLE)
                # dig.Destroy()
            else:
                wx.MessageBox("执行的命令还没有结束，无法操作", "提示", wx.OK | wx.ICON_WARNING)
        elif EventId == 3:
            self.KillProcess()
            self.textOut.AppendText('\n用户取消任务')

        elif EventId == 4:
            # 删除pyo文件
            fileDir = self.dictParam.get('Dir')
            listFile = os.listdir(fileDir)
            for name in listFile:
                ext = os.path.splitext(name)[1]
                if ext == '.pyo':
                    path = os.path.join(fileDir,name)
                    os.remove(path)
        elif EventId == 5:
            # 删除多余文件夹
            fileDir = self.dictParam.get('Dir')
            MainObj = self.textCtrlMain.GetValue()
            EName = self.textCtrlName.GetValue()
            CCommand.DeleteEndFile('手动删除', fileDir, MainObj, EName)
        elif EventId == 11:
            # 选择文件对话框
            filesFilter = "可执行文件 (*.exe)|*.exe|应用程序扩展 (.dll)|*.dll|All files (*.*)|*.*"
            dlg = wx.FileDialog(None,'选择可执行文件',wildcard = filesFilter)
            vID = dlg.ShowModal()
            Path = dlg.GetPath()  # 获取文本框中输入的值
            dlg.Destroy()
            if vID == wx.ID_OK:
                # Path = dlg.GetPath()  # 获取文本框中输入的值
                dictResult = VerEditDialog.SaveFileInfo(Path)
                result = dictResult.get('result')
                if result:
                    verPath = dictResult.get('Path')
                    filesFilter = "文本文件 (*.txt)|*.txt|All files (*.*)|*.*"
                    dlg = wx.FileDialog(None,'保存文件到路径',defaultFile=verPath, wildcard=filesFilter,style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
                    if dlg.ShowModal() == wx.ID_OK:
                        verPath = dlg.GetPath()  # 获取文本框中输入的值
                        content = dictResult.get('content') #将要写入的内容
                        FileO.writeFile(verPath, content)
                        wx.MessageBox("操作完成\n\n文件在目录：\n%s" % verPath, "提示", wx.OK | wx.ICON_INFORMATION)
                        if len(self.textCtrlVer.GetValue()) < 1 :
                            self.textCtrlVer.SetLabel(verPath)
                    dlg.Destroy()
                else:
                    msg = dictResult.get('msg')
                    wx.MessageBox("%s" % msg, "提示", wx.OK | wx.ICON_ERROR)
        elif EventId == 12:
            # 修改版本文件
            path = self.textCtrlVer.GetValue()
            if os.path.exists(path) and os.path.isfile(path):
                frame = VerEditDialog.ButtonFrame()
                frame.UpdateUI(path)
                frame.ShowModal()
                frame.Destroy()

    def OnClick(self,event):   #开始执行
        strCommand = self.GetStrCommand()
        self.StartThreadint(strCommand)

    def StartThreadint(self,strCommand):
        if len(strCommand)>0:
            self.isKill = False
            self.EnableUI(False)
            print(strCommand)
            self.textOut.Show()
            self.textOut.SetLabel('开始任务\n')
            # self.ExecuteCommand(strCommand)
            t = threading.Thread(target=self.ExecuteCommand, args=(strCommand,))
            t.setDaemon(True)  # 设置为守护线程
            t.start()
            # t.join(15)    # 进行线程同步，会阻塞主线程

    def ExecuteCommand(self, strCommand):
        self.isTasking = True
        ret_code = ShellScript.ShellCode(strCommand, self.textOut)
        print("操作返回错误代号：",ret_code)
        # self.textOut.AppendText("\n操作返回代号：%d" % return_code)
        print("结束任务")
        wx.CallAfter(self.EndCommand, ret_code)

    def EndCommand(self,ret_code):
        self.isTasking = False
        self.EnableUI()
        self.textOut.AppendText("\n结束任务")

        if ret_code == None or ret_code == 0:
            # self.textOut.AppendText("\n操作完成")
            wx.MessageBox("操作完成", "提示", wx.OK | wx.ICON_INFORMATION)
            retCode = wx.MessageBox("是否删除多余文件夹", "提示", wx.OK |wx.CANCEL | wx.ICON_MASK)
            if retCode == wx.OK:
                # 删除多余文件夹
                fileDir = self.dictParam.get('Dir')
                MainObj = self.textCtrlMain.GetValue()
                EName = self.textCtrlName.GetValue()
                CCommand.DeleteEndFile('手动删除', fileDir, MainObj, EName)
        else:
            # self.textOut.AppendText("\n操作失败，错误码：%d" % return_code)
            self.ShowMessage("操作失败，错误码：%d"%ret_code)

    def UpdateUI(self, args):
        # print(args)
        isDir = args.get('isDir')
        listFile = args.get('list')
        MainObj = args.get('Main')
        path = args.get('Dir')
        self.dictParam['list'] = listFile
        self.dictParam['Dir'] = path
        iconPath = ''
        verPath = ""
        curPath = os.getcwd()
        if isDir and len(listFile)>0:
            verPath = os.path.join(curPath, 'file_version_info.txt')
            iconPath = os.path.join(curPath,'icon\\favicon.ico')
            self.dictParam['type'] = 'dir'
            self.textCtrlName.SetLabel(os.path.split(path)[1])
        elif not isDir:
            verPath = os.path.join(curPath, 'file_version_info.txt')
            iconPath = os.path.join(curPath, 'icon\\favicon.ico')
            self.dictParam['type'] = 'file'
            self.textCtrlName.SetLabel(os.path.splitext(MainObj)[0])
        else:
            wx.MessageBox("路径不正确","提示",wx.OK|wx.ICON_INFORMATION)
            return
        if not os.path.exists(verPath):
            verPath = ""
        if not os.path.exists(iconPath):
            iconPath = ""
        self.textCtrlVer.SetLabel(verPath)
        self.textCtrlIcon.SetLabel(iconPath)
        self.textCtrlMain.SetLabel(MainObj)
        # print(args)
        if FileO.GetExecuteExt() == '.py' and path == 'E:\\Python工程\\测试工程\\PyInstaller打包工具':
            self.textCtrlIcon.SetLabel('E:\\Python工程\\icon\\bitbug_favicon.ico')

    def ShowMessage(self, content):
        return wx.MessageBox(content, "提示", wx.OK | wx.ICON_INFORMATION)

    def OnClose(self, evt):
        isExit = False
        if self.isTasking:
            ret = wx.MessageBox('任务还没有结束，你确定要退出?', '提示', wx.OK | wx.CANCEL)
            if ret == wx.OK:
                self.KillProcess()
                isExit = True
                # exit(0)
        else:
            isExit = True
        if isExit:
            evt.Skip()
            self.Destroy()
            if self.delegate != None:
                self.delegate.SetShow(True)

    def KillProcess(self):
        self.isKill = True
        ShellScript.KillProcess(['pyinstaller.exe'])
        # ShellScript.KillProcess('cmd.exe')
        fileDir = self.dictParam.get('Dir')
        MainObj = self.textCtrlMain.GetValue()
        EName = self.textCtrlName.GetValue()
        CCommand.DeleteEndFile("操作失败", fileDir, MainObj, EName)
        print("终止全部进程")

if __name__ == '__main__':
    listFile = ['contentFrame.py', 'wx_main.py', 'xDialog.py', 'utils.py', 'guiManager.py', 'loginFrame.py']
    strPath = "E:\\Python工程\\wxPyFrame"
    MainObj = 'wx_main.py'
    # strPath = "E:\\Python工程\\wxPyFrame\\wx_main.py"
    # MainObj = os.path.split(strPath)[1]
    app = wx.App()
    frame = ButtonFrame()
    frame.Show()
    frame.UpdateUI({'isDir': False, 'Dir': strPath, "Main": MainObj})
    frame.SetDelegate(None)
    # frame.UpdateUI({'path': strPath, "main": MainObj,'list':listFile})
    # frame.UpdateUI({'path': strPath, "main": MainObj})
    app.MainLoop()