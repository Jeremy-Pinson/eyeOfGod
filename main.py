#main.py

from rtspFluxScanner import rtspFluxScannerStarter
from rtspIpFinder import rtspIPFinder
from multiprocessing import Process
import sys
import time


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("need 2 ip for range scan")
        exit()
    ip_start = sys.argv[1]
    Ip_end = sys.argv[2]
    RTSPIpList = []
    print("Scan from " + ip_start + " to " + Ip_end)

#parcour la range d'ip et cherche des port rtsp d'ouvert
    ipFinder = rtspIPFinder(ip_start, Ip_end)
    ipFinder.startScan()
    RTSPIpList = ipFinder.getRTSPList()

    print(RTSPIpList) #affiche la liste d'ip contenant des ports rtsp

    procces_list = []
    for i in RTSPIpList :
        procces = Process(target=rtspFluxScannerStarter, args=(i, ))
        procces_list.append(procces)
        procces.start()
        time.sleep(1)

    for i in procces_list:
        i.join()

    print("work done")