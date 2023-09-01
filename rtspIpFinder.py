#rtspIpFinder

import ipaddress
import socket

class rtspIPFinder:
    _ipListStart = None
    _IpListEnd = None
    _RTSPIpListe = []

    def __init__(self, ipListStart, ipListEnd) -> None:
        self._ipListStart = ipaddress.IPv4Address(ipListStart)
        self._ipListEnd = ipaddress.IPv4Address(ipListEnd)

    def __checkIfRtspIsOn(self, ip):
        print("try connect to: " + str(ip) + ":554")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Set a timeout for the connection attempt
            sock.connect((str(ip), 554))
            sock.close()
            self._RTSPIpListe.append(ip)
            print("rtsp port was found: " + str(ip))
            return 1
        except (socket.timeout, ConnectionRefusedError):
            print("rtsp port NOT found at: " + str(ip))
            return 0

    def startScan(self):
        ipIterator = self._ipListStart
        nbRTSPFound = 0
        nbIpScan = 0
    
        while ipIterator != self._ipListEnd:
            nbRTSPFound += self.__checkIfRtspIsOn(ipIterator)
            ipIterator += 1
            nbIpScan += 1
        print("Ip scan finish")
        print(str(nbIpScan) + " ip was scann")
        print(str(nbRTSPFound) + " rtsp ip was found")
    
    def getRTSPList(self):
        return self._RTSPIpListe
        
        

