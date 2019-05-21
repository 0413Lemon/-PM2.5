from tkinter import *
import wx
import pymysql
from tkinter.messagebox import *
from beijing import *
from chengdu import *
from shenyang import *
from shanghai import *
from guangzhou import *
from all import *
from register import *
class LoginPage(wx.Frame):
	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id, title = '登录界面', pos = (150,100), size = (300,200))
		panel = wx.Panel(self)  #创建画板
#创建标题，并设置字体
		self.title = wx.StaticText(panel,label = '用户登录', pos = (120,20))
		font = wx.Font(10,wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
		self.title.SetFont(font)
#创建输入，文字文本
		self.Tuser = wx.StaticText(panel, label = '用户名:', pos = (20, 50))
		self.Cuser = wx.TextCtrl(panel, pos = (70, 50), size = (200,25), style = wx.TE_LEFT)

		self.Tpass = wx.StaticText(panel, label = '密码:', pos = (20, 90))
		self.Cpass = wx.TextCtrl(panel, pos = (70, 90), size = (200,25), style = wx.TE_PASSWORD)

		self.Bcheck = wx.Button(panel, label = '登录', pos = (50,120), size = wx.DefaultSize, style = 0)
		self.Bcheck.Bind(wx.EVT_BUTTON, self.loginCheck)
		self.Bcancel = wx.Button(panel, label = '注册', pos = (150,120), size = wx.DefaultSize, style = 0)
		self.Bcancel.Bind(wx.EVT_BUTTON, self.OnclickCancel)

	def loginCheck(self, event):
		name = self.Cuser.GetValue()
		secret = self.Cpass.GetValue()
		#print(name)
		#print(type(name))
		name = "\""+str(name)+"\""
		#print (name)
		sql = "select * from users where username="+name
		db = pymysql.connect("localhost", "root", "123", "homework")
		cursor = db.cursor()
		cursor.execute(sql)
		reslist = cursor.fetchone()
		if reslist and reslist[1]==secret:
			if reslist[2]=='北京':
				self.Destroy()
				app = wx.App()
				frame = BJMyFrame(parent = None, id=-1)
				frame.Show()
				app.MainLoop()
			elif reslist[2]=='成都':
				self.Destroy()
				app = wx.App()
				frame = CDMyFrame(parent = None, id=-1)
				frame.Show()
				app.MainLoop()
			elif reslist[2]=='广州':
				self.Destroy()
				app = wx.App()
				frame = GZMyFrame(parent = None, id=-1)
				frame.Show()
				app.MainLoop()
			elif reslist[2]=='沈阳':
				self.Destroy()
				app = wx.App()
				frame = SYMyFrame(parent = None, id=-1)
				frame.Show()
				app.MainLoop()
			elif reslist[2]=='上海':
				self.Destroy()
				app = wx.App()
				frame = SHMyFrame(parent = None, id=-1)
				frame.Show()
				app.MainLoop()
			else:
				self.Destroy()
				app = wx.App()
				frame = allMyFrame(parent = None, id=-1)
				frame.Show()
				app.MainLoop()
		else:
			wx.MessageBox('账号或密码错误！',u"错误")


	def OnclickCancel(self, event):
		app = wx.App()
		frame = reMyFrame(parent = None, id=-1)
		frame.Show()
		app.MainLoop()

if __name__ == '__main__':
	app = wx.App()
	frame = LoginPage(parent = None, id=-1)
	frame.Show()
	app.MainLoop()