#main.py

from rtspFluxScanner import rtspFluxScannerStarter
from rtspIpFinder import rtspIPFinder
from multiprocessing import Process


if __name__ == "__main__":
    ip_start = "109.190.0.0"
    Ip_end = "109.190.50.0"
    RTSPIpList = []

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

    for i in procces_list:
        i.join()

    print("work done")