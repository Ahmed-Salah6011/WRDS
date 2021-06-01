import cv2
import face_recognition


class FaceChecker():
    '''
        A class to check whther a reference image (ID image) contains the same face in another images
    '''
    def __init__(self,ref_image):
        self.ref = cv2.cvtColor(ref_image,cv2.COLOR_BGR2GRAY)
        self.ref = cv2.cvtColor(self.ref,cv2.COLOR_BGR2RGB)

        self.ref_encodings= self.get_face_encodings(self.ref)
    
    def get_face_encodings(self,image):
        '''
            input:
                image : the image to extract face encodings from it
            output:
                returns the face encodings in the image
            constrains:
                if there is more than on face in the image raise an error
        '''
        faceLoc = face_recognition.face_locations(image)
        if len(faceLoc) >1:
            raise Exception("Video should contain one person only!")

        encodeElon = face_recognition.face_encodings(image)[0] 

        return encodeElon
    
    def change_ref(self,image):
        '''
            helps if the user wants to change the ref image entered
        '''
        self.ref = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        self.ref = cv2.cvtColor(self.ref,cv2.COLOR_BGR2RGB)

        self.ref_encodings= self.get_face_encodings(self.ref)
    
    def check_faces(self,images,confidence=0.75):
        '''
            input:
                images: list of images contains faces and each one must have one face
                confidence: probabilty of acceptance 
            output:
                returns 1 if a percentage of hits is bigger than or equal the confidence 
                        0 otherwise
        '''
        hits=0
        for img in images:
            img= cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
            encodeElon= self.get_face_encodings(img)
            result = face_recognition.compare_faces([encodeElon],self.ref_encodings)[0]
            if result:
                hits +=1
        

        if hits/len(images) >= confidence:
            return 1
        
        return 0





ref= cv2.imread('bta2a.jpg')
face_comp = FaceChecker(ref)

img = cv2.imread('org.jpg')

print(face_comp.check_faces([img]))


