import cv2
import sys
import numpy as np
import os
from antispoofing import SmileDetection,BlinkingCounter

def write_frames(frames,type,dir='faces/'):
    i=0
    for frame in frames:
        cv2.imwrite(os.path.join(dir,'{}_{}.jpg'.format(type,i)),frame)
        i+=1

if(sys.argv[1]=="1"):
    smile = SmileDetection("test_m.MKV")
    res, frames = smile.detect()
    if(res):
        write_frames(frames,"smile","random_images/")
        print(1)
    else:
        print(0)

elif(sys.argv[1]=="2"):
    smile = SmileDetection("test_m.MKV")
    res, frames = smile.detect()
    if not (res):
        write_frames(frames,"not_smile","random_images/")
        print(1)
    else:
        print(0)

elif(sys.argv[1]=="3"):
    blink = BlinkingCounter("test_m.MKV")
    res, frames = blink.count()
    if(res):
        write_frames(frames,"blink","random_images/")
        print(1)
    else:
        print(0)
