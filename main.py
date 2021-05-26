import face_recognition as facer
import numpy as np
import cv2
import os
import time
from threading import Thread


# what should I be doing?!?!
# get the list of reference pictures.
# take a picture from my webcam and get its encodings
# compare encodings of my ref img to Encodings from the webcam
# mark found students as present, others as absent
# export all of this to other students
def encode(images):
    encodes = []
    for image in images:
        encode = facer.face_encodings(image)[0]
        encodes.append(encode)
    return encodes

# def check():
#     time.sleep(5)
#     if answer is not None:
#         return
#     print("\nimage taken")
#     bool1aq = False
#     cv2.destroyAllWindows()

# get the list of reference pictures.
video = cv2.VideoCapture(0)

rFaces = []
rNames=[]
rItems = os.listdir('refrences')
for item in rItems:
    img = cv2.imread(f'refrences/{item}')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rFaces.append(img)
    name=item.split(".")[0]
    rNames.append(name)
print(rNames)
rEncodes = encode(rFaces)
print(f"\" {len(rFaces)} \" refrence pictures found")

# take a picture from my webcam and get its encodings & loc
boolaq = True
while True:
    if video.isOpened() and input("press Enter to take a picture")=="":
        print("Video is Opened")
        # Take each frame of the video.
        success, frame = video.read()
        frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        fLocs = facer.face_locations(frame2)
        fEncodes = facer.face_encodings(frame2,fLocs)

        print(f"encoded, found {len(fEncodes)} face(s) in the image")

        for fEncode,fLoc in zip(fEncodes,fLocs):
            matches = facer.compare_faces(rEncodes, fEncode)
            fDistance = facer.face_distance(rEncodes, fEncode)
            print(fDistance)
            matchIndex = np.argmin(fDistance[0])

            print(matchIndex)
            if matches[matchIndex]:
                name = rNames[matchIndex].upper()
                print(name)
            if not success:
                raise Exception('Failed to read the frame number: {}')    # frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    else:
        raise Exception("video isn't opening")  # frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
        # if cv2.waitKey(1) == ord('e'):
        #     cv2.destroyAllWindows()

        #cv2.imshow("video", frame)
        #cv2.waitKey(5000)




        #Thread(target=check).start()
        #answer = input("recapture? (press 'a' to recapture)")
        #print(answer)

# compare encodings of my ref img to Encodings from the webcam
