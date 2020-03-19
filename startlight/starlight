#!/usr/bin/python3
import socket
import json
import requests
import matplotlib.pyplot as plt
import pandas as pd

class ErrSatistics:
	fileUrl = ""
	dataDict = {}
	dateList = []  # 日期
	codeTypeMap = {"1300":"tokenExpired" }
	codeTypeMap["1402"] = "errPasswd"
	codeTypeMap["10403"] = "userNotFound"
	codeTypeMap["10110"] = "mailFailed"
	codeTypeMap["10417"] = "bihuPasswdIsNull"
	codeTypeMap["10410"] = "permDenied"
	codeTypeMap["11102"] = "acctAlreadyBinded"
	codeTypeMap["1110"] = "timeOuts"
	codeTypeMap["1500"] = "interSrvFailed"
	codeTypeMap["1600"] = "dbFailed"
	codeTypeMap["11203"] = "deadlineExceeded"

	def __init__(self,fileUrl):
		self.fileUrl = fileUrl

	def init(self):
		res = requests.get(self.fileUrl)
		with open("data.log", 'wb') as f:
  			f.write(res.content)
		f.close()

		with open("data.log", 'r') as f:
			data_json = f.readline()
		f.close()

		dataDict = json.loads(data_json)

		self.dataDict = dataDict
		self.dateList = list(dataDict.keys())
		self.dateList.sort()


	def findKey(self,value):
		for key in self.codeTypeMap.keys():
			if self.codeTypeMap[key] == value:
				return key
		return ""

	def printTotalErr(self):
		total_list = []  # 所有接口的报错数
		for log_date in self.dateList:
			total = 0
			for api in self.dataDict[log_date]:
				total = total + api["totalErrs"]
			total_list.append(total)
	
		plt.plot(self.dateList,total_list)
		plt.xlabel('date')
		plt.ylabel('total errors')
		plt.title('total errors')
		plt.show()

	def printErrInfoByCode(self):
		for code in self.codeTypeMap.keys():
			self.printSpecificErrByCode(code)
		plt.legend() # 显示图例
		plt.title("error code")
		plt.show()

	# 打印每个报错类型的情况
	def printSpecificErrByCode(self,code):
		totalList = []
		for logDate  in self.dateList:
			total = 0
			for api in self.dataDict[logDate]:
				total = total + api[self.codeTypeMap[code]]
			totalList.append(total)
		plt.plot(self.dateList,totalList, label=code)


	# 画特定接口的报错
	def printSpecificApi(self,apiName):
		# data [[],[]] 没一个[]元素为每天的数据
		data = []
		for logDate  in self.dateList:
			today = []
			for api in self.dataDict[logDate]:
				if api['apiName'] == apiName:
					for code in self.codeTypeMap.keys():
						today.append(api[self.codeTypeMap[code]])
					break
			data.append(today)		     
		df = pd.DataFrame(data,index=self.dateList,columns=list(self.codeTypeMap.keys()))
		df.plot(kind='bar',stacked=True)

	# 画表格,显示单天信息
	def printSpecificDay(self, targetDay):
		label = []
		index = []
		data = []
		apiList = self.dataDict[targetDay] # [{api1},{api2}]
		for key in apiList[0]:   # 表头
			if key != "serviceName" and key != "apiName":
				code = self.findKey(key)
				if code != "":
					label.append(code)
				else:
					label.append(key)
		for api in apiList:   # api {"name":"adf","1600":20}
			xData = []
			for key in api.keys():
				if key == "serviceName":
					continue
				elif key == "apiName":
					index.append(api[key])
				else:
					xData.append(api[key])
			data.append(xData)
		df = pd.DataFrame(data,columns=label,index=index)
		return df