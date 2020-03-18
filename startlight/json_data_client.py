#!/usr/bin/python3
import socket
import json
import requests
import matplotlib.pyplot as plt
import pandas as pd

file_url = "http://172.16.26.1:12345/startlight_err_data.json"

class ErrSatistics:
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

	def __init__(self,dataDict):
		self.dataDict = dataDict
		self.dateList = list(dataDict.keys())
		self.dateList.sort()

	def printTotalErrByDay(self):
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
		df = pd.DataFrame(np.random.rand(10, 3), columns=['a', 'b','c'])
		totalList = []
		for logDate  in self.dateList:
			total = 0
			for api in self.dataDict[logDate]:
				if api['apiName'] == apiName:
					total = total + api['totalErrs']
					break
			totalList.append(total)
		plt.plot(self.dateList,totalList)
		plt.title(apiName)
		plt.show()


res = requests.get(file_url)
with open("data.log", 'wb') as f:
  f.write(res.content)
f.close()

with open("data.log", 'r') as f:
	data_json = f.readline()
f.close()

data_dict = json.loads(data_json)
#print(data_dict)

errSatistics = ErrSatistics(data_dict)
errSatistics.printErrInfoByCode()
errSatistics.printSpecificApi("GetGroupHistoryJobByCluster")