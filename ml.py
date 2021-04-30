import argparse
import sys
from collections import Counter
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import tensorflow as tf 
import time
from flask import Flask, render_template, request, redirect ,Response,send_file,session
inpWidth = 416  # Width of YoloTiny network's input image
inpHeight = 416  # Height of YoloTiny network's input image

####
confThreshold = 0.5
nmsThreshold = 0.5
MODEL = None
modelConfiguration = "YoloModel/yolov3-tiny.cfg"
modelWeights = "YoloModel/yolov3-tiny.backup"
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
 
YoloClasses = 'LP'
alphabet = {
    "a": "أ", "b": "ب", "t": "ت", "th": "ث", "g": "ج", "hh": "ح", "kh": "خ", "d": "د", "the": "ذ",
    "r": "ر", "z": "ز", "c": "س", "sh": "ش", "s": "ص", "dd": "ض", "tt": "ط", "zz": "ظ", "i": "ع",
    "gh": "غ", "f": "ف", "q": "ق", "k": "ك", "l": "ل", "m": "م", "n": "ن", "h": "ه", "w": "و",
    "y": "ي", "0": "٠", "1": "١", "2": "٢", "3": "٣", "4": "٤", "5": "٥", "6": "٦", "7": "٧",
    "8": "٨", "9": "٩"
}

classes = list(alphabet.keys())
    
class alpr:
    PlateImage = None
    running=False

    
    def getOutputsNames(self,n):
        # Get the names of all the layers in the network
        layersNames = n.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in n.getUnconnectedOutLayers()]
    
    def square(self,img):
        assert type(img) == np.ndarray
        d, r = divmod(abs(img.shape[0] - img.shape[1]), 2)
        if img.shape[0] > img.shape[1]:
            return cv2.copyMakeBorder(img, 0, 0, d if not r else d + 1, d, cv2.BORDER_CONSTANT, 0)
        else:
            return cv2.copyMakeBorder(img, d if not r else d + 1, d, 0, 0, cv2.BORDER_CONSTANT, 0)

    def predict_image(self,img, model=None):
        if not model:
            raise ValueError("You Need to Submit a Model File or a Model Object")
    
        digits, marked = self.mark(img)
        prediction = {}
        plate = ''
        for i in range(len(digits)):
            try:
                resized = cv2.resize(self.square(digits[i]), (40, 40), interpolation=cv2.INTER_AREA)
                #cv2.imshow(str(i), resized)
                filename = 'opencv'+str(i)+'.png'
                #cv2.imwrite(filename, resized) #  .png !
    
                result = model.predict(np.array(resized[tf.newaxis, ..., tf.newaxis], dtype='f'))
                prediction[i] = {}
                prediction[i][classes[int(np.argmax(result))]] = float(np.max(result) * 100)
                plate += (alphabet[classes[int(np.argmax(result))]] + ' ')
            
            except AssertionError:
                print("empty")
        #print(plate)
        self.printDict(prediction)
        return plate, marked
  
    def printDict(self,d):
        for k, v in d.items():
            if isinstance(v, dict):
                self.printDict(v)
            else:
                print("{0} : {1:5.2f}%, ".format(k, v), end='')

    def mark(self,img):
        chars = {}
        digits = []
        copy = img.copy()
        # Convert to Gray
        gray = cv2.inRange(img, (0, 0, 0), (150, 79, 255)) ###############
        
        #gray = cv2.inRange(img, (0, 0, 0), (150, 100, 255)) ###############
        #gray = cv2.inRange(img, (0, 0, 0), (150, 102, 255)) ######Worked Trust#########
        #gray = cv2.inRange(img, (0, 0, 0), (150, 106, 255)) ######Worked Trust2#########
        #gray = cv2.inRange(img, (0, 0, 0), (150, 110, 255)) ######Worked Trust2#########

        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("plate", gray)
        
        # Noise removal
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations=3 if img.shape[0] > 250 else 1)
        #cv2.imshow("platee", opening)
        
    
    

        # Finding characters
        cnt, he = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        k = [key for (key, value) in Counter([x[3] for x in he[0]]).items() if value >= 5]
        #print(k)
        t1, t2, _ = img.shape
        for r in k:
            for i, v in enumerate(cnt):
                if he[0][i][3] == r:
                    x, y, w, h = cv2.boundingRect(v)
                    if .5 * t1 > h > .1 * t1 and .3 * t2 > w > .01 * t2:
                        chars[x] = opening[y:y + h, x:x + w]
                        cv2.rectangle(copy, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), 2)
            if len(chars) < 5:
                chars = {}
                copy = img.copy()
            else:
                break
        if len(chars) >= 1:
            for i, key in enumerate(sorted(chars.keys())):
                digits.append(chars[key])
            
            #cv2.imshow("final", copy)
        
        
        return digits, copy
