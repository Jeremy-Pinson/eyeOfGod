#main.py

from rtspFluxScanner import rtspFluxScannerStarter
from rtspIpFinder import rtspIPFinder
import threading

ip_start = "193.250.0.0"
Ip_end = "193.254.255.255"
RTSPIpList = []

ipFinder = rtspIPFinder(ip_start, Ip_end)
ipFinder.startScan()
RTSPIpList = ipFinder.getRTSPList()

print(RTSPIpList)

threads_list = []
for i in RTSPIpList :
    thread = threading.Thread(target=rtspFluxScannerStarter, args=(i,))
    threads_list.append(thread)

for i in threads_list:
    i.start()

for i in threads_list:
    i.join()

print("work done")