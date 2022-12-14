import cv2 as cv
import numpy as np 

cap = cv.VideoCapture(0)

#loading Deep Neural Network for Yolo weights and yolo config file with classes name specified and finally outputlayer connected.
net = cv.dnn.readNet("yolov3_training_best.weights", "yolov3_training.cfg")
classes = ["NOMask","Mask"]
layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

print(output_layers)

while True: 
    ret,img=cap.read()
    img = cv.resize(img, None, fx=0.6, fy=0.6)
    height, width, channels = img.shape
    blob = cv.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    #print(blob)
    net.setInput(blob)
    outs = net.forward(output_layers)
    font = cv.FONT_HERSHEY_SIMPLEX
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence>=0.65:
                obj_name=classes[class_id] #Get obj name from classes list with class id index
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                if class_id == 0:
                    color = (0,0,255)
                elif class_id == 1:
                    color = (0,255,0)
                else:
                    color = (255,0,0)
                img=cv.rectangle(img,(x,y),(x+w,y+h),color,2)
                img = cv.putText(img,obj_name,(x-5,y-5), font,1.5, color, 2)            
        imS = cv.resize(img, (800, 600))
        cv.imshow('output',imS)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()