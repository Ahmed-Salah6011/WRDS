from ArabicOcr import arabicocr
import cv2

image = cv2.imread('ID.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# blurring the image
blurred = cv2.GaussianBlur(gray, (5,5), 0)
	#use canny edge detector to detect edges in the image
edged = cv2.Canny(blurred, 30, 110, 30)

cv2.imwrite('test0.jpeg',edged)

image_path='test0.jpeg'
out_image='out.jpg'

results=arabicocr.arabic_ocr(image_path,out_image)

# print(results)
words=[]
for i in range(len(results)):	
		word=results[i][1]
		words.append(word)
with open ('file.txt','w',encoding='utf-8')as myfile:
		myfile.write(str(words))
img = cv2.imread('out.jpg', cv2.IMREAD_UNCHANGED)
cv2.imshow("arabic ocr",img)
cv2.waitKey(0)