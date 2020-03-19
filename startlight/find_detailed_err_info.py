#!/usr/bin/python3
import os
import subprocess
import json
import sys

serviceName = sys.argv[1]
print(serviceName)
findPodCmd = "kubectl get pods -n sl-v4-pro |grep '\\-{}\\-' ".format(serviceName) + "| awk '{print $1}'"
print(findPodCmd)
(status, podName)=subprocess.getstatusoutput(findPodCmd)
if status != 0:
	print("failed to find {}'pod".format(serviceName))
else:
	#print("pad name is " + podName)
	findApiErrorLogsCmd = "kubectl logs -n sl-v4-pro {} ".format(podName)
	(status, podName)=subprocess.getstatusoutput(findApiErrorLogsCmd)