from os import fstat
import cv2
import numpy as np
from joblib import load
import dlib
from face_detection import FaceDetectorSSD
from face_alignment import FaceAlignment
import random
from scipy.spatial import distance as dist
from imutils import face_utils



class Antispoofing():
    '''
        The abstract class for antispoofing
    '''
    def __init__(self,video_path=None):
        self.video_path=video_path
    
    def detect(self):
        raise NotImplementedError
    
    def change_video_path(self,video_path):
        raise NotImplementedError

    def get_labels(self):
        '''
            return the labels
        '''
        raise NotImplementedError
    


class SmileDetection(Antispoofing):
    '''
        Class that checks smiling in videos using haarcascade classifiers in opencv
    '''
    def __init__(self,video_path=None,model_path=cv2.data.haarcascades +'haarcascade_smile.xml'):
        super().__init__(video_path)

        self.model_path = model_path
    
    def change_video_path(self,video_path):
        self.video_path= video_path

    def detect(self):
        '''
            algorithim:
                for each frame in video check whether a person is smilling or not usibg haarcascade classifier
            constrains:
                if more than one person in any frame, raise an error
            output:
                1 if smiling
                0 if not smiling
                None if not sure (some frames detects a smile and others not)

                also with a list of randomly chosen frames from the video
        '''
        vid = cv2.VideoCapture(self.video_path)
         
        detector= FaceDetectorSSD()
        face_align = FaceAlignment()
        smile_cascade = cv2.CascadeClassifier(self.model_path)



        frames=[]
        counter=[0,0]
        while vid.isOpened():
            ret,frame= vid.read()
            
            if not ret:
                break
            frames.append(frame)

            faces= detector.detect(frame)
            if len(faces)>1 :
                raise Exception("Video should contain one person only!")
            
            face= faces[0]

            roi = face_align.frontalize_face(face['box'], frame)

            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) 
            # roi_gray = frame[y:y + h, x:x + w]
            smiles = smile_cascade.detectMultiScale(gray, 1.8, 20)
            if len(smiles) != 0 :
                counter[1]+=1 #smile
            else:
                counter[0]+=1 #not smile

        vid.release()
        cv2.destroyAllWindows()
        ###
        length = len(frames)
        l= 15 if length>=30 else length//2 
        ###
        smiling= counter[1]
        not_smiling= counter[0]
        samples=random.sample(frames, l)
        if smiling/length > 0.6:
            return 1, samples #smile
        elif not_smiling/length >0.6:
            return 0, samples #not smile
        else:
            return None, samples #not consistant
    
    def get_labels(self):
        '''
            return the labels
        '''
        return ['Not Smile','Smile']


class BlinkingCounter(Antispoofing):
    '''
        class to count the number of blinks in a video
    '''
    def __init__(self,video_path=None,model_path='pretrained_models/shape_predictor_68_face_landmarks.dat'):
        super().__init__(video_path)

        self.model_path = model_path

    def change_video_path(self,video_path):
        self.video_path= video_path
    
    def _eye_aspect_ratio(self,eye):
        '''
            takes the eye landmarks and returns the EAR (Eye Aspect Ratio)
        '''
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        # return the eye aspect ratio
        return ear
    
    def count(self):
        '''
            counts the number of blinks in video by calculating the eye aspect ratio and
            then detects a blink based on a thershold

            also returns a list contains randomly chosen frames from the video
        '''
        EYE_AR_THRESH = 0.3
        EYE_AR_CONSEC_FRAMES = 3

        COUNTER = 0
        TOTAL = 0

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.model_path)

        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


        vid = cv2.VideoCapture(self.video_path)
         

        frames=[]


        while vid.isOpened():
            ret,frame= vid.read()
            

            if not ret:
                break
            frames.append(frame)
            
            
            # frame = cv2.resize(frame, (450,450))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # detect faces in the grayscale frame
            rects = detector(gray, 0)
            if len(rects)==0:
                continue

            if len(rects)>1 :
                raise Exception("Video should contain one person only!")

            rect=rects[0]
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = self._eye_aspect_ratio(leftEye)
            rightEAR = self._eye_aspect_ratio(rightEye)

            EAR = (leftEAR + rightEAR) / 2.0
            if EAR < EYE_AR_THRESH:
                COUNTER += 1
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1
                # reset the eye frame counter
                COUNTER = 0

        vid.release()
        cv2.destroyAllWindows()
        ##
        length = len(frames)
        l= 15 if length>=30 else length//2 
        ##
        samples=random.sample(frames, l)
        if TOTAL>= 5 and TOTAL<=10:
            return TOTAL,samples #all ok
        else:
            return 0,samples #not ok

            



            
                
            





