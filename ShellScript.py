#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'YSL-PC'

import wx
import sys
import chardet
import psutil
import subprocess

def ExitProgress():
    sys.exit()

# def ExecuteCode(strCommand,textOut=None):
#     wx.CallAfter(UpdateText, textOut, "开始任务")
#     ret_code = os.system(strCommand)  # 执行shell命令
#     print(ret_code)
#     return ret_code

def ShellCode(strCommand,textOut=None):
    # wx.CallAfter(UpdateText, textOut, "准备任务")
    # ret_code = os.system(strCommand)  # 执行shell命令

    print("开始任务")
    p = subprocess.Popen(strCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    while True:
        data = p.stdout.readline()
        if data == b'':
            if p.poll() != None:
                # print('break',ps.poll())
                break
        else:
            tEncode = chardet.detect(data)["encoding"]
            s = data.decode(tEncode)
            wx.CallAfter(UpdateText, textOut, s)
            # print('Sum of requests from LAN:', len(newlist))

    ret_code = p.returncode
    p.terminate()   #终结任务(=kill)
    return ret_code

def UpdateText(textOut,s,Show=False):
    textOut.AppendText(s)
    if not textOut.IsShown() and Show == True:
        textOut.Show()

def KillProcess(listName):
   """raises the exception, performs cleanup if needed"""
   pids = psutil.pids()
   for pid in pids:
       p = psutil.Process(pid)
       name = p.name()
       if name in listName:
           print(name, pid)
           p.kill()
