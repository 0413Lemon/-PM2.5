import wx
from tkinter import *
import    os
import pymysql
import matplotlib.pyplot as plt  # plt用于显示图片
import matplotlib.image as mping  # mping用于读取图片
import matplotlib.dates as mdates
from pylab import *

class GZMyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id=1, title = '广州PM2.5查询', pos = (150,100), size = (500,600))
        panel = wx.Panel(self)  #创建画板
#创建标题，并设置字体
        self.title = wx.StaticText(panel,label = '广州PM2.5查询', pos = (200,50))
        font = wx.Font(16,wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        self.title.SetFont(font)
#创建输入，文字文本
        #年
        self.Tyear = wx.StaticText(panel, label = '年:', pos = (50, 120))
        self.Cyear = wx.TextCtrl(panel, pos = (80, 120), size = (360,25), style = wx.TE_LEFT)
        #月
        self.Tmonth = wx.StaticText(panel, label = '月:', pos = (50, 170))
        self.Cmonth = wx.TextCtrl(panel, pos = (80, 170), size = (360,25), style = wx.TE_LEFT)
        #日
        self.Tday = wx.StaticText(panel, label = '日:', pos = (50, 230))
        self.Cday = wx.TextCtrl(panel, pos = (80, 230), size = (360,25), style = wx.TE_LEFT)
        #时
        self.Thour = wx.StaticText(panel, label = '时:', pos = (50, 280))
        self.Chour = wx.TextCtrl(panel, pos = (80, 280), size = (360,25), style = wx.TE_LEFT)
#查询结果输出框
        self.TOut = wx.StaticText(panel, label = '查询结果:', pos = (20, 350))
        self.COut = wx.TextCtrl(panel, pos = (80, 350), size = (360,30))
#两个按钮，‘查询’和‘清空’
        self.Bcheck = wx.Button(panel, label = '查询', pos = (100,420), size = wx.DefaultSize, style = 0)
        self.Bcheck.Bind(wx.EVT_BUTTON, self.OnclickCheck)
        self.Bcancel = wx.Button(panel, label = '清空', pos = (300,420), size = wx.DefaultSize, style = 0)
        self.Bcancel.Bind(wx.EVT_BUTTON, self.OnclickCancel)
#点击确定按钮
    def OnclickCheck(self, event):
        #获取输入框的值
        year = self.Cyear.GetValue()
        month = self.Cmonth.GetValue()
        day = self.Cday.GetValue()
        hour = self.Chour.GetValue()
#先判断地点，查询不同的表
#再判断输入时间是否符合
        if year and month and day and hour:
                self.COut.SetValue("")
                sql = "select Site,Parameter,Date,Value,Unit,Duration,QCName from guangzhou where Year=%s and Month=%s and Day=%s and Hour=%s"%(year,month,day,hour) 
                allvalue(self,sql)
        elif year and month and day and not hour:
            self.COut.SetValue("")
            #mysql3(site, year, month, day)
            data = mysql2(year, month, day)
            draw_trend_chart(data,'广州',str(year)+"年"+str(month)+"月"+str(day) +"号")

        elif year and month and not day and not hour:
            self.COut.SetValue("")
            data = mysql3(year, month)
            draw_trend_chart(data,'广州',str(year)+"年"+str(month) + "月（每日平均值）")
#点击清空按钮
    def OnclickCancel(self, event):
        self.Cyear.SetValue("")
        self.Cmonth.SetValue("")
        self.Cday.SetValue("")
        self.Chour.SetValue("")
        self.COut.SetValue("")

def allvalue(self,sql1):
    db = pymysql.connect("localhost", "root", "123", "homework")
    cursor = db.cursor()
    #创建一个cursor对象,帮助我们执行sql语句
    cursor.execute(sql1)
    reslist = cursor.fetchone()
    if reslist:
        for item in reslist:
            self.COut.AppendText(str(item)+' ')
    else:
        self.COut.AppendText('时间输入错误')
    cursor.close()
    db.close()
########################################################################

#一天的图像
def mysql2(year,month,day):
    db = pymysql.connect(host="localhost", user="root", password="123", database="homework")
    # 用cursor创建一个游标对象cursor
    cursor = db.cursor()
    TableName = 'guangzhou'
    sql = 'select Value,Hour from ' + TableName +  " where Year=%s and Month=%s and Day=%s" % (year,month,day)
    cursor.execute(sql)
    result = cursor.fetchmany(24)
    Time = []
    Value = []
    for i in result:
        Time.append(i[1])
        Value.append(i[0])
    # 关闭数据库
    cursor.close()
    db.close()
    return [Time,Value]

#########################################################
#求一个图像（平均值）
def mysql3(year,month):
    db = pymysql.connect(host="localhost", user="root", password="123", database="homework")
    # 用cursor创建一个游标对象cursor
    cursor = db.cursor()
    TableName = 'guangzhou'
    str1 = "select Value,Day from "+ TableName + " where Year=%s and Month=%s" % (year, month)
    cursor.execute(str1)
    result = cursor.fetchall()
    Value = []
    Time = []
    for i in result:
        Time.append(i[1])
        Value.append(i[0])
    # 关闭数据库
    cursor.close()
    db.close()
    Value2 = []
    Time2 = []
    j = Time[0]
    #计算平均值
    sum = 0
    cnt = 0
    index = 0
    Time2.append(1)
    for i in Time:
        if i == j:
            sum += int(Value[index])
            cnt += 1
            index+=1
        else :
            Value2.append(sum/cnt)
            Time2.append(i)
            j = i
            cnt = 0
            sum = 0
    Value2.append(sum/cnt)
    return [Time2,Value2]

def draw_trend_chart(data,site,value):
    x = data[0]
    y = data[1]
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    plt.figure()
    plt.plot(x, y, "r", linewidth=1)
    plt.title( site + "PM2.5" + value+"状况")  # 标题
    plt.savefig("图片")  # 保存图片名称
    lena = mping.imread('图片.png')  # 读取图片文件信息
    lena.shape
    plt.title(site + value + " PM2.5"+"状况")
    plt.show()