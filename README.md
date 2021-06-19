# WIRED REGESTERATION DOCUMENTS SYSTEM (WRDS)

## Idea
**Wired Regesteration Documents System (WRDS)** is a cross-platform that facilitates applying to government organizations (e.g Collages, Banks...etc) from home by simply uploading 
the required documents and then pass by Antispoofing techniques to check the person identification and liveness and then apply OCR to the documents to extract the required
information from them.

The application developed using multiple frameworks:

* Backend implemented using Python OpenCV library for computer vision and NodeJs for web services
* Frontend implemented using basic CSS & React Framewrok

This Github Repo contains many directories:

* [Views](https://github.com/Ahmed-Salah6011/WRDS/tree/master/views) : Contains the ejs files for video recording, images uploading & side tasks
* [Public](https://github.com/Ahmed-Salah6011/WRDS/tree/master/public) : Contains the CSS & designg files and images
* [Antispoofing](https://github.com/Ahmed-Salah6011/WRDS/tree/master/antispoofing) : Contains the classes and modules used to detect antispoofing using smile detection & blink counting
* [OCR](https://github.com/Ahmed-Salah6011/WRDS/tree/master/ocr): Contains the modules used to apply OCR and extract important information from the documents
* [Trainingfiles](https://github.com/Ahmed-Salah6011/WRDS/tree/master/trainingfiles) : Contains the training files used for OCR
* [Random_images](https://github.com/Ahmed-Salah6011/WRDS/tree/master/random_images) : Contains random images taken from the user while recording
* [Uploads](https://github.com/Ahmed-Salah6011/WRDS/tree/master/uploads) : Contains the documents' images uploaded by the user
* [Videos](https://github.com/Ahmed-Salah6011/WRDS/tree/master/videos) : Contains the recorded videos from the user



## Team Members & Their Contribution
| Name                                   | Contribution                                            |
| ---------------------------------------| --------------------------------------------------------|
| [Ahmed Mohammed Salah](https://github.com/Ahmed-Salah6011)               | Antispoofing (Blinking & Face Comparison)               |
| [Ibrahim Atef Abd El-Halim](https://github.com/Ibrahimatef)             | Antispoofing (Smiling & Face Comparison)                |
| [Abd El-Hamid Amr Abd El-Hamid](https://github.com/Hamiedamr)         | OCR                                                     |
| [Mark Sameh Azer](https://github.com/marksameh19)                        | Web Interface (Video Recording & DB) & OCR              |
| [Fatma Elzahraa Mahmoud Esmail Mahmoud](https://github.com/fatma-elzahraa99)  | Web Interface (Frontend & DB) & Antispoofing (Blinking) |

## Features

### Antispoofing
Apply different algorithms to detect the liveness and the identity of the user by:
1. Ask the user to record a "8" second live video asking him to make a certain action and then make sure he did the asked action, the actions are
    * Smiling & Not Smiling, these actions are detected by the SmileDetection class in [antispoofing.py](https://github.com/Ahmed-Salah6011/WRDS/blob/master/antispoofing/antispoofing.py)
    * Blinking (5 To 10 Times), this action is detected by the BlinkingCounter class in [antispoofing.py](https://github.com/Ahmed-Salah6011/WRDS/blob/master/antispoofing/antispoofing.py
   While checking these actions we take a random frames from the recorded videos of the user's face to compare it with his/her face in his/her ID
2. Then after making sure that the user performed all the asked actions we take the random saved images of his/her face and take the face in his/her uploaded ID and compare the
faces with each other to make sure that the user is actually who claims he/she is and prevent phishing and forgery

### OCR
Allow the user to uppload the required documents for registering into his/her required system ( in our case which is applying for collage, he/she must upload the two
faces of the National ID & high school certificate
* You can find the basic code for detecting the national id in [NationalID.py](https://github.com/Ahmed-Salah6011/WRDS/blob/master/ocr/NatinalID.py) &
[IDNumberParser.py](https://github.com/Ahmed-Salah6011/WRDS/blob/master/ocr/IDNumberParser.py)
* You can find the main code of the OCR task in [ocr.py](https://github.com/Ahmed-Salah6011/WRDS/blob/master/ocr/ocr.py)

### Web Platform
Full integrated web platform supports:
* Saving the users data after applying and allows the user to check if his/her application approved or not by entering his/her National ID & the result will appear to him/her
* Support for realtime video recording to check for antispoofing
* Support for uploading the required documents & apply OCR to extract information then allow the user the edit this information if he/she likes
* All this implemented using JS & Node with Basic CSS & React in Frontend


## Installation
* Supported OS : Windows10, Linux/UNIX and MacOS
* Requreid packages and libraries found in [requirements.txt](https://github.com/Ahmed-Salah6011/WRDS/blob/master/requirements.txt) file

  > pip install -r requirements.txt
* You need also to install pytessaract following this [link](https://tesseract-ocr.github.io/tessdoc/?fbclid=IwAR1fW9IUiFzU8c2inAUyiLjJw1XyCZwjLWP478Oa9yqhiqpawKMTmb3lkRY#binaries)
* After installing you nedd to put the training files in [trainingfiles dir](https://github.com/Ahmed-Salah6011/WRDS/tree/master/trainingfiles) in the "tessdata" folder installed in your OS 


## Development
* Open Command/Terminal Window in your local directory and clone the repo

  > git clone https://github.com/Ahmed-Salah6011/WRDS.git
* Navigate to the repo's directory
  
  > cd WRDS/
* Install node

  > npm install
* Run the application

  > npm start
* Open the address appeared in the terminal (http://localhost:4000/) with your browser

ENJOY!

## Future Work ISA
This application is highley scalable, but just simple modification we can enlarge it to support multiple organizations and support various regesteration applications.
We will ISA in the future try to expand the system and provide it with more feature to support multiple systems and document types.




