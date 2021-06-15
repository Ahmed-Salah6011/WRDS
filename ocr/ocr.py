from os import name
from ArabicOcr import arabicocr
import cv2
import numpy as np
import re
	#<==========Start of Blurring and Edging==============>
def img_preprocess(img_path):
	image = cv2.imread(img_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# blurred = cv2.GaussianBlur(gray, (11,11), 0)
	# edged = cv2.Canny(blurred, 30, 110, 30)
	# cv2.imwrite("edged_" +img_path.split('/')[-1],gray)
	return gray
	#<==========End of Blurring and Edging==============>

	#<==========Start SIFT Method============>
def rotate_bound(image,angle):
	(h,w) = image.shape[:2]
	#Define rotation matrix
	center = (h//2, w//2)
	# angle = 30 # A negative value will rotate the image clockwise
	scale = 1.0
	rotationMatrix = cv2.getRotationMatrix2D(center, angle, scale)

	# Rotate the image

	# rotation calculates the cos and sin, taking absolutes of those.
	abs_cos = abs(rotationMatrix[0,0]) 
	abs_sin = abs(rotationMatrix[0,1])

	# find the new width and height bounds
	bound_w = int(h * abs_sin + w * abs_cos)
	bound_h = int(h * abs_cos + w * abs_sin)

	# subtract old image center (bringing image back to origo) and adding the new image center coordinates
	rotationMatrix[0, 2] += bound_w/2 - center[0]
	rotationMatrix[1, 2] += bound_h/2 - center[1]

	# rotate image with the new bounds and translated rotation matrix
	rotatedImage = cv2.warpAffine(image, rotationMatrix, (bound_w, bound_h))


	# rotatedImage = cv2.warpAffine(image, rotationMatrix,(image.shape[1],image.shape[0]))
	return rotatedImage

def detect_rotation(warp, matrix):
    """
    @Input : warp, matrix 
    		
    @Output : warp
    
    @Intent :   Detect rotation of the detected ID 
   				this function uses the output matrix from findHomography function 
    			to evaluate two angles then we use arctan2 to get the angle between two lines 
    			we then rotate the warped image to be 0 angled
    
    @Assumptions (The less assumptions, the less coupling in the code) : 
    - right data format, no checking
    - no null stuff inserted
    
    """
    angle_1 = matrix[0:1]

    angle_2 = matrix[1:2]

    # for Debugging
    theta = np.arctan2(angle_2, angle_1)
    angle = np.round(np.cos(theta[0][0]), 1)
    # for Debugging

    if np.sign(theta[0][0]) == -1:
        if angle == 1:
            pass
        elif angle >= -1 and angle <= -0.7:
            warp = rotate_bound(warp, 180)
        else:
            warp = rotate_bound(warp, 90)

    else:

        if angle >= 0 and angle < 0.5:
            
            warp = rotate_bound(warp, 270)

        elif(angle <= - 0.1 ):

            warp = rotate_bound(warp,270)

        elif (angle <= 1 and angle >= 0.5):
            
            pass

        else:
            warp = rotate_bound(warp, 180)
    return warp
def crop(ref_img, img,min):
	'''
	inp : reference image (front or back), the image we want to crop(front or back)
	out : cropped image 
	'''
	sift = cv2.SIFT_create()

	kp1 , des1 = sift.detectAndCompute(ref_img,None)
	kp2 , des2 = sift.detectAndCompute(img,None)

	#use FLANN Matching

	#flann param
	FLANN_INDEX_KDTREE = 1
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks = 50)

	flann = cv2.FlannBasedMatcher(index_params, search_params)
	matches = flann.knnMatch(des1,des2,k=2)
	# store all the good matches as per Lowe's ratio test.
	good = []
	for m,n in matches:
		if m.distance < 0.75*n.distance:
			good.append(m)
			
	#cropping
	print(len(good))
	MIN_MATCH_COUNT=min
	if len(good) > MIN_MATCH_COUNT:
		src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
		dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
		M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
		# matchesMask = mask.ravel().tolist()
		h,w= ref_img.shape
		pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
		dst = cv2.perspectiveTransform(pts,M)
	else:
		raise Exception("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))

	maskImage=np.zeros(img.shape[:2], dtype='uint8') 
	cv2.fillConvexPoly(maskImage, np.int32(dst), 255)
	masked=cv2.bitwise_and(img,img,mask=maskImage)

	#rotate
	out=detect_rotation(masked, M)
	return out

	#<==========End SIFT Method============>
	#<==========Start Main============>
def front_id(inp_img,ref_img):
	ref_nid_img= img_preprocess(ref_img)
	img= img_preprocess(inp_img)
	nid_img= crop(ref_nid_img,img,1)
	nid_img = cv2.GaussianBlur(nid_img, (7,7), 0)
	nid_img = cv2.Canny(nid_img, 30, 110, 30)
	cv2.imwrite('out/front.jpeg',nid_img)
	return 'out/front.jpeg'

def back_id(inp_img,ref_img):
	ref_nid_img= img_preprocess(ref_img)
	img= img_preprocess(inp_img)
	nid_img= crop(ref_nid_img,img,1)
	nid_img = cv2.GaussianBlur(nid_img, (7,7), 0)
	nid_img = cv2.Canny(nid_img, 30, 110, 30)
	cv2.imwrite('out/back.jpeg',nid_img)
	return 'out/back.jpeg'

def ocr(inp_img,out_img,out_file,status):
	with open (out_file,'w',encoding='utf-8')as myfile:
			words=arabicocr.arabic_ocr(inp_img,out_img)
			if status == 'back':
				words = [ word for word in words if word in ['انثى','ذكر','أنثى','مسلم','مسيحى','طالب','دكر']]
				for word in words:
						myfile.write(word + "\n")
				myfile.close()
			elif status == 'front':
				print(words)
				for word in words:
					id   = re.match('^[\u0660-\u0669]+$',word.replace(' ',''))
					text   = re.match('^[\u0621-\u064A\u0660-\u0669]+$',word.replace(' ',''))
					if id:
						myfile.write('ID: '+id.string+ "\n")
					if text and id:
						if text.string != id.string:
							myfile.write('Applicant: '+text.string+ "\n")
			elif status == 'top':
				# print(words)
				for word in words:
					id   = re.match('^[\u0660-\u0669]+$',word[1].replace(' ',''))
					if id:
						myfile.write('ID: '+id.string+ "\n")
					else:
						myfile.write('Applicant: '+word[1] + "\n")
				
				myfile.close()

FRONT_ID = './sample.jpg'
REF_FRONT = './a.jpeg'

BACK_ID = './hamied_ID_back.jpeg'
REF_BACK = './ID_back_Ref.jpeg'

FRONT_OUT = './front.txt'
BACK_OUT = './back.txt'

CER = './cert.jpg'
REF_TOP_CER = './cert_top_ref.jpg'
REF_BOTTOM_CER = './cert_bottom_ref.jpg'

TOP_OUT = './top.txt'
BOTTOM_OUT = './bottom.txt'

##CERT
ocr(front_id(CER,REF_TOP_CER),'ocr.jpeg',TOP_OUT,'top')
ocr(front_id(CER,REF_BOTTOM_CER),'ocr.jpeg',BOTTOM_OUT,'top')

#ID
ocr(front_id(FRONT_ID,REF_FRONT),'ocr.jpeg',FRONT_OUT,'top')

ocr(back_id(BACK_ID,REF_BACK),'ocr.jpeg',BACK_OUT,'back')

# inp_img = './sample.jpg'
# ref_img = './atef.jpeg'
# front_id(inp_img,ref_img)
	#<==========End Main============>

