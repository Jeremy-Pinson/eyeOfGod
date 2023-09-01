import cv2
import os
import time
from rtsp_path import RTSP_local_path

class rtspFluxScanner:
    _ip = None
    _rtsp_path = None
    def __init__(self, _ip) -> None:
        self._ip = _ip

    def __rtsp_path_finder(self):
        # cherche le path du stream
        for i in RTSP_local_path:
            if i == "end":
                print("No stream found: Path not found")
                return None
            rtsp_url = "rtsp://" + self._ip + "/" + i
            cap = cv2.VideoCapture(rtsp_url)
                
            if cap.isOpened():
                print("a stream was find at: " + rtsp_url)
                break
            else:
                print(i + ": path dosnt work")
        self._rtsp_path = rtsp_url
        print("Camera stream open")
        return cap
    
    #Reseptione le flux video
    def __rtsp_flux_reader(self, cap):
        ret, frame = cap.read()
        print("Reading flux")
        if not ret:
            print("Rtsp path was found: " + self._rtsp_path + "; but cant read it")
            return None
        time.sleep(3) #attend que le flux ce stabilise pour prendre la capture
        return frame
    
    #savegarde les data
    def __rtsp_data_saver(self, frame):
        screenPath = self._ip + "/" + self._ip + ".jpg"
        dataPath = self._ip + "/" + self._ip + ".txt"
        if not os.path.exists(self._ip):
            os.mkdir(self._ip)

        #sauvegarde le path complet dans un fichier texte
        f = open(dataPath, "a")
        f.write(self._rtsp_path)
        f.close()

        #sauvegarde un screenshot de la camera en jpg
        cv2.imwrite(screenPath, frame)

        print("Stream was on at: " + self._rtsp_path)
        print("screen was save at " + screenPath)

    #Fonction principale, lance l'execution de la classe
    def Analize(self):
        cap = self.__rtsp_path_finder()
        if cap is None:
            return 84
        frame = self.__rtsp_flux_reader(cap)
        if frame is None:
            return 84
        self.__rtsp_data_saver(frame)
        cap.release()
        return 0
