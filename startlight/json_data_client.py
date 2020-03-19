#!/usr/bin/python3
from starlight import ErrSatistics

file_url = "http://172.16.26.1:12345/startlight_err_data.json"

errSatistics = ErrSatistics(file_url)
errSatistics.init()
errSatistics.printTotalErrByDay()
errSatistics.printErrInfoByCode()
errSatistics.printSpecificApi("GetUserCpuHours")
errSatistics.printSpecificDay("2020/03/19")