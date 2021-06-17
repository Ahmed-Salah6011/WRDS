import cv2
import os
import face_recognition
import numpy as np

class FaceChecker():
    '''
        A class to check whther a reference image (ID image) contains the same face in another images
    '''
    def __init__(self,ref_image):
        self.ref = cv2.cvtColor(ref_image,cv2.COLOR_BGR2GRAY)
        self.ref = cv2.cvtColor(self.ref,cv2.COLOR_BGR2RGB)

        self.ref_encodings= self.get_face_encodings(self.ref)
        self.images=[]
    
    def upload_images_from_directory(self,directory):
        '''
            gets the path of directory in which imagaes of faces are saved
            and loads them in self.images
        '''
        files= os.listdir(directory)
        for file in files:
            img = cv2.imread(os.path.join(directory,file))
            self.images.append(img)

    
    def get_face_encodings(self,image):
        '''
            input:
                image : the image to extract face encodings from it
            output:
                returns the face encodings in the image
            constrains:
                if there is more than on face in the image raise an error
        '''
        try:
            faceLoc = face_recognition.face_locations(image)
            if len(faceLoc) != 1:
                raise RuntimeError("Video should contain one person only!")

            encodeElon = face_recognition.face_encodings(image)[0] 

            return encodeElon,1
        except RuntimeError:
            return [-1],-1
            
    
    def change_ref(self,image):
        '''
            helps if the user wants to change the ref image entered
        '''
        self.ref = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        self.ref = cv2.cvtColor(self.ref,cv2.COLOR_BGR2RGB)

        self.ref_encodings= self.get_face_encodings(self.ref)
    
    
    def check_faces(self,images_directory,confidence=0.75):
        '''
            input:
                confidence: probabilty of acceptance 
            output:
                returns 1 if a percentage of hits is bigger than or equal the confidence 
                        0 otherwise
            algorithim: check the faces in self.images
        '''
        self.upload_images_from_directory(images_directory)
        encs=[]
        for img in self.images:
            img= cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
            encodeElon,ret= self.get_face_encodings(img)
            if ret == -1:
                print(-1)
                break
            encs.append(encodeElon)

        if ret != -1:
            results = face_recognition.compare_faces(encs,self.ref_encodings)
            hits= np.sum(np.array(results,dtype='int'))
            if hits/len(self.images) >= confidence:
                return 1
        
        return 0





# ref= cv2.imread('bta2a.jpg')
# face_comp = FaceChecker(ref)

# img = cv2.imread('org.jpg')

# print(face_comp.check_faces([img]))


