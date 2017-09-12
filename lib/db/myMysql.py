#!/usr/bin/python
#-*- coding:utf-8 -*-

import MySQLdb

class mymysql:
	#def __init__(self,db,host="128.199.227.220",user="fscan",passwd="fscan123",port=3306):
	def __init__(self, db, host="45.55.79.161", user="root", passwd="toorsec!502", port=3306):

		self.config={'db':db,
					'host':host,
					'user':user,
					'passwd':passwd,
					'port':port,
					'charset':'utf8',
					'unix_socket':'/tmp/mysql.sock'
					}					
		self.conn = MySQLdb.connect(**self.config)
		self.cursor = self.conn.cursor()
		self.cursor.execute("SET NAMES UTF8")
		self.id=[]

	#data = [(x,y,z),(a,b,c)]格式,columns=(column1,column2,column3)
	def insert(self,table,columns,data):
		values = []
		for x in xrange(len(data[0])):
			values.append("%s")
		sqli = "insert into "+table+"("+",".join(columns)+") values("+",".join(values)+")"
		self.cursor.executemany(sqli,data)	
		self.conn.commit()


    #qcolumn = (a,b,c)格式
    #qcolumn = [a,b,c]格式
	def query(self,table,qcolumn,wcolumn = 1,wvalue= 1):
		sqlq ="select "+",".join(qcolumn)+" from %s where %s=%s" % (table,wcolumn,wvalue)
		if len(qcolumn) == 1:
			sqlq = "select distinct(%s) from %s where %s=%s" % (qcolumn[0],table,wcolumn,wvalue)
		self.cursor.execute(sqlq)
		data = self.cursor.fetchall()
		return data

	def delete(self,table,column,value):
		sqld = "delete from %s where %s='%s'" % (table,column,value)
		self.cursor.execute(sqld)
		self.conn.commit()
    
    #data =[(column1,newvalue,column2,value2)]
	def update(self,table,data):
		sqlu = "update table set %s = '%s' where %s = '%s'"
		self.cursor.executemany(sqlu,data)
		self.conn.commit()

	def execsql(self,sql):
		self.cursor.execute(sql)
		self.conn.commit()

	def __del__(self):
		self.cursor.close()
		self.conn.close()
	def queryPrikey(self,table,column="id"):
		temp=self.query(table,(column,))
		ids=[]
		for i in temp:
			ids.append(i[0])
		return ids
	def queryPrikey1(self,table,column="id",nums=100):
		sqlq ="select "+column+" from "+table+" order by rand() limit "+str(nums)
		self.cursor.execute(sqlq)
		data = self.cursor.fetchall()		
		ids=[]
		for i in data:
			ids.append(i[0])
		return ids
    #value = [3,1,2] 格式
	def deletePrikey(self,table,value,prikey):
		#print table,value,column
		sqlq = "delete from %s where %s in (%s)" % (table,prikey,",".join(value))
		self.cursor.execute(sqlq)
	#columns = ["username","password"] 格式
	#value = ['3','1','2'] 格式
	def queryColumns(self,table,columns,value,prikey):
		#print table,value,columns
		sqlq = "select %s from %s where %s in (%s)" % (",".join(columns),table,prikey,",".join(value))
		self.cursor.execute(sqlq)
		data = self.cursor.fetchall()
		return data




