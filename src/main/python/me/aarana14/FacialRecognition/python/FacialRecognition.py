import os
import cv2
import threading
import time
import concurrent.futures
from DetRec import DetecRecog
from UserInterface import Facial_RecognitionApp

class FacialDetecRecog:
    def runDetRec(self):
        while True:
            self.det_rec_out.main()
            cv2.imshow('Video', self.det_rec_out.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def runUI(self):
        self.userInter = Facial_RecognitionApp(self.det_rec_out.getRET(), self.det_rec_out.getFrame()).run()            
        # self.userInter.setNewFrame(self.det_rec_out.getRET(), self.det_rec_out.getFrame())

    def __init__(self):
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     faceThread = executor.submit(self.runDetRec)
        #     return_value = faceThread.result()
        faceThread = threading.Thread(target=self.runDetRec, args=())
        uiThread = threading.Thread(target=self.runUI, args=())
        self.det_rec_out = DetecRecog(os.getcwd())
        faceThread.start()
        # uiThread.start()

if __name__ == "__main__":
    FacialDetecRecog()