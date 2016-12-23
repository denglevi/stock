# encoding:utf-8
import wx

app = wx.App()

frame = wx.Frame(None, -1, u"股票分析系统")
frame.ShowFullScreen(True,style=0)

app.MainLoop()