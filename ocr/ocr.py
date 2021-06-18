import json
import cv2
import NatinalID

	#<==========Start Main============>
inp_img = cv2.imread('uploads/cert.jpg')
grade = NatinalID.CERTScanner_bottom(inp_img)
cert_data = NatinalID.CERTScanner_top(inp_img)
if grade:
    cert_data['المجموع'] = grade['المجموع']
# print(cert_data)

inp_img = cv2.imread('uploads/ID_front.jpg')
inp_img1 = cv2.imread('uploads/ID_back.jpg')

id_data = NatinalID.IDScanner(inp_img)
id_data.update(NatinalID.IDScanner_back(inp_img1))
# print(NatinalID.IDScanner_back(inp_img1))
# print(id_data)


with open('ID.json', 'w',encoding='utf-8') as fp:
    json.dump(id_data, fp,ensure_ascii = False)

with open('CERT.json', 'w',encoding='utf-8') as fp:
    json.dump(cert_data, fp,ensure_ascii = False)
print('Finish')
	#<==========End Main============>

