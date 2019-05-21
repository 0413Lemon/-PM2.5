# coding=utf-8
import wx
import pymysql
class reMyFrame(wx.Frame):
	"""docstring for register"""
	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id, title = '用户注册', pos = (500,200), size = (400,450))
		panel = wx.Panel(self)  #创建画板

		self.Tuser = wx.StaticText(panel, label = '用户名:', pos = (10, 70))
		self.Cuser = wx.TextCtrl(panel, pos = (90, 70), size = (250,25), style = wx.TE_LEFT)

		self.Tpasswd = wx.StaticText(panel, label = '密码:', pos = (10, 100))
		self.Cpass = wx.TextCtrl(panel, pos = (90, 100), size = (250,25), style = wx.TE_PASSWORD)

		self.Tpasswd_again = wx.StaticText(panel, label = '再次输入密码:', pos = (10, 130))
		self.Cpasswd_again = wx.TextCtrl(panel, pos = (90, 130), size = (250,25), style = wx.TE_PASSWORD)

		self.Tadd = wx.StaticText(panel, label = '地址:', pos = (10, 160))
		self.Cadd = wx.TextCtrl(panel,value="例如：北京、上海、沈阳、成都、广州、all", pos = (90, 160), size = (250,25), style = wx.TE_LEFT)

		self.Bcheck = wx.Button(panel, label = '注册', pos = (80,250), size = wx.DefaultSize, style = 0)
		self.Bcheck.Bind(wx.EVT_BUTTON, self.onCheck)
		self.Bcancel = wx.Button(panel, label = '取消', pos = (220,250), size = wx.DefaultSize, style = 0)
		self.Bcancel.Bind(wx.EVT_BUTTON, self.onCancel)

	def onCheck(self, event):
		user = self.Cuser.GetValue()
		passwd = self.Cpass.GetValue()
		passwd_again = self.Cpasswd_again.GetValue()
		if passwd == passwd_again:
			add = self.Cadd.GetValue()
			db = pymysql.connect("localhost", "root", "123", "homework")
			cursor = db.cursor()
			user = "\"" +user+"\""
			add = "\'"+add+"\'"
			sql = "select * from users where username = %s"%(user)
			cursor.execute(sql)
			reslist = cursor.fetchone()
			cursor.close()
			db.close()
			if False:
				wx.MessageBox('用户名已存在！',u"错误")
			else:
				passwd = "\"" +passwd+"\""
				#print(user + add + passwd)
				db = pymysql.connect("localhost", "root", "123", "homework")
				cursor = db.cursor()
				sql1 = 'insert into users' + '(username,password,address) values('+user + ','+ passwd + ','+ add+')'

				print(sql1)
				cursor.execute(sql1)
				wx.MessageBox('注册成功！',u"成功")
			cursor.close()
			db.commit()
			db.close()
		else:
			wx.MessageBox('密码输入错误！',u"密码错误")
	def onCancel(self, event):
		self.Destroy()


# if __name__ == '__main__':
#     app = wx.App()
#     frame = reMyFrame(parent = None, id=-1)
#     frame.Show()
#     app.MainLoop()