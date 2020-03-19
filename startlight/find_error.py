#!/usr/bin/python3
import os
import subprocess
import json

is_save_logs = True
target_day='2020/03/17'

class LogAnalyzerReslut:
    serviceName = ""
    apiName = ""
    totalErrs = 0
    tokenExpired = 0          # 1300 token失效
    errPasswd = 0             # 1402 密码和账户名不匹配
    userNotFound = 0          # 10403 找不到该用户
    mailFailed = 0            # 10110 邮件发送失败
    bihuPasswdIsNull = 0      # 10417 user bihupasswd is null
    permDenied = 0            # 10410 您没有权限进行当前的操作
    acctAlreadyBinded = 0     # 11102 此账号已经被绑定过
    timeOuts = 0              # 1110 请求超时
    interSrvFailed = 0        # 1500 服务间调用失败
    dbFailed = 0              # 1600 数据库调用失败
    deadlineExceeded =0       # 11203 DeadlineExceededcontext
    others = 0

    def __init__(self,serviceName,apiName):
        self.serviceName = serviceName
        self.apiName = apiName
        self.totalErrs = 0
        self.tokenExpired = 0          # 1300 token失效
        self.errPasswd = 0             # 1402 密码和账户名不匹配
        self.userNotFound = 0          # 10403 找不到该用户
        self.mailFailed = 0            # 10110 邮件发送失败
        self.bihuPasswdIsNull = 0      # 10417 user bihupasswd is null
        self.permDenied = 0            # 10410 您没有权限进行当前的操作
        self.acctAlreadyBinded = 0     # 11102 此账号已经被绑定过
        self.timeOuts = 0              # 1110 请求超时
        self.interSrvFailed = 0        # 1500 服务间调用失败
        self.dbFailed = 0              # 1600 数据库调用失败
        self.deadlineExceeded =0       # 11203 DeadlineExceededcontext
        self.others = 0

    def getOthers(self):
        self.others = self.totalErrs - self.tokenExpired - self.timeOuts - self.interSrvFailed - self.errPasswd -  self.userNotFound - self.mailFailed - self.bihuPasswdIsNull - self.permDenied - self.dbFailed - self.acctAlreadyBinded - self.deadlineExceeded
        return self.others

    def printMetaData():
        print(LogAnalyzerReslut.getMetaData())

    def getMetaData():
        metaData = "{:<12s}{:<30s}{:<6s}{:<6s}{:<6s}{:<6s}{:<6s}{:<6s}{:<6s}{:<6s}{:<6s}{:<6s}{:<6s}{:<6s}{:<6s}".format("srv_name","api_name","total","1300","1402","10403","10110","10417","10410","11102","1110","1500","1600","11203","others")
        return metaData

    def printData(self):
        print(self.getData())

    def getData(self):
        data = "{:<12s}{:<30s}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}".format(self.serviceName,self.apiName,self.totalErrs,self.tokenExpired,self.errPasswd,self.userNotFound,self.mailFailed,self.bihuPasswdIsNull,self.permDenied,self.acctAlreadyBinded,self.timeOuts,self.interSrvFailed,self.dbFailed,self.deadlineExceeded,self.getOthers())
        return data

    # 错误代码提示
    def getErrCodeDetails():
        details = {}
        details[1300] = "token失效"
        details[1402] = "密码和账户名不匹配"
        details[10403] = "找不到该用户"
        details[10110] = "邮件发送失败"
        details[10417] = "bihupasswd为空"
        details[10410] = "没有权限"
        details[11102] = "账号已被绑定"
        details[1110] = "请求超时"
        details[1500] = "服务间调用失败"
        details[1600] = "数据库调用失败"
        details[11203] = "gRPC超时"
        return details

    def getSumByErrType(logAnalyzerReslutList):
 #       countOfErrs = [0,0,0,0,0,0,0,0,0,0,0,0]
        totalErrs = 0
        tokenExpired = 0          # 1300
        errPasswd = 0             # 1402 密码和账户名不匹配
        userNotFound = 0          # 10403 找不到该用户
        mailFailed = 0            # 10110 邮件发送失败
        bihuPasswdIsNull = 0      # 10417 user bihupasswd is null
        permDenied = 0            # 10410 您没有权限进行当前的操作
        acctAlreadyBinded = 0     # 11102 此账号已经被绑定过
        timeOuts = 0              # 1110
        interSrvFailed = 0        # 1500 服务间调用失败
        dbFailed = 0              # 1600 数据库调用失败
        deadlineExceeded = 0
        others = 0
        for result in logAnalyzerReslutList:
            totalErrs = totalErrs + result.totalErrs
            tokenExpired = tokenExpired + result.tokenExpired
            errPasswd = errPasswd + result.errPasswd
            userNotFound = userNotFound + result.userNotFound
            mailFailed = mailFailed + result.mailFailed
            bihuPasswdIsNull = bihuPasswdIsNull + result.bihuPasswdIsNull
            permDenied = permDenied + result.permDenied
            acctAlreadyBinded = acctAlreadyBinded + result.acctAlreadyBinded
            timeOuts = timeOuts + result.timeOuts
            interSrvFailed = interSrvFailed + result.interSrvFailed
            dbFailed = dbFailed + result.dbFailed
            deadlineExceeded = deadlineExceeded + result.deadlineExceeded
            others = others + result.others
        return "{:<42s}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}{:<6d}".format("sum",totalErrs,tokenExpired,errPasswd,userNotFound,mailFailed,bihuPasswdIsNull,permDenied,acctAlreadyBinded,timeOuts,interSrvFailed,dbFailed,deadlineExceeded,others)

