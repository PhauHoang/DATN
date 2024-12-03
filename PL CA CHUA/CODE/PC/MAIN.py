from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from matplotlib import pyplot as plt
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import argparse
import time
import cv2
from time import sleep
import numpy as np
import array as arr
import math
import sys
import serial
import os
from imutils.video import VideoStream
from imutils import face_utils
from PIL import Image
import imutils
from datetime import datetime
#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#ser = serial.Serial('/dev/ttyUSB0',9600)
ser = serial.Serial('COM5',baudrate = 9600, timeout = 1)
print(ser.name)
vs = VideoStream(src=1).start()
frame = vs.read()
image = frame
cp = 0
khac = 0; hong = 0; dat = 0
mang = []*10
loai = 0; runn = 0
st = 0; mode = 0; g1 = 0; g2 = 0; bt = 0
mode_ht = 0; st_ht = 0
dem = 0
def XLA():
    #print("xl------------a")
    global frame
    global image
    global loai, dem
    
    loai = 1
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
    
    
    scale = 0.00392
    classes = None
    with open(cll, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    #COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    COLORS = [(85,255,0),(255,0,0),(255,170,0)]    
    net = cv2.dnn.readNet(ww, cc)

    #image = cv2.imread(ii)
    image = frame
    Width = image.shape[1]
    Height = image.shape[0]

    blob = cv2.dnn.blobFromImage(image, scale, (320, 320), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    batdau = time.time()
    outs = net.forward(get_output_layers(net))
    ketthuc = time.time()
    tgian = ketthuc - batdau
    print(tgian)
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
            if confidence > 0.5:
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
    for i in indices:
        #i = i[0]
        if i >= 0:
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
            if class_ids[i] == 0: # HỎNG
                loai = 0
            if class_ids[i] == 1: # CHÍN
                loai = 1
            if class_ids[i] == 2: # XANH
                loai = 2
            
#---------------------------------------------------------------------------------------------
def Time(): 
    global status_str
    global status
    global hong, khac, dat, loai, runn
    global st_ht, mode_ht
    global image
    global frame
    ii = "data/IM74.jpg"
    call.lb_hong.setText(str(hong))
    call.lb_khac.setText(str(khac))
    call.lb_dat.setText(str(dat))
    if mode_ht == 0:
        call.BT_MODE.setText("MODE:AUTO")
        call.BT_MODE.setStyleSheet("background-color: rgb(255, 255, 0)")
    if mode_ht == 1:
        call.BT_MODE.setText("MODE: MANUAL")
        call.BT_MODE.setStyleSheet("background-color: rgb(255, 170, 0)")
    if st_ht == 0:
        call.lb_st.setStyleSheet("background-color: rgb(255, 255, 255)")
    if st_ht == 1:
        call.lb_st.setStyleSheet("background-color: rgb(85, 255, 0)")
    if st_ht == 2:
        call.lb_st.setStyleSheet("background-color: rgb(255, 0, 0)")
    
    # Đọc ảnh từ camera
    frame = vs.read()
    #frame = cv2.imread(ii)
    # chỉnh kích thước ảnh để tăng tốc độ xử lý
    frame = imutils.resize(frame, width=600)
    # Hiển thị các ảnh lên label liên tiếp như một video
    img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
    pix = QPixmap.fromImage(img)
    call.lb_im.setPixmap(pix)
    #--------------------------------------Nhận dữ liệu--------------------------------------------
    if(ser.in_waiting > 0):
        #0|0|0|0|0|0
        s = ser.readline()          #Doc vao data
        data = s.decode()           # decode s
        data = data.rstrip()        # cut "\r\n" at last of string
        #print(data)                     #In ra man hinh       
        mang = data.split("|")
        mode_ht = int(mang[0])
        try:
            st_ht = int(mang[1])
        except:
            print("loi nhan du lieu 1")
        try:
            runn = int(mang[2])
        except:
            print("loi nhan du lieu 2")
        try:
            hong = int(mang[4])
        except:
            print("loi nhan du lieu 3")
        try:
            khac = int(mang[3])
        except:
            print("loi nhan du lieu 4")
        try:
            dat = int(mang[5])
        except:
            print("loi nhan du lieu 5")
    if runn == 1:
        #-----------------------------------------------------------------
        #cv2.imwrite("A.jpg3",frame)
        XLA()
        img2 = QImage(image, image.shape[1],image.shape[0],image.strides[0], QImage.Format_RGB888).rgbSwapped()      
        pix2 = QPixmap.fromImage(img2)
        call.lb_kq.setPixmap(pix2)
        #-----------------------------------------------------------------          
        ser.write(b'f')
        ser.write(b'|');
        ser.write(str(loai).encode())
        ser.write(b'\r\n')
        ser.flush()
        print("Loai = ",loai)
        if loai == 0:
            call.lb_loai.setText("TRÁI HỎNG")    
        elif loai == 1:
            call.lb_loai.setText("TRÁI CHÍN")
        elif loai == 2:
            call.lb_loai.setText("TRÁI XANH")
        ser.write(b'g')
        ser.write(b'|');
        ser.write(b'1')
        ser.write(b'\r\n')
        ser.flush()
        #loai = 0
        runn = 0
#------------------------------------------------------------------#
def thoat():
    call.close()
    exit(app.exec())
#------------------------------------------------------------------#
def bt_mode():
    global mode, st
    mode = mode + 1
    if mode >= 2:
        mode = 0
    ser.write(b'a')
    ser.write(b'|')
    ser.write(str(mode).encode())
    ser.write(b'\r\n')
    ser.flush()
#------------------------------------------------------------------#
def bt_start():
    global st
    st = 1
    ser.write(b'b')
    ser.write(b'|')
    ser.write(str(st).encode())
    ser.write(b'\r\n')
    ser.flush()
#------------------------------------------------------------------#
def bt_stop():
    global st
    st = 2
    ser.write(b'b')
    ser.write(b'|')
    ser.write(str(st).encode())
    ser.write(b'\r\n')
    ser.flush()
#------------------------------------------------------------------#
def bt_gat1():
    global g1
    g1 = g1 + 1
    if g1 >= 2:
        g1 = 0
    ser.write(b'c')
    ser.write(b'|')
    ser.write(str(g1).encode())
    ser.write(b'\r\n')
    ser.flush()
#------------------------------------------------------------------#
def bt_gat2():
    global g2
    g2 = g2 + 1
    if g2 >= 2:
        g2 = 0
    ser.write(b'd')
    ser.write(b'|')
    ser.write(str(g2).encode())
    ser.write(b'\r\n')
    ser.flush()
#------------------------------------------------------------------#
def bt_bt():
    global bt
    bt = bt + 1
    if bt >= 2:
        bt = 0
    ser.write(b'e')
    ser.write(b'|')
    ser.write(str(bt).encode())
    ser.write(b'\r\n')
    ser.flush()
#------------------------------------------------------------------#    
def doc_mau():
    global loai
    loai = 1
#------------------------------------------------------------------#
app=QtWidgets.QApplication([])
call=uic.loadUi("AUTO.ui")
call.THOAT.clicked.connect(thoat)
call.BT_MODE.clicked.connect(bt_mode)
call.BT_START.clicked.connect(bt_start)
call.BT_STOP.clicked.connect(bt_stop)
call.BT_GAT1.clicked.connect(bt_gat1)
call.BT_GAT2.clicked.connect(bt_gat2)
call.BT_BT.clicked.connect(bt_bt)
call.timer = QTimer()
call.timer.timeout.connect(Time)
call.timer.start(50)
call.show()
app.exec()


    
