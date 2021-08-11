import face_recognition
import cv2
import numpy as np
import os
import glob

class DetecRecog: 
    def __init__(self, current_dir):
        self.current_dir = current_dir
        self.setUp()
        self.imageAssociation()
        print("Done")

    def setUp(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        path = os.path.join(self.current_dir, 'FacialRecognition/data/faces/')
        list_of_files = []
        for dirpath,_,filenames in os.walk(path):
            for name in filenames:
                if name.endswith('.jpg'):
                    list_of_files.append(os.path.join(path, dirpath,name))
        number_files = len(list_of_files)
        self.names = list_of_files.copy()
        self.number_files = number_files
        self.list_of_files = list_of_files
        self.video_capture = cv2.VideoCapture(0)
        self.ret, self.frame = self.video_capture.read()

    #Associates images with a people
    def imageAssociation(self):
        faces_encodings = []
        faces_names = []
        for i in range(self.number_files):
            globals()['image_{}'.format(i)] = face_recognition.load_image_file(self.list_of_files[i])
            globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
            faces_encodings.append(globals()['image_encoding_{}'.format(i)])
            self.names[i] = self.names[i].replace(self.current_dir, "")
            self.names[i] = self.names[i].replace("\\FacialRecognition/data/faces/", "")
            self.names[i] = self.names[i].replace(".jpg", "")
            self.names[i] = self.names[i].replace("-", " ")
            self.names[i] = self.names[i][0 : self.names[i].find("\\")]
            self.names[i] = self.names[i].upper()
            faces_names.append(self.names[i])
        self.faces_names = faces_names
        self.faces_encodings = faces_encodings

    def webCam(self):
        self.ret, self.frame = self.video_capture.read()
        small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        return rgb_small_frame, small_frame

    def display(self):
        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # Draw a rectangle around the face
            cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 255, 0), 1)
            
            # Input text label with a name below the face
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.frame, name, (left, bottom + 25), font, 0.7, (255, 255, 255), 1)

    def recognition(self):
        matches = face_recognition.compare_faces(self.faces_encodings, self.face_encoding)
        self.name = "Unknown"
        face_distances = face_recognition.face_distance(self.faces_encodings, self.face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            self.name = self.faces_names[best_match_index]
        self.face_names.append(self.name)

    def main(self):
        self.rgb_small_frame, self.small_frame = self.webCam()

        if self.process_this_frame:
            self.face_locations = face_recognition.face_locations(self.rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(self.rgb_small_frame, self.face_locations)
            
            self.face_names = []
            for self.face_encoding in self.face_encodings:
                self.recognition()

        self.process_this_frame = not self.process_this_frame
        
        self.display()
            
    def getFrame(self):
        return self.frame

    def getRET(self):
        return self.ret