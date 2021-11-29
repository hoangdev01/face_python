import face_recognition
from database import Database
from imutils import paths
import cv2
import pickle
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
class Render:
    known_face_encodings = []
    known_face_names = []
    known_face_ID = []
    def __init__(self, folderName, databaseName):
        self.imagePaths = list(paths.list_images(folderName))
        self.db = Database(databaseName)
    def renderInfo(self):
        for (i, imagePath) in enumerate(self.imagePaths):
            personImage = face_recognition.load_image_file(imagePath)   
            self.known_face_encodings.append(face_recognition.face_encodings(personImage)[0] )
        # print(self.known_face_encodings)
        data = {"encodings": self.known_face_encodings}
        with open("encodings.pickle", "wb") as f:
            f.write(pickle.dumps(data))
        data = pickle.load(open("encodings.pickle","rb")) 
        return data["encodings"]
    def getInfo(self):
        for (i, imagePath) in enumerate(self.imagePaths):
            id,name = self.db.getProfile(imagePath.split(".")[1])  
            self.known_face_names.append(str(name))
            self.known_face_ID.append(str(id))
        return (self.known_face_ID, self.known_face_names)
    def getEncode(self):
        with open('encodings.pickle', 'rb') as f:
            data = pickle.load(f)
        return data["encodings"]
