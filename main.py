#main.py

from rtspFluxScanner import rtspFluxScannerStarter
from rtspIpFinder import rtspIPFinder
import threading

ip_start = "192.168.1.0"
Ip_end = "192.168.1.200"
RTSPIpList = []

#parcour la range d'ip et cherche des port rtsp d'ouvert
ipFinder = rtspIPFinder(ip_start, Ip_end)
ipFinder.startScan()
RTSPIpList = ipFinder.getRTSPList()

print(RTSPIpList) #affiche la liste d'ip contenant des ports rtsp

threads_list = []
for i in RTSPIpList :
    thread = threading.Thread(target=rtspFluxScannerStarter, args=(i,))
    threads_list.append(thread)

for i in threads_list:
    i.start()

for i in threads_list:
    i.join()

print("work done")