########
    def drawPred(self,fr, classId, conf, left, top, right, bottom):
        # Draw a bounding box.
        
        cv2.rectangle(fr, (left, top), (right, bottom), (255, 255, 255), 3)
        # Get the label for the class name and its confidence
        lab = '%s:%.2f' % (YoloClasses[classId], conf)
        
        # Display the label at the top of the bounding box
        labelSize, baseLine = cv2.getTextSize(lab, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        cv2.rectangle(fr, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
                    (0, 0, 255), cv2.FILLED)
        cv2.putText(fr, lab, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
    
    def postprocess(self,fr, outs, confT, nmsT):
        frameHeight = fr.shape[0]
        frameWidth = fr.shape[1]
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        classIds = []
        confidences = []
        boxes = []
        for o in outs:
            for detection in o:
                scores = detection[5:]
                classId = np.argmax(scores)
            
                confidence = scores[classId]
                if confidence > confT:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
    
        # Perform non maximum suppression to eliminate redundant overlapping boxes with lower confidences.
        indices = cv2.dnn.NMSBoxes(boxes, confidences, confT, nmsT)
    
        cropped = None
        for i in indices:
        
            i = i[0]
            box = boxes[i]
            left = max(box[0], 0)
            top = max(box[1], 0)
            width = max(box[2], 0)+12
            height = max(box[3], 0)+11
            if height > width:
                continue
            cropped = fr[top:(top + height), left:(left + width)]
    
            self.drawPred(fr, classIds[i], confidences[i], left, top, left + width, top + height)
        #cv2.imshow("awwa",cropped)
        #print("aaa")

        return len(indices) > 0, cropped



    def plateRecog(self,pic,MODEL):
        cap = cv2.VideoCapture(pic)
    
        frWidth = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frHeight = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # # if not hasFrame:
        # #         print("Done processing !!!")
        # #         print("Output file is stored as ", outputFile)
        # #         cv2.waitKey(3000)  # I love you 3000 ^_^
        # #         break
        img_counter = 0
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), (0, 0, 0), 1, crop=False)
        net.setInput(blob)
        run = net.forward(self.getOutputsNames(net))    
        rec, plateImg = self.postprocess(frame, run, confThreshold, nmsThreshold)
        #cv2.imshow("Capture", cv2.resize(frame, (400, 300)))
        if rec and plateImg is not None:
                out, final ,gray = self.predict_image(plateImg, model=MODEL)
                frame[0:final.shape[0], 0:final.shape[1], :] = final
                image = Image.fromarray(frame)
                draw = ImageDraw.Draw(image)
                font = ImageFont.truetype('Fonts/tradbdo.ttf', round(frWidth / 40))
                draw.text((10, final.shape[0]+2), out, font=font, fill=(0, 255, 0, 0))
                frame = np.array(image)
                ###########
                img_name = "opencv_frame_{}.png".format(img_counter)
                #cv2.imwrite(img_name, frame)
                ##########
        return out

    number = ""
    def liveFeed(self,cap,MODEL):
        #cap = cv2.VideoCapture("test.jpg")
        #cap = cv2.VideoCapture("http://192.168.137.70:8080/video")
        #cap=cv2.VideoCapture("outt.avi")

        # used to record the time when we processed last frame 
        prev_frame_time = 0
        
        # used to record the time at which we processed current frame 
        new_frame_time = 0
        
        img_counter = 0
        # frWidth = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # frHeight = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        img_counter = 0
        count=0
        
        #cap.start()
        #time.sleep(1.0)
        while cap:
            
            self.running=True
            new_frame_time = time.time() 
            fps = 1/(new_frame_time-prev_frame_time) 
            prev_frame_time = new_frame_time 
            fps = int(fps) 
            fps = str(fps)
            print("Fps") 
            print(fps)

            frame = cap.read()
           
            # if not success:
            #     break

            blob = cv2.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), (0, 0, 0), 1, crop=False)
            net.setInput(blob)
            run = net.forward(self.getOutputsNames(net))    
            rec, plateImg= self.postprocess(frame, run, confThreshold, nmsThreshold)
            
            if rec and plateImg is not None:
                    
                    out, final = self.predict_image(plateImg, model=MODEL)
  
                    plateImg = cv2.resize(plateImg, dsize=(300, 300), interpolation=cv2.INTER_CUBIC)
        
                    carPic = cv2.resize(frame, dsize=(300, 300), interpolation=cv2.INTER_CUBIC) 
                    both = np.hstack((plateImg,carPic))
                    framee = cv2.imencode('.jpg', both)[1].tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + framee + b'\r\n')
  
                    self.PlateImage = plateImg
                    frame[0:final.shape[0], 0:final.shape[1], :] = final
                    image = Image.fromarray(frame)
                    draw = ImageDraw.Draw(image)
                    font = ImageFont.truetype('Fonts/tradbdo.ttf', round(1000 / 40))
                    draw.text((10, final.shape[0]+2), out, font=font, fill=(0, 255, 0, 0))
                    frame = np.array(image)
                    ###########
                    img_name = "opencv_frame_{}.png".format(img_counter)
                    self.number=""
                    self.number=out

                    # sampleDict = {"number_Plate": f"{str(out)}", 
                    # "GateId":1,
                    # "Acess_DateTime":"2019-01-06T17:16:40"}     
                    # print(sampleDict) 
                    # print("ssssssssss")
                    # response = requests.post('http://localhost:50455/Account/Access', json=sampleDict)
                 # todo with response
                                            
                    print("aaaaaaaa")
                    print(out)
                    print("aaaaaaaa")

                    #cv2.imwrite(img_name, frame)
                    ##########

        

    def getPlate(self,cap):
            
                yield self.number[::-1]


    # def camera(self):
    #     stream = cv2.VideoCapture("1.avi")

    #     while True:
    #         frame = stream.read()
    #         #outputFrame=cv2.resize(frame, (500, 300))
    #         framee = cv2.imencode('.jpg', frame)[1].tobytes()
    #         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + framee + b'\r\n')

    def camera(self,cap):
        """Video streaming generator function."""

        # Read until video is completed
        while(cap.stream.isOpened()):
        # Capture frame-by-frame
            img = cap.read()
            # if not sucess:
            #     break
            
            if img is not None:
                img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(0.1)
            else: 
                cap.stop()
          