import face_recognition
import cv2
import numpy as np
import os
import glob

def setUp(current_dir):
    path = os.path.join(current_dir, 'FacialRecognition/data/faces/')
    list_of_files = []
    for dirpath,_,filenames in os.walk(path):
        for name in filenames:
            if name.endswith('.jpg'):
                list_of_files.append(os.path.join(path, dirpath,name))
    number_files = len(list_of_files)
    return list_of_files.copy(), number_files, list_of_files

#Associates images with a people
def imageAssociation(names, number_files, list_of_files):
    faces_encodings = []
    faces_names = []
    for i in range(number_files):
        globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
        globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
        faces_encodings.append(globals()['image_encoding_{}'.format(i)])
        names[i] = names[i].replace(current_dir, "")
        names[i] = names[i].replace("\\FacialRecognition/data/faces/", "")
        names[i] = names[i].replace(".jpg", "")
        names[i] = names[i].replace("-", " ")
        names[i] = names[i][0 : names[i].find("\\")]
        names[i] = names[i].upper()
        faces_names.append(names[i])
    return faces_names, faces_encodings

def webCam(video_capture):
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    return video_capture, rgb_small_frame, small_frame, ret, frame

def display(frame, face_locations, face_names):
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        
        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
        
        # Input text label with a name below the face
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left, bottom + 25), font, 0.7, (255, 255, 255), 1)
    
    # Display the resulting image
    cv2.imshow('Video', frame)

def recognition(face_names, face_encoding):
    matches = face_recognition.compare_faces(faces_encodings, face_encoding)
    name = "Unknown"
    face_distances = face_recognition.face_distance(faces_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = faces_names[best_match_index]
    face_names.append(name)
    return face_names, name

def main(faces_names, faces_encodings):
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    video_capture = cv2.VideoCapture(0)

    while True:
        video_capture, rgb_small_frame, small_frame, ret, frame = webCam(video_capture)

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            face_names = []
            for face_encoding in face_encodings:
                face_names, name = recognition(face_names, face_encoding)

        process_this_frame = not process_this_frame
        
        display(frame, face_locations, face_names)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    current_dir = os.getcwd()
    names, number_files, list_of_files = setUp(current_dir)
    faces_names, faces_encodings = imageAssociation(names, number_files, list_of_files)
    main(faces_names, faces_encodings)