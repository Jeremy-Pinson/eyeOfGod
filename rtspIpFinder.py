#rtspIpFinder

import ipaddress
import socket
import threading
import time

class rtspIPFinder:
    _ipListStart = None
    _IpListEnd = None
    _NbRTSPFound = 0
    _RTSPIpListe = []

    def __init__(self, ipListStart, ipListEnd) -> None:
        self._ipListStart = ipaddress.IPv4Address(ipListStart)
        self._ipListEnd = ipaddress.IPv4Address(ipListEnd)

    def __checkIfRtspIsOn(self, ip):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Set a timeout for the connection attempt
            sock.connect((str(ip), 554))
            sock.close()
            self._RTSPIpListe.append(str(ip))
            print("rtsp port was found: " + str(ip))
            self._NbRTSPFound += 1
            return 1
        except (socket.timeout, ConnectionRefusedError):
            return 0

    def startScan(self):
        ipIterator = self._ipListStart
        
        nbIpScan = 0
        Thread_list = []
    
        while ipIterator != self._ipListEnd:
            thread = threading.Thread(target=self.__checkIfRtspIsOn, args=(ipIterator,))
            Thread_list.append(thread)
            ipIterator += 1
            nbIpScan += 1
    
        for i in Thread_list:
            time.sleep(0.01)
            i.start()

        for i in Thread_list:
            i.join()

        print("Ip scan finish")
        print(str(nbIpScan) + " ip was scann")
        print(str(self._NbRTSPFound) + " rtsp ip was found")
    
    def getRTSPList(self):
        return self._RTSPIpListe
        
        

