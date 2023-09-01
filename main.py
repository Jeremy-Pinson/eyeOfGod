#main.py

from rtspFluxScanner import rtspFluxScanner
from rtspIpFinder import rtspIPFinder

ip = "92.151.95.124"
False_ip = "92.151.95.123"

ipFinder = rtspIPFinder("92.151.95.120", "92.151.95.130")
ipFinder.startScan()
RTSPIpList = ipFinder.getRTSPList()
print(RTSPIpList)
#flusScanner = rtspFluxScanner(False_ip)
#flusScanner.Analize()