class StartLightLogAnalyzer:
    __service_api_dict = {}  # { serviceName : { apiName : []}} 存放错误日志
    __analyze_result_list = []  # [ {serviceName} ]
    __targetDay = ""
    __from = "k8s"

    def __init__(self,targetDay):
        self.__targetDay = targetDay

    def loadApiListFromFile(self,fileName):
        try:
            startlight_apis_file=open(fileName, mode='r')
            for line in startlight_apis_file:
                service_api = line.split("@")
                service_api[1] = service_api[1].rstrip('\n')
                self.addApi(service_api[0],service_api[1])
        finally:
            startlight_apis_file.close()

    def addApi(self,serviceName,apiName):
        if serviceName in self.__service_api_dict.keys():
            if apiName not in self.__service_api_dict[serviceName].keys():
                self.__service_api_dict[serviceName][apiName] = []
        else:
            self.__service_api_dict[serviceName] = { apiName : [] } 

    def analyze(self):
        for serviceName in self.__service_api_dict.keys():
            findPodCmd = "kubectl get pods -n sl-v4-pro |grep '\\-{}\\-' ".format(serviceName) + "| awk '{print $1}'"
            (status, podName)=subprocess.getstatusoutput(findPodCmd)
            if status != 0:
                print("failed to find {}'pod".format(serviceName))
                continue
            for apiName in self.__service_api_dict[serviceName].keys():
                print("finding errors of " + apiName)
                result = LogAnalyzerReslut(serviceName,apiName)
                findApiErrorLogsCmd = "kubectl logs -n sl-v4-pro {} | grep '{}' | grep '{}' |grep -v '200  ' | grep -v '接收访问请求' |grep '标识：'".format(podName,apiName,self.__targetDay)
                (status, logs)=subprocess.getstatusoutput(findApiErrorLogsCmd)
                if status == 0 and logs != "":
                    logListTmp = logs.split("\n")                   
                    self.__service_api_dict[serviceName][apiName] = self.__service_api_dict[serviceName][apiName] + logListTmp
                    logList = self.__service_api_dict[serviceName][apiName]
                    result.totalErrs = len(logList)
                    result.tokenExpired = self.__countSpecificErrs(logList,"1300 您的登陆信息无效")
                    result.errPasswd = self.__countSpecificErrs(logList,"1402 您输入的密码和账户名不匹配")
                    result.userNotFound = self.__countSpecificErrs(logList,"10403 找不到该用户")
                    result.mailFailed = self.__countSpecificErrs(logList,"10110 邮件发送失败")
                    result.bihuPasswdIsNull = self.__countSpecificErrs(logList,"10417 ")
                    result.permDenied = self.__countSpecificErrs(logList,"10410 ")
                    result.acctAlreadyBinded = self.__countSpecificErrs(logList,"11102 ")
                    result.timeOuts = self.__countSpecificErrs(logList,"1110 处理超时")
                    result.interSrvFailed = self.__countSpecificErrs(logList,"1500 服务间调用失败")   
                    result.dbFailed = self.__countSpecificErrs(logList,"1600 数据库调用失败") 
                    result.deadlineExceeded = self.__countSpecificErrs(logList,"11203 DeadlineExceededcontext")                       
                self.__analyze_result_list.append(result)
        print("analyzing completed")
        print("save result to disk ...")
        self.saveResultToFile()
        print("result saved")
        print("save err logs to disk ...")
        self.saveErrLogsToFile()
        print("err logs saved")

    def printAnalyzeResult(self):
        LogAnalyzerReslut.printMetaData()
        for result in self.__analyze_result_list:
            result.printData()
        print(LogAnalyzerReslut.getSumByErrType(self.__analyze_result_list))


    def saveResultToFile(self):
        day = self.__targetDay.replace("/","_")
        error_log_file = open("logs/startlight_err_info_of_{}.txt".format(day), mode='w')
        error_log_file.write(LogAnalyzerReslut.getMetaData() + "\n")
        for result in self.__analyze_result_list:
            error_log_file.write(result.getData() + "\n")
        error_log_file.write(LogAnalyzerReslut.getSumByErrType(self.__analyze_result_list) + "\n")
        error_log_file.write(str(LogAnalyzerReslut.getErrCodeDetails()) + "\n") # 打印错误代码提示
        error_log_file.close()

        try:
            json_data_file = open("data/startlight_err_data.json", mode='r') # 一行为一天的数据
            data_str = json_data_file.readline()
        except Exception as e:
            print(f"{e}")
        finally:
            json_data_file.close()
        
