import requests
import json
import base64

data = {}
img = ""
with open('ID.jpg', mode='rb') as file:
    img = file.read()
data['url'] = base64.encodebytes(img).decode('utf-8')


# print(json.dumps(data))
url = 'https://eastus.api.cognitive.microsoft.com/vision/v1.0/ocr?language=ar&detectOrientation=true'

# myobj = {'somekey': 'somevalue'}
# data  = json.dumps(data)
x = requests.post(url, data = img,headers={"Content-Type":"image/jpg","Ocp-Apim-Subscription-Key":"46223ef89079470bbeea3c17845bac70"})
d = json.loads(x.text)
with open('out.txt','w+',encoding="utf-8") as out:
    for region in d['regions']:
        for line in region['lines']:
            for word in line['words']:
                out.writelines(word['text']+"\n")

# print(d['regions'][0]['lines'][0]['words'][0]['text'])