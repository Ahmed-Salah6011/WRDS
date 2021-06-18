import cv2
import sys
import numpy as np
import os
from antispoofing import SmileDetection,BlinkingCounter
from face_comparison import FaceChecker

def write_frames(frames,type,dir='faces/'):
    i=0
    for frame in frames:
        cv2.imwrite(os.path.join(dir,'{}_{}.jpg'.format(type,i)),frame)
        i+=1

if(sys.argv[1]=="1"):
    smile = SmileDetection("videos/test.MKV")
    res, frames = smile.detect()
    if(res ==1):
        write_frames(frames,"smile","random_images/")
        print(1)
    elif res==-1:
        print(-1)
    else:
        print(0)

elif(sys.argv[1]=="2"):
    smile = SmileDetection("videos/test.MKV")
    res, frames = smile.detect()
    if (res ==0):
        write_frames(frames,"not_smile","random_images/")
        print(1)
    elif res==-1:
        print(-1)
    else:
        print(0)

elif(sys.argv[1]=="3"):
    blink = BlinkingCounter("videos/test.MKV")
    res, frames = blink.count()
    if(res >= 5 and res <=10):
        write_frames(frames,"blink","random_images/")
        print(1)
    elif res==-1:
        print(-1)
    else:
        print(0)

elif(sys.argv[1]=="4"):
    ref= cv2.imread("uploads/ID_front.jpg")
    face_comp = FaceChecker(ref)
    final_res=face_comp.check_faces(images_directory='random_images/')
    if(final_res==1):
        print(1)
    elif final_res == -1:
        print(-1)
    else:
        print(0)
    sys.exit()
