import cv2
import NatinalID

	#<==========Start Main============>

inp_img = cv2.imread('cert.jpg')
grade = NatinalID.CERTScanner_bottom(inp_img)
cert_data = NatinalID.CERTScanner_top(inp_img)
cert_data['المجموع'] = grade['المجموع']
print(cert_data)

inp_img = cv2.imread('Salah.jpg')
inp_img1 = cv2.imread('Back.jpg')

id_data = NatinalID.IDScanner(inp_img)
id_data.update(NatinalID.IDScanner_back(inp_img1))
print(id_data)
	#<==========End Main============>