#        print("data_str is : " + data_str)
        if data_str == "":
            data_str = "{}"
        try:            
            data_dict = json.loads(data_str)  # 转成字典
        except Exception as e:
            print(f"{e}")
            return
        print(data_dict)
        data_dict[self.__targetDay] = []  # key为日期，value为接口的数组，数组的每一个元素为一个接口的信息
        for result in self.__analyze_result_list:
#            print("???")
            r_dict = result.__dict__
#            print(r_dict)
            data_dict[self.__targetDay].append(r_dict)
#            print(data_dict)
#            break
            # json_data_file.write(json.dumps() + "\n")
        json_data_file = open("data/startlight_err_data.json", mode='w')    
        # json_data_file.truncate() # 清空文件
        json_data_file.write(json.dumps(data_dict))
        json_data_file.close()      

    def saveErrLogsToFile(self):
        day = self.__targetDay.replace("/","_")
        error_log_file = open("logs/startlight_err_log_of_{}.log".format(day), mode='w')
        for serviceName in self.__service_api_dict.keys():
            for apiName in self.__service_api_dict[serviceName].keys():
                for log in self.__service_api_dict[serviceName][apiName]:
                    error_log_file.write(log + "\n")
        error_log_file.close()

    def __countSpecificErrs(self,errLogList,err_type):
        result = 0
        for log in errLogList:
            if err_type in log:
                result = result + 1
        return result

logAnalyer = StartLightLogAnalyzer(target_day)
logAnalyer.loadApiListFromFile("startlight_apis.txt")
logAnalyer.analyze()
logAnalyer.printAnalyzeResult()