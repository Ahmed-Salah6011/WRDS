import cv2
from antispoofing import SmileDetection, BlinkingCounter
from face_comparison import FaceChecker
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-sv", "--smiling_video", required=True,help="path to smiling video")
ap.add_argument("-nsv", "--not_smiling_video", required=True,help="path to not smiling video")
ap.add_argument("-bv", "--blinking_video", required=True,help="path to blinking video")
ap.add_argument("-r", "--ref", required=True,help="path to reference image")
args = ap.parse_args()

ref= cv2.imread(args.ref)

smile_detector= SmileDetection(args.smiling_video)
blink_counter= BlinkingCounter(args.blinking_video)
face_comp = FaceChecker(ref)


def write_frames(frames,type,dir='faces/'):
    i=0
    for frame in frames:
        cv2.imwrite(os.path.join(dir,'{}_{}.jpg'.format(type,i)),frame)
        i+=1

print("Checking Smiling Video!")
res,frames= smile_detector.detect()


if res: #detected smile
    write_frames(frames,'smile')

    smile_detector.change_video_path(args.not_smiling_video)
    print("Checking Not Smiling Video!")
    res,frames = smile_detector.detect()
    
    

    if res==0: #detected not smile
        write_frames(frames,'not_smile')

        print("Checking Blinking Video!")
        res,frames= blink_counter.count()

        if res: #detects the blinking
            write_frames(frames,'blink')

            #finally check faces
            print("Checking Faces!")
            final_res=face_comp.check_faces(images_directory='faces/')
            if final_res:
                print("ALL CLEAR!")
            else :
                print("NOT CLEAR!")
        
        else:
            print("Error in Blinking Video :(")

    else:
        print("Error in Not Smiling Video :(")

else:
    print("Error in Smiling Video :(")







