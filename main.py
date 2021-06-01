import cv2
from antispoofing import SmileDetection, BlinkingCounter
from face_comparison import FaceChecker
import argparse


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


print("Checking Smiling Video!")
res,frames= smile_detector.detect()
if res: #detected smile
    smile_detector.change_video_path(args.not_smiling_video)
    print("Checking Not Smiling Video!")
    res,f = smile_detector.detect()
    

    if res==0: #detected not smile
        frames.extend(f)
        print("Checking Blinking Video!")
        res,f = blink_counter.count()
        if res: #detects the blinking
            frames.extend(f)
            

            #finally check faces
            print("Checking Faces!")
            final_res=face_comp.check_faces(frames)
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







