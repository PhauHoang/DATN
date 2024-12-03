import time
import cv2
import argparse
import numpy as np
import imutils
from imutils.video import VideoStream
#ii = "data/A.jpg"
ii = "IM9.jpg"
cll = "yolo.names"
ww = 'yolov4-tiny_final.weights'
cc = 'yolov4-tiny.cfg'
def get_output_layers(net):
    layer_names = net.getLayerNames()
    #output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
    return output_layers
def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
vs = VideoStream(src=0).start()
frame = vs.read()
frame = imutils.resize(frame, width=600)

scale = 0.00392
classes = None
with open(cll, 'r') as f:
    classes = [line.strip() for line in f.readlines()]
#COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
COLORS = [(85,255,0),(255,170,0),(255,170,0)]    
net = cv2.dnn.readNet(ww, cc)

image = cv2.imread(ii)
#image = frame
Width = image.shape[1]
Height = image.shape[0]

blob = cv2.dnn.blobFromImage(image, scale, (320, 320), (0, 0, 0), True, crop=False)

net.setInput(blob)
batdau = time.time()
outs = net.forward(get_output_layers(net))
ketthuc = time.time()
tgian = ketthuc - batdau
#print(tgian)

#print("11111111111111")
class_ids = []
confidences = []
boxes = []
conf_threshold = 0.5
nms_threshold = 0.4

# Thực hiện xác định bằng HOG và SVM
start = time.time()
heo = 0
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.9:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2
            y = center_y - h / 2
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])
indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
#print("indices = ",indices)
#print(indices)
for i in indices:
    #i = i[0]
    if i >= 0:
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        heo = heo + 1
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
        #print("box = ",box)
            

cv2.imshow("object detection", image)
end = time.time()
print("YOLO Execution time: " + str(end-start))
cv2.waitKey()
cv2.destroyAllWindows()
vs.stop()

